/**
 * ReasoningPanel Component: Collapsible Judge-Proof Audit & Evidence Area.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 5, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React, { useState } from 'react';
import type { AnalysisResult } from '../types';
import {
  Users,
  CloudLightning,
  TrendingUp,
  MapPin,
  ChevronDown,
  ChevronUp,
  ShieldCheck,
} from 'lucide-react';

interface ReasoningPanelProps {
  result: AnalysisResult;
}

export const ReasoningPanel: React.FC<ReasoningPanelProps> = ({ result }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const topMandi = result.nearbyMandis[0];

  return (
    <div className="bg-slate-900 rounded-2xl border border-emerald-500/20 text-white shadow-lg overflow-hidden">
      {/* Header / Toggle Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 flex items-center justify-between hover:bg-white/5 transition duration-150 text-left"
      >
        <div className="flex items-center gap-2.5">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <div>
            <h3 className="text-sm font-bold text-white">
              System Decision Audit & Explainability
            </h3>
            <p className="text-[11px] text-gray-400">
              Full transparency into ranking math, ML provenance, weather risk, and economics
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            {isOpen ? 'Hide Audit Trail' : 'View Audit Trail'}
          </span>
          {isOpen ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
        </div>
      </button>

      {/* Expandable Content */}
      {isOpen && (
        <div className="p-5 pt-1 border-t border-white/10 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            {/* 1. Best Location Routing */}
            <div className="p-3.5 bg-white/5 rounded-xl border border-white/10 space-y-1.5">
              <div className="flex items-center gap-1.5 text-emerald-400 font-bold text-xs">
                <MapPin className="w-3.5 h-3.5" />
                <span>1. Best Location & Ranking Proof</span>
              </div>
              <p className="text-gray-300 leading-relaxed text-[11px]">
                {topMandi ? (
                  <>
                    <strong>{topMandi.mandi.mandiName}</strong> ranks #1 with score{' '}
                    <strong>{topMandi.rankingScore}</strong> (70% Risk-Adj Return: ₹
                    {topMandi.riskAdjustedReturn.toLocaleString('en-IN')}, 20% Buyer Signal: {topMandi.buyerSignal.buyerSignalScore}, 10% Data Quality: {topMandi.rankingBreakdown?.dataQualityScore || 80}).
                  </>
                ) : (
                  'No candidate inside requested radius.'
                )}
              </p>
            </div>

            {/* 2. Synthetic Buyer Intelligence */}
            <div className="p-3.5 bg-white/5 rounded-xl border border-white/10 space-y-1.5">
              <div className="flex items-center gap-1.5 text-blue-400 font-bold text-xs">
                <Users className="w-3.5 h-3.5" />
                <span>2. Synthetic Buyer Intelligence</span>
              </div>
              <p className="text-gray-300 leading-relaxed text-[11px]">
                {topMandi ? (
                  <>
                    <strong>{topMandi.buyerSignal.activeBuyerCount} active buyers</strong> aggregated from market trader network. Demand: <strong>{topMandi.buyerSignal.demandLevel}</strong>, Offer: {topMandi.buyerSignal.offerStrength}%, Reliability: {topMandi.buyerSignal.reliability}%.
                    <br />
                    <span className="text-[10px] text-amber-300 font-bold uppercase block mt-0.5">
                      Honesty Classification: {topMandi.buyerSignal.classification}
                    </span>
                  </>
                ) : (
                  'No active buyer records.'
                )}
              </p>
            </div>

            {/* 3. Weather Source & Risk Override */}
            <div className="p-3.5 bg-white/5 rounded-xl border border-white/10 space-y-1.5">
              <div className="flex items-center gap-1.5 text-rose-400 font-bold text-xs">
                <CloudLightning className="w-3.5 h-3.5" />
                <span>3. Weather Source & Risk Override</span>
              </div>
              <p className="text-gray-300 leading-relaxed text-[11px]">
                Status: <strong>{result.weather.status}</strong> • Impact: <strong>{result.weather.impactLevel}</strong> • Source: <strong>{result.weather.classification}</strong>.
                <br />
                Override Triggered:{' '}
                <strong className={result.decision.riskOverrideApplied ? 'text-amber-300' : 'text-emerald-300'}>
                  {result.decision.riskOverrideApplied ? 'YES (Forced Safe Selling)' : 'NO (Normal Hold/Sell)'}
                </strong>
              </p>
            </div>

            {/* 4. ML Forecast Provenance */}
            <div className="p-3.5 bg-white/5 rounded-xl border border-white/10 space-y-1.5">
              <div className="flex items-center gap-1.5 text-amber-400 font-bold text-xs">
                <TrendingUp className="w-3.5 h-3.5" />
                <span>4. ML Forecast Provenance & Peak Alert</span>
              </div>
              <p className="text-gray-300 leading-relaxed text-[11px]">
                Model: <strong>{result.forecast.modelType === 'LIVE' ? 'Live ML Inference' : 'Precomputed Series'}</strong> ({result.forecast.forecastScope}) • Basis: <strong>{result.forecast.historyClassification === 'SYNTHETIC' ? 'Synthetic Training Baseline' : result.forecast.historyClassification === 'SEEDED' ? 'Seeded Market Baseline' : 'Historical Baseline'}</strong> ({result.forecast.historyWindowDays}-day series).
                <br />
                Peak Price: <strong>₹{result.forecast.expectedPeakPrice.toLocaleString('en-IN')}</strong> on <strong>Day {result.forecast.peakDay}</strong> (Peak Alert: {result.forecast.peakAlert ? 'ACTIVE' : 'OFF'}).
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
