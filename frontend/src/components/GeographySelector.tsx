/**
 * GeographySelector Component: Dynamic State and District cascading selector.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 1
 */
import React from 'react';
import type { State, District } from '../types';

interface GeographySelectorProps {
  states: State[];
  districts: District[];
  selectedStateId: string;
  selectedDistrictId: string;
  loadingStates: boolean;
  loadingDistricts: boolean;
  onSelectState: (stateId: string) => void;
  onSelectDistrict: (districtId: string) => void;
}

export const GeographySelector: React.FC<GeographySelectorProps> = ({
  states,
  districts,
  selectedStateId,
  selectedDistrictId,
  loadingStates,
  loadingDistricts,
  onSelectState,
  onSelectDistrict,
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
          State (Context Scope)
        </label>
        <select
          id="state-select"
          value={selectedStateId}
          onChange={(e) => onSelectState(e.target.value)}
          disabled={loadingStates}
          className="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl shadow-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900 dark:text-gray-100 transition duration-150"
        >
          <option value="" disabled>
            {loadingStates ? 'Loading states...' : '-- Select State --'}
          </option>
          {states.map((s) => (
            <option key={s.stateId} value={s.stateId}>
              {s.stateName}
            </option>
          ))}
        </select>
        <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Search is coordinate-based and can cross state borders.
        </p>
      </div>

      <div>
        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
          District
        </label>
        <select
          id="district-select"
          value={selectedDistrictId}
          onChange={(e) => onSelectDistrict(e.target.value)}
          disabled={!selectedStateId || loadingDistricts}
          className="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl shadow-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900 dark:text-gray-100 transition duration-150 disabled:opacity-50"
        >
          <option value="" disabled>
            {!selectedStateId
              ? '-- Select State First --'
              : loadingDistricts
              ? 'Loading districts...'
              : '-- Select District --'}
          </option>
          {districts.map((d) => (
            <option key={d.districtId} value={d.districtId}>
              {d.districtName}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};
