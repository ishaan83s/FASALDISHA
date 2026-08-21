/**
 * ForecastChart / ForecastPanel Component: 7-Day ML Price Horizons, Peak Alert, and Provenance.
 * SSOT Reference: 02_DATA_AND_ML_SSOT.md Section 5 & 8, 06_FRONTEND_CONTRACT.md Section 3, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React from 'react';
import type { ForecastOutput } from '../types';
import {
  TrendingUp,
  Sparkles,
  Database,
  CheckCircle2,
} from 'lucide-react';

interface ForecastChartProps {
  forecast: ForecastOutput;
  commodityName: string;
}

export const ForecastChart: React.FC<ForecastChartProps> = ({
  forecast,
}) => {
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
    <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-5 md:p-6 shadow-sm space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-gray-100 dark:border-gray-700/60">
        <div>
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-lg font-bold text-gray-900 dark:text-white">
              7-Day Price Forecast & Peak Analysis
            </h2>
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
            Model: <span className="font-semibold text-gray-700 dark:text-gray-300">{forecast.modelType}</span> ({forecast.forecastScope}) • Provenance: <span className="font-semibold text-gray-700 dark:text-gray-300">{forecast.historyClassification}</span> ({forecast.historyWindowDays}-day series)
          </p>
        </div>

        {/* Peak Alert Banner */}
        {forecast.peakAlert ? (
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-500/15 border border-amber-500/40 rounded-xl text-amber-800 dark:text-amber-300 text-xs font-bold animate-pulse">
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span>PEAK ALERT: +{gainPercent}% Gain Expected</span>
          </div>
        ) : (
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gray-100 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 rounded-xl text-gray-600 dark:text-gray-300 text-xs font-medium">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
            <span>Normal Price Trajectory</span>
          </div>
        )}
      </div>

      {/* Key Horizon Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="p-3.5 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-200/80 dark:border-gray-700">
          <span className="text-xs font-medium text-gray-500 dark:text-gray-400">Current Modal</span>
          <p className="text-lg font-extrabold text-gray-900 dark:text-white mt-1">
            ₹{forecast.currentPrice.toLocaleString('en-IN')}
          </p>
          <span className="text-[11px] text-gray-400">Baseline Price</span>
        </div>

        <div className="p-3.5 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-200/80 dark:border-gray-700">
          <span className="text-xs font-medium text-gray-500 dark:text-gray-400">Day 1 Forecast</span>
          <p className="text-lg font-extrabold text-emerald-700 dark:text-emerald-400 mt-1">
            ₹{forecast.forecast1Day.toLocaleString('en-IN')}
          </p>
          <span className="text-[11px] text-gray-400">24-hour horizon</span>
        </div>

        <div className="p-3.5 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-200/80 dark:border-gray-700">
          <span className="text-xs font-medium text-gray-500 dark:text-gray-400">Day 3 Forecast</span>
          <p className="text-lg font-extrabold text-emerald-700 dark:text-emerald-400 mt-1">
            ₹{forecast.forecast3Day.toLocaleString('en-IN')}
          </p>
          <span className="text-[11px] text-gray-400">72-hour horizon</span>
        </div>

        <div className="p-3.5 bg-amber-50 dark:bg-amber-950/30 rounded-xl border border-amber-200 dark:border-amber-800/60">
          <span className="text-xs font-medium text-amber-800 dark:text-amber-300 flex items-center justify-between">
            <span>Expected Peak</span>
            <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-amber-200 dark:bg-amber-900 text-amber-900 dark:text-amber-200">
              Day {forecast.peakDay}
            </span>
          </span>
          <p className="text-lg font-extrabold text-amber-900 dark:text-amber-300 mt-1">
            ₹{forecast.expectedPeakPrice.toLocaleString('en-IN')}
          </p>
          <span className="text-[11px] text-amber-700/80 dark:text-amber-400 font-medium">
            +{gainPercent}% (₹{gainFromCurrent.toLocaleString('en-IN')}/q)
          </span>
        </div>
      </div>

      {/* 7-Day Visual Bar/Point Trend */}
      {forecast.dailyForecast.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>7-Day Price Progression (₹/Quintal)</span>
            <span>Confidence: {Math.round(forecast.forecastConfidence * 100)}%</span>
          </div>

          <div className="grid grid-cols-7 gap-1.5 sm:gap-2 pt-2">
            {forecast.dailyForecast.map((point) => {
              const isPeak = point.day === forecast.peakDay;
              const heightPercent = Math.max(
                15,
                Math.round(((point.predictedPrice - minPrice + 20) / (range + 40)) * 100)
              );

              return (
                <div key={point.day} className="flex flex-col items-center gap-1.5">
                  <div className="w-full h-24 bg-gray-100 dark:bg-gray-900/60 rounded-lg flex flex-col justify-end p-1 relative overflow-hidden">
                    {isPeak && (
                      <div className="absolute top-1 left-1/2 -translate-x-1/2">
                        <span className="text-[9px] font-extrabold text-amber-700 dark:text-amber-300 bg-amber-200 dark:bg-amber-900/90 px-1 rounded-sm">
                          PEAK
                        </span>
                      </div>
                    )}
                    <div
                      style={{ height: `${heightPercent}%` }}
                      className={`w-full rounded-md transition-all duration-300 ${
                        isPeak
                          ? 'bg-amber-500 dark:bg-amber-400 shadow-lg shadow-amber-500/30'
                          : 'bg-emerald-500/80 dark:bg-emerald-600'
                      }`}
                    />
                  </div>
                  <span className="text-[11px] font-bold text-gray-700 dark:text-gray-300">
                    ₹{Math.round(point.predictedPrice)}
                  </span>
                  <span className="text-[10px] text-gray-400">Day {point.day}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Historical Basis & Provenance Footnote */}
      <div className="p-3 bg-gray-50 dark:bg-gray-900/40 rounded-xl border border-gray-200/60 dark:border-gray-800 text-xs text-gray-600 dark:text-gray-400 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Database className="w-3.5 h-3.5 text-gray-400" />
          <span>
            History Basis: <strong className="text-gray-700 dark:text-gray-300">{forecast.historySourceLabel}</strong>
          </span>
        </div>
        <span className="text-[11px] text-gray-400">
          Classification: <strong>{forecast.historyClassification}</strong>
        </span>
      </div>
    </div>
  );
};
