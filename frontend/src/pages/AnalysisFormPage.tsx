/**
 * AnalysisFormPage Component: Stitch-inspired Farmer Input & Scenario Selector.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md Section 1
 */
import React, { useState, useEffect } from 'react';
import type { State, District, Commodity, AnalysisRequest } from '../types';
import { apiClient } from '../api/client';
import { GeographySelector } from '../components/GeographySelector';
import { LocationPicker } from '../components/LocationPicker';
import { CommoditySelector } from '../components/CommoditySelector';
import {
  ArrowRight,
  AlertCircle,
  Sparkles,
  MapPin,
  Leaf,
  Truck,
  Compass,
} from 'lucide-react';

interface AnalysisFormPageProps {
  onAnalysisComplete: (result: any) => void;
}

const RADIUS_OPTIONS = [50, 100, 120, 150, 200];

export const AnalysisFormPage: React.FC<AnalysisFormPageProps> = ({
  onAnalysisComplete,
}) => {
  const [states, setStates] = useState<State[]>([]);
  const [districts, setDistricts] = useState<District[]>([]);
  const [commodities, setCommodities] = useState<Commodity[]>([]);

  const [selectedStateId, setSelectedStateId] = useState<string>('maharashtra');
  const [selectedDistrictId, setSelectedDistrictId] = useState<string>('pune');
  const [latitude, setLatitude] = useState<number>(18.52);
  const [longitude, setLongitude] = useState<number>(73.85);
  const [selectedCommodityId, setSelectedCommodityId] = useState<string>('onion');
  const [quantityQuintals, setQuantityQuintals] = useState<number>(25);
  const [radiusKm, setRadiusKm] = useState<number>(120);
  const [customTransportRate, setCustomTransportRate] = useState<string>('');

  const [loadingStates, setLoadingStates] = useState<boolean>(true);
  const [loadingDistricts, setLoadingDistricts] = useState<boolean>(false);
  const [loadingCommodities, setLoadingCommodities] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Load catalogs on mount
  useEffect(() => {
    async function initCatalog() {
      try {
        const [statesData, commoditiesData] = await Promise.all([
          apiClient.getStates(),
          apiClient.getCommodities(),
        ]);
        setStates(statesData);
        setCommodities(commoditiesData);
        setLoadingStates(false);
        setLoadingCommodities(false);

        const dists = await apiClient.getDistricts('maharashtra');
        setDistricts(dists);
      } catch (err: any) {
        setErrorMsg(`Failed to load catalogs: ${err.message}`);
        setLoadingStates(false);
        setLoadingCommodities(false);
      }
    }
    initCatalog();
  }, []);

  const handleSelectState = async (stateId: string) => {
    setSelectedStateId(stateId);
    setSelectedDistrictId('');
    setLoadingDistricts(true);
    try {
      const dists = await apiClient.getDistricts(stateId);
      setDistricts(dists);
      if (dists.length > 0) {
        setSelectedDistrictId(dists[0].districtId);
      }
    } catch (err: any) {
      setErrorMsg(`Failed to load districts: ${err.message}`);
    } finally {
      setLoadingDistricts(false);
    }
  };

  const handleApplyDemoPreset = async (preset: {
    stateId: string;
    districtId: string;
    lat: number;
    lon: number;
    commodityId: string;
    quantityQuintals: number;
    radiusKm: number;
  }) => {
    setSelectedStateId(preset.stateId);
    setLatitude(preset.lat);
    setLongitude(preset.lon);
    setSelectedCommodityId(preset.commodityId);
    setQuantityQuintals(preset.quantityQuintals);
    setRadiusKm(preset.radiusKm);

    try {
      const dists = await apiClient.getDistricts(preset.stateId);
      setDistricts(dists);
      setSelectedDistrictId(preset.districtId);
    } catch {
      // fallback
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedStateId || !selectedDistrictId || !selectedCommodityId) {
      setErrorMsg('Please select state, district, and commodity.');
      return;
    }
    if (quantityQuintals <= 0) {
      setErrorMsg('Quantity must be greater than 0 quintals.');
      return;
    }

    setSubmitting(true);
    setErrorMsg(null);

    const payload: AnalysisRequest = {
      stateId: selectedStateId,
      districtId: selectedDistrictId,
      latitude,
      longitude,
      commodityId: selectedCommodityId,
      quantityQuintals,
      radiusKm,
      transportRatePerQuintalPerKm: customTransportRate
        ? parseFloat(customTransportRate)
        : undefined,
    };

    try {
      const result = await apiClient.runAnalysis(payload);
      onAnalysisComplete(result);
    } catch (err: any) {
      setErrorMsg(err.message || 'Analysis run failed. Please check backend connection.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Stitch-style Hero Intro */}
      <div className="text-center space-y-2 pt-2 pb-1">
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 dark:bg-emerald-950/70 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
          <Sparkles className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
          Cross-Boundary Decision Support
        </span>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight font-heading">
          Where & When Should You Sell Your Harvest?
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 max-w-xl mx-auto">
          Compare real-time mandis, 7-day ML price forecasts, transit costs, and active weather risks to maximize your net return.
        </p>
      </div>

      {errorMsg && (
        <div className="p-4 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 rounded-2xl flex items-center gap-3 text-rose-800 dark:text-rose-300 text-xs sm:text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Main Stitch Card Form */}
      <form
        onSubmit={handleSubmit}
        className="bg-white dark:bg-[#151b23] rounded-3xl border border-slate-200/80 dark:border-slate-800 shadow-sm p-5 sm:p-7 space-y-6"
      >
        {/* Step 1: Location & Coordinates */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            <MapPin className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span>1. Geographic Scope & Coordinates</span>
          </div>

          <GeographySelector
            states={states}
            districts={districts}
            selectedStateId={selectedStateId}
            selectedDistrictId={selectedDistrictId}
            loadingStates={loadingStates}
            loadingDistricts={loadingDistricts}
            onSelectState={handleSelectState}
            onSelectDistrict={setSelectedDistrictId}
          />

          <LocationPicker
            latitude={latitude}
            longitude={longitude}
            onCoordinatesChange={(lat, lon) => {
              setLatitude(lat);
              setLongitude(lon);
            }}
            onApplyDemoPreset={handleApplyDemoPreset}
          />
        </div>

        {/* Step 2: Commodity & Perishability */}
        <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-800/80">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            <Leaf className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span>2. Crop & Perishability Class</span>
          </div>

          <CommoditySelector
            commodities={commodities}
            selectedCommodityId={selectedCommodityId}
            loading={loadingCommodities}
            onSelectCommodity={setSelectedCommodityId}
          />
        </div>

        {/* Step 3: Harvest Volume & Search Radius */}
        <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-800/80">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            <Truck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            <span>3. Harvest Volume & Market Radius</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Harvest Quantity (Quintals)
              </label>
              <div className="relative">
                <input
                  id="quantity-input"
                  type="number"
                  min="0.1"
                  step="0.5"
                  value={quantityQuintals}
                  onChange={(e) => setQuantityQuintals(parseFloat(e.target.value) || 0)}
                  className="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-[#0e1318] border border-slate-300 dark:border-slate-700 rounded-xl text-sm font-semibold text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:bg-white dark:focus:bg-[#151b23] transition"
                  required
                />
                <span className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-xs text-slate-400 font-medium">
                  Quintals
                </span>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Transport Rate Override (Optional)
              </label>
              <input
                id="transport-rate-input"
                type="number"
                step="0.1"
                placeholder="Default: ₹2.5/Q/km"
                value={customTransportRate}
                onChange={(e) => setCustomTransportRate(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-[#0e1318] border border-slate-300 dark:border-slate-700 rounded-xl text-sm text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:bg-white dark:focus:bg-[#151b23] transition"
              />
            </div>
          </div>

          {/* Quick Radius Selector Pills */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1">
                <Compass className="w-3.5 h-3.5 text-slate-400" />
                <span>Search Radius: <strong className="text-emerald-600 dark:text-emerald-400">{radiusKm} km</strong></span>
              </label>
              <span className="text-[11px] text-slate-400">Max 300 km</span>
            </div>

            <div className="flex flex-wrap gap-2">
              {RADIUS_OPTIONS.map((r) => (
                <button
                  key={r}
                  type="button"
                  onClick={() => setRadiusKm(r)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition duration-150 ${
                    radiusKm === r
                      ? 'bg-emerald-600 text-white shadow-sm shadow-emerald-600/30'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                  }`}
                >
                  {r} km
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Big Action Submit CTA */}
        <div className="pt-2">
          <button
            id="run-analysis-button"
            type="submit"
            disabled={submitting}
            className="w-full py-3.5 px-6 bg-gradient-to-r from-emerald-600 via-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-bold rounded-2xl shadow-lg shadow-emerald-600/25 flex items-center justify-center gap-2 text-sm sm:text-base transition duration-200 disabled:opacity-50"
          >
            {submitting ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Calculating Optimal Market Routing & Risks...</span>
              </>
            ) : (
              <>
                <span>Analyze Optimal Mandis & Price Forecast</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
