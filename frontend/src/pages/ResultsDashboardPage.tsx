/**
 * ResultsDashboardPage Component: Assembles full decision dashboard and evidence panels.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 3 & 5, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React from 'react';
import type { AnalysisResult } from '../types';
import { RecommendationBanner } from '../components/RecommendationBanner';
import { ForecastChart } from '../components/ForecastChart';
import { MandiComparisonList } from '../components/MandiComparisonList';
import { RiskPanel } from '../components/RiskPanel';
import { WeatherAlert } from '../components/WeatherAlert';
import { ReasoningPanel } from '../components/ReasoningPanel';
import { ArrowLeft } from 'lucide-react';

interface ResultsDashboardPageProps {
  result: AnalysisResult;
  onModifySearch: () => void;
}

export const ResultsDashboardPage: React.FC<ResultsDashboardPageProps> = ({
  result,
  onModifySearch,
}) => {
  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Navigation & Context Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white dark:bg-gray-800 p-4 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <button
          type="button"
          onClick={onModifySearch}
          className="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-xl text-xs font-bold transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Modify Parameters</span>
        </button>

        <div className="flex flex-wrap items-center gap-2 text-xs text-gray-600 dark:text-gray-300">
          <span className="font-bold text-gray-900 dark:text-white capitalize">
            {result.commodity.commodityName} ({result.commodity.perishabilityClass.replace(/_/g, ' ')})
          </span>
          <span>•</span>
          <span>
            Quantity: <strong>{result.farmerContext.quantityQuintals} Quintals</strong>
          </span>
          <span>•</span>
          <span>
            Radius: <strong>{result.farmerContext.radiusKm} km</strong>
          </span>
          <span>•</span>
          <span className="capitalize">
            {result.farmerContext.districtId}, {result.farmerContext.stateId}
          </span>
        </div>
      </div>

      {/* 1. Hero Recommendation Banner */}
      <RecommendationBanner
        decision={result.decision}
        commodityName={result.commodity.commodityName}
      />

      {/* 2. Weather Advisory & Alert Flag */}
      <WeatherAlert weather={result.weather} />

      {/* 3. ML Forecast & Peak Horizons */}
      <ForecastChart
        forecast={result.forecast}
        commodityName={result.commodity.commodityName}
      />

      {/* 4. Ranked Dynamic Candidate Mandis */}
      <MandiComparisonList
        candidates={result.nearbyMandis}
        quantityQuintals={result.farmerContext.quantityQuintals}
        radiusKm={result.farmerContext.radiusKm}
        crossBoundary={result.search.crossBoundaryCandidatesIncluded}
      />

      {/* 5. Operational Risk Assessment Panel */}
      <RiskPanel
        riskSummary={result.riskSummary}
        weather={result.weather}
        commodity={result.commodity}
        riskOverrideApplied={result.decision.riskOverrideApplied}
      />

      {/* 6. Judge-Proof Evidence & Reasoning Panel */}
      <ReasoningPanel result={result} />
    </div>
  );
};
