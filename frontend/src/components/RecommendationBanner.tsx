/**
 * RecommendationBanner Component: Clean, High-Impact Hero Banner.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 3, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React from 'react';
import type { DecisionOutput, WeatherSignal, CandidateMandi } from '../types';
import {
  TrendingUp,
  MapPin,
  Clock,
  AlertOctagon,
  ShieldCheck,
  Zap,
  CloudRain,
  IndianRupee,
} from 'lucide-react';

interface RecommendationBannerProps {
  decision: DecisionOutput;
  weather: WeatherSignal;
  topMandi?: CandidateMandi;
}

export const RecommendationBanner: React.FC<RecommendationBannerProps> = ({
  decision,
  weather,
  topMandi,
}) => {
  const isRiskOverride = decision.riskOverrideApplied;
  const isSevereWeather = weather.impactLevel === 'HIGH' || weather.impactLevel === 'CRITICAL';

  const getStyle = () => {
    const rec = String(decision.finalRecommendation);
    if (isRiskOverride || rec === 'SELL_EARLY_DUE_TO_RISK') {
      return {
        bg: 'from-amber-950/90 via-slate-900 to-rose-950/80',
        badgeBg: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
        badgeText: '⚠️ RISK OVERRIDE',
        icon: <AlertOctagon className="w-7 h-7 text-rose-400" />,
      };
    }
    if (rec === 'SELL_AT_RECOMMENDED_MANDI' || rec === 'TRAVEL') {
      return {
        bg: 'from-emerald-950/90 via-slate-900 to-teal-950/80',
        badgeBg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
        badgeText: '✨ OPTIMAL ROUTING',
        icon: <TrendingUp className="w-7 h-7 text-emerald-400" />,
      };
    }
    if (rec === 'HOLD') {
      return {
        bg: 'from-blue-950/90 via-slate-900 to-indigo-950/80',
        badgeBg: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
        badgeText: '⏳ STRATEGIC HOLD',
        icon: <Clock className="w-7 h-7 text-blue-400" />,
      };
    }
    return {
      bg: 'from-slate-900 via-gray-900 to-slate-950',
      badgeBg: 'bg-gray-500/20 text-gray-300 border-gray-500/30',
      badgeText: '📦 SELL NOW',
      icon: <ShieldCheck className="w-7 h-7 text-gray-300" />,
    };
  };

  const style = getStyle();

  const getTitle = () => {
    const rec = String(decision.finalRecommendation);
    switch (rec) {
      case 'SELL_EARLY_DUE_TO_RISK':
        return 'Sell Early due to Weather Risk';
      case 'SELL_AT_RECOMMENDED_MANDI':
        return `Sell at ${decision.recommendedMandi?.mandiName || 'Recommended Market'}`;
      case 'HOLD':
        return 'Hold Crop for Peak Price';
      case 'AVOID_MANDI_OR_ROUTE':
        return 'Avoid Transit Corridor (High Risk)';
      case 'SELL_NOW':
        return 'Sell Now at Local APMC';
      default:
        return rec.replace(/_/g, ' ');
    }
  };

  return (
    <div
      className={`relative overflow-hidden rounded-2xl bg-gradient-to-r ${style.bg} border border-white/10 p-5 md:p-6 text-white shadow-xl`}
    >
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-5">
        <div className="space-y-2.5 max-w-2xl">
          {/* Status Badges Row */}
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <span className={`px-2.5 py-0.5 rounded-full font-bold border ${style.badgeBg}`}>
              {style.badgeText}
            </span>

            {isRiskOverride && (
              <span className="px-2 py-0.5 rounded-full font-semibold bg-amber-500/20 text-amber-200 border border-amber-500/30 flex items-center gap-1">
                <Zap className="w-3 h-3 text-amber-300" />
                Base Decision (HOLD) Overridden
              </span>
            )}

            {isSevereWeather && (
              <span className="px-2 py-0.5 rounded-full font-semibold bg-rose-500/20 text-rose-200 border border-rose-500/30 flex items-center gap-1">
                <CloudRain className="w-3 h-3 text-rose-300" />
                Heavy Rain Alert ({weather.classification})
              </span>
            )}

            <span className="text-gray-400 ml-auto md:ml-0">
              Confidence: <strong>{Math.round(decision.decisionConfidence * 100)}%</strong>
            </span>
          </div>

          {/* Main Action Title */}
          <h1 className="text-xl md:text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
            {getTitle()}
          </h1>

          {/* Plain Human Readable Reason */}
          <p className="text-xs md:text-sm text-gray-300 leading-relaxed">
            {decision.humanReadableReason}
          </p>
        </div>

        {/* Quick Decision Snapshot Pills */}
        <div className="grid grid-cols-2 md:grid-cols-1 gap-2.5 min-w-[200px]">
          {decision.recommendedMandi && (
            <div className="bg-white/5 border border-white/10 rounded-xl p-2.5 flex items-center gap-2">
              <MapPin className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              <div>
                <span className="text-[10px] text-gray-400 block uppercase">Target Market</span>
                <span className="text-xs font-bold text-white line-clamp-1">
                  {decision.recommendedMandi.mandiName}
                </span>
              </div>
            </div>
          )}

          {topMandi && (
            <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-2.5 flex items-center gap-2">
              <IndianRupee className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              <div>
                <span className="text-[10px] text-emerald-300 block uppercase">Risk-Adjusted Return</span>
                <span className="text-sm font-black text-emerald-300">
                  ₹{topMandi.riskAdjustedReturn.toLocaleString('en-IN')}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
