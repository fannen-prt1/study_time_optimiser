import { useState, useEffect, useCallback, useRef } from 'react';
import { Play, Pause, Square } from 'lucide-react';

interface SessionTimerProps {
  /** Whether the timer is actively running */
  isRunning: boolean;
  /** Whether the timer is paused */
  isPaused: boolean;
  /** Planned duration in minutes */
  plannedDuration: number;
  /** Start time ISO string (used to calculate elapsed) */
  startTime?: string;
  /** Total pause duration in minutes from backend */
  totalPauseDurationMinutes?: number;
  /** Callbacks */
  onStart: () => void;
  onPause: () => void;
  onResume: () => void;
  onComplete: (elapsedMinutes: number) => void;
}

export function SessionTimer({
  isRunning,
  isPaused,
  plannedDuration,
  startTime,
  totalPauseDurationMinutes = 0,
  onStart,
  onPause,
  onResume,
  onComplete,
}: SessionTimerProps) {
  const [elapsed, setElapsed] = useState(0); // seconds
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Calculate initial elapsed from startTime, subtracting pause duration
  useEffect(() => {
    if (startTime && isRunning) {
      // Backend stores UTC times - ensure we parse as UTC
      const utcStartTime = startTime.endsWith('Z') ? startTime : startTime + 'Z';
      const start = new Date(utcStartTime).getTime();
      const now = Date.now();
      const pauseSeconds = (totalPauseDurationMinutes || 0) * 60;
      setElapsed(Math.max(0, Math.floor((now - start) / 1000) - pauseSeconds));
    }
  }, [startTime, isRunning, totalPauseDurationMinutes]);

  // Timer tick
  useEffect(() => {
    if (isRunning && !isPaused) {
      intervalRef.current = setInterval(() => {
        setElapsed((prev) => prev + 1);
      }, 1000);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isRunning, isPaused]);

  const handleComplete = useCallback(() => {
    const minutes = Math.max(1, Math.round(elapsed / 60));
    onComplete(minutes);
    setElapsed(0);
  }, [elapsed, onComplete]);

  const totalSeconds = plannedDuration * 60;
  const progress = Math.min((elapsed / totalSeconds) * 100, 100);
  const isOvertime = elapsed > totalSeconds;

  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    if (h > 0) {
      return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    }
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-[#0F172A] rounded-xl shadow-lg p-6">
      {/* Timer display */}
      <div className="text-center mb-6">
        <div className="relative inline-flex items-center justify-center">
          {/* Progress ring */}
          <svg className="w-48 h-48 -rotate-90" viewBox="0 0 200 200">
            <circle
              cx="100"
              cy="100"
              r="90"
              fill="none"
              stroke="#e5e7eb"
              strokeWidth="8"
            />
            <circle
              cx="100"
              cy="100"
              r="90"
              fill="none"
              stroke={isOvertime ? '#ef4444' : '#6366f1'}
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={`${2 * Math.PI * 90}`}
              strokeDashoffset={`${2 * Math.PI * 90 * (1 - progress / 100)}`}
              className="transition-all duration-1000"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span
              className={`text-4xl font-mono font-bold ${
                isOvertime ? 'text-red-400' : 'text-white'
              }`}
            >
              {formatTime(elapsed)}
            </span>
            <span className="text-sm text-[#7a96b0] mt-1">
              / {formatTime(totalSeconds)}
            </span>
            {isOvertime && (
              <span className="text-xs text-red-500 mt-1 font-medium">Overtime!</span>
            )}
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="flex items-center justify-center gap-3">
        {!isRunning ? (
          <button
            onClick={onStart}
            className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 transition-colors font-medium"
          >
            <Play className="w-5 h-5" />
            Start
          </button>
        ) : (
          <>
            {isPaused ? (
              <button
                onClick={onResume}
                className="flex items-center gap-2 px-5 py-3 bg-green-600 text-white rounded-full hover:bg-green-700 transition-colors font-medium"
              >
                <Play className="w-5 h-5" />
                Resume
              </button>
            ) : (
              <button
                onClick={onPause}
                className="flex items-center gap-2 px-5 py-3 bg-yellow-500 text-white rounded-full hover:bg-yellow-600 transition-colors font-medium"
              >
                <Pause className="w-5 h-5" />
                Pause
              </button>
            )}
            <button
              onClick={handleComplete}
              className="flex items-center gap-2 px-5 py-3 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors font-medium"
            >
              <Square className="w-5 h-5" />
              Finish
            </button>
          </>
        )}
      </div>

      {/* Info bar */}
      {isRunning && (
        <div className="mt-4 flex items-center justify-center gap-4 text-sm text-[#7a96b0]">
          <span>{Math.round(elapsed / 60)} min elapsed</span>
          <span>•</span>
          <span>
            {Math.max(0, plannedDuration - Math.round(elapsed / 60))} min remaining
          </span>
        </div>
      )}
    </div>
  );
}
