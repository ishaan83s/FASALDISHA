/**
 * MandiLocationRadarMap Component: Visual Location & Mandi Regional Map.
 * SSOT & Wireframe Reference: "Map that shows current location to Mandis in search radius and highlights
 * the Mandi region by colour which gives best -> worst profit (Blue are mandis, green is best mandi)".
 */
import React, { useState } from 'react';
import type { CandidateMandi, FarmerContext } from '../types';
import { useLanguage } from '../i18n';
import { Compass } from 'lucide-react';

interface MandiLocationRadarMapProps {
  farmerContext: FarmerContext;
  candidates: CandidateMandi[];
  recommendedMandiId?: string;
}

export const MandiLocationRadarMap: React.FC<MandiLocationRadarMapProps> = ({
  farmerContext,
  candidates,
  recommendedMandiId,
}) => {
  const { t } = useLanguage();
  const [selectedMandiId, setSelectedMandiId] = useState<string | null>(null);

  const radiusKm = farmerContext.radiusKm || 100;
  const farmerLat = Number(farmerContext.latitude) || 18.5204;
  const farmerLng = Number(farmerContext.longitude) || 73.8567;

  // SVG viewport dimensions
  const svgSize = 340;
  const center = svgSize / 2;
  const maxPixelRadius = center - 36; // leave margin for labels

  // Dynamic distance ring definitions (1/3, 2/3, 1.0 of radiusKm)
  const distanceRings = [
    { fraction: 0.333, km: Math.round(radiusKm / 3) },
    { fraction: 0.666, km: Math.round((radiusKm * 2) / 3) },
    { fraction: 1.0, km: Math.round(radiusKm) },
  ];

  // Project lat/lng offset to polar X, Y on the map
  const projectMandi = (mLat?: number, mLng?: number, distKm?: number) => {
    if (mLat == null || mLng == null || isNaN(mLat) || isNaN(mLng)) {
      return null;
    }
    const safeDist = distKm != null && !isNaN(distKm) ? distKm : 10;
    // Relative km offset in lat/lng (~111km per degree latitude)
    const dLat = (mLat - farmerLat) * 111.0;
    const dLng = (mLng - farmerLng) * 111.0 * Math.cos((farmerLat * Math.PI) / 180);

    // Scale distance relative to radiusKm
    const effectiveDist = Math.min(safeDist, radiusKm * 1.05);
    const r = (effectiveDist / Math.max(radiusKm, 1)) * maxPixelRadius;
    const angle = Math.atan2(dLat, dLng); // trigonometric angle

    // SVG coordinates (X increases right, Y increases down, so invert dLat)
    const x = center + r * Math.cos(angle);
    const y = center - r * Math.sin(angle);

    return { x, y, r };
  };

  const recommendedCandidate =
    candidates.find((c) => c.mandi.mandiId === recommendedMandiId || c.rank === 1) || candidates[0] || null;

  const selectedCandidate = candidates.find((c) => c.mandi.mandiId === selectedMandiId) || null;
  const activeCandidate = selectedCandidate || recommendedCandidate;

  return (
    <div className="bg-white dark:bg-[#151c24] border border-earth-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center gap-2">
          <Compass className="w-5 h-5 text-agri-600 dark:text-agri-400" />
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white font-heading">
              {t('radar.title')}
            </h3>
            <p className="text-[11px] text-slate-400">
              {t('radar.subtitle', { radius: radiusKm })}
            </p>
          </div>
        </div>

        <span className="text-xs font-bold px-2 py-0.5 rounded-lg bg-earth-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
          {t('radar.marketsCount', { count: candidates.length })}
        </span>
      </div>

      {/* Interactive Map Visual Area */}
      <div className="relative w-full aspect-square max-w-[340px] mx-auto bg-earth-50/60 dark:bg-slate-950/70 rounded-2xl border border-earth-200 dark:border-slate-800 overflow-hidden flex items-center justify-center p-2">
        <svg
          viewBox={`0 0 ${svgSize} ${svgSize}`}
          className="w-full h-full select-none"
        >
          {/* Compass grid lines */}
          <line
            x1={center}
            y1={16}
            x2={center}
            y2={svgSize - 16}
            stroke="currentColor"
            className="text-slate-200 dark:text-slate-800"
            strokeDasharray="3 3"
          />
          <line
            x1={16}
            y1={center}
            x2={svgSize - 16}
            y2={center}
            stroke="currentColor"
            className="text-slate-200 dark:text-slate-800"
            strokeDasharray="3 3"
          />

          {/* Dynamic Concentric Distance Rings */}
          {distanceRings.map((ring) => {
            const r = maxPixelRadius * ring.fraction;
            return (
              <g key={`ring-${ring.km}`}>
                <circle
                  cx={center}
                  cy={center}
                  r={r}
                  fill="none"
                  stroke="currentColor"
                  className={ring.fraction === 1.0 ? 'text-emerald-400/80 dark:text-emerald-700/80' : 'text-slate-200 dark:text-slate-800'}
                  strokeWidth={ring.fraction === 1.0 ? 1.5 : 1}
                  strokeDasharray={ring.fraction === 1.0 ? 'none' : '4 4'}
                />
                <text
                  x={center + 4}
                  y={center - r + 11}
                  className="text-[9px] fill-slate-400 font-mono select-none pointer-events-none"
                >
                  {ring.km} km
                </text>
              </g>
            );
          })}

          {/* Subtle Radar Sweep (isolated decorative layer) */}
          <g
            className="animate-[spin_10s_linear_infinite] pointer-events-none"
            style={{ transformOrigin: `${center}px ${center}px` }}
          >
            <defs>
              <linearGradient id="radarSweepGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#10b981" stopOpacity="0.14" />
                <stop offset="100%" stopColor="#10b981" stopOpacity="0.0" />
              </linearGradient>
            </defs>
            <path
              d={`M ${center} ${center} L ${center + maxPixelRadius} ${center} A ${maxPixelRadius} ${maxPixelRadius} 0 0 1 ${center + maxPixelRadius * 0.707} ${center + maxPixelRadius * 0.707} Z`}
              fill="url(#radarSweepGradient)"
            />
            <line
              x1={center}
              y1={center}
              x2={center + maxPixelRadius}
              y2={center}
              stroke="#10b981"
              strokeWidth={1}
              strokeOpacity={0.35}
            />
          </g>

          {/* Geographic Straight-Line Route Connectors from Origin to Mandis */}
          {candidates.map((c) => {
            const proj = projectMandi(c.mandi.latitude, c.mandi.longitude, c.distanceKm);
            if (!proj) return null;
            const { x, y } = proj;
            const isRec = c.mandi.mandiId === recommendedMandiId || c.rank === 1;
            const isSelected = c.mandi.mandiId === selectedMandiId;

            return (
              <g key={`route-${c.mandi.mandiId}`}>
                {/* Glow aura for recommended route */}
                {isRec && (
                  <line
                    x1={center}
                    y1={center}
                    x2={x}
                    y2={y}
                    stroke="#10b981"
                    strokeWidth={5}
                    strokeOpacity={0.25}
                    strokeLinecap="round"
                  />
                )}
                <line
                  x1={center}
                  y1={center}
                  x2={x}
                  y2={y}
                  stroke={isRec ? '#059669' : isSelected ? '#2563eb' : '#64748b'}
                  strokeWidth={isRec ? 2.5 : isSelected ? 2 : 1.2}
                  strokeDasharray={isRec ? 'none' : isSelected ? '4 2' : '3 3'}
                  strokeOpacity={isRec ? 0.95 : isSelected ? 0.8 : 0.45}
                  strokeLinecap="round"
                />
              </g>
            );
          })}

          {/* Center: Farmer Location */}
          <g key="farmer-origin">
            <circle
              cx={center}
              cy={center}
              r={14}
              fill="#10b981"
              fillOpacity={0.18}
            />
            <circle
              cx={center}
              cy={center}
              r={8}
              className="fill-emerald-600 dark:fill-emerald-400 stroke-white dark:stroke-slate-900"
              strokeWidth={2}
            />
            <text
              x={center}
              y={center + 18}
              textAnchor="middle"
              className="text-[10px] font-bold fill-slate-800 dark:fill-slate-200 select-none pointer-events-none"
            >
              {t('radar.yourFarm')}
            </text>
          </g>

          {/* Mandi Markers */}
          {candidates.map((c) => {
            const proj = projectMandi(c.mandi.latitude, c.mandi.longitude, c.distanceKm);
            if (!proj) return null;
            const { x, y } = proj;
            const isRec = c.mandi.mandiId === recommendedMandiId || c.rank === 1;
            const isSelected = c.mandi.mandiId === selectedMandiId;

            return (
              <g
                key={`mandi-${c.mandi.mandiId}`}
                className="cursor-pointer"
                onClick={() => setSelectedMandiId(c.mandi.mandiId === selectedMandiId ? null : c.mandi.mandiId)}
              >
                {/* Spotlight aura for recommended mandi */}
                {isRec && (
                  <>
                    <circle
                      cx={x}
                      cy={y}
                      r={15}
                      fill="#10b981"
                      className="animate-[pulse_3s_ease-in-out_infinite]"
                      fillOpacity={0.22}
                    />
                    <circle
                      cx={x}
                      cy={y}
                      r={21}
                      fill="none"
                      stroke="#10b981"
                      strokeWidth={1}
                      strokeDasharray="2 2"
                      strokeOpacity={0.4}
                    />
                  </>
                )}

                {/* Mandi Node */}
                <circle
                  cx={x}
                  cy={y}
                  r={isRec ? 9 : isSelected ? 8 : 6.5}
                  fill={isRec ? '#059669' : isSelected ? '#2563eb' : '#3b82f6'}
                  stroke="#ffffff"
                  strokeWidth={2}
                />

                {/* Rank number inside node */}
                <text
                  x={x}
                  y={y + 3}
                  textAnchor="middle"
                  className="text-[8px] font-extrabold fill-white select-none pointer-events-none"
                >
                  {c.rank}
                </text>

                {/* Spotlight Badge for Recommended Market */}
                {isRec && (
                  <g className="pointer-events-none select-none">
                    <rect
                      x={x - 44}
                      y={y - 32}
                      width={88}
                      height={16}
                      rx={4}
                      fill="#065f46"
                      fillOpacity={0.92}
                      stroke="#10b981"
                      strokeWidth={0.75}
                    />
                    <text
                      x={x}
                      y={y - 21}
                      textAnchor="middle"
                      className="text-[7.5px] font-black fill-emerald-100 font-mono tracking-wider"
                    >
                      {t('radar.bestBadge', { amount: Math.round(c.riskAdjustedReturn).toLocaleString('en-IN') })}
                    </text>
                  </g>
                )}

                {/* Mandi Name Label */}
                <text
                  x={x}
                  y={y + 17}
                  textAnchor="middle"
                  className={`text-[9px] font-bold select-none pointer-events-none ${
                    isRec
                      ? 'fill-emerald-800 dark:fill-emerald-300 font-extrabold'
                      : 'fill-slate-700 dark:fill-slate-300'
                  }`}
                >
                  {c.mandi.mandiName.replace(/APMC /i, '')}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Legend Overlay at Bottom Right */}
        <div className="absolute bottom-2 right-2 bg-white/90 dark:bg-slate-900/90 backdrop-blur-xs border border-earth-200 dark:border-slate-800 rounded-xl p-1.5 text-[9px] font-semibold space-y-1 shadow-2xs">
          <div className="flex items-center gap-1.5 text-emerald-700 dark:text-emerald-400">
            <span className="w-2.5 h-0.5 bg-emerald-600 rounded-full inline-block" />
            <span>{t('radar.recommendedRouteLegend')}</span>
          </div>
          <div className="flex items-center gap-1.5 text-slate-500 dark:text-slate-400">
            <span className="w-2.5 h-0.5 bg-slate-400 border-t border-dashed border-slate-500 inline-block" />
            <span>{t('radar.candidateRoutesLegend')}</span>
          </div>
        </div>
      </div>

      {/* Vector disclaimer footnote */}
      <p className="text-[10px] text-slate-400 dark:text-slate-500 text-center italic">
        {t('radar.disclaimer')}
      </p>

      {/* Economic Selection Callout (Level 4: Market Price -> Transport -> Net Return) */}
      {activeCandidate && (
        <div className="p-3.5 bg-earth-50/80 dark:bg-slate-900/90 rounded-2xl border border-earth-200 dark:border-slate-800 space-y-2.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <span
                className={`px-1.5 py-0.5 rounded text-[10px] font-bold font-mono ${
                  activeCandidate.rank === 1
                    ? 'bg-emerald-600 text-white'
                    : 'bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300'
                }`}
              >
                #{activeCandidate.rank}
              </span>
              <span className="font-bold text-slate-900 dark:text-white text-xs font-heading">
                {activeCandidate.mandi.mandiName}
              </span>
              {activeCandidate.rank === 1 && (
                <span className="text-[9px] font-extrabold px-1.5 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
                  {t('radar.topRecommendationBadge')}
                </span>
              )}
            </div>
            <span className="text-[11px] font-semibold text-slate-500 dark:text-slate-400 font-mono">
              {t('radar.kmAway', { distance: activeCandidate.distanceKm })}
            </span>
          </div>

          {/* 3-Step Economic Reasoning Hierarchy */}
          <div className="grid grid-cols-3 gap-2 text-center pt-1 border-t border-earth-200/60 dark:border-slate-800">
            <div className="p-1.5 bg-white dark:bg-slate-800/80 rounded-xl border border-earth-100 dark:border-slate-700/60">
              <span className="text-[9px] uppercase font-bold text-slate-400 block">
                {t('radar.marketPrice')}
              </span>
              <span className="text-xs font-bold text-slate-800 dark:text-slate-200 font-heading">
                ₹{activeCandidate.currentPrice.toLocaleString('en-IN')}/q
              </span>
            </div>

            <div className="p-1.5 bg-white dark:bg-slate-800/80 rounded-xl border border-earth-100 dark:border-slate-700/60">
              <span className="text-[9px] uppercase font-bold text-slate-400 block">
                {t('radar.transitImpact')}
              </span>
              <span className="text-xs font-bold text-amber-700 dark:text-amber-400 font-heading">
                -₹{Math.round(activeCandidate.totalTransportCost).toLocaleString('en-IN')}
              </span>
            </div>

            <div className="p-1.5 bg-emerald-50/90 dark:bg-emerald-950/40 rounded-xl border border-emerald-200 dark:border-emerald-800/60">
              <span className="text-[9px] uppercase font-bold text-emerald-800 dark:text-emerald-300 block">
                {t('radar.netReturn')}
              </span>
              <span className="text-xs font-black text-emerald-900 dark:text-emerald-200 font-heading">
                ₹{Math.round(activeCandidate.riskAdjustedReturn).toLocaleString('en-IN')}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
