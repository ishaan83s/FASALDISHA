/**
 * ForecastTrendChart Component: LEVEL 3 "When Should I Sell?"
 * Day 1 -> Day 14 Clean Price Trend, Peak Detection, and Visual Forecast Bars.
 * SSOT & Wireframe Reference: "Expected Day 1 - Day 14 Trend".
 */
import React from 'react';
import type { ForecastOutput } from '../types';
import { TrendingUp, Sparkles, CheckCircle2 } from 'lucide-react';

interface ForecastTrendChartProps {
  forecast: ForecastOutput;
  commodityName: string;
}

export const ForecastTrendChart: React.FC<ForecastTrendChartProps> = ({
  forecast,
  commodityName,
}) => {
  const dailyPoints = forecast.dailyForecast || [];
  const maxPrice = Math.max(
    forecast.currentPrice,
    forecast.expectedPeakPrice,
    ...dailyPoints.map((d) => d.predictedPrice)
  );
  const minPrice = Math.min(
    forecast.currentPrice,
    forecast.forecast7Day,
    ...dailyPoints.map((d) => d.predictedPrice)
  );
  const priceRange = Math.max(maxPrice - minPrice, 50);

  const gainFromCurrent = forecast.expectedPeakPrice - forecast.currentPrice;
  const gainPercent = ((gainFromCurrent / Math.max(forecast.currentPrice, 1)) * 100).toFixed(1);

  return (
    <div className="bg-white dark:bg-[#151c24] border border-earth-200 dark:border-slate-800 rounded-3xl p-5 sm:p-6 shadow-sm space-y-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100 dark:border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-lg font-bold text-slate-900 dark:text-white font-heading">
              Expected Price Trend (Day 1 → Day 7 Horizon)
            </h2>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            AI price projection for {commodityName} based on historical mandi patterns and weather signals.
          </p>
        </div>

        {/* Peak Callout Badge */}
        {forecast.peakAlert ? (
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-50 dark:bg-amber-950/60 border border-amber-300 dark:border-amber-700/80 rounded-2xl text-amber-900 dark:text-amber-200 text-xs font-bold shadow-2xs">
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span>Peak Day {forecast.peakDay}: ₹{forecast.expectedPeakPrice.toLocaleString('en-IN')}/q (+{gainPercent}%)</span>
          </div>
        ) : (
          <div className="inline-flex items-center gap-1 px-3 py-1.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl text-slate-600 dark:text-slate-300 text-xs font-semibold">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
            <span>Steady Price Horizon</span>
          </div>
        )}
      </div>

      {/* 3 Metric Pills */}
      <div className="grid grid-cols-3 gap-2.5 text-xs">
        <div className="p-3 bg-earth-50 dark:bg-slate-900/60 rounded-2xl border border-earth-200/80 dark:border-slate-800 text-center">
          <span className="text-slate-400 text-[10px] uppercase font-bold block">Current Modal</span>
          <span className="text-base sm:text-lg font-extrabold text-slate-900 dark:text-white font-heading">
            ₹{forecast.currentPrice.toLocaleString('en-IN')}
          </span>
          <span className="text-[10px] text-slate-400 block">Today's baseline</span>
        </div>

        <div className="p-3 bg-earth-50 dark:bg-slate-900/60 rounded-2xl border border-earth-200/80 dark:border-slate-800 text-center">
          <span className="text-slate-400 text-[10px] uppercase font-bold block">Day 3 Forecast</span>
          <span className="text-base sm:text-lg font-extrabold text-emerald-600 dark:text-emerald-400 font-heading">
            ₹{forecast.forecast3Day.toLocaleString('en-IN')}
          </span>
          <span className="text-[10px] text-slate-400 block">72-hr projection</span>
        </div>

        <div className="p-3 bg-amber-50/70 dark:bg-amber-950/30 rounded-2xl border border-amber-200 dark:border-amber-800/60 text-center">
          <span className="text-amber-800 dark:text-amber-300 text-[10px] uppercase font-bold block">Expected Peak</span>
          <span className="text-base sm:text-lg font-black text-amber-900 dark:text-amber-200 font-heading">
            ₹{forecast.expectedPeakPrice.toLocaleString('en-IN')}
          </span>
          <span className="text-[10px] font-bold text-amber-700 dark:text-amber-400 block">Day {forecast.peakDay}</span>
        </div>
      </div>

      {/* Visual Daily Horizon Cards (Apple Weather Style in Wireframe) */}
      {dailyPoints.length > 0 && (
        <div className="pt-2">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span>Daily Price Trajectory (₹/Quintal)</span>
            <span>Forecast Confidence: {Math.round(forecast.forecastConfidence * 100)}%</span>
          </div>

          <div className="grid grid-cols-7 gap-1.5 sm:gap-2">
            {dailyPoints.map((dp) => {
              const isPeak = dp.day === forecast.peakDay;
              const heightPercent = Math.max(
                25,
                Math.round(((dp.predictedPrice - minPrice + 10) / (priceRange + 20)) * 100)
              );

              return (
                <div
                  key={dp.day}
                  className={`p-2 rounded-2xl border flex flex-col items-center justify-between gap-1.5 transition-all ${
                    isPeak
                      ? 'bg-amber-50/90 dark:bg-amber-950/50 border-amber-300 dark:border-amber-700 shadow-sm ring-1 ring-amber-400/40'
                      : 'bg-slate-50/70 dark:bg-slate-900/40 border-slate-200/80 dark:border-slate-800'
                  }`}
                >
                  <span className={`text-[11px] font-bold ${isPeak ? 'text-amber-800 dark:text-amber-300' : 'text-slate-500 dark:text-slate-400'}`}>
                    Day {dp.day}
                  </span>

                  {/* Vertical bar */}
                  <div className="w-full h-20 bg-slate-200/60 dark:bg-slate-800 rounded-lg flex flex-col justify-end p-0.5 overflow-hidden">
                    <div
                      style={{ height: `${heightPercent}%` }}
                      className={`w-full rounded-md transition-all duration-300 ${
                        isPeak
                          ? 'bg-amber-500 dark:bg-amber-400 shadow-sm'
                          : 'bg-emerald-500/80 dark:bg-emerald-600'
                      }`}
                    />
                  </div>

                  <span className={`text-xs font-black font-heading ${isPeak ? 'text-amber-900 dark:text-amber-200' : 'text-slate-800 dark:text-slate-200'}`}>
                    ₹{Math.round(dp.predictedPrice)}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Provenance note */}
      <div className="pt-2 flex items-center justify-between text-[11px] text-slate-400 border-t border-slate-100 dark:border-slate-800">
        <span>Basis: {forecast.historySourceLabel}</span>
        <span>Model: {forecast.modelType}</span>
      </div>
    </div>
  );
};
