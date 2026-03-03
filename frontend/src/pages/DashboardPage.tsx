import { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppSelector } from '../store/hooks';
import { analyticsService } from '../services/analyticsService';
import { aiService } from '../services/aiService';
import { ENDPOINTS } from '../config/constants';
import apiClient from '../services/apiClient';
import type { DashboardAnalytics, AiProductivityPrediction, PeakStudyHoursResponse } from '../types';

/* ══════════════════════════════════════════════════════════════════════════════
   DASHBOARD PAGE - Modern Analytics Design
   Matches reference: primary #137fec, Lexend font, Material Symbols icons
══════════════════════════════════════════════════════════════════════════════ */

type Tab = 'overview' | 'predictions' | 'history';

export function DashboardPage() {
  const navigate = useNavigate();
  const { user } = useAppSelector((state) => state.auth);
  const [analytics, setAnalytics] = useState<DashboardAnalytics | null>(null);
  const [_loading, setLoading] = useState(true);
  const [aiPrediction, setAiPrediction] = useState<AiProductivityPrediction | null>(null);
  const [peakHours, setPeakHours] = useState<PeakStudyHoursResponse | null>(null);
  const [aiLoading, setAiLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<Tab>('overview');

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const data = await analyticsService.getDashboard(30);
      setAnalytics(data);
      loadAiData(data.study_time_stats);
    } catch {
      loadAiData(null);
    } finally {
      setLoading(false);
    }
  };

  const loadAiData = async (studyStats: DashboardAnalytics['study_time_stats'] | null) => {
    setAiLoading(true);
    try {
      let sleepHours = 7, stressLevel = 5, focusScore = 50;
      try {
        const wellnessRes = await apiClient.get(ENDPOINTS.WELLNESS.BASE, { params: { limit: 1 } });
        const latest = wellnessRes.data?.[0];
        if (latest) {
          sleepHours = latest.sleep_hours ?? 7;
          stressLevel = latest.stress_level ?? 5;
          focusScore = latest.focus_score ?? 50;
        }
      } catch { /* ignore */ }

      const studyHoursPerDay = studyStats?.total_minutes
        ? Math.round((studyStats.total_minutes / 30 / 60) * 10) / 10
        : 3;

      const [prediction, hours] = await Promise.allSettled([
        aiService.predictProductivity({
          study_hours_per_day: studyHoursPerDay,
          sleep_hours: sleepHours,
          stress_level: stressLevel,
          focus_score: focusScore,
        }),
        aiService.getPeakHours(),
      ]);
      if (prediction.status === 'fulfilled') setAiPrediction(prediction.value);
      if (hours.status === 'fulfilled') setPeakHours(hours.value);
    } catch { /* ignore */ }
    finally { setAiLoading(false); }
  };

  /* ─── Computed Values ─── */
  const stats = analytics?.study_time_stats;
  const streak = analytics?.streak_info;
  const trends = analytics?.productivity_trends ?? [];
  const totalHours = stats ? +(stats.total_minutes / 60).toFixed(1) : 0;
  const productivityScore = aiPrediction
    ? Math.round(aiPrediction.predicted_score)
    : stats ? Math.round(stats.average_productivity_score) : 0;

  /* ─── Helpers ─── */
  const formatMinutes = (m: number) => m >= 60 ? `${Math.floor(m/60)}h ${m%60 > 0 ? `${m%60}m` : ''}`.trim() : `${m}m`;
  const formatHour = (h: number) => h === 0 ? '12 AM' : h === 12 ? '12 PM' : h < 12 ? `${h} AM` : `${h-12} PM`;

  /* ─── SVG Trend Path ─── */
  const trendPath = useMemo(() => {
    if (trends.length < 2) return null;
    const recent = trends.slice(-14);
    const maxProd = Math.max(...recent.map(t => t.average_productivity), 1);
    const width = 478, height = 140;
    const step = width / (recent.length - 1);
    const points = recent.map((t, i) => ({
      x: i * step,
      y: height - (t.average_productivity / maxProd) * (height - 10) - 5,
    }));
    let d = `M${points[0].x} ${points[0].y}`;
    for (let i = 0; i < points.length - 1; i++) {
      const p0 = points[Math.max(i - 1, 0)];
      const p1 = points[i];
      const p2 = points[i + 1];
      const p3 = points[Math.min(i + 2, points.length - 1)];
      const cp1x = p1.x + (p2.x - p0.x) / 6;
      const cp1y = p1.y + (p2.y - p0.y) / 6;
      const cp2x = p2.x - (p3.x - p1.x) / 6;
      const cp2y = p2.y - (p3.y - p1.y) / 6;
      d += ` C${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${p2.x} ${p2.y}`;
    }
    const fillD = d + ` L${points[points.length-1].x} ${height} L${points[0].x} ${height} Z`;
    return { line: d, fill: fillD, labels: recent };
  }, [trends]);

  /* ═══════════════════════════════════════════════════════════════════════════ */
  /*                              R E N D E R                                    */
  /* ═══════════════════════════════════════════════════════════════════════════ */

  const tabs: { key: Tab; label: string }[] = [
    { key: 'overview', label: 'Overview' },
    { key: 'predictions', label: 'Predictions' },
    { key: 'history', label: 'History' },
  ];

  return (
    <div className="max-w-5xl mx-auto">
      {/* ══════════ PAGE HEADER ══════════ */}
      <div className="flex items-center justify-between mb-2">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
            Analytics &amp; Insights
          </h1>
          <p className="text-sm text-[#7a96b0] mt-0.5">
            Welcome back, {user?.full_name?.split(' ')[0] || 'Student'}
          </p>
        </div>
        <button
          onClick={() => navigate('/analytics')}
          className="hidden sm:flex items-center gap-1.5 text-sm font-medium text-primary hover:text-primary-700 transition-colors"
        >
          <span>Full report</span>
          <span className="material-symbols-outlined text-lg">arrow_forward</span>
        </button>
      </div>

      {/* ══════════ TAB NAVIGATION ══════════ */}
      <div className="flex border-b border-[#233648] mt-4 mb-6 gap-8">
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setActiveTab(t.key)}
            className={`pb-3 pt-1 text-sm font-bold leading-normal border-b-[3px] transition-all duration-200 ${
              activeTab === t.key
                ? 'border-primary text-primary'
                : 'border-transparent text-[#4a6580] hover:text-white'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* ════════════════════════════════════════════════════════════════════════ */}
      {/*                         O V E R V I E W   T A B                          */}
      {/* ════════════════════════════════════════════════════════════════════════ */}
      {activeTab === 'overview' && (
        <>
          {/* Key Stats Cards */}
          <div className="flex flex-wrap gap-4 mb-6">
            <StatCard
              label="Study Score"
              value={productivityScore}
              suffix="/100"
              trend={productivityScore >= 50 ? 'up' : 'down'}
              trendValue={productivityScore >= 50 ? 'Good' : 'Low'}
              icon="emoji_events"
            />
            <StatCard
              label="Study Hours"
              value={totalHours}
              trend="up"
              trendValue={`${stats?.total_sessions ?? 0} sessions`}
              icon="schedule"
            />
            <StatCard
              label="Current Streak"
              value={streak?.current_streak ?? 0}
              suffix=" days"
              trend="fire"
              trendValue={`Best: ${streak?.longest_streak ?? 0}`}
              icon="local_fire_department"
            />
          </div>

          {/* Performance Trend Chart */}
          <div className="mb-6">
            <div className="flex flex-col gap-4 p-6 rounded-xl border border-[#233648] bg-[#0F172A] shadow-card">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-white text-base font-bold">Performance Trend</p>
                  <p className="text-slate-400 text-xs">Average score over last 30 days</p>
                </div>
                <div className="bg-primary/10 text-primary px-3 py-1 rounded-full text-xs font-bold">
                  Monthly
                </div>
              </div>
              <div className="flex min-h-[180px] flex-col gap-4 py-2">
                {trendPath ? (
                  <>
                    <svg fill="none" height="140" preserveAspectRatio="none" viewBox="0 0 478 140" width="100%" xmlns="http://www.w3.org/2000/svg">
                      <defs>
                        <linearGradient id="trendGrad" x1="239" y1="0" x2="239" y2="140" gradientUnits="userSpaceOnUse">
                          <stop stopColor="#137fec" stopOpacity="0.3" />
                          <stop offset="1" stopColor="#137fec" stopOpacity="0" />
                        </linearGradient>
                      </defs>
                      <path d={trendPath.fill} fill="url(#trendGrad)" />
                      <path d={trendPath.line} stroke="#137fec" strokeLinecap="round" strokeWidth="3" />
                    </svg>
                    <div className="flex justify-between px-1">
                      {trendPath.labels.filter((_, i) => i % Math.max(Math.floor(trendPath.labels.length / 4), 1) === 0).slice(0, 4).map((t) => (
                        <p key={t.date} className="text-slate-400 text-[10px] font-bold uppercase">
                          {new Date(t.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                        </p>
                      ))}
                    </div>
                  </>
                ) : (
                  <div className="flex items-center justify-center h-[140px] text-slate-300">
                    <span className="material-symbols-outlined text-4xl mr-3">insert_chart</span>
                    <p className="text-sm text-[#4a6580]">Complete study sessions to see your trend</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Subject + Deadlines Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
            {/* Subject Breakdown */}
            <div className="flex flex-col gap-4 p-6 rounded-xl border border-[#233648] bg-[#0F172A] shadow-card">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-primary">menu_book</span>
                  <p className="text-white text-base font-bold">Subject Breakdown</p>
                </div>
                <button onClick={() => navigate('/subjects')} className="text-xs font-bold text-primary hover:text-primary-700 transition-colors">
                  View all
                </button>
              </div>
              {analytics?.subject_stats && analytics.subject_stats.length > 0 ? (
                <div className="space-y-3">
                  {analytics.subject_stats.slice(0, 5).map((s) => (
                    <div key={s.subject_id} className="flex items-center gap-3">
                      <div className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: s.subject_color }} />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-medium text-slate-800 truncate">{s.subject_name}</span>
                          <span className="text-xs text-[#4a6580] font-medium">{formatMinutes(s.total_minutes)}</span>
                        </div>
                        <div className="h-1.5 bg-[#233648] rounded-full overflow-hidden">
                          <div className="h-1.5 rounded-full transition-all" style={{
                            width: `${Math.min((s.total_minutes / Math.max(...analytics.subject_stats.map(x => x.total_minutes), 1)) * 100, 100)}%`,
                            backgroundColor: s.subject_color,
                          }} />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState icon="menu_book" text="No study data yet. Start a session!" />
              )}
            </div>

            {/* Upcoming Deadlines */}
            <div className="flex flex-col gap-4 p-6 rounded-xl border border-[#233648] bg-[#0F172A] shadow-card">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-warning-500">event</span>
                  <p className="text-white text-base font-bold">Upcoming Deadlines</p>
                </div>
                <button onClick={() => navigate('/deadlines')} className="text-xs font-bold text-primary hover:text-primary-700 transition-colors">
                  View all
                </button>
              </div>
              {analytics?.upcoming_deadlines && analytics.upcoming_deadlines.length > 0 ? (
                <div className="space-y-2">
                  {analytics.upcoming_deadlines.slice(0, 5).map((d) => {
                    const dueDate = new Date(d.deadline_date);
                    const daysLeft = Math.ceil((dueDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24));
                    const urgencyClass = daysLeft <= 1 ? 'bg-danger-900/40 border-danger-700 text-danger-400' : daysLeft <= 3 ? 'bg-warning-900/30 border-warning-700 text-warning-400' : 'bg-[#102337] border-[#233648] text-[#7a96b0]';
                    return (
                      <div key={d.id} className={`flex items-center justify-between p-3 rounded-lg border ${daysLeft <= 1 ? 'border-danger-800 bg-danger-900/20' : daysLeft <= 3 ? 'border-warning-800 bg-warning-900/20' : 'border-[#233648] bg-[#102337]'}`}>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-white truncate">{d.title}</p>
                          <p className="text-xs text-[#4a6580]">{dueDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</p>
                        </div>
                        <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${urgencyClass}`}>
                          {daysLeft <= 0 ? 'Overdue' : `${daysLeft}d left`}
                        </span>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <EmptyState icon="event" text="No upcoming deadlines" />
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <QuickAction icon="timer" label="Start Session" desc="Track study time" color="primary" onClick={() => navigate('/sessions')} />
            <QuickAction icon="favorite" label="Log Wellness" desc="Track well-being" color="rose" onClick={() => navigate('/wellness')} />
            <QuickAction icon="bar_chart" label="View Analytics" desc="Full reports" color="emerald" onClick={() => navigate('/analytics')} />
          </div>
        </>
      )}

      {/* ════════════════════════════════════════════════════════════════════════ */}
      {/*                     P R E D I C T I O N S   T A B                        */}
      {/* ════════════════════════════════════════════════════════════════════════ */}
      {activeTab === 'predictions' && (
        <>
          {/* AI Header */}
          <div className="flex items-center gap-2 mb-5">
            <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>auto_awesome</span>
            <h3 className="text-white text-lg font-bold">AI Predictions</h3>
          </div>

          {aiLoading ? (
            <div className="flex items-center justify-center py-16">
              <div className="animate-spin rounded-full h-10 w-10 border-[3px] border-[#233648] border-t-primary" />
            </div>
          ) : (
            <>
              {/* Prediction Cards Grid */}
              <div className="grid grid-cols-2 gap-3 mb-6">
                {/* Main Prediction */}
                <div className="bg-primary/5 border border-primary/20 p-5 rounded-xl flex flex-col gap-1 col-span-2 sm:col-span-1">
                  <p className="text-slate-400 text-xs font-medium uppercase tracking-wider">Productivity Score</p>
                  <div className="flex items-baseline gap-3 mt-1">
                    <p className="text-white text-4xl font-bold">{aiPrediction ? Math.round(aiPrediction.predicted_score) : '—'}</p>
                    <span className="text-slate-400 text-sm">/100</span>
                  </div>
                  {aiPrediction && (
                    <p className="text-slate-400 text-[11px] mt-2 flex items-center gap-1">
                      <span className="material-symbols-outlined text-xs">verified</span>
                      Confidence: {Math.round(aiPrediction.confidence * 100)}%
                    </p>
                  )}
                </div>

                {/* Subject Cards */}
                {analytics?.subject_stats && analytics.subject_stats.length > 0 ? (
                  analytics.subject_stats.slice(0, 3).map((s) => (
                    <div key={s.subject_id} className="bg-[#102337] border border-[#233648] p-4 rounded-xl flex flex-col gap-1">
                      <p className="text-slate-400 text-xs font-medium">{s.subject_name}</p>
                      <p className="text-white text-xl font-bold">{Math.round(s.average_productivity)}%</p>
                      <p className="text-slate-400 text-[10px] mt-2">{s.total_sessions} sessions · {formatMinutes(s.total_minutes)}</p>
                    </div>
                  ))
                ) : (
                  <div className="bg-[#102337] border border-[#233648] p-4 rounded-xl flex flex-col items-center justify-center gap-1 col-span-1">
                    <span className="material-symbols-outlined text-slate-300 text-2xl">menu_book</span>
                    <p className="text-slate-400 text-xs">No subjects yet</p>
                  </div>
                )}
              </div>

              {/* Study Insights */}
              <h3 className="text-white text-lg font-bold mb-4">Study Insights</h3>
              <div className="space-y-3 mb-6">
                {peakHours && peakHours.peak_hours.length > 0 && (
                  <InsightCard icon="lightbulb" iconBg="bg-success-500" borderColor="border-[#233648]" bgColor="bg-[#102337]"
                    title={`Peak Morning Focus: ${formatHour(peakHours.best_hour)}`}
                    description={`Your productivity is ${Math.round(peakHours.best_productivity)}% higher during this hour. Schedule important study here.`}
                  />
                )}
                {aiPrediction?.top_factors?.slice(0, 2).map((f, i) => f.impact === 'positive' ? (
                  <InsightCard key={i} icon="psychology" iconBg="bg-primary" borderColor="border-[#233648]" bgColor="bg-[#102337]"
                    title={`Strong Point: ${f.factor}`}
                    description={`This factor positively impacts your productivity by ${f.value} points.`}
                  />
                ) : (
                  <InsightCard key={i} icon="warning" iconBg="bg-warning-500" borderColor="border-[#233648]" bgColor="bg-[#102337]"
                    title={`Needs Attention: ${f.factor}`}
                    description={`This factor is pulling your score down by ${Math.abs(f.value)} points. Consider improving it.`}
                  />
                ))}
                {aiPrediction?.recommendation && (
                  <InsightCard icon="tips_and_updates" iconBg="bg-violet-600" borderColor="border-[#233648]" bgColor="bg-[#102337]"
                    title="AI Recommendation"
                    description={aiPrediction.recommendation}
                  />
                )}
                {!aiPrediction && !peakHours && (
                  <EmptyState icon="psychology" text="Log study sessions and wellness data to unlock AI insights" />
                )}
              </div>
            </>
          )}
        </>
      )}

      {/* ════════════════════════════════════════════════════════════════════════ */}
      {/*                         H I S T O R Y   T A B                            */}
      {/* ════════════════════════════════════════════════════════════════════════ */}
      {activeTab === 'history' && (
        <>
          {/* Peak Study Hours */}
          <div className="flex flex-col gap-4 p-6 rounded-xl border border-[#233648] bg-[#0F172A] shadow-card mb-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-warning-500">schedule</span>
                <div>
                  <p className="text-white text-base font-bold">Peak Study Hours</p>
                  <p className="text-slate-400 text-xs">When you're most productive</p>
                </div>
              </div>
              {peakHours && peakHours.peak_hours.length > 0 && (
                <div className="bg-[#102337] text-warning-400 px-3 py-1 rounded-full text-xs font-bold border border-[#233648]">
                  {peakHours.total_sessions_analyzed} sessions
                </div>
              )}
            </div>
            {aiLoading ? (
              <div className="flex items-center justify-center py-10">
                <div className="animate-spin rounded-full h-8 w-8 border-[3px] border-[#233648] border-t-warning-500" />
              </div>
            ) : peakHours && peakHours.peak_hours.length > 0 ? (
              <div>
                <div className="bg-[#102337] border border-[#233648] rounded-xl p-4 mb-5 text-center">
                  <p className="text-xs text-[#7a96b0] font-medium mb-1">Best time to study</p>
                  <p className="text-2xl font-bold text-white">{formatHour(peakHours.best_hour)} — {formatHour((peakHours.best_hour + 1) % 24)}</p>
                  <p className="text-xs text-warning-400 mt-1">Avg productivity: {Math.round(peakHours.best_productivity)}%</p>
                </div>
                <div className="space-y-2.5">
                  {peakHours.peak_hours.sort((a, b) => b.average_productivity - a.average_productivity).slice(0, 8).map((h) => {
                    const isTop = h.hour === peakHours.best_hour;
                    return (
                      <div key={h.hour} className="flex items-center gap-3">
                        <span className="text-xs font-mono text-[#4a6580] w-14 text-right">{formatHour(h.hour)}</span>
                        <div className="flex-1 h-4 bg-[#233648] rounded-full overflow-hidden">
                          <div className={`h-4 rounded-full transition-all ${isTop ? 'bg-gradient-to-r from-warning-400 to-warning-500' : 'bg-warning-200'}`} style={{ width: `${Math.max(h.average_productivity, 5)}%` }} />
                        </div>
                        <span className="text-xs font-bold text-slate-600 w-10">{Math.round(h.average_productivity)}%</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            ) : (
              <EmptyState icon="schedule" text="Complete more study sessions to discover your peak hours" />
            )}
          </div>

          {/* Study Streak */}
          <div className="flex flex-col gap-4 p-6 rounded-xl border border-[#233648] bg-[#0F172A] shadow-card mb-6">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-danger-500" style={{ fontVariationSettings: "'FILL' 1" }}>local_fire_department</span>
              <p className="text-white text-base font-bold">Study Streak</p>
            </div>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-3xl font-bold text-white">{streak?.current_streak ?? 0}</p>
                <p className="text-xs text-[#4a6580] mt-1">Current Streak</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-white">{streak?.longest_streak ?? 0}</p>
                <p className="text-xs text-[#4a6580] mt-1">Longest Streak</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-white">{streak?.total_study_days ?? 0}</p>
                <p className="text-xs text-[#4a6580] mt-1">Total Study Days</p>
              </div>
            </div>
            {streak?.last_study_date && (
              <p className="text-xs text-[#4a6580] text-center mt-2">
                Last studied: {new Date(streak.last_study_date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
              </p>
            )}
          </div>

          {/* Wellness Correlation */}
          {analytics?.wellness_correlation && (
            <div className="flex flex-col gap-4 p-6 rounded-xl border border-[#233648] bg-[#0F172A] shadow-card mb-6">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>favorite</span>
                <p className="text-white text-base font-bold">Wellness &amp; Productivity</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-[#102337] border border-[#233648] rounded-xl p-4 text-center">
                  <p className="text-2xl font-bold text-white">{analytics.wellness_correlation.average_sleep_hours.toFixed(1)}h</p>
                  <p className="text-xs text-[#7a96b0] mt-1">Avg Sleep</p>
                </div>
                <div className="bg-[#102337] border border-[#233648] rounded-xl p-4 text-center">
                  <p className="text-2xl font-bold text-white">{Math.round(analytics.wellness_correlation.average_productivity)}%</p>
                  <p className="text-xs text-[#7a96b0] mt-1">Avg Productivity</p>
                </div>
                <div className="bg-[#102337] border border-[#233648] rounded-xl p-4 text-center col-span-2">
                  <p className="text-sm font-medium text-[#7a96b0]">
                    Optimal sleep: <span className="font-bold text-white">{analytics.wellness_correlation.optimal_sleep_range[0]}–{analytics.wellness_correlation.optimal_sleep_range[1]}h</span>
                  </p>
                  <p className="text-xs text-primary mt-1">
                    Energy correlation: {analytics.wellness_correlation.energy_productivity_correlation}
                  </p>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════════════
   S U B - C O M P O N E N T S
═══════════════════════════════════════════════════════════════════════════════ */

function StatCard({ label, value, suffix, trend, trendValue, icon }: {
  label: string;
  value: number | string;
  suffix?: string;
  trend: 'up' | 'down' | 'fire';
  trendValue: string;
  icon: string;
}) {
  const trendColors = {
    up: 'text-success-500',
    down: 'text-warning-500',
    fire: 'text-danger-500',
  };
  const trendIcons = {
    up: 'trending_up',
    down: 'trending_down',
    fire: 'local_fire_department',
  };
  return (
    <div className="flex min-w-[150px] flex-1 flex-col gap-2 rounded-xl p-5 border border-[#233648] bg-[#0F172A]/50 shadow-card">
      <div className="flex items-center justify-between">
        <p className="text-slate-400 text-xs font-medium uppercase tracking-wider">{label}</p>
        <span className="material-symbols-outlined text-primary/40 text-xl">{icon}</span>
      </div>
      <div className="flex items-baseline gap-2">
        <p className="text-white text-3xl font-bold">
          {value}
          {suffix && <span className="text-sm font-normal text-[#4a6580]">{suffix}</span>}
        </p>
        <p className={`text-sm font-bold flex items-center gap-0.5 ${trendColors[trend]}`}>
          <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: trend === 'fire' ? "'FILL' 1" : "'FILL' 0" }}>{trendIcons[trend]}</span>
          {trendValue}
        </p>
      </div>
    </div>
  );
}

function InsightCard({ icon, iconBg, borderColor, bgColor, title, description }: {
  icon: string;
  iconBg: string;
  borderColor: string;
  bgColor: string;
  title: string;
  description: string;
}) {
  return (
    <div className={`flex items-center gap-4 p-4 rounded-xl ${bgColor} border ${borderColor}`}>
      <div className={`${iconBg} text-white w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0`}>
        <span className="material-symbols-outlined text-xl">{icon}</span>
      </div>
      <div className="min-w-0">
        <p className="text-white text-sm font-bold">{title}</p>
        <p className="text-slate-500 text-xs leading-relaxed">{description}</p>
      </div>
    </div>
  );
}

function QuickAction({ icon, label, desc, color, onClick }: {
  icon: string;
  label: string;
  desc: string;
  color: 'primary' | 'rose' | 'emerald';
  onClick: () => void;
}) {
  const colors = {
    primary: 'border-primary/30 hover:border-primary hover:bg-[#102337] text-primary',
    rose: 'border-rose-800 hover:border-rose-600 hover:bg-[#102337] text-rose-400',
    emerald: 'border-emerald-800 hover:border-emerald-600 hover:bg-[#102337] text-emerald-400',
  };
  return (
    <button onClick={onClick} className={`p-4 border rounded-xl transition-all duration-200 text-left group flex items-center gap-3 ${colors[color]}`}>
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${color === 'primary' ? 'bg-primary/10' : color === 'rose' ? 'bg-rose-100' : 'bg-success-100'}`}>
        <span className="material-symbols-outlined text-xl">{icon}</span>
      </div>
      <div className="flex-1 min-w-0">
        <p className="font-bold text-sm text-white">{label}</p>
        <p className="text-xs text-[#4a6580]">{desc}</p>
      </div>
      <span className="material-symbols-outlined text-slate-300 group-hover:text-slate-500 transition-colors">arrow_forward</span>
    </button>
  );
}

function EmptyState({ icon, text }: { icon: string; text: string }) {
  return (
    <div className="text-center py-8">
      <span className="material-symbols-outlined text-slate-300 text-4xl mb-2">{icon}</span>
      <p className="text-sm text-[#4a6580]">{text}</p>
    </div>
  );
}
