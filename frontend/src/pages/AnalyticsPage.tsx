import { useEffect, useState } from 'react';
import { analyticsService } from '../services/analyticsService';
import type {
  StudyTimeStats,
  SubjectStats,
  ProductivityTrend,
  StreakInfo,
  WellnessCorrelation,
} from '../types';

export function AnalyticsPage() {
  const [stats, setStats] = useState<StudyTimeStats | null>(null);
  const [subjectStats, setSubjectStats] = useState<SubjectStats[]>([]);
  const [trends, setTrends] = useState<ProductivityTrend[]>([]);
  const [streak, setStreak] = useState<StreakInfo | null>(null);
  const [wellness, setWellness] = useState<WellnessCorrelation | null>(null);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(30);

  useEffect(() => {
    loadData();
  }, [days]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [s, sub, t, st, w] = await Promise.all([
        analyticsService.getStudyTime(days),
        analyticsService.getSubjectStats(days),
        analyticsService.getProductivityTrends(days),
        analyticsService.getStreak(),
        analyticsService.getWellnessCorrelation(days),
      ]);
      setStats(s);
      setSubjectStats(sub);
      setTrends(t);
      setStreak(st);
      setWellness(w);
    } catch {
      // empty
    } finally {
      setLoading(false);
    }
  };

  const formatMinutes = (minutes: number) => {
    if (minutes >= 60) {
      const h = Math.floor(minutes / 60);
      const m = minutes % 60;
      return m > 0 ? `${h}h ${m}m` : `${h}h`;
    }
    return `${minutes}m`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-[3px] border-[#233648] border-t-primary" />
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Analytics</h1>
          <p className="text-sm text-[#7a96b0] mt-0.5">Insights into your study patterns</p>
        </div>
        <div className="flex gap-1.5">
          {[7, 14, 30, 90].map((d) => (
            <button
              key={d}
              onClick={() => setDays(d)}
              className={`px-3 py-1.5 rounded-lg text-sm font-bold transition-colors ${
                days === d
                  ? 'bg-primary text-white shadow-sm'
                  : 'bg-[#233648] text-[#7a96b0] hover:bg-[#2d4560]'
              }`}
            >
              {d}d
            </button>
          ))}
        </div>
      </div>

      {stats && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Study Time', value: formatMinutes(stats.total_minutes), icon: 'schedule' },
            { label: 'Sessions', value: String(stats.total_sessions), icon: 'menu_book' },
            { label: 'Avg Productivity', value: `${(stats.average_productivity_score || 0).toFixed(1)}/100`, icon: 'trending_up' },
            { label: 'Avg Focus', value: `${(stats.average_focus_score || 0).toFixed(1)}/100`, icon: 'psychology' },
          ].map((card) => (
            <div key={card.label} className="rounded-xl border border-[#233648] bg-[#0F172A] p-5">
              <div className="flex items-center gap-2 mb-2">
                <span className="material-symbols-outlined text-primary text-xl">{card.icon}</span>
                <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0]">{card.label}</p>
              </div>
              <p className="text-2xl font-bold text-white">{card.value}</p>
            </div>
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="rounded-xl border border-[#233648] bg-[#0F172A] p-6">
          <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-4 flex items-center gap-1.5">
            <span className="material-symbols-outlined text-primary text-lg">menu_book</span>
            Study Time by Subject
          </p>
          {subjectStats.length > 0 ? (
            <div className="space-y-4">
              {subjectStats.map((s) => {
                const maxMinutes = Math.max(...subjectStats.map((x) => x.total_minutes), 1);
                return (
                  <div key={s.subject_id}>
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center gap-2">
                        <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: s.subject_color }} />
                        <span className="text-sm font-medium text-white">{s.subject_name}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-sm font-bold text-slate-300">{formatMinutes(s.total_minutes)}</span>
                        <span className="text-xs text-[#4a6580] ml-2">({s.total_sessions} sessions)</span>
                      </div>
                    </div>
                    <div className="h-1.5 bg-[#233648] rounded-full overflow-hidden">
                      <div className="h-1.5 rounded-full transition-all" style={{ width: `${(s.total_minutes / maxMinutes) * 100}%`, backgroundColor: s.subject_color }} />
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-center py-8 text-[#4a6580] text-sm">No data yet</p>
          )}
        </div>

        <div className="rounded-xl border border-[#233648] bg-[#0F172A] p-6">
          <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-4 flex items-center gap-1.5">
            <span className="material-symbols-outlined text-amber-500 text-lg" style={{ fontVariationSettings: "'FILL' 1" }}>local_fire_department</span>
            Study Streak
          </p>
          {streak ? (
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-[#102337] border border-[#233648] rounded-xl p-4 text-center">
                <p className="text-3xl font-bold text-amber-400">{streak.current_streak}</p>
                <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mt-1">Current</p>
              </div>
              <div className="bg-[#102337] border border-[#233648] rounded-xl p-4 text-center">
                <p className="text-3xl font-bold text-primary">{streak.longest_streak}</p>
                <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mt-1">Longest</p>
              </div>
              <div className="bg-[#102337] border border-[#233648] rounded-xl p-4 text-center">
                <p className="text-3xl font-bold text-emerald-400">{streak.total_study_days}</p>
                <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mt-1">Study Days</p>
              </div>
              <div className="bg-[#102337] border border-[#233648] rounded-xl p-4 text-center">
                <p className="text-sm font-bold text-slate-300">
                  {streak.last_study_date ? new Date(streak.last_study_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : 'N/A'}
                </p>
                <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mt-1">Last Session</p>
              </div>
            </div>
          ) : (
            <p className="text-center py-8 text-[#4a6580] text-sm">No streak data yet</p>
          )}
        </div>
      </div>

      {trends.length > 0 && (
        <div className="rounded-xl border border-[#233648] bg-[#0F172A] p-6 mb-8">
          <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-4 flex items-center gap-1.5">
            <span className="material-symbols-outlined text-emerald-500 text-lg">trending_up</span>
            Productivity Trends — Last {days} Days
          </p>
          <div className="overflow-x-auto">
            <div className="flex items-end gap-1 h-40 min-w-[400px]">
              {trends.map((t) => {
                const maxMinutes = Math.max(...trends.map((x) => x.total_minutes), 1);
                const height = Math.max((t.total_minutes / maxMinutes) * 100, 4);
                return (
                  <div
                    key={t.date}
                    className="flex-1 flex flex-col items-center gap-1"
                    title={`${new Date(t.date).toLocaleDateString()}: ${t.total_minutes}min, Prod: ${t.average_productivity}`}
                  >
                    <div
                      className="w-full bg-primary rounded-t hover:bg-primary/80 transition-colors cursor-help"
                      style={{ height: `${height}%` }}
                    />
                    {trends.length <= 14 && (
                      <span className="text-[10px] text-[#4a6580] -rotate-45 origin-top-left whitespace-nowrap">
                        {new Date(t.date).toLocaleDateString('en-US', { month: 'numeric', day: 'numeric' })}
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {wellness && (
        <div className="rounded-xl border border-[#233648] bg-[#0F172A] p-6">
          <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-4 flex items-center gap-1.5">
            <span className="material-symbols-outlined text-violet-500 text-lg">psychology</span>
            Wellness & Productivity Correlation
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-[#102337] border border-[#233648] rounded-xl p-4">
              <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-2">Sleep & Productivity</p>
              <p className="text-sm text-slate-300">Avg sleep: <span className="font-bold text-white">{wellness.average_sleep_hours.toFixed(1)}h</span></p>
              <p className="text-sm text-slate-300 mt-1">High prod: <span className="font-bold text-white">{wellness.high_productivity_sleep_average.toFixed(1)}h</span></p>
            </div>
            <div className="bg-[#102337] border border-[#233648] rounded-xl p-4">
              <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-2">Energy ↔ Productivity</p>
              <p className="text-lg font-bold text-amber-400 capitalize">{wellness.energy_productivity_correlation}</p>
            </div>
            <div className="bg-[#102337] border border-[#233648] rounded-xl p-4">
              <p className="text-xs font-bold uppercase tracking-wider text-[#7a96b0] mb-2">Low Prod Sleep</p>
              <p className="text-lg font-bold text-rose-400">{wellness.low_productivity_sleep_average.toFixed(1)}h avg</p>
            </div>
          </div>
          {wellness.optimal_sleep_range && (
            <p className="text-sm text-[#7a96b0] mt-4 pt-4 border-t border-[#233648]">
              Optimal sleep range: <span className="font-bold text-white">{wellness.optimal_sleep_range[0]}–{wellness.optimal_sleep_range[1]} hours</span>
            </p>
          )}
        </div>
      )}
    </div>
  );
}
