/**
 * MandiComparisonCard Component: Renders full economic, buyer intelligence, risk, and ranking breakdown.
 * SSOT Reference: 03_DECISION_ENGINE_SSOT.md, 06_FRONTEND_CONTRACT.md Section 3, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React, { useState } from 'react';
import type { CandidateMandi } from '../types';
import {
  Users,
  ChevronDown,
  ChevronUp,
  Sparkles,
  CheckCircle2,
} from 'lucide-react';

interface MandiComparisonCardProps {
  candidate: CandidateMandi;
  isRecommended: boolean;
  quantityQuintals: number;
}

export const MandiComparisonCard: React.FC<MandiComparisonCardProps> = ({
  candidate,
  isRecommended,
}) => {
  const [showDetails, setShowDetails] = useState<boolean>(isRecommended);

  const getRiskBadge = (level: string) => {
    switch (level) {
      case 'LOW':
        return 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800';
      case 'MODERATE':
        return 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border-amber-200 dark:border-amber-800';
      case 'HIGH':
        return 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border-rose-200 dark:border-rose-800';
      case 'CRITICAL':
        return 'bg-red-200 dark:bg-red-950 text-red-900 dark:text-red-200 border-red-300 dark:border-red-700';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div
      className={`rounded-2xl border transition-all duration-200 overflow-hidden ${
        isRecommended
          ? 'bg-emerald-50/40 dark:bg-emerald-950/20 border-emerald-400 dark:border-emerald-600 shadow-md ring-1 ring-emerald-400/50'
          : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 shadow-sm hover:border-gray-300 dark:hover:border-gray-600'
      }`}
    >
      {/* Top Header */}
      <div className="p-5 md:p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-start gap-3">
            <div
              className={`flex-shrink-0 w-8 h-8 rounded-xl font-extrabold flex items-center justify-center text-sm ${
                isRecommended
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
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
                  <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-emerald-600 text-white tracking-wide uppercase shadow-sm">
                    Recommended #1
                  </span>
                )}
              </div>
              <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                <span className="capitalize">{candidate.mandi.districtId}, {candidate.mandi.stateId}</span>
                <span>•</span>
                <span className="font-semibold text-gray-700 dark:text-gray-300">{candidate.distanceKm} km away</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 self-start sm:self-auto">
            <span
              className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${getRiskBadge(
                candidate.riskLevel
              )}`}
            >
              Risk: {candidate.riskLevel} ({candidate.riskScore})
            </span>
            <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-50 dark:bg-blue-950/50 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
              Rank Score: {candidate.rankingScore}
            </span>
          </div>
        </div>

        {/* Primary Economics Metrics */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
          <div className="p-3 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-100 dark:border-gray-700/60">
            <span className="text-xs text-gray-500 dark:text-gray-400 block">Current Price</span>
            <span className="text-base font-bold text-gray-900 dark:text-white">
              ₹{candidate.currentPrice.toLocaleString('en-IN')}/q
            </span>
          </div>

          <div className="p-3 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-100 dark:border-gray-700/60">
            <span className="text-xs text-gray-500 dark:text-gray-400 block">7-Day Forecast</span>
            <span className="text-base font-bold text-emerald-600 dark:text-emerald-400">
              ₹{candidate.forecast.forecast7Day.toLocaleString('en-IN')}/q
            </span>
          </div>

          <div className="p-3 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-100 dark:border-gray-700/60">
            <span className="text-xs text-gray-500 dark:text-gray-400 block">Total Transit Cost</span>
            <span className="text-base font-bold text-amber-700 dark:text-amber-400">
              ₹{candidate.totalTransportCost.toLocaleString('en-IN')}
            </span>
            <span className="text-[10px] text-gray-400 block">(₹{candidate.transportCostPerQuintal}/q)</span>
          </div>

          <div className="p-3 bg-emerald-50/80 dark:bg-emerald-950/40 rounded-xl border border-emerald-200 dark:border-emerald-800">
            <span className="text-xs font-semibold text-emerald-800 dark:text-emerald-300 block">
              Risk-Adjusted Return
            </span>
            <span className="text-lg font-black text-emerald-700 dark:text-emerald-300">
              ₹{candidate.riskAdjustedReturn.toLocaleString('en-IN')}
            </span>
            <span className="text-[10px] text-gray-500 dark:text-gray-400 block">
              Est. Net: ₹{candidate.netReturn.toLocaleString('en-IN')}
            </span>
          </div>
        </div>

        {/* Synthetic Buyer Intelligence Row (SSOT 13 Section C) */}
        <div className="p-3.5 bg-gradient-to-r from-blue-50/60 via-indigo-50/40 to-transparent dark:from-blue-950/30 dark:via-indigo-950/20 dark:to-transparent border border-blue-100 dark:border-blue-900/40 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <Users className="w-4 h-4 text-blue-600 dark:text-blue-400" />
            <div className="text-xs">
              <span className="font-bold text-gray-900 dark:text-gray-100">
                {candidate.buyerSignal.activeBuyerCount} Active Buyers Detected
              </span>
              <span className="text-gray-500 dark:text-gray-400 ml-1.5">
                (Demand: <strong>{candidate.buyerSignal.demandLevel}</strong> • Offer: <strong>{candidate.buyerSignal.offerStrength}%</strong> • Reliability: <strong>{candidate.buyerSignal.reliability}%</strong>)
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-900/60 text-blue-800 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
              SYNTHETIC DEMO DATASET
            </span>
            <span className="text-xs font-semibold text-gray-700 dark:text-gray-300">
              Score: {candidate.buyerSignal.buyerSignalScore}/100
            </span>
          </div>
        </div>

        {/* Toggle Detailed Breakdown Button */}
        <button
          type="button"
          onClick={() => setShowDetails(!showDetails)}
          className="w-full pt-2 flex items-center justify-center gap-1 text-xs font-semibold text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200 transition"
        >
          <span>{showDetails ? 'Hide Ranking Breakdown' : 'Show Ranking Breakdown & Top Factors'}</span>
          {showDetails ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {/* Expandable Ranking Breakdown & Top Factors (SSOT 13 Section D) */}
      {showDetails && candidate.rankingBreakdown && (
        <div className="px-5 pb-5 md:px-6 md:pb-6 pt-3 bg-gray-50/70 dark:bg-gray-900/60 border-t border-gray-100 dark:border-gray-700/60 space-y-3">
          <div className="flex items-center gap-1.5 text-xs font-bold text-gray-800 dark:text-gray-200">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            <span>Ranking Explainability Formula</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
            <div className="p-2.5 bg-white dark:bg-gray-800 rounded-lg border border-gray-200/70 dark:border-gray-700">
              <span className="text-gray-400 text-[10px] uppercase font-bold block">70% Risk-Adj Return</span>
              <span className="font-bold text-emerald-600 dark:text-emerald-400">
                {candidate.rankingBreakdown.normalizedRiskAdjustedReturn} / 100
              </span>
            </div>

            <div className="p-2.5 bg-white dark:bg-gray-800 rounded-lg border border-gray-200/70 dark:border-gray-700">
              <span className="text-gray-400 text-[10px] uppercase font-bold block">20% Buyer Signal</span>
              <span className="font-bold text-blue-600 dark:text-blue-400">
                {candidate.rankingBreakdown.buyerSignalScore} / 100
              </span>
            </div>

            <div className="p-2.5 bg-white dark:bg-gray-800 rounded-lg border border-gray-200/70 dark:border-gray-700">
              <span className="text-gray-400 text-[10px] uppercase font-bold block">10% Data Quality</span>
              <span className="font-bold text-purple-600 dark:text-purple-400">
                {candidate.rankingBreakdown.dataQualityScore} / 100
              </span>
            </div>
          </div>

          {candidate.rankingBreakdown.topFactors.length > 0 && (
            <div className="space-y-1 pt-1">
              <span className="text-[11px] font-semibold text-gray-500 dark:text-gray-400">Top Decision Drivers:</span>
              <div className="flex flex-wrap gap-1.5">
                {candidate.rankingBreakdown.topFactors.map((factor, fIdx) => (
                  <span
                    key={fIdx}
                    className="inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-md bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700"
                  >
                    <CheckCircle2 className="w-3 h-3 text-emerald-500" />
                    {factor}
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
