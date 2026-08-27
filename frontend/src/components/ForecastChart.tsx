/**
 * ForecastChart Component: Streamlined 7-Day ML Price Horizons & Trend.
 * SSOT Reference: 02_DATA_AND_ML_SSOT.md Section 5 & 8, 06_FRONTEND_CONTRACT.md Section 3, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React from 'react';
import type { ForecastOutput } from '../types';
import {
  TrendingUp,
  Sparkles,
  CheckCircle2,
} from 'lucide-react';

interface ForecastChartProps {
  forecast: ForecastOutput;
}

export const ForecastChart: React.FC<ForecastChartProps> = ({ forecast }) => {
  const maxPrice = Math.max(
    forecast.currentPrice,
    forecast.expectedPeakPrice,
    ...forecast.dailyForecast.map((d) => d.predictedPrice)
  );
  const minPrice = Math.min(
    forecast.currentPrice,
    forecast.forecast7Day,
    ...forecast.dailyForecast.map((d) => d.predictedPrice)
  );
  const range = Math.max(maxPrice - minPrice, 50);

  const gainFromCurrent = forecast.expectedPeakPrice - forecast.currentPrice;
  const gainPercent = ((gainFromCurrent / Math.max(forecast.currentPrice, 1)) * 100).toFixed(1);

  return (
    <div className="bg-white dark:bg-gray-800/90 rounded-2xl border border-gray-200 dark:border-gray-700 p-4 md:p-5 shadow-sm space-y-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-gray-100 dark:border-gray-700/60">
        <div className="flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          <h2 className="text-base font-bold text-gray-900 dark:text-white">
            7-Day Price Forecast & Peak Detection
          </h2>
        </div>

        {forecast.peakAlert ? (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-amber-500/15 border border-amber-500/30 rounded-full text-amber-800 dark:text-amber-300 text-xs font-bold animate-pulse">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            <span>Peak Expected: +{gainPercent}% (Day {forecast.peakDay})</span>
          </span>
        ) : (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full text-[11px]">
            <CheckCircle2 className="w-3 h-3 text-emerald-500" />
            <span>Normal Trajectory</span>
          </span>
        )}
      </div>

      {/* 4 Stat Highlights */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
        <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded-xl border border-gray-100 dark:border-gray-700/60">
          <span className="text-gray-400 text-[10px] uppercase font-semibold">Current Modal</span>
          <p className="text-base font-bold text-gray-900 dark:text-white mt-0.5">
            ₹{forecast.currentPrice.toLocaleString('en-IN')}/q
          </p>
        </div>

        <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded-xl border border-gray-100 dark:border-gray-700/60">
          <span className="text-gray-400 text-[10px] uppercase font-semibold">Day 1 Horizon</span>
          <p className="text-base font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">
            ₹{forecast.forecast1Day.toLocaleString('en-IN')}/q
          </p>
        </div>

        <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded-xl border border-gray-100 dark:border-gray-700/60">
          <span className="text-gray-400 text-[10px] uppercase font-semibold">Day 3 Horizon</span>
          <p className="text-base font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">
            ₹{forecast.forecast3Day.toLocaleString('en-IN')}/q
          </p>
        </div>

        <div className="p-2.5 bg-amber-50/80 dark:bg-amber-950/30 rounded-xl border border-amber-200 dark:border-amber-800/50">
          <div className="flex items-center justify-between">
            <span className="text-amber-800 dark:text-amber-300 text-[10px] uppercase font-bold">Expected Peak</span>
            <span className="text-[9px] font-extrabold px-1 rounded bg-amber-200 dark:bg-amber-900 text-amber-900 dark:text-amber-200">
              Day {forecast.peakDay}
            </span>
          </div>
          <p className="text-base font-black text-amber-900 dark:text-amber-200 mt-0.5">
            ₹{forecast.expectedPeakPrice.toLocaleString('en-IN')}/q
          </p>
        </div>
      </div>

      {/* 7-Day Visual Progression Bars */}
      {forecast.dailyForecast.length > 0 && (
        <div className="pt-1">
          <div className="grid grid-cols-7 gap-1.5 sm:gap-2">
            {forecast.dailyForecast.map((point) => {
              const isPeak = point.day === forecast.peakDay;
              const heightPercent = Math.max(
                20,
                Math.round(((point.predictedPrice - minPrice + 10) / (range + 20)) * 100)
              );

              return (
                <div key={point.day} className="flex flex-col items-center gap-1">
                  <div className="w-full h-16 bg-gray-100 dark:bg-gray-900/50 rounded-lg flex flex-col justify-end p-0.5 relative overflow-hidden">
                    <div
                      style={{ height: `${heightPercent}%` }}
                      className={`w-full rounded transition-all duration-200 ${
                        isPeak
                          ? 'bg-amber-500 dark:bg-amber-400 shadow-md'
                          : 'bg-emerald-500/80 dark:bg-emerald-600'
                      }`}
                    />
                  </div>
                  <span className="text-[10px] font-bold text-gray-700 dark:text-gray-300">
                    ₹{Math.round(point.predictedPrice)}
                  </span>
                  <span className="text-[9px] text-gray-400">D{point.day}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Provenance Footnote */}
      <div className="pt-2 flex items-center justify-between text-[11px] text-gray-400 border-t border-gray-100 dark:border-gray-700/60">
        <span>Basis: {forecast.historySourceLabel}</span>
        <span>Model: {forecast.modelType === 'LIVE' ? 'Live ML Inference' : 'Precomputed Series'}</span>
      </div>
    </div>
  );
};
