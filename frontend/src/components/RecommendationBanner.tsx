/**
 * RecommendationBanner Component: Top Hero Banner on Results Dashboard.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 3, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React from 'react';
import type { DecisionOutput } from '../types';
import {
  TrendingUp,
  MapPin,
  Clock,
  AlertOctagon,
  ShieldCheck,
  Zap,
} from 'lucide-react';

interface RecommendationBannerProps {
  decision: DecisionOutput;
  commodityName: string;
}

export const RecommendationBanner: React.FC<RecommendationBannerProps> = ({
  decision,
}) => {
  const getBannerStyle = (rec: string, isOverride: boolean) => {
    if (isOverride || rec === 'SELL_EARLY_DUE_TO_RISK' || rec === 'AVOID_MANDI_OR_ROUTE') {
      return {
        bg: 'from-amber-900/90 via-rose-900/80 to-slate-900',
        badgeBg: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
        accentColor: 'text-rose-400',
        icon: <AlertOctagon className="w-8 h-8 text-rose-400" />,
        label: 'RISK OVERRIDE RECOMMENDATION',
      };
    }
    if (rec === 'SELL_AT_RECOMMENDED_MANDI' || rec === 'TRAVEL') {
      return {
        bg: 'from-emerald-900/90 via-teal-900/80 to-slate-900',
        badgeBg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
        accentColor: 'text-emerald-400',
        icon: <TrendingUp className="w-8 h-8 text-emerald-400" />,
        label: 'OPTIMAL MARKET ROUTING',
      };
    }
    if (rec === 'HOLD') {
      return {
        bg: 'from-blue-900/90 via-indigo-900/80 to-slate-900',
        badgeBg: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
        accentColor: 'text-blue-400',
        icon: <Clock className="w-8 h-8 text-blue-400" />,
        label: 'STRATEGIC HOLD RECOMMENDATION',
      };
    }
    return {
      bg: 'from-slate-800 via-gray-900 to-slate-950',
      badgeBg: 'bg-gray-500/20 text-gray-300 border-gray-500/30',
      accentColor: 'text-gray-300',
      icon: <ShieldCheck className="w-8 h-8 text-gray-300" />,
      label: 'MARKET RECOMMENDATION',
    };
  };

  const style = getBannerStyle(
    decision.finalRecommendation,
    decision.riskOverrideApplied
  );

  const formatRecommendationTitle = (rec: string) => {
    switch (rec) {
      case 'SELL_EARLY_DUE_TO_RISK':
        return 'SELL EARLY DUE TO RISK';
      case 'SELL_AT_RECOMMENDED_MANDI':
        return `SELL AT ${decision.recommendedMandi?.mandiName.toUpperCase() || 'RECOMMENDED MANDI'}`;
      case 'HOLD':
        return 'HOLD CROP FOR EXPECTED PEAK PRICE';
      case 'AVOID_MANDI_OR_ROUTE':
        return 'AVOID DANGEROUS TRANSIT CORRIDOR';
      case 'SELL_NOW':
        return 'SELL NOW AT LOCAL APMC';
      default:
        return rec.replace(/_/g, ' ');
    }
  };

  return (
    <div
      className={`relative overflow-hidden rounded-2xl bg-gradient-to-br ${style.bg} border border-white/10 p-6 md:p-8 text-white shadow-2xl backdrop-blur-md`}
    >
      <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-3 max-w-3xl">
          <div className="flex flex-wrap items-center gap-2.5">
            <span
              className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border tracking-wider uppercase ${style.badgeBg}`}
            >
              {style.label}
            </span>

            {decision.riskOverrideApplied && (
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/30 text-amber-200 border border-amber-500/40 animate-pulse">
                <Zap className="w-3 h-3 text-amber-300" />
                Base Decision ({decision.baseDecision}) Overridden
              </span>
            )}

            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-white/10 text-gray-300 border border-white/10">
              Confidence: {Math.round(decision.decisionConfidence * 100)}%
            </span>
          </div>

          <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
            {formatRecommendationTitle(decision.finalRecommendation)}
          </h1>

          <p className="text-sm md:text-base text-gray-200 leading-relaxed">
            {decision.humanReadableReason}
          </p>

          {decision.recommendedMandi && (
            <div className="flex items-center gap-2 text-xs font-medium text-emerald-300 bg-black/30 w-fit px-3 py-1.5 rounded-lg border border-white/10">
              <MapPin className="w-3.5 h-3.5" />
              <span>Target Market: {decision.recommendedMandi.mandiName}</span>
            </div>
          )}
        </div>

        <div className="flex-shrink-0 p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm hidden sm:flex items-center justify-center">
          {style.icon}
        </div>
      </div>
    </div>
  );
};
