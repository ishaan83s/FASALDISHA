/**
 * MandiComparisonList Component: Dynamic candidate list renderer (no fixed count).
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 3, 07_ENGINEERING_RULES.md Section 5
 */
import React from 'react';
import type { CandidateMandi } from '../types';
import { MandiComparisonCard } from './MandiComparisonCard';
import { Building2, Compass, AlertCircle } from 'lucide-react';

interface MandiComparisonListProps {
  candidates: CandidateMandi[];
  radiusKm: number;
  crossBoundary: boolean;
}

export const MandiComparisonList: React.FC<MandiComparisonListProps> = ({
  candidates,
  radiusKm,
  crossBoundary,
}) => {
  if (!candidates || candidates.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-8 text-center space-y-3">
        <AlertCircle className="w-10 h-10 text-amber-500 mx-auto" />
        <h3 className="text-base font-bold text-gray-900 dark:text-white">
          No Eligible Mandis Found Within {radiusKm} km
        </h3>
        <p className="text-xs text-gray-500 dark:text-gray-400 max-w-md mx-auto">
          Try expanding your search radius up to 300 km or select a different commodity.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <Building2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          <h2 className="text-base font-bold text-gray-900 dark:text-white">
            Market Rankings ({candidates.length} Mandis Found)
          </h2>
        </div>

        <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
          <Compass className="w-3.5 h-3.5 text-gray-400" />
          <span>Radius: {radiusKm} km</span>
          {crossBoundary && (
            <span className="font-semibold text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/60 px-2 py-0.5 rounded-full border border-indigo-200 dark:border-indigo-800 text-[10px]">
              Cross-Boundary
            </span>
          )}
        </div>
      </div>

      <div className="space-y-3">
        {candidates.map((candidate, idx) => (
          <MandiComparisonCard
            key={candidate.mandi.mandiId}
            candidate={candidate}
            isRecommended={idx === 0}
          />
        ))}
      </div>
    </div>
  );
};
