/**
 * GeographySelector Component: Dynamic State and District cascading selector.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 1
 */
import React from 'react';
import type { State, District } from '../types';
import { useLanguage } from '../i18n';

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
  const { t, translateState, translateDistrict } = useLanguage();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
          {t('geography.stateLabel')}
        </label>
        <select
          id="state-select"
          value={selectedStateId}
          onChange={(e) => onSelectState(e.target.value)}
          disabled={loadingStates}
          className="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl shadow-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900 dark:text-gray-100 transition duration-150"
        >
          <option value="" disabled>
            {loadingStates ? t('geography.loadingStates') : t('geography.selectStatePrompt')}
          </option>
          {states.map((s) => (
            <option key={s.stateId} value={s.stateId}>
              {translateState(s.stateName)}
            </option>
          ))}
        </select>
        <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
          {t('geography.coordinateSearchNote')}
        </p>
      </div>

      <div>
        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
          {t('geography.districtLabel')}
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
              ? t('geography.selectStateFirst')
              : loadingDistricts
              ? t('geography.loadingDistricts')
              : t('geography.selectDistrictPrompt')}
          </option>
          {districts.map((d) => (
            <option key={d.districtId} value={d.districtId}>
              {translateDistrict(d.districtName)}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

