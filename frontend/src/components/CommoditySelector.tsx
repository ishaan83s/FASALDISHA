/**
 * CommoditySelector Component: Displays commodities with category and perishability badges.
 * SSOT Reference: 02_DATA_AND_ML_SSOT.md Section 4, 06_FRONTEND_CONTRACT.md, 13_JUDGE_PROOF_AND_P0_ACCEPTANCE.md
 */
import React from 'react';
import type { Commodity, PerishabilityClass } from '../types';
import { Leaf, Clock, AlertTriangle } from 'lucide-react';

interface CommoditySelectorProps {
  commodities: Commodity[];
  selectedCommodityId: string;
  loading: boolean;
  onSelectCommodity: (commodityId: string) => void;
}

export const CommoditySelector: React.FC<CommoditySelectorProps> = ({
  commodities,
  selectedCommodityId,
  loading,
  onSelectCommodity,
}) => {
  const getPerishabilityBadge = (pClass: PerishabilityClass) => {
    switch (pClass) {
      case 'HIGHLY_PERISHABLE':
        return {
          label: 'Highly Perishable',
          color: 'bg-rose-100 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border-rose-200 dark:border-rose-800',
          icon: <AlertTriangle className="w-3 h-3 text-rose-600 dark:text-rose-400" />,
          desc: '1-3 day holding limit; high spoilage risk',
        };
      case 'MODERATELY_PERISHABLE':
        return {
          label: 'Moderately Perishable',
          color: 'bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border-amber-200 dark:border-amber-800',
          icon: <Clock className="w-3 h-3 text-amber-600 dark:text-amber-400" />,
          desc: '1-2 week storage with proper ventilation',
        };
      case 'NON_PERISHABLE':
        return {
          label: 'Non-Perishable / Durable',
          color: 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800',
          icon: <Leaf className="w-3 h-3 text-emerald-600 dark:text-emerald-400" />,
          desc: 'Extended holding allowed for peak price capture',
        };
      default:
        return {
          label: 'Standard',
          color: 'bg-gray-100 text-gray-800',
          icon: null,
          desc: '',
        };
    }
  };

  const selectedCommodity = commodities.find((c) => c.commodityId === selectedCommodityId);

  return (
    <div className="space-y-3">
      <div>
        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">
          Commodity
        </label>
        <select
          id="commodity-select"
          value={selectedCommodityId}
          onChange={(e) => onSelectCommodity(e.target.value)}
          disabled={loading}
          className="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl shadow-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900 dark:text-gray-100 transition duration-150"
        >
          <option value="" disabled>
            {loading ? 'Loading catalog...' : '-- Select Commodity --'}
          </option>
          {commodities.map((c) => (
            <option key={c.commodityId} value={c.commodityId}>
              {c.commodityName} ({c.commodityCategory}) — {c.perishabilityClass.replace('_', ' ')}
            </option>
          ))}
        </select>
      </div>

      {selectedCommodity && (
        <div className="p-3 bg-gray-50 dark:bg-gray-800/60 border border-gray-200 dark:border-gray-700 rounded-xl flex items-start gap-3">
          <div className="mt-0.5">
            {getPerishabilityBadge(selectedCommodity.perishabilityClass).icon}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-0.5">
              <span className="text-xs font-bold text-gray-900 dark:text-gray-100">
                {selectedCommodity.commodityName} ({selectedCommodity.commodityCategory})
              </span>
              <span
                className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${
                  getPerishabilityBadge(selectedCommodity.perishabilityClass).color
                }`}
              >
                {getPerishabilityBadge(selectedCommodity.perishabilityClass).label}
              </span>
            </div>
            <p className="text-xs text-gray-600 dark:text-gray-400">
              {getPerishabilityBadge(selectedCommodity.perishabilityClass).desc}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
