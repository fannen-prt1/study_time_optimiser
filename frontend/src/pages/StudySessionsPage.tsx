import { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchSubjects } from '../store/slices/subjectsSlice';
import {
  fetchSessions,
  createSession,
  startSession,
  pauseSession,
  resumeSession,
  completeSession,
  deleteSession,
} from '../store/slices/sessionsSlice';
import { SessionTimer } from '../components/SessionTimer';
import type { CreateSessionRequest, CompleteSessionRequest, SessionStatus, SessionType } from '../types';
import toast from 'react-hot-toast';

const STATUS_CONFIG: Record<SessionStatus, { label: string; color: string; icon: string }> = {
  active: { label: 'Active', color: 'bg-sky-100 text-sky-700', icon: 'play_circle' },
  paused: { label: 'Paused', color: 'bg-amber-100 text-amber-700', icon: 'pause_circle' },
  completed: { label: 'Completed', color: 'bg-emerald-100 text-emerald-700', icon: 'check_circle' },
  cancelled: { label: 'Cancelled', color: 'bg-rose-100 text-rose-700', icon: 'cancel' },
};

export function StudySessionsPage() {
  const dispatch = useAppDispatch();
  const { sessions, activeSession, isLoading } = useAppSelector((state) => state.sessions);
  const { subjects } = useAppSelector((state) => state.subjects);

  const [showNewSession, setShowNewSession] = useState(false);
  const [showCompleteForm, setShowCompleteForm] = useState(false);
  const [filterStatus, setFilterStatus] = useState<string>('all');

  // New session form
  const [newSession, setNewSession] = useState<CreateSessionRequest>({
    subject_id: '',
    session_type: 'focused_study',
    planned_duration_minutes: 30,
    notes: '',
  });

  // Complete session form
  const [completeData, setCompleteData] = useState<CompleteSessionRequest>({
    productivity_score: 70,
    focus_score: 70,
    energy_level: 3,
    difficulty_level: 3,
    satisfaction_level: 3,
    notes: '',
  });

  useEffect(() => {
    dispatch(fetchSessions(undefined));
    dispatch(fetchSubjects(false));
  }, [dispatch]);

  const filteredSessions =
    filterStatus === 'all' ? sessions : sessions.filter((s) => s.status === filterStatus);

  const handleCreateAndStart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSession.subject_id) {
      toast.error('Please select a subject');
      return;
    }
    try {
      const session = await dispatch(
        createSession({ ...newSession, start_time: new Date().toISOString() })
      ).unwrap();
      await dispatch(startSession(session.id)).unwrap();
      toast.success('Session started!');
      setShowNewSession(false);
    } catch (err) {
      toast.error(typeof err === 'string' ? err : 'Failed to start session');
    }
  };

  const handlePause = async () => {
    if (!activeSession) return;
    try {
      await dispatch(pauseSession(activeSession.id)).unwrap();
      toast.success('Session paused');
    } catch (err) {
      toast.error(typeof err === 'string' ? err : 'Failed to pause');
    }
  };

  const handleResume = async () => {
    if (!activeSession) return;
    try {
      await dispatch(resumeSession(activeSession.id)).unwrap();
      toast.success('Session resumed');
    } catch (err) {
      toast.error(typeof err === 'string' ? err : 'Failed to resume');
    }
  };

  const handleTimerComplete = (_elapsedMinutes: number) => {
    setShowCompleteForm(true);
  };

  const handleCompleteSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeSession) return;
    try {
      await dispatch(completeSession({ id: activeSession.id, data: completeData })).unwrap();
      toast.success('Session completed! Great work!');
      setShowCompleteForm(false);
      setCompleteData({
        productivity_score: 70,
        focus_score: 70,
        energy_level: 3,
        difficulty_level: 3,
        satisfaction_level: 3,
        notes: '',
      });
    } catch (err) {
      toast.error(typeof err === 'string' ? err : 'Failed to complete session');
    }
  };

  const handleDeleteSession = async (id: string) => {
    try {
      await dispatch(deleteSession(id)).unwrap();
      toast.success('Session deleted');
    } catch (err) {
      toast.error(typeof err === 'string' ? err : 'Failed to delete');
    }
  };

  const getSubjectName = (subjectId: string) => {
    return subjects.find((s) => s.id === subjectId)?.name || 'Unknown';
  };

  const getSubjectColor = (subjectId: string) => {
    return subjects.find((s) => s.id === subjectId)?.color || '#6b7280';
  };

  const formatDuration = (minutes: number) => {
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    if (h > 0) return `${h}h ${m}m`;
    return `${m}m`;
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Study Sessions</h1>
          <p className="text-sm text-[#7a96b0] mt-0.5">Track and manage your study time</p>
        </div>
        {!activeSession && (
          <button
            onClick={() => setShowNewSession(true)}
            className="inline-flex items-center gap-2 px-4 py-2.5 bg-primary text-white rounded-lg shadow-sm hover:bg-primary/90 transition-colors font-bold text-sm"
          >
            <span className="material-symbols-outlined text-lg">add</span>
            New Session
          </button>
        )}
      </div>

      {activeSession && (
        <div className="mb-8 rounded-xl border border-[#233648] bg-[#0F172A] p-5">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-2.5 h-2.5 rounded-full animate-pulse" style={{ backgroundColor: getSubjectColor(activeSession.subject_id) }} />
            <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0]">Active Session — {getSubjectName(activeSession.subject_id)}</p>
          </div>
          <SessionTimer
            isRunning={true}
            isPaused={activeSession.status === 'paused'}
            plannedDuration={activeSession.planned_duration_minutes || 30}
            startTime={activeSession.start_time}
            totalPauseDurationMinutes={activeSession.total_pause_duration_minutes || 0}
            onStart={() => {}}
            onPause={handlePause}
            onResume={handleResume}
            onComplete={handleTimerComplete}
          />
        </div>
      )}

      <div className="flex gap-1.5 mb-6 overflow-x-auto pb-2">
        {['all', 'active', 'paused', 'completed', 'cancelled'].map((status) => (
          <button
            key={status}
            onClick={() => setFilterStatus(status)}
            className={`px-3 py-1.5 rounded-lg text-sm font-bold whitespace-nowrap transition-colors ${
              filterStatus === status
                ? 'bg-primary text-white shadow-sm'
                : 'bg-[#233648] text-[#7a96b0] hover:bg-[#2d4560]'
            }`}
          >
            {status === 'all'
              ? `All (${sessions.length})`
              : `${STATUS_CONFIG[status as SessionStatus]?.label || status} (${sessions.filter((s) => s.status === status).length})`}
          </button>
        ))}
      </div>

      {isLoading && sessions.length === 0 ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-10 w-10 border-[3px] border-[#233648] border-t-primary" />
        </div>
      ) : filteredSessions.length === 0 ? (
        <div className="rounded-xl border border-[#233648] bg-[#0F172A] p-14 text-center">
          <span className="material-symbols-outlined text-slate-300 text-5xl mb-3">timer</span>
          <h3 className="text-base font-bold text-white mb-1">No sessions found</h3>
          <p className="text-sm text-[#7a96b0]">Start a new study session to begin tracking your progress</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredSessions.map((session) => {
            const status = STATUS_CONFIG[session.status] || STATUS_CONFIG.active;
            return (
              <div
                key={session.id}
                className="rounded-xl border border-[#233648] bg-[#0F172A] hover:border-slate-300 transition-colors p-4"
              >
                <div className="flex items-center gap-4">
                  <div className="w-1 h-12 rounded-full flex-shrink-0" style={{ backgroundColor: getSubjectColor(session.subject_id) }} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-bold text-white">{getSubjectName(session.subject_id)}</span>
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-bold ${status.color}`}>
                        <span className="material-symbols-outlined text-xs" style={{ fontVariationSettings: "'FILL' 1", fontSize: '12px' }}>{status.icon}</span>
                        {status.label}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-[#7a96b0]">
                      <span className="flex items-center gap-1">
                        <span className="material-symbols-outlined text-sm">schedule</span>
                        {session.actual_duration_minutes
                          ? formatDuration(session.actual_duration_minutes)
                          : formatDuration(session.planned_duration_minutes || 0)}
                        {!session.actual_duration_minutes && ' (planned)'}
                      </span>
                      <span>{formatDate(session.start_time)}</span>
                    </div>
                    {session.notes && <p className="text-sm text-[#4a6580] mt-1 truncate">{session.notes}</p>}
                  </div>
                  {session.status === 'completed' && session.productivity_score && (
                    <div className="hidden sm:flex items-center gap-3">
                      <div className="text-center">
                        <div className="flex items-center gap-0.5">
                          <span className="material-symbols-outlined text-amber-400 text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>star</span>
                          <span className="text-sm font-bold text-white">{session.productivity_score}%</span>
                        </div>
                        <span className="text-xs text-[#4a6580]">Productivity</span>
                      </div>
                      <div className="text-center">
                        <span className="text-sm font-bold text-white">{session.focus_score}%</span>
                        <br />
                        <span className="text-xs text-[#4a6580]">Focus</span>
                      </div>
                    </div>
                  )}
                  {session.status === 'cancelled' && (
                    <button onClick={() => handleDeleteSession(session.id)} className="p-2 text-[#4a6580] hover:text-rose-400 rounded-lg hover:bg-rose-900/20 transition-colors">
                      <span className="material-symbols-outlined text-lg">delete</span>
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {showNewSession && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#102337] rounded-xl border border-[#233648] shadow-xl w-full max-w-md">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#233648]">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-primary">timer</span>
                <h2 className="text-base font-bold text-white">New Study Session</h2>
              </div>
              <button onClick={() => setShowNewSession(false)} className="text-slate-400 hover:text-white transition-colors">
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form onSubmit={handleCreateAndStart} className="p-6 space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Subject *</label>
                <select value={newSession.subject_id} onChange={(e) => setNewSession({ ...newSession, subject_id: e.target.value })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none text-sm text-white bg-[#102337]">
                  <option value="">Select a subject...</option>
                  {subjects.filter((s) => !s.is_archived).map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
                </select>
                {subjects.filter((s) => !s.is_archived).length === 0 && (
                  <p className="text-xs text-amber-600 mt-1">No subjects yet. Create one from the Subjects page first.</p>
                )}
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Session Type *</label>
                <select value={newSession.session_type} onChange={(e) => setNewSession({ ...newSession, session_type: e.target.value as SessionType })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none text-sm text-white bg-[#102337]">
                  <option value="focused_study">Focused Study</option>
                  <option value="practice">Practice</option>
                  <option value="reading">Reading</option>
                  <option value="review">Review</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Planned Duration *</label>
                <div className="flex gap-1.5 flex-wrap mb-2">
                  {[15, 30, 45, 60, 90, 120].map((d) => (
                    <button key={d} type="button" onClick={() => setNewSession({ ...newSession, planned_duration_minutes: d })}
                      className={`px-3 py-1.5 rounded-lg text-sm font-bold transition-colors ${
                        newSession.planned_duration_minutes === d ? 'bg-primary text-white shadow-sm' : 'bg-[#233648] text-[#7a96b0] hover:bg-[#2d4560]'
                      }`}>
                      {d >= 60 ? `${d / 60}h` : `${d}m`}
                    </button>
                  ))}
                </div>
                <input type="number" min={1} max={480} value={newSession.planned_duration_minutes || 30}
                  onChange={(e) => setNewSession({ ...newSession, planned_duration_minutes: Number(e.target.value) })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none text-sm text-white bg-[#102337]" />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Notes (optional)</label>
                <textarea value={newSession.notes || ''} onChange={(e) => setNewSession({ ...newSession, notes: e.target.value })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none text-sm text-white bg-[#102337]" rows={2}
                  placeholder="What are you planning to study?" />
              </div>
              <div className="flex gap-3 pt-1">
                <button type="button" onClick={() => setShowNewSession(false)} className="flex-1 px-4 py-2.5 border border-[#233648] text-slate-300 rounded-lg hover:bg-[#102337] font-medium text-sm transition-colors">Cancel</button>
                <button type="submit" disabled={isLoading} className="flex-1 px-4 py-2.5 bg-primary text-white rounded-lg hover:bg-primary/90 font-bold text-sm shadow-sm transition-colors disabled:opacity-50">
                  {isLoading ? 'Starting...' : 'Start Session'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showCompleteForm && activeSession && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#102337] rounded-xl border border-[#233648] shadow-xl w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#233648]">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-emerald-500" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
                <h2 className="text-base font-bold text-white">Session Complete!</h2>
              </div>
              <button onClick={() => setShowCompleteForm(false)} className="text-slate-400 hover:text-white transition-colors">
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <form onSubmit={handleCompleteSubmit} className="p-6 space-y-5">
              <div className="bg-emerald-900/30 rounded-xl p-3 text-sm text-emerald-400 text-center border border-emerald-900">
                Great session studying <strong>{getSubjectName(activeSession.subject_id)}</strong>!
              </div>
              <ScoreSlider label="Productivity" description="How productive were you?" value={completeData.productivity_score || 70} max={100} onChange={(v) => setCompleteData({ ...completeData, productivity_score: v })} />
              <ScoreSlider label="Focus" description="How focused were you?" value={completeData.focus_score || 70} max={100} onChange={(v) => setCompleteData({ ...completeData, focus_score: v })} />
              <ScoreSlider label="Energy" description="How was your energy level?" value={completeData.energy_level || 3} max={5} onChange={(v) => setCompleteData({ ...completeData, energy_level: v })} />
              <ScoreSlider label="Difficulty" description="How difficult was the material?" value={completeData.difficulty_level || 3} max={5} onChange={(v) => setCompleteData({ ...completeData, difficulty_level: v })} />
              <ScoreSlider label="Satisfaction" description="How satisfied are you?" value={completeData.satisfaction_level || 3} max={5} onChange={(v) => setCompleteData({ ...completeData, satisfaction_level: v })} />
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Notes (optional)</label>
                <textarea value={completeData.notes || ''} onChange={(e) => setCompleteData({ ...completeData, notes: e.target.value })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none text-sm text-white bg-[#102337]" rows={2}
                  placeholder="Any notes about this session?" />
              </div>
              <button type="submit" disabled={isLoading} className="w-full px-4 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 font-bold text-sm shadow-sm transition-colors disabled:opacity-50">
                {isLoading ? 'Saving...' : 'Save & Complete Session'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

// Score slider sub-component
function ScoreSlider({
  label,
  description,
  value,
  max = 100,
  onChange,
}: {
  label: string;
  description: string;
  value: number;
  max?: number;
  onChange: (v: number) => void;
}) {
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <label className="text-xs font-bold uppercase tracking-wider text-[#7a96b0]">{label}</label>
        <span className="text-sm font-bold text-primary">
          {value}{max <= 5 ? `/${max}` : '%'}
        </span>
      </div>
      <p className="text-xs text-[#4a6580] mb-2">{description}</p>
      <input
        type="range"
        min={max <= 5 ? 1 : 0}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full accent-primary"
      />
      <div className="flex justify-between text-xs text-[#4a6580]">
        <span>Low</span>
        <span>High</span>
      </div>
    </div>
  );
}
