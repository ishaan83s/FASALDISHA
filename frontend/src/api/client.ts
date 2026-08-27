/**
 * Centralized Typed API Client for FasalDisha.
 * SSOT Reference: 05_API_CONTRACT.md, 06_FRONTEND_CONTRACT.md
 */
import type {
  State,
  District,
  Commodity,
  ResolvedLocation,
  AnalysisRequest,
  AnalysisResult,
  APIEnvelope,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

console.log('FASALDISHA API URL:', API_BASE_URL);

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMsg = `HTTP ${response.status}: ${response.statusText}`;
    try {
      const errorJson: APIEnvelope<null> = await response.json();
      if (errorJson.error?.message) {
        errorMsg = errorJson.error.message;
      }
    } catch {
      // ignore json parse error
    }
    throw new Error(errorMsg);
  }

  const envelope: APIEnvelope<T> = await response.json();
  if (!envelope.success || envelope.data === null) {
    throw new Error(envelope.error?.message || 'API request failed');
  }

  return envelope.data;
}

export const apiClient = {
  async getStates(): Promise<State[]> {
    const res = await fetch(`${API_BASE_URL}/geography/states`);
    return handleResponse<State[]>(res);
  },

  async getDistricts(stateId: string): Promise<District[]> {
    const res = await fetch(`${API_BASE_URL}/geography/districts?stateId=${encodeURIComponent(stateId)}`);
    return handleResponse<District[]>(res);
  },

  async getCommodities(stateId?: string, districtId?: string): Promise<Commodity[]> {
    const params = new URLSearchParams();
    if (stateId) params.append('stateId', stateId);
    if (districtId) params.append('districtId', districtId);
    const url = params.toString()
      ? `${API_BASE_URL}/geography/commodities?${params.toString()}`
      : `${API_BASE_URL}/geography/commodities`;
    const res = await fetch(url);
    return handleResponse<Commodity[]>(res);
  },

  async runAnalysis(request: AnalysisRequest): Promise<AnalysisResult> {
    const res = await fetch(`${API_BASE_URL}/analysis/run`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    return handleResponse<AnalysisResult>(res);
  },

  async checkHealth(): Promise<{ status: string; app: string; version: string }> {
    const res = await fetch(`${API_BASE_URL}/health`);
    return handleResponse<{ status: string; app: string; version: string }>(res);
  },

  async resolveLocation(latitude: number, longitude: number): Promise<ResolvedLocation> {
    const res = await fetch(
      `${API_BASE_URL}/geography/resolve-location?latitude=${encodeURIComponent(latitude)}&longitude=${encodeURIComponent(longitude)}`
    );
    return handleResponse<ResolvedLocation>(res);
  },
};
