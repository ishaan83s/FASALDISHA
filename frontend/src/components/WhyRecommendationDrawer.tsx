/**
 * WhyRecommendationDrawer Component: LEVEL 6 "Why This Recommendation?"
 * Collapsible audit trail and judge-proof explainability panel.
 * SSOT Reference: 00_MASTER_PRODUCT_SSOT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md.
 */
import React, { useState } from 'react';
import type { AnalysisResult } from '../types';
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
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const { decision, forecast, dataProvenance, nearbyMandis } = result;

  const topMandi = nearbyMandis[0];

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
              Why We Recommend This (Decision & Logic Audit Trail)
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Inspect the 4 mathematical pillars, buyer signals, weather overrides, and ML data provenance.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs font-bold text-agri-700 dark:text-agri-400">
          <span>{isOpen ? 'Collapse Details' : 'View Audit Trail'}</span>
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
                <span>1. Multi-Factor Ranking Formula</span>
              </div>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
                Mandis are ranked deterministically:
                <br />
                <code className="bg-white dark:bg-slate-800 px-1.5 py-0.5 rounded font-mono text-slate-800 dark:text-slate-200">
                  Score = (0.70 × NetReturn) + (0.20 × BuyerScore) + (0.10 × DataQuality)
                </code>
              </p>
              {topMandi && topMandi.rankingBreakdown && (
                <div className="p-2.5 bg-white dark:bg-slate-800/80 rounded-xl border border-earth-200/80 dark:border-slate-700/60 text-[11px] space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-500">Net Return Subscore (70%):</span>
                    <strong className="text-agri-600 dark:text-agri-400">{topMandi.rankingBreakdown.normalizedRiskAdjustedReturn}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Buyer Signal Subscore (20%):</span>
                    <strong className="text-blue-600 dark:text-blue-400">{topMandi.rankingBreakdown.buyerSignalScore}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Data Quality Subscore (10%):</span>
                    <strong className="text-purple-600 dark:text-purple-400">{topMandi.rankingBreakdown.dataQualityScore}</strong>
                  </div>
                  <div className="flex justify-between pt-1 border-t border-slate-100 dark:border-slate-700 font-bold">
                    <span>Composite Final Score:</span>
                    <span>{topMandi.rankingScore} / 100</span>
                  </div>
                </div>
              )}
            </div>

            {/* Pillar 2: Synthetic Buyer Signals */}
            <div className="p-4 bg-earth-50/70 dark:bg-slate-900/70 rounded-2xl border border-earth-200 dark:border-slate-800 space-y-2.5">
              <div className="flex items-center gap-2 text-blue-700 dark:text-blue-400 font-bold font-heading text-sm">
                <Users className="w-4 h-4" />
                <span>2. Buyer Liquidity & Signals</span>
              </div>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
                Buyer signals measure market liquidity and purchasing power:
                <br />
                <code className="bg-white dark:bg-slate-800 px-1.5 py-0.5 rounded font-mono text-slate-800 dark:text-slate-200">
                  BuyerScore = (0.35 × Demand) + (0.25 × Count) + (0.20 × Offer) + (0.20 × Reliability)
                </code>
              </p>
              {topMandi && (
                <div className="p-2.5 bg-white dark:bg-slate-800/80 rounded-xl border border-earth-200/80 dark:border-slate-700/60 text-[11px] space-y-1">
                  <div className="flex justify-between">
                    <span className="text-slate-500">Active Verified Buyers:</span>
                    <strong className="text-slate-800 dark:text-slate-200">{topMandi.buyerSignal.activeBuyerCount} Buyers</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Demand Category:</span>
                    <strong className="text-slate-800 dark:text-slate-200">{topMandi.buyerSignal.demandLevel}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Offer / Reliability Index:</span>
                    <strong className="text-slate-800 dark:text-slate-200">{topMandi.buyerSignal.offerStrength} / {topMandi.buyerSignal.reliability}</strong>
                  </div>
                  <div className="flex justify-between pt-1 border-t border-slate-100 dark:border-slate-700 text-slate-400 text-[10px]">
                    <span>Classification:</span>
                    <span className="font-mono bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-300 px-1 rounded">{dataProvenance.buyerDataClassification}</span>
                  </div>
                </div>
              )}
            </div>

            {/* Pillar 3: Weather Risk & Override Rules */}
            <div className="p-4 bg-earth-50/70 dark:bg-slate-900/70 rounded-2xl border border-earth-200 dark:border-slate-800 space-y-2.5">
              <div className="flex items-center gap-2 text-amber-700 dark:text-amber-400 font-bold font-heading text-sm">
                <CloudSun className="w-4 h-4" />
                <span>3. Risk Override Logic</span>
              </div>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
                Perishability classification directly dictates risk thresholds. When severe weather threatens transit corridors, HOLD recommendations are safely converted to SELL EARLY.
              </p>
              <div className="p-2.5 bg-white dark:bg-slate-800/80 rounded-xl border border-earth-200/80 dark:border-slate-700/60 text-[11px] space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-500">Base Algorithm Decision:</span>
                  <strong className="text-slate-800 dark:text-slate-200 font-mono">{decision.baseDecision}</strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Risk Override Triggered:</span>
                  <strong className={decision.riskOverrideApplied ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'}>
                    {decision.riskOverrideApplied ? 'YES (Triggered for Safety)' : 'NO (Normal Trajectory)'}
                  </strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Final Actionable Advice:</span>
                  <strong className="text-agri-600 dark:text-agri-400 font-mono">{decision.finalRecommendation}</strong>
                </div>
              </div>
            </div>

            {/* Pillar 4: ML Forecast Provenance */}
            <div className="p-4 bg-earth-50/70 dark:bg-slate-900/70 rounded-2xl border border-earth-200 dark:border-slate-800 space-y-2.5">
              <div className="flex items-center gap-2 text-purple-700 dark:text-purple-400 font-bold font-heading text-sm">
                <BrainCircuit className="w-4 h-4" />
                <span>4. Machine Learning Provenance</span>
              </div>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed text-[11px]">
                Price projections are computed via live in-memory XGBoost regression trained on regional market patterns, evaluating a 7-day price trajectory with peak horizon detection.
              </p>
              <div className="p-2.5 bg-white dark:bg-slate-800/80 rounded-xl border border-earth-200/80 dark:border-slate-700/60 text-[11px] space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-500">Model Engine Type:</span>
                  <strong className="text-slate-800 dark:text-slate-200 font-mono">
                    {forecast.modelType === 'LIVE' ? 'Live ML Inference (XGBoost)' : 'Precomputed Series'}
                  </strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Training / Data Basis:</span>
                  <strong className="text-slate-800 dark:text-slate-200">
                    {forecast.historyClassification === 'SYNTHETIC'
                      ? 'Synthetic Training Baseline'
                      : forecast.historyClassification === 'SEEDED'
                      ? 'Seeded Market Baseline'
                      : 'Historical Series'} ({forecast.historyWindowDays}-Day Window)
                  </strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Data Source Label:</span>
                  <span className="text-slate-600 dark:text-slate-300 text-[10px]">{forecast.historySourceLabel}</span>
                </div>
                <div className="flex justify-between pt-1 border-t border-slate-100 dark:border-slate-700">
                  <span className="text-slate-500">Forecast Scope:</span>
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
