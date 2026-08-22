/**
 * LocationContextBar Component: Top-level Location, Crop & Mandi Context.
 * SSOT & Design Reference: Level 0 Context Header.
 */
import React from 'react';
import type { AnalysisResult } from '../types';
import { ArrowLeft, MapPin, Wheat, Scale, Compass, CalendarCheck } from 'lucide-react';

interface LocationContextBarProps {
  result: AnalysisResult;
  onModifySearch: () => void;
}

export const LocationContextBar: React.FC<LocationContextBarProps> = ({
  result,
  onModifySearch,
}) => {
  const { farmerContext, commodity, forecast } = result;

  const getPerishabilityColor = (pClass: string) => {
    switch (pClass) {
      case 'HIGHLY_PERISHABLE':
        return 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border-rose-200 dark:border-rose-800';
      case 'MODERATELY_PERISHABLE':
        return 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border-amber-200 dark:border-amber-800';
      case 'NON_PERISHABLE':
        return 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800';
      default:
        return 'bg-slate-100 text-slate-700';
    }
  };

  return (
    <div className="bg-white dark:bg-[#151c24] border border-earth-200 dark:border-slate-800 rounded-2xl p-3.5 sm:p-4 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-3">
      {/* Left: Modify Button & Current Location */}
      <div className="flex flex-wrap items-center gap-2 sm:gap-3">
        <button
          type="button"
          onClick={onModifySearch}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-earth-100 dark:bg-slate-800 hover:bg-earth-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 rounded-xl text-xs font-bold transition shadow-2xs cursor-pointer"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Change Inputs</span>
        </button>

        <div className="flex items-center gap-1.5 text-xs font-medium text-slate-700 dark:text-slate-300">
          <MapPin className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
          <span className="capitalize font-bold text-slate-900 dark:text-white">
            {farmerContext.districtId}, {farmerContext.stateId}
          </span>
          <span className="text-[11px] text-slate-400 font-mono hidden sm:inline">
            ({farmerContext.latitude.toFixed(2)}°N, {farmerContext.longitude.toFixed(2)}°E)
          </span>
        </div>
      </div>

      {/* Right: Crop, Volume & Horizon Chips */}
      <div className="flex flex-wrap items-center gap-2 text-xs">
        {/* Commodity Badge */}
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-agri-50 dark:bg-agri-950/50 border border-agri-200 dark:border-agri-800/80 font-bold text-agri-800 dark:text-agri-300">
          <Wheat className="w-3.5 h-3.5 text-agri-600 dark:text-agri-400" />
          <span>{commodity.commodityName}</span>
          <span className={`text-[10px] px-1.5 py-0.2 rounded-md font-semibold border ${getPerishabilityColor(commodity.perishabilityClass)}`}>
            {commodity.perishabilityClass.replace(/_/g, ' ')}
          </span>
        </span>

        {/* Quantity */}
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-xl bg-slate-50 dark:bg-slate-800/70 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-medium">
          <Scale className="w-3.5 h-3.5 text-slate-400" />
          <strong>{farmerContext.quantityQuintals} Quintals</strong>
        </span>

        {/* Radius */}
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-xl bg-slate-50 dark:bg-slate-800/70 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-medium">
          <Compass className="w-3.5 h-3.5 text-slate-400" />
          <span>{farmerContext.radiusKm} km radius</span>
        </span>

        {/* Best Day Pill */}
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-amber-900 dark:text-amber-200 font-bold">
          <CalendarCheck className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
          <span>Best Day: Day {forecast.peakDay}</span>
        </span>
      </div>
    </div>
  );
};
