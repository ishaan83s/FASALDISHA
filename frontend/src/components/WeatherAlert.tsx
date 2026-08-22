/**
 * WeatherAlert Component: Near-recommendation meteorological indicator.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 3, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React from 'react';
import type { WeatherSignal } from '../types';
import { CloudRain, AlertTriangle, CheckCircle2, CloudOff } from 'lucide-react';

interface WeatherAlertProps {
  weather: WeatherSignal;
}

export const WeatherAlert: React.FC<WeatherAlertProps> = ({ weather }) => {
  if (weather.status === 'UNAVAILABLE') {
    return (
      <div className="p-4 bg-gray-50 dark:bg-gray-800/80 border border-gray-300 dark:border-gray-700 rounded-xl flex items-center gap-3 text-xs text-gray-600 dark:text-gray-400">
        <CloudOff className="w-5 h-5 text-gray-400 flex-shrink-0" />
        <div>
          <span className="font-bold text-gray-800 dark:text-gray-200 block">
            Weather Signal Unavailable
          </span>
          <span>Live meteorological radar feed offline; decision relies on baseline transport and perishability models.</span>
        </div>
      </div>
    );
  }

  const isSevere = weather.impactLevel === 'HIGH' || weather.impactLevel === 'CRITICAL';
  const isModerate = weather.impactLevel === 'MODERATE';

  return (
    <div
      className={`p-4 rounded-xl border flex items-start gap-3 text-xs ${
        isSevere
          ? 'bg-rose-50/90 dark:bg-rose-950/40 border-rose-300 dark:border-rose-800 text-rose-900 dark:text-rose-200'
          : isModerate
          ? 'bg-amber-50/90 dark:bg-amber-950/40 border-amber-300 dark:border-amber-800 text-amber-900 dark:text-amber-200'
          : 'bg-emerald-50/80 dark:bg-emerald-950/30 border-emerald-200 dark:border-emerald-800 text-emerald-900 dark:text-emerald-200'
      }`}
    >
      <div className="mt-0.5 flex-shrink-0">
        {isSevere ? (
          <AlertTriangle className="w-5 h-5 text-rose-600 dark:text-rose-400 animate-bounce" />
        ) : isModerate ? (
          <CloudRain className="w-5 h-5 text-amber-600 dark:text-amber-400" />
        ) : (
          <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
        )}
      </div>

      <div className="flex-1 space-y-1">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="font-bold uppercase tracking-wider text-[11px]">
            {isSevere ? 'Severe Weather / Road Alert Active' : isModerate ? 'Moderate Weather Caution' : 'Optimal Weather & Transit Conditions'}
          </span>
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-black/10 dark:bg-white/10 uppercase">
            Source: {weather.classification}
          </span>
        </div>

        {weather.events.length > 0 ? (
          <div className="space-y-0.5 text-xs">
            {weather.events.map((e, idx) => (
              <p key={idx} className="font-medium">
                {e.description || e.eventType.replace(/_/g, ' ')} ({e.sourceLabel})
              </p>
            ))}
          </div>
        ) : (
          <p className="text-xs opacity-90">
            No active transit disruptions detected. {weather.sourceLabel}
          </p>
        )}
      </div>
    </div>
  );
};
