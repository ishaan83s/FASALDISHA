/**
 * ResultsDashboardPage Component: Structural Skeleton aligned with Wireframe & Stitch Inspiration.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md, Prompt Section 14 "Results Page Structure".
 */
import React from 'react';
import type { AnalysisResult } from '../types';
import { LocationContextBar } from '../components/LocationContextBar';
import { DecisionHeroCard } from '../components/DecisionHeroCard';
import { ForecastTrendChart } from '../components/ForecastTrendChart';
import { MandiRankingList } from '../components/MandiRankingList';
import { MandiLocationRadarMap } from '../components/MandiLocationRadarMap';
import { AnalysisConfidenceCard } from '../components/AnalysisConfidenceCard';
import { WeatherImpactCard } from '../components/WeatherImpactCard';
import { WhyRecommendationDrawer } from '../components/WhyRecommendationDrawer';

interface ResultsDashboardPageProps {
  result: AnalysisResult;
  onModifySearch: () => void;
}

export const ResultsDashboardPage: React.FC<ResultsDashboardPageProps> = ({
  result,
  onModifySearch,
}) => {
  const topMandi = result.nearbyMandis[0];
  const recommendedMandiId = result.decision.recommendedMandi?.mandiId || topMandi?.mandi.mandiId;

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* 1. Location / Mandi Context Header */}
      <LocationContextBar
        result={result}
        onModifySearch={onModifySearch}
      />

      {/* 2. Primary Decision & Profit Hero Card (Level 1 & 2: Focal Point) */}
      <DecisionHeroCard
        decision={result.decision}
        forecast={result.forecast}
        topMandi={topMandi}
        commodityName={result.commodity.commodityName}
      />

      {/* 3. Expected Day 1 -> Day 14 Price Trend (Level 3) */}
      <ForecastTrendChart
        forecast={result.forecast}
        commodityName={result.commodity.commodityName}
      />

      {/* 4. Two-Column Layout (Matching Wireframe Structural Skeleton) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column (7 cols): Ranked Mandis in Range */}
        <div className="lg:col-span-7 space-y-4">
          <MandiRankingList
            candidates={result.nearbyMandis}
            recommendedMandiId={recommendedMandiId}
            radiusKm={result.farmerContext.radiusKm}
            isCrossBoundary={result.search.crossBoundaryCandidatesIncluded}
          />
        </div>

        {/* Right Column (5 cols): Map & Regional Highlights, Confidence, and Weather */}
        <div className="lg:col-span-5 space-y-5">
          {/* Visual Location & Radar Map (As sketched in top-right of Wireframe) */}
          <MandiLocationRadarMap
            farmerContext={result.farmerContext}
            candidates={result.nearbyMandis}
            recommendedMandiId={recommendedMandiId}
          />

          {/* Confidence of Our Analysis (As sketched in bottom-right of Wireframe) */}
          <AnalysisConfidenceCard
            decision={result.decision}
            riskSummary={result.riskSummary}
            forecast={result.forecast}
            search={result.search}
          />

          {/* Contextual Weather Impact */}
          <WeatherImpactCard
            weather={result.weather}
            commodityName={result.commodity.commodityName}
          />
        </div>
      </div>

      {/* 5. Level 6: Why This Recommendation? (Judge Proof & Audit Trail) */}
      <div className="pt-2">
        <WhyRecommendationDrawer result={result} />
      </div>
    </div>
  );
};
