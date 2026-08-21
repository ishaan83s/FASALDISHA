/**
 * AnalysisFormPage Component: Primary Farmer Context & Analysis Input Form.
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
  Wheat,
} from 'lucide-react';

interface AnalysisFormPageProps {
  onAnalysisComplete: (result: any) => void;
}

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
  const [radiusKm, setRadiusKm] = useState<number>(100);
  const [customTransportRate, setCustomTransportRate] = useState<string>('');

  const [loadingStates, setLoadingStates] = useState<boolean>(true);
  const [loadingDistricts, setLoadingDistricts] = useState<boolean>(false);
  const [loadingCommodities, setLoadingCommodities] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Load initial states and commodities
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

        // Load default districts for Maharashtra
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

  // Handle State Change
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
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-emerald-800 via-emerald-700 to-teal-800 rounded-3xl p-6 md:p-8 text-white shadow-xl">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-white/10 rounded-xl backdrop-blur-sm">
            <Wheat className="w-7 h-7 text-emerald-300" />
          </div>
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">
              FasalDisha — फसल दिशा
            </h1>
            <p className="text-xs md:text-sm text-emerald-100 font-medium">
              AI Price Forecasting • Cross-Boundary Market Routing • Risk-Adjusted Decisions
            </p>
          </div>
        </div>
      </div>

      {errorMsg && (
        <div className="p-4 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 rounded-2xl flex items-center gap-3 text-rose-800 dark:text-rose-300 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Main Form Card */}
      <form
        onSubmit={handleSubmit}
        className="bg-white dark:bg-gray-800 rounded-3xl border border-gray-200 dark:border-gray-700 p-6 md:p-8 shadow-sm space-y-6"
      >
        {/* Section 1: Geographic Context */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
            <span className="w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200 flex items-center justify-center text-xs">
              1
            </span>
            <span>Geographic Context & Administrative Scope</span>
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
        </div>

        {/* Section 2: Authoritative Coordinates */}
        <div className="space-y-4 pt-4 border-t border-gray-100 dark:border-gray-700">
          <div className="flex items-center gap-2 text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
            <span className="w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200 flex items-center justify-center text-xs">
              2
            </span>
            <span>Farmer Location & Nearby Radius</span>
          </div>

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

        {/* Section 3: Commodity, Harvest Quantity & Radius */}
        <div className="space-y-4 pt-4 border-t border-gray-100 dark:border-gray-700">
          <div className="flex items-center gap-2 text-sm font-bold text-gray-900 dark:text-white uppercase tracking-wider">
            <span className="w-6 h-6 rounded-full bg-emerald-100 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200 flex items-center justify-center text-xs">
              3
            </span>
            <span>Crop Metadata & Harvest Economics</span>
          </div>

          <CommoditySelector
            commodities={commodities}
            selectedCommodityId={selectedCommodityId}
            loading={loadingCommodities}
            onSelectCommodity={setSelectedCommodityId}
          />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <div>
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
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
                  className="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl text-sm"
                  required
                />
                <span className="absolute inset-y-0 right-0 pr-3 flex items-center text-xs text-gray-400">
                  Quintals
                </span>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
                Search Radius (km)
              </label>
              <div className="relative">
                <input
                  id="radius-input"
                  type="number"
                  min="10"
                  max="300"
                  step="5"
                  value={radiusKm}
                  onChange={(e) => setRadiusKm(parseFloat(e.target.value) || 100)}
                  className="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl text-sm"
                  required
                />
                <span className="absolute inset-y-0 right-0 pr-3 flex items-center text-xs text-gray-400">
                  km (Max 300)
                </span>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
                Transport Rate Override (₹/Q/km)
              </label>
              <input
                id="transport-rate-input"
                type="number"
                step="0.1"
                placeholder="Default: ₹2.5/Q/km"
                value={customTransportRate}
                onChange={(e) => setCustomTransportRate(e.target.value)}
                className="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl text-sm"
              />
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-6">
          <button
            id="run-analysis-button"
            type="submit"
            disabled={submitting}
            className="w-full py-4 px-6 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-bold rounded-2xl shadow-lg shadow-emerald-600/30 flex items-center justify-center gap-2.5 text-base transition duration-200 disabled:opacity-50"
          >
            {submitting ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Running Routing & Decision Analysis...</span>
              </>
            ) : (
              <>
                <span>Run Market Routing & Risk Analysis</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
