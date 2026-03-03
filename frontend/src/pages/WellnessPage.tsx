import { useEffect, useState } from 'react';
import apiClient, { handleApiError } from '../services/apiClient';
import { ENDPOINTS } from '../config/constants';
import type { DailyWellness, CreateWellnessRequest } from '../types';
import toast from 'react-hot-toast';

const MOOD_OPTIONS: { value: number; label: string; emoji: string; color: string }[] = [
  { value: 1, label: 'Terrible', emoji: '😫', color: 'bg-red-900/30 text-red-400' },
  { value: 2, label: 'Bad', emoji: '😞', color: 'bg-orange-900/30 text-orange-400' },
  { value: 3, label: 'Neutral', emoji: '😐', color: 'bg-slate-700 text-slate-300' },
  { value: 4, label: 'Good', emoji: '😊', color: 'bg-green-900/30 text-green-400' },
  { value: 5, label: 'Excellent', emoji: '🤩', color: 'bg-emerald-900/30 text-emerald-400' },
];

export function WellnessPage() {
  const [entries, setEntries] = useState<DailyWellness[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState<CreateWellnessRequest>({
    date: new Date().toISOString().split('T')[0],
    sleep_hours: 7,
    sleep_quality: 3,
    energy_level: 3,
    stress_level: 5,
    mood: 4,
    focus_score: 50,
    notes: '',
  });

  useEffect(() => {
    loadEntries();
  }, []);

  const loadEntries = async () => {
    try {
      const res = await apiClient.get<DailyWellness[]>(ENDPOINTS.WELLNESS.BASE);
      setEntries(res.data);
    } catch {
      // empty
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await apiClient.post<DailyWellness>(ENDPOINTS.WELLNESS.BASE, formData);
      setEntries((prev) => [res.data, ...prev]);
      toast.success('Wellness entry logged!');
      setShowModal(false);
    } catch (error) {
      toast.error(handleApiError(error));
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await apiClient.delete(ENDPOINTS.WELLNESS.BY_ID(id));
      setEntries((prev) => prev.filter((e) => e.id !== id));
      toast.success('Entry deleted');
    } catch (error) {
      toast.error(handleApiError(error));
    }
  };

  const getMoodConfig = (mood?: number) =>
    MOOD_OPTIONS.find((m) => m.value === mood) || MOOD_OPTIONS[2];

  return (
    <div className="max-w-5xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Wellness Tracker</h1>
          <p className="text-sm text-[#7a96b0] mt-0.5">Log your daily wellness to track wellbeing trends</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="inline-flex items-center gap-2 px-4 py-2.5 bg-primary text-white rounded-lg shadow-sm hover:bg-primary/90 transition-colors font-bold text-sm"
        >
          <span className="material-symbols-outlined text-lg">add</span>
          Log Today
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-10 w-10 border-[3px] border-[#233648] border-t-primary" />
        </div>
      ) : entries.length === 0 ? (
        <div className="rounded-xl border border-[#233648] bg-[#0F172A] p-14 text-center">
          <span className="material-symbols-outlined text-slate-300 text-5xl mb-3">favorite</span>
          <h3 className="text-base font-bold text-white mb-1">No wellness entries yet</h3>
          <p className="text-sm text-[#7a96b0] mb-5">Start logging your daily wellness and track your trends</p>
          <button
            onClick={() => setShowModal(true)}
            className="inline-flex items-center gap-2 px-4 py-2.5 bg-primary text-white rounded-lg shadow-sm hover:bg-primary/90 font-bold text-sm"
          >
            <span className="material-symbols-outlined text-lg">add</span>
            Log First Entry
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {entries.map((entry) => {
            const moodConfig = getMoodConfig(entry.mood);
            return (
              <div key={entry.id} className="rounded-xl border border-[#233648] bg-[#0F172A] p-5 hover:shadow-card transition-shadow">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-bold uppercase tracking-wider text-[#7a96b0]">
                    {new Date(entry.date).toLocaleDateString('en-US', {
                      weekday: 'short', month: 'short', day: 'numeric',
                    })}
                  </span>
                  <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${moodConfig.color}`}>
                    {moodConfig.emoji} {moodConfig.label}
                  </span>
                </div>

                <div className="space-y-3">
                  <WellnessBar label="Sleep" value={entry.sleep_hours || 0} max={12} unit="hrs" color="bg-primary" />
                  <WellnessBar label="Sleep Quality" value={entry.sleep_quality || 0} max={5} color="bg-violet-500" />
                  <WellnessBar label="Energy" value={entry.energy_level || 0} max={5} color="bg-amber-500" />
                  <WellnessBar label="Stress" value={entry.stress_level || 0} max={10} color="bg-rose-500" />
                  <WellnessBar label="Focus" value={entry.focus_score || 0} max={100} color="bg-emerald-500" />
                </div>

                {entry.notes && (
                  <p className="text-xs text-[#4a6580] mt-3 italic">"{entry.notes}"</p>
                )}

                <button
                  onClick={() => handleDelete(entry.id)}
                  className="mt-3 flex items-center gap-1 text-xs text-[#4a6580] hover:text-rose-500 transition-colors"
                >
                  <span className="material-symbols-outlined text-sm">delete</span>
                  Delete
                </button>
              </div>
            );
          })}
        </div>
      )}

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#102337] rounded-xl border border-[#233648] shadow-xl w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#233648]">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>favorite</span>
                <h2 className="text-base font-bold text-white">Log Wellness</h2>
              </div>
              <button
                onClick={() => setShowModal(false)}
                className="text-slate-400 hover:text-white transition-colors"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>
            <form onSubmit={handleCreate} className="p-6 space-y-5">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Date</label>
                <input
                  type="date"
                  value={formData.date}
                  onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none text-sm text-white bg-[#102337]"
                />
              </div>

              {/* Mood */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-2">Mood</label>
                <div className="flex gap-2">
                  {MOOD_OPTIONS.map((m) => (
                    <button
                      key={m.value}
                      type="button"
                      onClick={() => setFormData({ ...formData, mood: m.value })}
                      className={`flex-1 py-2 text-center rounded-lg text-sm transition-all ${
                        formData.mood === m.value
                          ? `${m.color} ring-2 ring-offset-1 ring-primary/50`
                          : 'bg-[#102337] text-[#7a96b0] hover:bg-[#233648]'
                      }`}
                    >
                      <div className="text-lg">{m.emoji}</div>
                      <div className="text-[10px] mt-0.5 font-medium">{m.label}</div>
                    </button>
                  ))}
                </div>
              </div>

              <SliderField label="Sleep Hours" value={formData.sleep_hours || 7} min={0} max={12} step={0.5} unit="hrs" onChange={(v) => setFormData({ ...formData, sleep_hours: v })} />
              <SliderField label="Sleep Quality" value={formData.sleep_quality || 3} min={1} max={5} onChange={(v) => setFormData({ ...formData, sleep_quality: v })} />
              <SliderField label="Energy Level" value={formData.energy_level || 3} min={1} max={5} onChange={(v) => setFormData({ ...formData, energy_level: v })} />
              <SliderField label="Stress Level" value={formData.stress_level || 5} min={1} max={10} onChange={(v) => setFormData({ ...formData, stress_level: v })} />
              <SliderField label="Focus Score" value={formData.focus_score || 50} min={1} max={100} step={5} onChange={(v) => setFormData({ ...formData, focus_score: v })} />

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-1.5">Notes</label>
                <textarea
                  value={formData.notes || ''}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  className="w-full px-3 py-2 border border-[#233648] rounded-lg focus:ring-2 focus:ring-primary/30 focus:border-primary outline-none resize-none text-sm text-white"
                  rows={2}
                  placeholder="How was your day?"
                />
              </div>

              <div className="flex gap-3 pt-1">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 px-4 py-2.5 border border-[#233648] text-slate-300 rounded-lg hover:bg-[#102337] font-medium text-sm transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2.5 bg-primary text-white rounded-lg hover:bg-primary/90 font-bold text-sm transition-colors shadow-sm"
                >
                  Save Entry
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function WellnessBar({ label, value, max, unit, color }: {
  label: string; value: number; max: number; unit?: string; color: string;
}) {
  const pct = (value / max) * 100;
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-500 font-medium">{label}</span>
        <span className="font-bold text-white">{value}{unit ? ` ${unit}` : `/${max}`}</span>
      </div>
      <div className="h-1.5 bg-[#233648] rounded-full overflow-hidden">
        <div className={`h-1.5 rounded-full transition-all ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

function SliderField({ label, value, min, max, step = 1, unit, onChange }: {
  label: string; value: number; min: number; max: number; step?: number; unit?: string;
  onChange: (v: number) => void;
}) {
  return (
    <div>
      <div className="flex justify-between mb-1.5">
        <label className="text-xs font-bold uppercase tracking-wider text-[#7a96b0]">{label}</label>
        <span className="text-xs font-bold text-primary">{value}{unit ? ` ${unit}` : `/${max}`}</span>
      </div>
      <input
        type="range" min={min} max={max} step={step} value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full accent-primary"
      />
    </div>
  );
}
