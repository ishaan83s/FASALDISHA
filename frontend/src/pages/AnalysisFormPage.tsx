/**
 * AnalysisFormPage Component: 5-Step Farmer-First Guided Input Experience.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md, Prompt Section 12 "Redesign the Input Page".
 */
import React, { useState, useEffect } from 'react';
import type { State, District, Commodity, AnalysisRequest, AnalysisResult } from '../types';
import { apiClient } from '../api/client';
import { GeographySelector } from '../components/GeographySelector';
import { LocationPicker } from '../components/LocationPicker';
import { CommoditySelector } from '../components/CommoditySelector';
import { AnalysisLoadingModal } from '../components/AnalysisLoadingModal';
import {
  ArrowRight,
  AlertCircle,
  MapPin,
  Wheat,
  Scale,
  Compass,
  Sliders,
  Sprout,
} from 'lucide-react';

interface AnalysisFormPageProps {
  onAnalysisComplete: (result: AnalysisResult) => void;
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

  // Load state and crop catalogs on initial mount
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
      setErrorMsg('Please select your state, district, and crop.');
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
      // Give users a brief moment to experience the intelligent progress indicator
      setTimeout(() => {
        onAnalysisComplete(result);
        setSubmitting(false);
      }, 700);
    } catch (err: any) {
      setErrorMsg(err.message || 'Analysis run failed. Please check backend connection.');
      setSubmitting(false);
    }
  };

  const currentCrop = commodities.find((c) => c.commodityId === selectedCommodityId);

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Animated Loading Overlay */}
      {submitting && (
        <AnalysisLoadingModal commodityName={currentCrop?.commodityName || 'Crop'} />
      )}

      {/* Hero Title & Value Proposition */}
      <div className="text-center space-y-2 pt-1">
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-agri-100 dark:bg-agri-950/70 text-agri-800 dark:text-agri-300 border border-agri-200 dark:border-agri-800">
          <Sprout className="w-3.5 h-3.5 text-agri-600 dark:text-agri-400" />
          Smart Agricultural Mandi Advisor
        </span>
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight font-heading">
          Where & When Should You Sell Your Harvest?
        </h1>
        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 max-w-xl mx-auto leading-relaxed">
          Get transparent, risk-adjusted market rankings, 7-day AI price forecasts, transit economics, and weather alerts in seconds.
        </p>
      </div>

      {errorMsg && (
        <div className="p-4 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 rounded-2xl flex items-center gap-3 text-rose-800 dark:text-rose-300 text-xs sm:text-sm shadow-xs">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* 5-Step Guided Form Card */}
      <form
        onSubmit={handleSubmit}
        className="bg-white dark:bg-[#151c24] rounded-3xl border border-earth-200 dark:border-slate-800 shadow-sm p-5 sm:p-7 space-y-6"
      >
        {/* Step 1: Where are you? */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-agri-700 dark:text-agri-400">
            <MapPin className="w-4 h-4 text-agri-600 dark:text-agri-400" />
            <span>1. Where are you? (Location & District)</span>
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

        {/* Step 2: What are you selling? */}
        <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-agri-700 dark:text-agri-400">
            <Wheat className="w-4 h-4 text-agri-600 dark:text-agri-400" />
            <span>2. What are you selling? (Crop & Perishability)</span>
          </div>

          <CommoditySelector
            commodities={commodities}
            selectedCommodityId={selectedCommodityId}
            loading={loadingCommodities}
            onSelectCommodity={setSelectedCommodityId}
          />
        </div>

        {/* Step 3: How much? & Step 4: How far can you travel? */}
        <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-agri-700 dark:text-agri-400">
            <Scale className="w-4 h-4 text-agri-600 dark:text-agri-400" />
            <span>3. How much harvest do you have?</span>
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
                  step="0.1"
                  value={quantityQuintals}
                  onChange={(e) => setQuantityQuintals(parseFloat(e.target.value) || 0)}
                  className="w-full px-3.5 py-2.5 bg-earth-50/70 dark:bg-slate-900/80 border border-earth-200 dark:border-slate-700 rounded-xl text-sm font-bold text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-agri-500 focus:bg-white dark:focus:bg-[#151c24] transition"
                  required
                />
                <span className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-xs text-slate-400 font-medium">
                  Quintals
                </span>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1 flex items-center gap-1">
                <Sliders className="w-3.5 h-3.5 text-slate-400" />
                <span>Custom Transport Rate (Optional)</span>
              </label>
              <input
                id="transport-rate-input"
                type="number"
                step="0.1"
                placeholder="Default: ₹2.5 / Quintal / km"
                value={customTransportRate}
                onChange={(e) => setCustomTransportRate(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-earth-50/70 dark:bg-slate-900/80 border border-earth-200 dark:border-slate-700 rounded-xl text-sm text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-agri-500 focus:bg-white dark:focus:bg-[#151c24] transition"
              />
            </div>
          </div>

          {/* Step 4: Search Radius Pills */}
          <div className="pt-2">
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-bold uppercase tracking-wider text-agri-700 dark:text-agri-400 flex items-center gap-1.5">
                <Compass className="w-4 h-4 text-agri-600 dark:text-agri-400" />
                <span>4. How far can you travel? ({radiusKm} km)</span>
              </label>
              <span className="text-[11px] text-slate-400">Max 300 km radius</span>
            </div>

            <div className="flex flex-wrap gap-2">
              {RADIUS_OPTIONS.map((r) => (
                <button
                  key={r}
                  type="button"
                  onClick={() => setRadiusKm(r)}
                  className={`px-3.5 py-2 rounded-xl text-xs font-bold transition duration-150 cursor-pointer shadow-2xs ${
                    radiusKm === r
                      ? 'bg-agri-700 text-white shadow-sm ring-1 ring-agri-700'
                      : 'bg-earth-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-earth-200 dark:hover:bg-slate-700'
                  }`}
                >
                  {r} km
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Big Action CTA Button */}
        <div className="pt-3">
          <button
            id="run-analysis-button"
            type="submit"
            disabled={submitting}
            className="w-full py-4 px-6 bg-agri-700 hover:bg-agri-800 active:scale-[0.99] text-white font-extrabold rounded-2xl shadow-lg shadow-agri-900/20 flex items-center justify-center gap-2.5 text-base transition-all duration-150 cursor-pointer disabled:opacity-50 font-heading"
          >
            <span>Find My Best Market & Profit</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};
