/**
 * MandiComparisonCard Component: Clean, Streamlined Market Comparison Card.
 * SSOT Reference: 03_DECISION_ENGINE_SSOT.md, 06_FRONTEND_CONTRACT.md Section 3, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React, { useState } from 'react';
import type { CandidateMandi } from '../types';
import {
  Users,
  ChevronDown,
  ChevronUp,
  CheckCircle2,
} from 'lucide-react';

interface MandiComparisonCardProps {
  candidate: CandidateMandi;
  isRecommended: boolean;
}

export const MandiComparisonCard: React.FC<MandiComparisonCardProps> = ({
  candidate,
  isRecommended,
}) => {
  const [showDetails, setShowDetails] = useState<boolean>(false);

  const isLowRisk = candidate.riskLevel === 'LOW';
  const isModerateRisk = candidate.riskLevel === 'MODERATE';

  return (
    <div
      className={`rounded-2xl border transition-all duration-150 overflow-hidden ${
        isRecommended
          ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-400 dark:border-emerald-700 shadow-md ring-1 ring-emerald-400/40'
          : 'bg-white dark:bg-gray-800/90 border-gray-200 dark:border-gray-700 shadow-sm hover:border-gray-300 dark:hover:border-gray-600'
      }`}
    >
      <div className="p-4 md:p-5 space-y-3">
        {/* Top Row: Title, Badges, and Primary Net Return */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-start gap-3">
            <div
              className={`w-7 h-7 rounded-xl font-bold flex items-center justify-center text-xs flex-shrink-0 mt-0.5 ${
                isRecommended
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
              }`}
            >
              #{candidate.rank}
            </div>

            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="text-base font-bold text-gray-900 dark:text-white">
                  {candidate.mandi.mandiName}
                </h3>
                {isRecommended && (
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-600 text-white uppercase tracking-wider">
                    Best Choice
                  </span>
                )}
              </div>
              <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                <span className="capitalize">{candidate.mandi.districtId}, {candidate.mandi.stateId}</span>
                <span>•</span>
                <span className="font-semibold text-gray-700 dark:text-gray-300">{candidate.distanceKm} km transit</span>
              </div>
            </div>
          </div>

          {/* Right Side: Estimated Net Return */}
          <div className="text-left sm:text-right flex sm:flex-col items-baseline sm:items-end justify-between gap-1">
            <div>
              <span className="text-[10px] uppercase font-bold text-gray-400 block">Risk-Adjusted Return</span>
              <span className="text-lg font-black text-emerald-600 dark:text-emerald-400">
                ₹{candidate.riskAdjustedReturn.toLocaleString('en-IN')}
              </span>
            </div>
            <span className="text-[11px] text-gray-500 dark:text-gray-400">
              ₹{candidate.expectedRevenue.toLocaleString('en-IN')} gross - ₹{candidate.totalTransportCost.toLocaleString('en-IN')} transport
            </span>
          </div>
        </div>

        {/* Middle Row: Clean Summary Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 text-xs">
          <div className="p-2 bg-gray-50 dark:bg-gray-900/40 rounded-lg border border-gray-100 dark:border-gray-700/50 flex items-center justify-between">
            <span className="text-gray-400">Current</span>
            <span className="font-bold text-gray-800 dark:text-gray-200">₹{candidate.currentPrice}/q</span>
          </div>

          <div className="p-2 bg-gray-50 dark:bg-gray-900/40 rounded-lg border border-gray-100 dark:border-gray-700/50 flex items-center justify-between">
            <span className="text-gray-400">7d Forecast</span>
            <span className="font-bold text-emerald-600 dark:text-emerald-400">₹{candidate.forecast.forecast7Day}/q</span>
          </div>

          <div className="p-2 bg-blue-50/60 dark:bg-blue-950/30 rounded-lg border border-blue-100 dark:border-blue-900/40 flex items-center justify-between">
            <span className="text-blue-600 dark:text-blue-400 flex items-center gap-1">
              <Users className="w-3 h-3" />
              <span>Buyers</span>
            </span>
            <span className="font-bold text-blue-700 dark:text-blue-300">
              {candidate.buyerSignal.activeBuyerCount} ({candidate.buyerSignal.demandLevel})
            </span>
          </div>

          <div className="p-2 bg-gray-50 dark:bg-gray-900/40 rounded-lg border border-gray-100 dark:border-gray-700/50 flex items-center justify-between">
            <span className="text-gray-400">Risk Level</span>
            <span className={`font-bold ${isLowRisk ? 'text-emerald-600' : isModerateRisk ? 'text-amber-600' : 'text-rose-600'}`}>
              {candidate.riskLevel} ({candidate.riskScore})
            </span>
          </div>
        </div>

        {/* Bottom Detail Toggle */}
        <div className="flex items-center justify-between pt-1 text-[11px] text-gray-400 border-t border-gray-100 dark:border-gray-800">
          <span className="flex items-center gap-1 text-gray-400">
            <span className="px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-[10px] font-semibold text-gray-600 dark:text-gray-300">
              SYNTHETIC BUYERS
            </span>
            <span>• Rank Score: {candidate.rankingScore}</span>
          </span>

          <button
            type="button"
            onClick={() => setShowDetails(!showDetails)}
            className="inline-flex items-center gap-1 font-semibold text-emerald-600 dark:text-emerald-400 hover:underline"
          >
            <span>{showDetails ? 'Hide Score Math' : 'Explain Score'}</span>
            {showDetails ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Expandable 70/20/10 Breakdown Drawer */}
      {showDetails && candidate.rankingBreakdown && (
        <div className="px-4 pb-4 md:px-5 md:pb-5 pt-2 bg-gray-50/90 dark:bg-gray-900/80 border-t border-gray-100 dark:border-gray-700 space-y-2.5 text-xs">
          <div className="grid grid-cols-3 gap-2 text-center">
            <div className="p-2 bg-white dark:bg-gray-800 rounded-lg border border-gray-200/60 dark:border-gray-700">
              <span className="text-[10px] text-gray-400 uppercase block font-semibold">70% Return Score</span>
              <span className="font-extrabold text-emerald-600 dark:text-emerald-400">
                {candidate.rankingBreakdown.normalizedRiskAdjustedReturn}
              </span>
            </div>
            <div className="p-2 bg-white dark:bg-gray-800 rounded-lg border border-gray-200/60 dark:border-gray-700">
              <span className="text-[10px] text-gray-400 uppercase block font-semibold">20% Buyer Score</span>
              <span className="font-extrabold text-blue-600 dark:text-blue-400">
                {candidate.rankingBreakdown.buyerSignalScore}
              </span>
            </div>
            <div className="p-2 bg-white dark:bg-gray-800 rounded-lg border border-gray-200/60 dark:border-gray-700">
              <span className="text-[10px] text-gray-400 uppercase block font-semibold">10% Data Quality</span>
              <span className="font-extrabold text-purple-600 dark:text-purple-400">
                {candidate.rankingBreakdown.dataQualityScore}
              </span>
            </div>
          </div>

          {candidate.rankingBreakdown.topFactors.length > 0 && (
            <div className="flex flex-wrap gap-1.5 pt-1">
              {candidate.rankingBreakdown.topFactors.map((factor, idx) => (
                <span
                  key={idx}
                  className="inline-flex items-center gap-1 text-[10px] font-medium px-2 py-0.5 rounded bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700"
                >
                  <CheckCircle2 className="w-2.5 h-2.5 text-emerald-500" />
                  {factor}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
