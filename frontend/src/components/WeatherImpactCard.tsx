/**
 * WeatherImpactCard Component: Contextual Weather & Transit Advisory.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md, Section 7 "Weather Impact".
 */
import React from 'react';
import type { WeatherSignal } from '../types';
import { CloudRain, Sun, AlertTriangle } from 'lucide-react';

interface WeatherImpactCardProps {
  weather: WeatherSignal;
  commodityName: string;
}

export const WeatherImpactCard: React.FC<WeatherImpactCardProps> = ({
  weather,
  commodityName,
}) => {
  const events = weather.events || [];
  const hasSevereWeather = weather.impactLevel === 'HIGH' || weather.impactLevel === 'CRITICAL';
  const hasModerateWeather = weather.impactLevel === 'MODERATE';

  const getImpactBadge = () => {
    if (hasSevereWeather) {
      return {
        label: 'HIGH IMPACT / DELAY RISK',
        style: 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border-rose-200 dark:border-rose-800',
        icon: <CloudRain className="w-5 h-5 text-rose-600 dark:text-rose-400" />,
        advice: `Active rainfall / waterlogging alert in transit corridor. Early sale recommended to prevent ${commodityName} spoilage.`,
      };
    }
    if (hasModerateWeather) {
      return {
        label: 'MODERATE WEATHER IMPACT',
        style: 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border-amber-200 dark:border-amber-800',
        icon: <CloudRain className="w-5 h-5 text-amber-600 dark:text-amber-400" />,
        advice: `Mild rain forecasted. Transit corridors remain operable with minor moisture precautions.`,
      };
    }
    return {
      label: 'CLEAR TRANSIT CONDITIONS',
      style: 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800',
      icon: <Sun className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />,
      advice: `No adverse weather threats detected. Safe road transit to all candidate mandis.`,
    };
  };

  const badge = getImpactBadge();

  return (
    <div className="bg-white dark:bg-[#151c24] border border-earth-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center gap-2">
          {badge.icon}
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white font-heading">
              Weather & Transit Impact
            </h3>
            <p className="text-[11px] text-slate-400">
              Regional weather radar evaluating crop storage and road delay risks.
            </p>
          </div>
        </div>

        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-lg border ${badge.style}`}>
          {badge.label}
        </span>
      </div>

      {/* Decision-Centric Advisory */}
      <div className="p-3 bg-earth-50 dark:bg-slate-900 rounded-2xl border border-earth-200/80 dark:border-slate-800 text-xs space-y-1.5">
        <span className="font-semibold text-slate-700 dark:text-slate-300 block">
          Farmer Selling Impact:
        </span>
        <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
          {badge.advice}
        </p>
      </div>

      {/* Event Details if any */}
      {events.length > 0 && (
        <div className="space-y-1 pt-1 text-xs">
          {events.map((evt, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between p-2 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-800 text-[11px]"
            >
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-500 flex-shrink-0" />
                <span className="font-medium text-slate-700 dark:text-slate-300">
                  {evt.eventType.replace(/_/g, ' ')}: {evt.description || 'Active advisory'}
                </span>
              </div>
              <span className="text-slate-400 font-mono text-[10px]">{evt.classification}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
