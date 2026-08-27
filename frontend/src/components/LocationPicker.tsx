/**
 * LocationPicker Component: Handles authoritative coordinates, GPS geolocation, and judge demo presets.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 1 & 2
 */
import React, { useState } from 'react';
import { Navigation, Sparkles, MapPin, CheckCircle2, AlertTriangle } from 'lucide-react';
import type { CanonicalLocation, ResolvedLocation } from '../types';
import { apiClient } from '../api/client';

interface LocationPickerProps {
  location: CanonicalLocation;
  onCoordinatesChange: (lat: number, lon: number) => void;
  onGpsStart: () => number;
  onGpsResolved: (resolved: ResolvedLocation, versionToken: number) => void;
  onApplyDemoPreset: (preset: {
    name: string;
    stateId: string;
    districtId: string;
    lat: number;
    lon: number;
    commodityId: string;
    quantityQuintals: number;
    radiusKm: number;
  }) => void;
}

interface ExamplePreset {
  id: string;
  name: string;
  title: string;
  description: string;
  stateId: string;
  districtId: string;
  lat: number;
  lon: number;
  commodityId: string;
  quantityQuintals: number;
  radiusKm: number;
  badge: string;
}

const EXAMPLE_PRESETS: ExamplePreset[] = [
  {
    id: 'pune-onion',
    name: 'Scenario A: Pune Onion (Weather Risk Override)',
    title: 'Scenario A: Pune Onion',
    description: 'Weather risk override demonstration',
    stateId: 'maharashtra',
    districtId: 'pune',
    lat: 18.52,
    lon: 73.85,
    commodityId: 'onion',
    quantityQuintals: 25,
    radiusKm: 120,
    badge: 'Risk Override',
  },
  {
    id: 'nashik-tomato',
    name: 'Scenario B: Tomato (Perishable vs Non-Perishable Urgency)',
    title: 'Scenario B: Nashik Tomato',
    description: 'Perishable vs non-perishable urgency',
    stateId: 'maharashtra',
    districtId: 'nashik',
    lat: 20.00,
    lon: 73.78,
    commodityId: 'tomato',
    quantityQuintals: 15,
    radiusKm: 100,
    badge: 'High Perishability',
  },
  {
    id: 'kota-wheat',
    name: 'Scenario C: Wheat (Non-Perishable Normal Hold)',
    title: 'Scenario C: Kota Wheat',
    description: 'Non-perishable standard hold analysis',
    stateId: 'rajasthan',
    districtId: 'kota',
    lat: 25.18,
    lon: 75.83,
    commodityId: 'wheat',
    quantityQuintals: 50,
    radiusKm: 100,
    badge: 'Standard Hold',
  },
  {
    id: 'ahmedabad-cotton',
    name: 'Scenario D: Ahmedabad (Multi-Mandi & Cross-Boundary)',
    title: 'Scenario D: Ahmedabad Cotton',
    description: 'Multi-mandi & cross-boundary discovery',
    stateId: 'gujarat',
    districtId: 'ahmedabad',
    lat: 23.02,
    lon: 72.57,
    commodityId: 'cotton',
    quantityQuintals: 30,
    radiusKm: 150,
    badge: 'Cross-Boundary',
  },
];

export const LocationPicker: React.FC<LocationPickerProps> = ({
  location,
  onCoordinatesChange,
  onGpsStart,
  onGpsResolved,
  onApplyDemoPreset,
}) => {
  const [geoError, setGeoError] = useState<string | null>(null);
  const [geoNotice, setGeoNotice] = useState<string | null>(null);
  const [isLocating, setIsLocating] = useState<boolean>(false);
  const [selectedPresetId, setSelectedPresetId] = useState<string | null>(null);
  const activeGpsReqRef = React.useRef<number>(0);

  const handleUseGeolocation = () => {
    setSelectedPresetId(null);
    if (!navigator.geolocation) {
      setGeoError('Geolocation is not supported by your browser.');
      setGeoNotice(null);
      return;
    }

    const versionToken = onGpsStart();
    const reqId = ++activeGpsReqRef.current;

    setIsLocating(true);
    setGeoError(null);
    setGeoNotice(null);

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        if (reqId !== activeGpsReqRef.current) return;
        const lat = parseFloat(position.coords.latitude.toFixed(4));
        const lon = parseFloat(position.coords.longitude.toFixed(4));

        try {
          const resolved = await apiClient.resolveLocation(lat, lon);
          if (reqId !== activeGpsReqRef.current) return;

          if (resolved.inSupportedRegion && resolved.districtId && resolved.stateId) {
            onGpsResolved(resolved, versionToken);
            setGeoNotice(
              `GPS location matched to ${resolved.districtName}, ${resolved.stateName} (~${resolved.distanceKm?.toFixed(1) || 0} km from district reference centroid).`
            );
            setGeoError(null);
          } else {
            setGeoError(
              `GPS coordinates (${lat}°N, ${lon}°E) are outside supported coverage regions (Maharashtra, Gujarat, Rajasthan). Retaining your manual selection.`
            );
            setGeoNotice(null);
          }
        } catch {
          if (reqId !== activeGpsReqRef.current) return;
          setGeoError(
            `Unable to verify GPS location against geography catalog. Retaining manual location selection.`
          );
          setGeoNotice(null);
        } finally {
          if (reqId === activeGpsReqRef.current) {
            setIsLocating(false);
          }
        }
      },
      (error) => {
        if (reqId !== activeGpsReqRef.current) return;
        setIsLocating(false);
        setGeoError(
          `Location access denied or unavailable (${error.message}). Retaining manual location.`
        );
        setGeoNotice(null);
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  };

  const handlePresetSelect = (preset: ExamplePreset) => {
    setSelectedPresetId(preset.id);
    onApplyDemoPreset(preset);
  };

  const handleCoordinatesInputChange = (lat: number, lon: number) => {
    setSelectedPresetId(null);
    onCoordinatesChange(lat, lon);
  };

  const getSourceBadge = () => {
    if (location.source === 'GPS') {
      return (
        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-700 dark:text-emerald-300 bg-emerald-100/80 dark:bg-emerald-950/80 px-2 py-0.5 rounded-lg border border-emerald-200 dark:border-emerald-800">
          <CheckCircle2 className="w-3 h-3 text-emerald-600" />
          <span>GPS Geolocation</span>
        </span>
      );
    }
    if (location.source === 'PRESET') {
      return (
        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-amber-700 dark:text-amber-300 bg-amber-100/80 dark:bg-amber-950/80 px-2 py-0.5 rounded-lg border border-amber-200 dark:border-amber-800">
          <Sparkles className="w-3 h-3 text-amber-600" />
          <span>Example Scenario</span>
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded-lg border border-slate-200 dark:border-slate-700">
        <MapPin className="w-3 h-3 text-slate-500" />
        <span>Manual Selection</span>
      </span>
    );
  };

  const selectedPreset = EXAMPLE_PRESETS.find((p) => p.id === selectedPresetId);

  return (
    <div className="space-y-4">
      {/* Geolocation Button */}
      <div className="flex items-center justify-between">
        <label className="block text-xs font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
          Authority Location Coordinates
        </label>
        <div className="flex items-center gap-2">
          {getSourceBadge()}
          <button
            type="button"
            onClick={handleUseGeolocation}
            disabled={isLocating}
            className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-400 text-white rounded-lg text-xs font-semibold shadow-xs transition duration-150 cursor-pointer"
          >
            <Navigation className={`w-3.5 h-3.5 ${isLocating ? 'animate-spin' : ''}`} />
            <span>{isLocating ? 'Acquiring GPS...' : 'Use Device GPS'}</span>
          </button>
        </div>
      </div>

      {/* Coordinate Display Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div>
          <label className="block text-xs font-semibold text-gray-600 dark:text-gray-400 mb-1">
            Latitude (°N)
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
              <span className="text-xs font-mono text-gray-400">LAT</span>
            </div>
            <input
              type="number"
              step="0.0001"
              value={location.latitude}
              onChange={(e) => handleCoordinatesInputChange(parseFloat(e.target.value) || 0, location.longitude)}
              className="w-full pl-12 pr-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl shadow-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900 dark:text-gray-100 text-sm font-mono"
              placeholder="e.g. 18.5200"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-gray-600 dark:text-gray-400 mb-1">
            Longitude (°E)
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
              <span className="text-xs font-mono text-gray-400">LON</span>
            </div>
            <input
              type="number"
              step="0.0001"
              value={location.longitude}
              onChange={(e) => handleCoordinatesInputChange(location.latitude, parseFloat(e.target.value) || 0)}
              className="w-full pl-12 pr-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl shadow-sm focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900 dark:text-gray-100 text-sm font-mono"
              placeholder="e.g. 73.8500"
              required
            />
          </div>
        </div>
      </div>

      {location.source === 'GPS' && geoNotice && (
        <div className="p-2.5 text-xs text-emerald-800 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-900 rounded-xl flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          <span>{geoNotice}</span>
        </div>
      )}

      {geoError && (
        <div className="p-2.5 text-xs text-amber-800 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900 rounded-xl flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span>{geoError}</span>
        </div>
      )}

      {/* Example Scenarios */}
      <div className="pt-2 border-t border-gray-100 dark:border-gray-800">
        <div className="flex items-center gap-1.5 mb-2">
          <Sparkles className="w-3.5 h-3.5 text-amber-500" />
          <span className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
            Try an Example Scenario
          </span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {EXAMPLE_PRESETS.map((preset) => {
            const isSelected = selectedPresetId === preset.id;
            return (
              <button
                key={preset.id}
                type="button"
                onClick={() => handlePresetSelect(preset)}
                className={`text-left p-2.5 rounded-xl transition duration-150 group cursor-pointer ${
                  isSelected
                    ? 'bg-emerald-50/90 dark:bg-emerald-950/60 border-2 border-emerald-500 dark:border-emerald-400 ring-2 ring-emerald-500/20 dark:ring-emerald-400/20 shadow-xs'
                    : 'bg-gray-50 dark:bg-gray-800/60 hover:bg-emerald-50/40 dark:hover:bg-emerald-950/20 border border-gray-200 dark:border-gray-700 hover:border-emerald-300 dark:hover:border-emerald-700'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span
                    className={`text-xs font-semibold ${
                      isSelected
                        ? 'text-emerald-900 dark:text-emerald-200 font-bold'
                        : 'text-gray-800 dark:text-gray-200 group-hover:text-emerald-700 dark:group-hover:text-emerald-300'
                    }`}
                  >
                    {preset.title}
                  </span>
                  <div className="flex items-center gap-1">
                    {isSelected && (
                      <span className="text-[10px] px-1.5 py-0.5 font-bold rounded-full bg-emerald-600 text-white flex items-center gap-0.5">
                        ✓ Selected
                      </span>
                    )}
                    <span
                      className={`text-[10px] px-1.5 py-0.5 font-medium rounded-full ${
                        isSelected
                          ? 'bg-emerald-200/80 dark:bg-emerald-900/80 text-emerald-900 dark:text-emerald-200'
                          : 'bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200'
                      }`}
                    >
                      {preset.badge}
                    </span>
                  </div>
                </div>
                <p
                  className={`text-[11px] line-clamp-1 ${
                    isSelected
                      ? 'text-emerald-700 dark:text-emerald-300 font-medium'
                      : 'text-gray-500 dark:text-gray-400'
                  }`}
                >
                  {preset.description}
                </p>
              </button>
            );
          })}
        </div>

        {/* Confirmation feedback */}
        {selectedPreset && (
          <div className="mt-2.5 p-2 bg-emerald-50/80 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 rounded-lg text-xs font-semibold text-emerald-800 dark:text-emerald-300 flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 flex-shrink-0" />
              <span>Loaded: <strong>{selectedPreset.title}</strong> — {selectedPreset.description}</span>
            </div>
            <span className="text-[10px] uppercase tracking-wider font-mono text-emerald-600 dark:text-emerald-400 hidden sm:inline">
              Ready
            </span>
          </div>
        )}
      </div>
    </div>
  );
};
