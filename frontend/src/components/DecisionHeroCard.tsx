/**
 * DecisionHeroCard Component: LEVEL 1 & 2 "What Should I Do?" & Primary Profit Focal Point.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 3, Design Reference Wireframe.
 */
import React from 'react';
import type { DecisionOutput, CandidateMandi, ForecastOutput } from '../types';
import { useLanguage } from '../i18n';
import {
  TrendingUp,
  MapPin,
  Clock,
  AlertTriangle,
  Zap,
  Calendar,
  ShieldCheck,
} from 'lucide-react';

interface DecisionHeroCardProps {
  decision: DecisionOutput;
  forecast: ForecastOutput;
  topMandi?: CandidateMandi;
  commodityName: string;
}

export const DecisionHeroCard: React.FC<DecisionHeroCardProps> = ({
  decision,
  forecast,
  topMandi,
  commodityName,
}) => {
  const { t, getLocalizedDecisionTitle, getLocalizedDecisionReason } = useLanguage();
  const isRiskOverride = decision.riskOverrideApplied;
  const rec = String(decision.finalRecommendation);
  const targetMandiName = decision.recommendedMandi?.mandiName || topMandi?.mandi.mandiName || '';

  const getCardTheme = () => {
    if (isRiskOverride || rec === 'SELL_EARLY_DUE_TO_RISK') {
      return {
        bg: 'from-amber-900/90 via-slate-900 to-rose-950/90',
        badgeColor: 'bg-rose-500/20 text-rose-300 border-rose-500/40',
        actionTag: t('decisionHero.riskOverrideTag'),
        actionTitle: getLocalizedDecisionTitle(rec, targetMandiName, commodityName, isRiskOverride),
        icon: <AlertTriangle className="w-8 h-8 text-rose-400 animate-pulse" />,
      };
    }
    if (rec === 'SELL_AT_RECOMMENDED_MANDI' || rec === 'TRAVEL') {
      return {
        bg: 'from-agri-950 via-slate-900 to-emerald-950',
        badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
        actionTag: t('decisionHero.recommendedMarketTag'),
        actionTitle: getLocalizedDecisionTitle(rec, targetMandiName, commodityName, isRiskOverride),
        icon: <TrendingUp className="w-8 h-8 text-emerald-400" />,
      };
    }
    if (rec === 'HOLD') {
      return {
        bg: 'from-blue-950 via-slate-900 to-indigo-950',
        badgeColor: 'bg-blue-500/20 text-blue-300 border-blue-500/40',
        actionTag: t('decisionHero.strategicHoldTag'),
        actionTitle: getLocalizedDecisionTitle(rec, targetMandiName, commodityName, isRiskOverride),
        icon: <Clock className="w-8 h-8 text-blue-400" />,
      };
    }
    return {
      bg: 'from-slate-900 via-stone-900 to-slate-950',
      badgeColor: 'bg-slate-500/20 text-slate-300 border-slate-500/40',
      actionTag: t('decisionHero.sellNowTag'),
      actionTitle: getLocalizedDecisionTitle(rec, targetMandiName, commodityName, isRiskOverride),
      icon: <ShieldCheck className="w-8 h-8 text-slate-300" />,
    };
  };

  const theme = getCardTheme();
  const localizedReason = getLocalizedDecisionReason(
    rec,
    decision.humanReadableReason,
    targetMandiName,
    commodityName,
    isRiskOverride
  );

  return (
    <div className={`relative overflow-hidden rounded-3xl bg-gradient-to-br ${theme.bg} border border-white/15 p-5 sm:p-7 text-white shadow-xl`}>
      {/* Background Decorative Glow */}
      <div className="absolute -top-24 -right-24 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 space-y-5">
        {/* Top Badges Row */}
        <div className="flex flex-wrap items-center justify-between gap-2.5 text-xs">
          <div className="flex flex-wrap items-center gap-2">
            <span className={`px-3 py-1 rounded-full font-bold border uppercase tracking-wider ${theme.badgeColor}`}>
              {theme.actionTag}
            </span>

            {isRiskOverride && (
              <span className="px-2.5 py-0.5 rounded-full font-semibold bg-amber-500/25 text-amber-200 border border-amber-500/40 flex items-center gap-1">
                <Zap className="w-3.5 h-3.5 text-amber-300" />
                {t('decisionHero.riskOverrideNotice')}
              </span>
            )}
          </div>

          <div className="flex items-center gap-2 text-slate-300">
            <span>{t('decisionHero.analysisConfidence')}</span>
            <span className="px-2 py-0.5 rounded-lg bg-white/10 font-extrabold text-white">
              {Math.round(decision.decisionConfidence * 100)}%
            </span>
          </div>
        </div>

        {/* Level 1: Primary Action Headline */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5 max-w-2xl">
            <span className="text-xs uppercase font-bold text-emerald-400 tracking-wider">
              {t('decisionHero.bestDecisionEyebrow')}
            </span>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight text-white font-heading">
              {theme.actionTitle}
            </h1>
            <p className="text-xs sm:text-sm text-slate-200 leading-relaxed pt-0.5">
              {localizedReason}
            </p>
          </div>

          <div className="hidden md:flex flex-shrink-0 w-16 h-16 rounded-2xl bg-white/10 border border-white/15 items-center justify-center backdrop-blur-sm shadow-inner">
            {theme.icon}
          </div>
        </div>

        {/* Level 2: Money & Profit Section (As indicated in Wireframe) */}
        {topMandi && (
          <div className="pt-2 border-t border-white/10">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {/* Primary Net Return Box */}
              <div className="p-3.5 bg-emerald-500/20 border border-emerald-400/40 rounded-2xl">
                <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-300 block">
                  {t('decisionHero.netReturnLabel')}
                </span>
                <p className="text-2xl sm:text-3xl font-black text-white mt-0.5 font-heading">
                  ₹{topMandi.riskAdjustedReturn.toLocaleString('en-IN')}
                </p>
                <span className="text-[11px] text-emerald-200/80 mt-0.5 block">
                  {t('decisionHero.netReturnSubtext')}
                </span>
              </div>

              {/* Best Day & Peak Expected */}
              <div className="p-3.5 bg-white/5 border border-white/10 rounded-2xl flex flex-col justify-between">
                <div className="flex items-center justify-between text-xs text-slate-300">
                  <span className="flex items-center gap-1 font-semibold">
                    <Calendar className="w-3.5 h-3.5 text-amber-400" />
                    <span>{t('decisionHero.bestSellingDay')}</span>
                  </span>
                  <span className="font-bold text-amber-300 px-1.5 py-0.2 rounded bg-amber-400/20">
                    {t('decisionHero.dayLabel', { day: forecast.peakDay })}
                  </span>
                </div>
                <div className="mt-1">
                  <p className="text-xl font-bold text-white font-heading">
                    ₹{forecast.expectedPeakPrice.toLocaleString('en-IN')}/q
                  </p>
                  <span className="text-[11px] text-slate-400">
                    {t('decisionHero.expectedPeakPrice')} (+{(((forecast.expectedPeakPrice - forecast.currentPrice) / Math.max(forecast.currentPrice, 1)) * 100).toFixed(1)}%)
                  </span>
                </div>
              </div>

              {/* Mandi & Transit Economics */}
              <div className="p-3.5 bg-white/5 border border-white/10 rounded-2xl flex flex-col justify-between">
                <div className="flex items-center justify-between text-xs text-slate-300">
                  <span className="flex items-center gap-1 font-semibold">
                    <MapPin className="w-3.5 h-3.5 text-emerald-400" />
                    <span>{t('decisionHero.targetMandi')}</span>
                  </span>
                  <span className="font-semibold text-slate-300">
                    {t('decisionHero.kmAway', { distance: topMandi.distanceKm })}
                  </span>
                </div>
                <div className="mt-1">
                  <p className="text-base font-bold text-white line-clamp-1">
                    {topMandi.mandi.mandiName}
                  </p>
                  <span className="text-[11px] text-slate-400">
                    {t('decisionHero.grossTransitFormula', {
                      gross: topMandi.expectedRevenue.toLocaleString('en-IN'),
                      transit: topMandi.totalTransportCost.toLocaleString('en-IN'),
                    })}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
