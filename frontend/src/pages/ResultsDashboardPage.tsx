/**
 * ResultsDashboardPage Component: Clean, Intuitive Market Decision Dashboard.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 3 & 5, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React from 'react';
import type { AnalysisResult } from '../types';
import { RecommendationBanner } from '../components/RecommendationBanner';
import { ForecastChart } from '../components/ForecastChart';
import { MandiComparisonList } from '../components/MandiComparisonList';
import { ReasoningPanel } from '../components/ReasoningPanel';
import { ArrowLeft, MapPin, Scale, Wheat } from 'lucide-react';

interface ResultsDashboardPageProps {
  result: AnalysisResult;
  onModifySearch: () => void;
}

export const ResultsDashboardPage: React.FC<ResultsDashboardPageProps> = ({
  result,
  onModifySearch,
}) => {
  const topMandi = result.nearbyMandis[0];

  return (
    <div className="max-w-6xl mx-auto space-y-5">
      {/* 1. Slim Top Navigation & Context Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white dark:bg-gray-800/90 px-4 py-3 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <button
          type="button"
          onClick={onModifySearch}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-xl text-xs font-bold transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Modify Parameters</span>
        </button>

        <div className="flex flex-wrap items-center gap-2 text-xs text-gray-600 dark:text-gray-300">
          <span className="inline-flex items-center gap-1 font-bold text-gray-900 dark:text-white capitalize bg-emerald-50 dark:bg-emerald-950/60 px-2 py-0.5 rounded-lg border border-emerald-200 dark:border-emerald-800">
            <Wheat className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            {result.commodity.commodityName}
          </span>
          <span>•</span>
          <span className="inline-flex items-center gap-1">
            <Scale className="w-3.5 h-3.5 text-gray-400" />
            <strong>{result.farmerContext.quantityQuintals} Quintals</strong>
          </span>
          <span>•</span>
          <span className="inline-flex items-center gap-1">
            <MapPin className="w-3.5 h-3.5 text-gray-400" />
            <span className="capitalize">{result.farmerContext.districtId}, {result.farmerContext.stateId}</span>
          </span>
        </div>
      </div>

      {/* 2. Sleek Hero Recommendation Banner */}
      <RecommendationBanner
        decision={result.decision}
        weather={result.weather}
        topMandi={topMandi}
      />

      {/* 3. Clean 2-Column Responsive Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        {/* Left Column: Ranked Mandis List (7 cols on desktop) */}
        <div className="lg:col-span-7 space-y-4">
          <MandiComparisonList
            candidates={result.nearbyMandis}
            radiusKm={result.farmerContext.radiusKm}
            crossBoundary={result.search.crossBoundaryCandidatesIncluded}
          />
        </div>

        {/* Right Column: 7-Day Forecast & Risk Glance (5 cols on desktop) */}
        <div className="lg:col-span-5 space-y-4">
          <ForecastChart forecast={result.forecast} />
        </div>
      </div>

      {/* 4. Collapsible System Audit & Judge Proof Section */}
      <div className="pt-2">
        <ReasoningPanel result={result} />
      </div>
    </div>
  );
};
