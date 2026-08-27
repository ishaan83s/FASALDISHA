/**
 * AnalysisConfidenceCard Component: LEVEL 5 "Confidence of Our Analysis".
 * SSOT & Wireframe Reference: "Confidence of our analysis".
 */
import React from 'react';
import type { DecisionOutput, RiskSummary, ForecastOutput, SearchMetadata } from '../types';
import { useLanguage } from '../i18n';
import { ShieldCheck, TrendingUp, Store, CloudSun, CheckCircle2 } from 'lucide-react';

interface AnalysisConfidenceCardProps {
  decision: DecisionOutput;
  riskSummary: RiskSummary;
  forecast: ForecastOutput;
  search: SearchMetadata;
}

export const AnalysisConfidenceCard: React.FC<AnalysisConfidenceCardProps> = ({
  decision,
  riskSummary,
  forecast,
  search,
}) => {
  const { t, translateRiskLevel } = useLanguage();
  const confidencePercent = Math.round(decision.decisionConfidence * 100);

  const getConfidenceLevelText = (val: number) => {
    if (val >= 80) return { label: t('confidence.highConfidence'), color: 'text-emerald-600 dark:text-emerald-400', bar: 'bg-emerald-500' };
    if (val >= 60) return { label: t('confidence.moderateConfidence'), color: 'text-amber-600 dark:text-amber-400', bar: 'bg-amber-500' };
    return { label: t('confidence.baselineHeuristic'), color: 'text-slate-600 dark:text-slate-400', bar: 'bg-slate-500' };
  };

  const status = getConfidenceLevelText(confidencePercent);

  return (
    <div className="bg-white dark:bg-[#151c24] border border-earth-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3.5">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          <h3 className="text-base font-bold text-slate-900 dark:text-white font-heading">
            {t('confidence.title')}
          </h3>
        </div>

        <span className={`text-xs font-black font-heading ${status.color}`}>
          {confidencePercent}% {status.label}
        </span>
      </div>

      {/* Progress Bar */}
      <div className="space-y-1.5">
        <div className="w-full h-3 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden p-0.5">
          <div
            style={{ width: `${confidencePercent}%` }}
            className={`h-full rounded-full transition-all duration-500 ${status.bar}`}
          />
        </div>
        <p className="text-[11px] text-slate-500 dark:text-slate-400">
          {t('confidence.compositeScoreDesc')}
        </p>
      </div>

      {/* Multi-Factor Support Breakdown */}
      <div className="space-y-2 pt-1 text-xs">
        <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
          {t('confidence.decisionSignalsTitle')}
        </span>

        <div className="grid grid-cols-2 gap-2">
          {/* Signal 1: Price Forecast */}
          <div className="p-2.5 bg-earth-50 dark:bg-slate-900/60 rounded-xl border border-earth-200/80 dark:border-slate-800 flex items-start gap-2">
            <TrendingUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-slate-800 dark:text-slate-200 block text-[11px]">{t('confidence.priceForecastSignal')}</span>
              <span className="text-[10px] text-slate-400" title="Forecast confidence is a model reliability heuristic for this forecast horizon.">
                {t('confidence.modelReliabilitySub', { percent: Math.round(forecast.forecastConfidence * 100) })}
              </span>
            </div>
          </div>

          {/* Signal 2: Market Density */}
          <div className="p-2.5 bg-earth-50 dark:bg-slate-900/60 rounded-xl border border-earth-200/80 dark:border-slate-800 flex items-start gap-2">
            <Store className="w-4 h-4 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-slate-800 dark:text-slate-200 block text-[11px]">{t('confidence.marketDensitySignal')}</span>
              <span className="text-[10px] text-slate-400">
                {t('confidence.apmcCandidatesSub', { count: search.candidateCount })}
              </span>
            </div>
          </div>

          {/* Signal 3: Weather Risk */}
          <div className="p-2.5 bg-earth-50 dark:bg-slate-900/60 rounded-xl border border-earth-200/80 dark:border-slate-800 flex items-start gap-2">
            <CloudSun className="w-4 h-4 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-slate-800 dark:text-slate-200 block text-[11px]">{t('confidence.weatherRouteSignal')}</span>
              <span className="text-[10px] text-slate-400">
                {t('confidence.riskMonitoredSub', { risk: translateRiskLevel(riskSummary.riskLevel) })}
              </span>
            </div>
          </div>

          {/* Signal 4: Data Quality */}
          <div className="p-2.5 bg-earth-50 dark:bg-slate-900/60 rounded-xl border border-earth-200/80 dark:border-slate-800 flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-purple-600 dark:text-purple-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-slate-800 dark:text-slate-200 block text-[11px]">{t('confidence.dataQualitySignal')}</span>
              <span className="text-[10px] text-slate-400">
                {t('confidence.verifiedSub', { percent: riskSummary.dataCompleteness })}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
