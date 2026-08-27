/**
 * MandiRankingList Component: List container for ranked candidate mandis.
 * SSOT & Wireframe Reference: "Mandis Ranked in range of 100km".
 */
import React from 'react';
import type { CandidateMandi } from '../types';
import { MandiRankingCard } from './MandiRankingCard';
import { useLanguage } from '../i18n';
import { Store, Globe } from 'lucide-react';

interface MandiRankingListProps {
  candidates: CandidateMandi[];
  recommendedMandiId?: string;
  radiusKm: number;
  isCrossBoundary?: boolean;
}

export const MandiRankingList: React.FC<MandiRankingListProps> = ({
  candidates,
  recommendedMandiId,
  radiusKm,
  isCrossBoundary,
}) => {
  const { t } = useLanguage();

  if (!candidates || candidates.length === 0) {
    return (
      <div className="p-8 text-center bg-white dark:bg-[#151c24] border border-earth-200 dark:border-slate-800 rounded-3xl">
        <Store className="w-8 h-8 text-slate-400 mx-auto mb-2" />
        <h3 className="text-base font-bold text-slate-700 dark:text-slate-300 font-heading">
          {t('rankings.emptyTitle', { radius: radiusKm })}
        </h3>
        <p className="text-xs text-slate-400 mt-1">
          {t('rankings.emptySubtitle')}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3.5">
      {/* Section Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-1">
        <div>
          <div className="flex items-center gap-2">
            <Store className="w-5 h-5 text-agri-600 dark:text-agri-400" />
            <h2 className="text-lg font-bold text-slate-900 dark:text-white font-heading">
              {t('rankings.sectionTitle', { count: candidates.length, radius: radiusKm })}
            </h2>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            {t('rankings.sectionSubtitle')}
          </p>
        </div>

        {isCrossBoundary && (
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-purple-50 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800 rounded-xl text-purple-800 dark:text-purple-300 text-xs font-semibold">
            <Globe className="w-3.5 h-3.5 text-purple-600 dark:text-purple-400" />
            <span>{t('rankings.crossDistrictActive')}</span>
          </div>
        )}
      </div>

      {/* Cards List */}
      <div className="space-y-3">
        {candidates.map((candidate) => {
          const isRecommended =
            candidate.mandi.mandiId === recommendedMandiId || candidate.rank === 1;

          return (
            <MandiRankingCard
              key={candidate.mandi.mandiId}
              candidate={candidate}
              isRecommended={isRecommended}
            />
          );
        })}
      </div>
    </div>
  );
};
