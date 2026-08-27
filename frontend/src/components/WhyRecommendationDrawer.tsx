/**
 * WhyRecommendationDrawer Component: LEVEL 6 "Why This Recommendation?"
 * Collapsible audit trail and judge-proof explainability panel.
 * SSOT Reference: 00_MASTER_PRODUCT_SSOT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md.
 */
import React, { useState } from 'react';
import type { AnalysisResult } from '../types';
import { useLanguage } from '../i18n';
import {
  ChevronDown,
  ChevronUp,
  Scale,
  Users,
  CloudSun,
  BrainCircuit,
  Info,
} from 'lucide-react';

interface WhyRecommendationDrawerProps {
  result: AnalysisResult;
}

export const WhyRecommendationDrawer: React.FC<WhyRecommendationDrawerProps> = ({
  result,
}) => {
  const { t, translateDemand, translateClassification } = useLanguage();
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const { decision, forecast, dataProvenance, nearbyMandis } = result;

  const topMandi = nearbyMandis[0];

  const getTrainingBasisText = () => {
    let basis = t('audit.historicalBaseline');
    if (forecast.historyClassification === 'SYNTHETIC') basis = t('audit.syntheticBaseline');
    else if (forecast.historyClassification === 'SEEDED') basis = t('audit.seededBaseline');
    const windowText = t('audit.daySeries', { days: forecast.historyWindowDays });
    return `${basis} (${windowText})`;
  };

  return (
    <div className="bg-white dark:bg-[#151c24] border border-earth-200 dark:border-slate-800 rounded-3xl overflow-hidden shadow-sm transition-all">
      {/* Toggle Header */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-5 sm:p-6 flex items-center justify-between text-left hover:bg-earth-50/50 dark:hover:bg-slate-900/50 transition cursor-pointer"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-earth-100 dark:bg-slate-800 flex items-center justify-center text-agri-700 dark:text-agri-400 flex-shrink-0">
            <Info className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white font-heading">
              {t('audit.drawerTitle')}
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              {t('audit.drawerSubtitle')}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs font-bold text-agri-700 dark:text-agri-400">
          <span>{isOpen ? t('audit.collapseDetails') : t('audit.viewAuditTrail')}</span>
          {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </div>
      </button>

      {/* Expanded Content Grid */}
      {isOpen && (
        <div className="p-5 sm:p-6 pt-0 border-t border-slate-100 dark:border-slate-800 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs pt-4">
            {/* Pillar 1: Ranking Math */}
            <div className="p-4 bg-earth-50/70 dark:bg-slate-900/70 rounded-2xl border border-earth-200 dark:border-slate-800 space-y-2.5">
              <div className="flex items-center gap-2 text-agri-700 dark:text-agri-400 font-bold font-heading text-sm">
                <Scale className="w-4 h-4" />
                <span>{t('audit.pillar1Title')}</span>
              </div>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
                {t('audit.pillar1Desc')}
                <br />
                <code className="bg-white dark:bg-slate-800 px-1.5 py-0.5 rounded font-mono text-slate-800 dark:text-slate-200">
                  {t('audit.pillar1Formula')}
                </code>
              </p>
              {topMandi && topMandi.rankingBreakdown && (
                <div className="p-2.5 bg-white dark:bg-slate-800/80 rounded-xl border border-earth-200/80 dark:border-slate-700/60 text-[11px] space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-500">{t('audit.netReturnSubscore')}</span>
                    <strong className="text-agri-600 dark:text-agri-400">{topMandi.rankingBreakdown.normalizedRiskAdjustedReturn}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">{t('audit.buyerSignalSubscore')}</span>
                    <strong className="text-blue-600 dark:text-blue-400">{topMandi.rankingBreakdown.buyerSignalScore}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">{t('audit.dataQualitySubscore')}</span>
                    <strong className="text-purple-600 dark:text-purple-400">{topMandi.rankingBreakdown.dataQualityScore}</strong>
                  </div>
                  <div className="flex justify-between pt-1 border-t border-slate-100 dark:border-slate-700 font-bold">
                    <span>{t('audit.compositeFinalScore')}</span>
                    <span>{topMandi.rankingScore} / 100</span>
                  </div>
                </div>
              )}
            </div>

            {/* Pillar 2: Synthetic Buyer Signals */}
            <div className="p-4 bg-earth-50/70 dark:bg-slate-900/70 rounded-2xl border border-earth-200 dark:border-slate-800 space-y-2.5">
              <div className="flex items-center gap-2 text-blue-700 dark:text-blue-400 font-bold font-heading text-sm">
                <Users className="w-4 h-4" />
                <span>{t('audit.pillar2Title')}</span>
              </div>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
                {t('audit.pillar2Desc')}
                <br />
                <code className="bg-white dark:bg-slate-800 px-1.5 py-0.5 rounded font-mono text-slate-800 dark:text-slate-200">
                  {t('audit.pillar2Formula')}
                </code>
              </p>
              {topMandi && (
                <div className="p-2.5 bg-white dark:bg-slate-800/80 rounded-xl border border-earth-200/80 dark:border-slate-700/60 text-[11px] space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-500">{t('audit.activeVerifiedBuyers')}</span>
                    <strong className="text-slate-800 dark:text-slate-200">{topMandi.buyerSignal.activeBuyerCount} Buyers</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">{t('audit.demandCategory')}</span>
                    <strong className="text-slate-800 dark:text-slate-200">{translateDemand(topMandi.buyerSignal.demandLevel)}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">{t('audit.offerReliabilityIndex')}</span>
                    <strong className="text-slate-800 dark:text-slate-200">{topMandi.buyerSignal.offerStrength} / {topMandi.buyerSignal.reliability}</strong>
                  </div>
                  <div className="flex justify-between pt-1 border-t border-slate-100 dark:border-slate-700 text-slate-400 text-[10px]">
                    <span>{t('audit.classification')}</span>
                    <span className="font-mono bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-300 px-1 rounded">{translateClassification(dataProvenance.buyerDataClassification)}</span>
                  </div>
                </div>
              )}
            </div>

            {/* Pillar 3: Weather Risk & Override Rules */}
            <div className="p-4 bg-earth-50/70 dark:bg-slate-900/70 rounded-2xl border border-earth-200 dark:border-slate-800 space-y-2.5">
              <div className="flex items-center gap-2 text-amber-700 dark:text-amber-400 font-bold font-heading text-sm">
                <CloudSun className="w-4 h-4" />
                <span>{t('audit.pillar3Title')}</span>
              </div>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
                {t('audit.pillar3Desc')}
              </p>
              <div className="p-2.5 bg-white dark:bg-slate-800/80 rounded-xl border border-earth-200/80 dark:border-slate-700/60 text-[11px] space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-500">{t('audit.baseAlgorithmDecision')}</span>
                  <strong className="text-slate-800 dark:text-slate-200 font-mono">{decision.baseDecision}</strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">{t('audit.riskOverrideTriggered')}</span>
                  <strong className={decision.riskOverrideApplied ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'}>
                    {decision.riskOverrideApplied ? t('audit.overrideYes') : t('audit.overrideNo')}
                  </strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">{t('audit.finalActionableAdvice')}</span>
                  <strong className="text-agri-600 dark:text-agri-400 font-mono">{decision.finalRecommendation}</strong>
                </div>
              </div>
            </div>

            {/* Pillar 4: ML Forecast Provenance */}
            <div className="p-4 bg-earth-50/70 dark:bg-slate-900/70 rounded-2xl border border-earth-200 dark:border-slate-800 space-y-2.5">
              <div className="flex items-center gap-2 text-purple-700 dark:text-purple-400 font-bold font-heading text-sm">
                <BrainCircuit className="w-4 h-4" />
                <span>{t('audit.pillar4Title')}</span>
              </div>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
                {t('audit.pillar4Desc')}
              </p>
              <div className="p-2.5 bg-white dark:bg-slate-800/80 rounded-xl border border-earth-200/80 dark:border-slate-700/60 text-[11px] space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-500">{t('audit.modelEngineType')}</span>
                  <strong className="text-slate-800 dark:text-slate-200 font-mono">
                    {forecast.modelType === 'LIVE' ? 'Live ML Inference (XGBoost)' : 'Precomputed Series'}
                  </strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">{t('audit.trainingDataBasis')}</span>
                  <strong className="text-slate-800 dark:text-slate-200">
                    {getTrainingBasisText()}
                  </strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">{t('audit.dataSourceLabel')}</span>
                  <span className="text-slate-600 dark:text-slate-300 text-[10px]">{forecast.historySourceLabel}</span>
                </div>
                <div className="flex justify-between pt-1 border-t border-slate-100 dark:border-slate-700">
                  <span className="text-slate-500">{t('audit.forecastScope')}</span>
                  <span className="font-mono text-purple-600 dark:text-purple-400 font-bold">{forecast.forecastScope}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
