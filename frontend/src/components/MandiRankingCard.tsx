/**
 * MandiRankingCard Component: LEVEL 4 "Which Mandi Should I Choose?"
 * Simple, scannable ranked market card with profit, distance, risk, and buyer signals.
 * SSOT & Wireframe Reference: Section 3 & "Mandis Ranked in Range".
 */
import React, { useState } from 'react';
import type { CandidateMandi } from '../types';
import { useLanguage } from '../i18n';
import {
  Users,
  ChevronDown,
  ChevronUp,
  MapPin,
  CheckCircle2,
  Award,
} from 'lucide-react';

interface MandiRankingCardProps {
  candidate: CandidateMandi;
  isRecommended: boolean;
}

export const MandiRankingCard: React.FC<MandiRankingCardProps> = ({
  candidate,
  isRecommended,
}) => {
  const { t, translateRiskLevel, translateDemand, translateState, translateDistrict, translateTopFactor } = useLanguage();
  const [showScoreMath, setShowScoreMath] = useState<boolean>(false);

  const getRiskBadge = (level: string) => {
    const riskLabel = translateRiskLevel(level);
    switch (level) {
      case 'LOW':
        return {
          text: riskLabel,
          color: 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800',
        };
      case 'MODERATE':
        return {
          text: riskLabel,
          color: 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border-amber-200 dark:border-amber-800',
        };
      case 'HIGH':
      case 'CRITICAL':
        return {
          text: riskLabel,
          color: 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border-rose-200 dark:border-rose-800',
        };
      default:
        return { text: riskLabel, color: 'bg-slate-100 text-slate-700' };
    }
  };

  const riskBadge = getRiskBadge(candidate.riskLevel);

  return (
    <div
      className={`rounded-3xl border transition-all duration-200 overflow-hidden ${
        isRecommended
          ? 'bg-agri-50/60 dark:bg-agri-950/20 border-agri-400 dark:border-agri-700 shadow-md ring-1 ring-agri-400/40'
          : 'bg-white dark:bg-[#151c24] border-earth-200 dark:border-slate-800 shadow-xs hover:border-earth-300 dark:hover:border-slate-700'
      }`}
    >
      <div className="p-4 sm:p-5 space-y-3.5">
        {/* Top Header: Rank, Mandi Name, Distance & Badges */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-start gap-3">
            {/* Rank Badge */}
            <div
              className={`w-8 h-8 rounded-2xl font-black flex items-center justify-center text-xs flex-shrink-0 mt-0.5 font-heading shadow-xs ${
                isRecommended
                  ? 'bg-agri-600 text-white shadow-agri-600/30'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300'
              }`}
            >
              #{candidate.rank}
            </div>

            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="text-base font-bold text-slate-900 dark:text-white font-heading">
                  {candidate.mandi.mandiName}
                </h3>
                {isRecommended && (
                  <span className="inline-flex items-center gap-1 text-[10px] font-black px-2 py-0.5 rounded-full bg-agri-600 text-white uppercase tracking-wider shadow-2xs">
                    <Award className="w-3 h-3" />
                    {t('rankings.recommendedBadge')}
                  </span>
                )}
              </div>

              <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                <span className="capitalize">{translateDistrict(candidate.mandi.districtId)}, {translateState(candidate.mandi.stateId)}</span>
                <span>•</span>
                <span className="font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1">
                  <MapPin className="w-3 h-3 text-slate-400" />
                  {t('rankings.kmAway', { distance: candidate.distanceKm })}
                </span>
              </div>
            </div>
          </div>

          {/* Right: Prominent Expected Net Return */}
          <div className="text-left sm:text-right flex sm:flex-col items-baseline sm:items-end justify-between gap-0.5">
            <div>
              <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
                {t('rankings.expectedNetReturn')}
              </span>
              <span className="text-xl font-black text-agri-700 dark:text-agri-400 font-heading">
                ₹{candidate.riskAdjustedReturn.toLocaleString('en-IN')}
              </span>
            </div>
            <span className="text-[11px] text-slate-500 dark:text-slate-400 font-medium">
              {t('rankings.grossTransitBreakdown', {
                gross: candidate.expectedRevenue.toLocaleString('en-IN'),
                transit: candidate.totalTransportCost.toLocaleString('en-IN'),
              })}
            </span>
          </div>
        </div>

        {/* Middle Stats Pills Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
          {/* Price */}
          <div className="p-2.5 bg-slate-50/80 dark:bg-slate-900/60 rounded-xl border border-slate-100 dark:border-slate-800">
            <span className="text-slate-400 text-[10px] uppercase block font-medium">{t('rankings.predictedPrice')}</span>
            <span className="text-sm font-bold text-slate-900 dark:text-white font-heading">
              ₹{candidate.currentPrice}/q
            </span>
          </div>

          {/* 7-Day Forecast */}
          <div className="p-2.5 bg-slate-50/80 dark:bg-slate-900/60 rounded-xl border border-slate-100 dark:border-slate-800">
            <span className="text-slate-400 text-[10px] uppercase block font-medium">{t('rankings.sevenDayHorizon')}</span>
            <span className="text-sm font-bold text-emerald-600 dark:text-emerald-400 font-heading">
              ₹{candidate.forecast.forecast7Day}/q
            </span>
          </div>

          {/* Buyer Demand */}
          <div className="p-2.5 bg-blue-50/60 dark:bg-blue-950/30 rounded-xl border border-blue-100 dark:border-blue-900/40">
            <span className="text-blue-600 dark:text-blue-400 text-[10px] uppercase block font-bold flex items-center gap-1">
              <Users className="w-3 h-3" />
              <span>{t('rankings.buyerDemand')}</span>
            </span>
            <span className="text-xs font-bold text-blue-800 dark:text-blue-300">
              {t('rankings.buyersCount', {
                count: candidate.buyerSignal.activeBuyerCount,
                demand: translateDemand(candidate.buyerSignal.demandLevel),
              })}
            </span>
          </div>

          {/* Risk Level */}
          <div className="p-2.5 bg-slate-50/80 dark:bg-slate-900/60 rounded-xl border border-slate-100 dark:border-slate-800">
            <span className="text-slate-400 text-[10px] uppercase block font-medium">{t('rankings.routeRisk')}</span>
            <span className={`text-[11px] font-bold px-1.5 py-0.2 rounded border ${riskBadge.color}`}>
              {riskBadge.text}
            </span>
          </div>
        </div>

        {/* Footer Row: Explain Score Toggle */}
        <div className="flex items-center justify-between pt-1 text-[11px] text-slate-400 border-t border-slate-100 dark:border-slate-800">
          <span>
            {t('rankings.overallRankScore')} <strong className="text-slate-700 dark:text-slate-300">{candidate.rankingScore} / 100</strong>
          </span>

          <button
            type="button"
            onClick={() => setShowScoreMath(!showScoreMath)}
            className="inline-flex items-center gap-1 font-bold text-agri-700 dark:text-agri-400 hover:underline cursor-pointer"
          >
            <span>{showScoreMath ? t('rankings.hideScoreBreakdown') : t('rankings.whyThisRank')}</span>
            {showScoreMath ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Expandable 70/20/10 Score Drawer */}
      {showScoreMath && candidate.rankingBreakdown && (
        <div className="px-4 pb-4 sm:px-5 sm:pb-5 pt-2 bg-earth-50/80 dark:bg-slate-900/90 border-t border-earth-200 dark:border-slate-800 space-y-2.5 text-xs">
          <div className="grid grid-cols-3 gap-2 text-center">
            <div className="p-2 bg-white dark:bg-[#151c24] rounded-xl border border-earth-200/80 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 uppercase block font-bold">{t('rankings.returnScore70')}</span>
              <span className="text-sm font-black text-agri-600 dark:text-agri-400 font-heading">
                {candidate.rankingBreakdown.normalizedRiskAdjustedReturn}
              </span>
            </div>

            <div className="p-2 bg-white dark:bg-[#151c24] rounded-xl border border-earth-200/80 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 uppercase block font-bold">{t('rankings.buyerScore20')}</span>
              <span className="text-sm font-black text-blue-600 dark:text-blue-400 font-heading">
                {candidate.rankingBreakdown.buyerSignalScore}
              </span>
            </div>

            <div className="p-2 bg-white dark:bg-[#151c24] rounded-xl border border-earth-200/80 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 uppercase block font-bold">{t('rankings.dataQuality10')}</span>
              <span className="text-sm font-black text-purple-600 dark:text-purple-400 font-heading">
                {candidate.rankingBreakdown.dataQualityScore}
              </span>
            </div>
          </div>

          {candidate.rankingBreakdown.topFactors.length > 0 && (
            <div className="space-y-1 pt-1">
              <span className="text-[11px] font-semibold text-slate-500 dark:text-slate-400">{t('rankings.keyDecisionDrivers')}</span>
              <div className="flex flex-wrap gap-1.5">
                {candidate.rankingBreakdown.topFactors.map((factor, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-lg bg-white dark:bg-[#151c24] text-slate-700 dark:text-slate-300 border border-earth-200 dark:border-slate-800"
                  >
                    <CheckCircle2 className="w-3 h-3 text-agri-600 dark:text-agri-400" />
                    {translateTopFactor(factor)}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
