/**
 * MandiLocationRadarMap Component: Visual Location & Mandi Regional Map.
 * SSOT & Wireframe Reference: "Map that shows current location to Mandis in 100km and highlights
 * the Mandi region by colour which gives best -> worst profit (Blue are mandis, green is best mandi)".
 */
import React, { useState } from 'react';
import type { CandidateMandi, FarmerContext } from '../types';
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
  const [selectedMandiId, setSelectedMandiId] = useState<string | null>(null);

  const radiusKm = farmerContext.radiusKm || 100;
  const farmerLat = farmerContext.latitude;
  const farmerLng = farmerContext.longitude;

  // SVG viewport dimensions
  const svgSize = 340;
  const center = svgSize / 2;
  const maxPixelRadius = center - 36; // leave margin for labels

  // Project lat/lng offset to polar X, Y on the map
  const projectMandi = (mLat: number, mLng: number, distKm: number) => {
    // Relative km offset in lat/lng (~111km per degree latitude)
    const dLat = (mLat - farmerLat) * 111.0;
    const dLng = (mLng - farmerLng) * 111.0 * Math.cos((farmerLat * Math.PI) / 180);

    // Scale distance relative to radiusKm
    const effectiveDist = Math.min(distKm, radiusKm * 1.05);
    const r = (effectiveDist / Math.max(radiusKm, 1)) * maxPixelRadius;
    const angle = Math.atan2(dLat, dLng); // trigonometric angle

    // SVG coordinates (X increases right, Y increases down, so invert dLat)
    const x = center + r * Math.cos(angle);
    const y = center - r * Math.sin(angle);

    return { x, y, r };
  };

  const selectedCandidate = candidates.find((c) => c.mandi.mandiId === selectedMandiId) || null;

  return (
    <div className="bg-white dark:bg-[#151c24] border border-earth-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm space-y-3">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center gap-2">
          <Compass className="w-5 h-5 text-agri-600 dark:text-agri-400" />
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white font-heading">
              Market Discovery Radar Map
            </h3>
            <p className="text-[11px] text-slate-400">
              Showing candidate mandis within {radiusKm} km radius of your location.
            </p>
          </div>
        </div>

        <span className="text-xs font-bold px-2 py-0.5 rounded-lg bg-earth-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
          {candidates.length} Markets
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

          {/* Concentric Range Rings */}
          {[0.33, 0.66, 1.0].map((fraction, idx) => {
            const r = maxPixelRadius * fraction;
            const km = Math.round(radiusKm * fraction);
            return (
              <g key={idx}>
                <circle
                  cx={center}
                  cy={center}
                  r={r}
                  fill="none"
                  stroke="currentColor"
                  className={fraction === 1.0 ? 'text-emerald-300/70 dark:text-emerald-800/70' : 'text-slate-200 dark:text-slate-800'}
                  strokeWidth={fraction === 1.0 ? 1.5 : 1}
                  strokeDasharray={fraction === 1.0 ? 'none' : '4 4'}
                />
                <text
                  x={center + 4}
                  y={center - r + 11}
                  className="text-[9px] fill-slate-400 font-mono"
                >
                  {km}km
                </text>
              </g>
            );
          })}

          {/* Dotted Route Lines to Mandis */}
          {candidates.map((c) => {
            const { x, y } = projectMandi(c.mandi.latitude, c.mandi.longitude, c.distanceKm);
            const isRec = c.mandi.mandiId === recommendedMandiId || c.rank === 1;

            return (
              <line
                key={`line-${c.mandi.mandiId}`}
                x1={center}
                y1={center}
                x2={x}
                y2={y}
                stroke={isRec ? '#059669' : '#94a3b8'}
                strokeWidth={isRec ? 2 : 1}
                strokeDasharray={isRec ? 'none' : '2 3'}
                strokeOpacity={isRec ? 0.8 : 0.4}
              />
            );
          })}

          {/* Center: Farmer Location */}
          <g>
            <circle
              cx={center}
              cy={center}
              r={16}
              className="fill-emerald-500/20 animate-ping origin-center"
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
              className="text-[10px] font-bold fill-slate-800 dark:fill-slate-200"
            >
              Your Farm
            </text>
          </g>

          {/* Mandi Markers */}
          {candidates.map((c) => {
            const { x, y } = projectMandi(c.mandi.latitude, c.mandi.longitude, c.distanceKm);
            const isRec = c.mandi.mandiId === recommendedMandiId || c.rank === 1;
            const isSelected = c.mandi.mandiId === selectedMandiId;

            return (
              <g
                key={`mandi-${c.mandi.mandiId}`}
                className="cursor-pointer group"
                onClick={() => setSelectedMandiId(c.mandi.mandiId === selectedMandiId ? null : c.mandi.mandiId)}
              >
                {/* Glow ring for recommended */}
                {isRec && (
                  <circle
                    cx={x}
                    cy={y}
                    r={14}
                    className="fill-emerald-500/30 animate-pulse"
                  />
                )}

                {/* Mandi Node */}
                <circle
                  cx={x}
                  cy={y}
                  r={isRec ? 9 : 6.5}
                  fill={isRec ? '#059669' : isSelected ? '#2563eb' : '#3b82f6'}
                  stroke="#ffffff"
                  strokeWidth={2}
                  className="transition-transform group-hover:scale-125"
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

                {/* Name Label */}
                <text
                  x={x}
                  y={y - 12}
                  textAnchor="middle"
                  className={`text-[9px] font-bold select-none pointer-events-none ${
                    isRec
                      ? 'fill-emerald-700 dark:fill-emerald-300 font-extrabold'
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
          <div className="flex items-center gap-1 text-emerald-700 dark:text-emerald-400">
            <span className="w-2 h-2 rounded-full bg-emerald-600 inline-block" />
            <span>Best Market (#1)</span>
          </div>
          <div className="flex items-center gap-1 text-blue-700 dark:text-blue-400">
            <span className="w-2 h-2 rounded-full bg-blue-600 inline-block" />
            <span>Candidate APMC</span>
          </div>
        </div>
      </div>

      {/* Selected Mandi Quick Tooltip */}
      {selectedCandidate && (
        <div className="p-3 bg-earth-50 dark:bg-slate-900 rounded-2xl border border-earth-200 dark:border-slate-800 text-xs flex items-center justify-between">
          <div>
            <span className="font-bold text-slate-900 dark:text-white block font-heading">
              #{selectedCandidate.rank} {selectedCandidate.mandi.mandiName}
            </span>
            <span className="text-[11px] text-slate-500 dark:text-slate-400">
              {selectedCandidate.distanceKm} km • Predicted ₹{selectedCandidate.currentPrice}/q
            </span>
          </div>

          <div className="text-right">
            <span className="text-[10px] text-slate-400 uppercase block font-bold">Net Return</span>
            <span className="font-extrabold text-agri-700 dark:text-agri-400 font-heading">
              ₹{selectedCandidate.riskAdjustedReturn.toLocaleString('en-IN')}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
