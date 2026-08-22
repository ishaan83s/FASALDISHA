/**
 * RiskPanel Component: Detailed Risk Factors and Spoilage Breakdown.
 * SSOT Reference: 03_DECISION_ENGINE_SSOT.md Section 5, 06_FRONTEND_CONTRACT.md Section 3, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React from 'react';
import type { RiskSummary, WeatherSignal, Commodity } from '../types';
import { ShieldAlert, Zap } from 'lucide-react';

interface RiskPanelProps {
  riskSummary: RiskSummary;
  weather: WeatherSignal;
  commodity: Commodity;
  riskOverrideApplied: boolean;
}

export const RiskPanel: React.FC<RiskPanelProps> = ({
  riskSummary,
  weather,
  commodity,
  riskOverrideApplied,
}) => {
  const getRiskScoreColor = (score: number) => {
    if (score <= 25) return 'text-emerald-600 dark:text-emerald-400';
    if (score <= 50) return 'text-amber-600 dark:text-amber-400';
    return 'text-rose-600 dark:text-rose-400';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5 md:p-6 shadow-sm space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-gray-100 dark:border-gray-700">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-rose-600 dark:text-rose-400" />
          <h2 className="text-base font-bold text-gray-900 dark:text-white">
            Operational Risk Assessment
          </h2>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-gray-500 dark:text-gray-400">
            Overall Score:
          </span>
          <span className={`text-lg font-black ${getRiskScoreColor(riskSummary.overallRiskScore)}`}>
            {riskSummary.overallRiskScore}/100 ({riskSummary.riskLevel})
          </span>
        </div>
      </div>

      {/* Risk Overrides Warning */}
      {riskOverrideApplied && (
        <div className="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl flex items-center gap-2.5 text-xs text-amber-900 dark:text-amber-200">
          <Zap className="w-4 h-4 text-amber-500 flex-shrink-0" />
          <span>
            <strong>Active Risk Override:</strong> High risk thresholds forced an urgent SELL EARLY / safe reroute recommendation.
          </span>
        </div>
      )}

      {/* Breakdown Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        <div className="p-3 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-100 dark:border-gray-700">
          <span className="text-gray-500 dark:text-gray-400 block font-medium">Weather Signal</span>
          <span className="font-bold text-gray-800 dark:text-gray-200 text-sm block mt-0.5">
            {weather.impactLevel} Risk ({weather.classification})
          </span>
          <span className="text-[10px] text-gray-400 block mt-1 line-clamp-1">{weather.sourceLabel}</span>
        </div>

        <div className="p-3 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-100 dark:border-gray-700">
          <span className="text-gray-500 dark:text-gray-400 block font-medium">Perishability Spoilage Risk</span>
          <span className="font-bold text-gray-800 dark:text-gray-200 text-sm block mt-0.5">
            {commodity.perishabilityClass.replace(/_/g, ' ')}
          </span>
          <span className="text-[10px] text-gray-400 block mt-1">Class: {commodity.commodityCategory}</span>
        </div>

        <div className="p-3 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-100 dark:border-gray-700">
          <span className="text-gray-500 dark:text-gray-400 block font-medium">Data Completeness</span>
          <span className="font-bold text-gray-800 dark:text-gray-200 text-sm block mt-0.5">
            {Math.round(riskSummary.dataCompleteness * 100)}% Complete
          </span>
          <span className="text-[10px] text-gray-400 block mt-1">Multi-factor support score</span>
        </div>
      </div>
    </div>
  );
};
