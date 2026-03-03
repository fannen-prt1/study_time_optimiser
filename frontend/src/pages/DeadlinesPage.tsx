import { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchSubjects } from '../store/slices/subjectsSlice';
import apiClient, { handleApiError } from '../services/apiClient';
import { ENDPOINTS } from '../config/constants';
import type { Deadline, CreateDeadlineRequest, Priority } from '../types';
import toast from 'react-hot-toast';

const PRIORITY_STYLES: Record<Priority, string> = {
  low: 'bg-sky-900/30 text-sky-400 border border-sky-800',
  medium: 'bg-amber-900/30 text-amber-400 border border-amber-800',
  high: 'bg-rose-900/30 text-rose-400 border border-rose-800',
  urgent: 'bg-violet-900/30 text-violet-400 border border-violet-800',
};

const PRIORITY_LEFT: Record<Priority, string> = {
  low: 'border-l-sky-400',
  medium: 'border-l-amber-400',
  high: 'border-l-rose-400',
  urgent: 'border-l-violet-500',
};

export function DeadlinesPage() {
  const dispatch = useAppDispatch();
  const { subjects } = useAppSelector((state) => state.subjects);
  const [deadlines, setDeadlines] = useState<Deadline[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState<CreateDeadlineRequest>({
    subject_id: '',
    title: '',
    description: '',
    deadline_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
    priority: 'medium',
  });

  useEffect(() => {
    loadDeadlines();
    dispatch(fetchSubjects(false));
  }, [dispatch]);

  const loadDeadlines = async () => {
    try {
      const res = await apiClient.get<Deadline[]>(ENDPOINTS.DEADLINES.BASE);
      setDeadlines(res.data);
    } catch {
      // empty
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await apiClient.post<Deadline>(ENDPOINTS.DEADLINES.BASE, formData);
      setDeadlines((prev) => [res.data, ...prev]);
      toast.success('Deadline created!');
      setShowModal(false);
    } catch (error) {
      toast.error(handleApiError(error));
    }
  };

  const handleToggleComplete = async (deadline: Deadline) => {
    try {
      const endpoint = deadline.is_completed
        ? ENDPOINTS.DEADLINES.INCOMPLETE(deadline.id)
        : ENDPOINTS.DEADLINES.COMPLETE(deadline.id);
      const res = await apiClient.post<Deadline>(endpoint);
      setDeadlines((prev) => prev.map((d) => (d.id === res.data.id ? res.data : d)));
      toast.success(deadline.is_completed ? 'Marked incomplete' : 'Marked complete!');
    } catch (error) {
      toast.error(handleApiError(error));
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await apiClient.delete(ENDPOINTS.DEADLINES.BY_ID(id));
      setDeadlines((prev) => prev.filter((d) => d.id !== id));
      toast.success('Deadline deleted');
    } catch (error) {
      toast.error(handleApiError(error));
    }
  };

  const pendingDeadlines = deadlines
    .filter((d) => !d.is_completed)
    .sort((a, b) => new Date(a.deadline_date).getTime() - new Date(b.deadline_date).getTime());
  const completedDeadlines = deadlines.filter((d) => d.is_completed);

  const getDaysLeft = (deadlineDate: string) => {
    return Math.ceil((new Date(deadlineDate).getTime() - Date.now()) / (1000 * 60 * 60 * 24));
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Deadlines</h1>
          <p className="text-sm text-[#7a96b0] mt-0.5">Track your upcoming deadlines and due dates</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="inline-flex items-center gap-2 px-4 py-2.5 bg-primary text-white rounded-lg shadow-sm hover:bg-primary/90 transition-colors font-bold text-sm"
        >
          <span className="material-symbols-outlined text-lg">add</span>
          Add Deadline
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-10 w-10 border-[3px] border-[#233648] border-t-primary" />
        </div>
      ) : deadlines.length === 0 ? (
        <div className="rounded-xl border border-[#233648] bg-[#0F172A] p-14 text-center">
          <span className="material-symbols-outlined text-slate-300 text-5xl mb-3">event</span>
          <h3 className="text-base font-bold text-white mb-1">No deadlines</h3>
          <p className="text-sm text-[#7a96b0] mb-5">Add deadlines to stay on top of your work</p>
          <button onClick={() => setShowModal(true)} className="inline-flex items-center gap-2 px-4 py-2.5 bg-primary text-white rounded-lg shadow-sm hover:bg-primary/90 font-bold text-sm">
            <span className="material-symbols-outlined text-lg">add</span>Add Deadline
          </button>
        </div>
      ) : (
        <>
          {pendingDeadlines.length > 0 && (
            <>
              <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-3">Pending ({pendingDeadlines.length})</p>
              <div className="space-y-3 mb-8">
                {pendingDeadlines.map((d) => {
                  const daysLeft = getDaysLeft(d.deadline_date);
                  const isOverdue = daysLeft <= 0;
                  return (
                    <div key={d.id} className={`rounded-xl border border-[#233648] bg-[#0F172A] p-4 border-l-4 ${PRIORITY_LEFT[d.priority]}`}>
                      <div className="flex items-center gap-4">
                        <button
                          onClick={() => handleToggleComplete(d)}
                          className="flex-shrink-0 w-5 h-5 rounded-full border-2 border-slate-600 hover:border-emerald-500 hover:bg-emerald-900/30 transition-colors"
                        />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="font-bold text-white text-sm">{d.title}</span>
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border capitalize ${PRIORITY_STYLES[d.priority]}`}>
                              {d.priority}
                            </span>
                          </div>
                          <div className="flex items-center gap-3 mt-1 text-xs text-[#7a96b0]">
                            <span className="flex items-center gap-1">
                              <span className="material-symbols-outlined text-sm">schedule</span>
                              {new Date(d.deadline_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                            </span>
                            <span className={isOverdue ? 'text-rose-600 font-bold flex items-center gap-0.5' : daysLeft <= 2 ? 'text-amber-600 font-medium' : ''}>
                              {isOverdue ? (
                                <><span className="material-symbols-outlined text-sm">warning</span> Overdue</>
                              ) : `${daysLeft}d left`}
                            </span>
                          </div>
                          {d.description && <p className="text-xs text-[#4a6580] mt-1">{d.description}</p>}
                        </div>
                        <button onClick={() => handleDelete(d.id)} className="p-2 text-[#4a6580] hover:text-rose-400 rounded-lg hover:bg-rose-900/20 transition-colors">
                          <span className="material-symbols-outlined text-lg">delete</span>
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </>
          )}

          {completedDeadlines.length > 0 && (
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-3 flex items-center gap-1.5">
                <span className="material-symbols-outlined text-emerald-500 text-lg">check_circle</span>
                Completed ({completedDeadlines.length})
              </p>
              <div className="space-y-2">
                {completedDeadlines.map((d) => (
                  <div key={d.id} className="rounded-xl border border-[#233648] bg-[#102337] p-4 flex items-center gap-4">
                    <button onClick={() => handleToggleComplete(d)} className="flex-shrink-0">
                      <span className="material-symbols-outlined text-emerald-500 text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
                    </button>
                    <span className="text-slate-400 line-through flex-1 text-sm">{d.title}</span>
                    <button onClick={() => handleDelete(d.id)} className="p-1.5 text-[#4a6580] hover:text-rose-400 rounded-lg hover:bg-rose-900/20 transition-colors">
                      <span className="material-symbols-outlined text-lg">delete</span>
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#102337] rounded-xl border border-[#233648] shadow-xl w-full max-w-md">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#233648]">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-primary">event</span>
                <h2 className="text-base font-bold text-white">New Deadline</h2>
              </div>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white transition-colors">
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>
            <form onSubmit={handleCreate} className="p-6 space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Title *</label>
                <input type="text" value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none text-sm text-white bg-[#102337]" required />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Subject *</label>
                <select value={formData.subject_id} onChange={(e) => setFormData({ ...formData, subject_id: e.target.value })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none text-sm text-white bg-[#102337]" required>
                  <option value="">Select a subject...</option>
                  {subjects.filter((s) => !s.is_archived).map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Deadline Date *</label>
                  <input type="datetime-local" value={formData.deadline_date ? formData.deadline_date.slice(0, 16) : ''}
                    onChange={(e) => setFormData({ ...formData, deadline_date: new Date(e.target.value).toISOString() })}
                    className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none text-sm text-white bg-[#102337]" required />
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Priority</label>
                  <select value={formData.priority} onChange={(e) => setFormData({ ...formData, priority: e.target.value as Priority })}
                    className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none text-sm text-white bg-[#102337]">
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Description</label>
                <textarea value={formData.description || ''} onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none text-sm text-white" rows={2} />
              </div>
              <div className="flex gap-3 pt-1">
                <button type="button" onClick={() => setShowModal(false)} className="flex-1 px-4 py-2.5 border border-[#233648] text-slate-300 rounded-lg hover:bg-[#102337] font-medium text-sm transition-colors">Cancel</button>
                <button type="submit" className="flex-1 px-4 py-2.5 bg-primary text-white rounded-lg hover:bg-primary/90 font-bold text-sm transition-colors shadow-sm">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
