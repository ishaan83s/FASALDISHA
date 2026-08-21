/**
 * ReasoningPanel Component: Judge-Proof Acceptance & Explainability Evidence Area.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 5, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React from 'react';
import type { AnalysisResult } from '../types';
import {
  CheckCircle2,
  Users,
  CloudLightning,
  TrendingUp,
  MapPin,
} from 'lucide-react';

interface ReasoningPanelProps {
  result: AnalysisResult;
}

export const ReasoningPanel: React.FC<ReasoningPanelProps> = ({ result }) => {
  const topMandi = result.nearbyMandis[0];

  return (
    <div className="bg-gradient-to-br from-slate-900 via-gray-900 to-slate-950 rounded-2xl border border-emerald-500/30 p-6 text-white shadow-xl space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-white/10">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <h2 className="text-lg font-bold text-white tracking-tight">
            Judge-Proof System Proof & Audit Trail
          </h2>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
          SSOT v2.1 Verification Gate
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Proof Anchor 1: Why is this mandi ranked first? */}
        <div className="p-4 bg-white/5 rounded-xl border border-white/10 space-y-2">
          <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs">
            <MapPin className="w-4 h-4" />
            <span>1. Best Location & Ranking Proof</span>
          </div>
          <p className="text-xs text-gray-300 leading-relaxed">
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

        {/* Proof Anchor 2: Synthetic Buyer Intelligence */}
        <div className="p-4 bg-white/5 rounded-xl border border-white/10 space-y-2">
          <div className="flex items-center gap-2 text-blue-400 font-bold text-xs">
            <Users className="w-4 h-4" />
            <span>2. Buyer Intelligence Audit</span>
          </div>
          <p className="text-xs text-gray-300 leading-relaxed">
            {topMandi ? (
              <>
                <strong>{topMandi.buyerSignal.activeBuyerCount} active buyers</strong> aggregated from demo dataset. Demand: <strong>{topMandi.buyerSignal.demandLevel}</strong>, Offer: {topMandi.buyerSignal.offerStrength}%, Reliability: {topMandi.buyerSignal.reliability}%.
                <br />
                <span className="text-[10px] text-amber-300 font-bold uppercase block mt-1">
                  Honesty Label: {topMandi.buyerSignal.classification} DEMO DATASET
                </span>
              </>
            ) : (
              'No active buyer records.'
            )}
          </p>
        </div>

        {/* Proof Anchor 3: Weather Source & Risk Override */}
        <div className="p-4 bg-white/5 rounded-xl border border-white/10 space-y-2">
          <div className="flex items-center gap-2 text-rose-400 font-bold text-xs">
            <CloudLightning className="w-4 h-4" />
            <span>3. Weather Source & Risk Override</span>
          </div>
          <p className="text-xs text-gray-300 leading-relaxed">
            Status: <strong>{result.weather.status}</strong> • Impact: <strong>{result.weather.impactLevel}</strong> • Source: <strong>{result.weather.classification}</strong> ({result.weather.sourceLabel}).
            <br />
            Override Applied:{' '}
            <strong className={result.decision.riskOverrideApplied ? 'text-amber-300' : 'text-emerald-300'}>
              {result.decision.riskOverrideApplied ? 'YES (Forced Safe Action)' : 'NO (Normal Trajectory)'}
            </strong>
          </p>
        </div>

        {/* Proof Anchor 4: ML Forecast Provenance & Peak Alert */}
        <div className="p-4 bg-white/5 rounded-xl border border-white/10 space-y-2">
          <div className="flex items-center gap-2 text-amber-400 font-bold text-xs">
            <TrendingUp className="w-4 h-4" />
            <span>4. ML Forecast Provenance & Peak Alert</span>
          </div>
          <p className="text-xs text-gray-300 leading-relaxed">
            Model: <strong>{result.forecast.modelType}</strong> ({result.forecast.forecastScope}) • Basis: <strong>{result.forecast.historyClassification}</strong> ({result.forecast.historyWindowDays}-day historical window).
            <br />
            Peak Detection: Peak at <strong>₹{result.forecast.expectedPeakPrice.toLocaleString('en-IN')}</strong> on <strong>Day {result.forecast.peakDay}</strong> (Alert: {result.forecast.peakAlert ? 'ACTIVE' : 'OFF'}).
          </p>
        </div>
      </div>
    </div>
  );
};
