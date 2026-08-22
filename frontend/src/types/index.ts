/**
 * TypeScript Type Definitions for FasalDisha.
 * SSOT Reference: 05_API_CONTRACT.md, 06_FRONTEND_CONTRACT.md
 */

export type DataClassification =
  | 'REAL'
  | 'CACHED_REAL'
  | 'SEEDED'
  | 'SYNTHETIC'
  | 'DERIVED'
  | 'UNAVAILABLE';

export type PerishabilityClass =
  | 'HIGHLY_PERISHABLE'
  | 'MODERATELY_PERISHABLE'
  | 'NON_PERISHABLE';

export type CropGroup = 'PERISHABLE' | 'NON_PERISHABLE';

export type BaseDecision = 'SELL_NOW' | 'HOLD' | 'TRAVEL';

export type FinalRecommendation =
  | 'SELL_NOW'
  | 'HOLD'
  | 'SELL_AT_RECOMMENDED_MANDI'
  | 'SELL_EARLY_DUE_TO_RISK'
  | 'AVOID_MANDI_OR_ROUTE';

export type RiskLevel = 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';

export type DemandLevel = 'LOW' | 'MEDIUM' | 'HIGH';

export type ModelType = 'LIVE' | 'PRECOMPUTED';

export type ForecastScope = 'DIRECT_MODEL' | 'DERIVED_PROPAGATION';

export interface State {
  stateId: string;
  stateName: string;
  active: boolean;
  sourceClassification: DataClassification;
}

export interface District {
  districtId: string;
  stateId: string;
  districtName: string;
  active: boolean;
  sourceClassification: DataClassification;
}

export interface Commodity {
  commodityId: string;
  commodityName: string;
  commodityCategory: string;
  perishabilityClass: PerishabilityClass;
  cropGroup: CropGroup;
  unit: string;
  active: boolean;
}

export interface Mandi {
  mandiId: string;
  mandiName: string;
  stateId: string;
  districtId: string;
  latitude: floatNumber;
  longitude: floatNumber;
  active: boolean;
  locationClassification: DataClassification;
}

type floatNumber = number;

export interface DailyForecastPoint {
  day: number;
  predictedPrice: number;
  confidence?: number;
}

export interface ForecastOutput {
  currentPrice: number;
  forecast1Day: number;
  forecast3Day: number;
  forecast7Day: number;
  expectedPeakPrice: number;
  peakDay: number;
  peakAlert: boolean;
  dailyForecast: DailyForecastPoint[];
  forecastConfidence: number;
  modelType: ModelType;
  historyWindowDays: number;
  historyClassification: DataClassification;
  historySourceLabel: string;
  forecastScope: ForecastScope;
}

export interface WeatherEventDetail {
  eventId?: string;
  eventType: string;
  severity: RiskLevel;
  eventDate?: string;
  description?: string;
  classification: DataClassification;
  sourceLabel: string;
}

export interface WeatherSignal {
  status: 'ACTIVE' | 'UNAVAILABLE';
  impactLevel: RiskLevel;
  events: WeatherEventDetail[];
  classification: DataClassification;
  sourceLabel: string;
}

export interface BuyerSignal {
  activeBuyerCount: number;
  demandLevel: DemandLevel;
  offerStrength: number;
  reliability: number;
  buyerSignalScore: number;
  classification: DataClassification;
  sourceLabel: string;
}

export interface RankingBreakdown {
  normalizedRiskAdjustedReturn: number;
  buyerSignalScore: number;
  dataQualityScore: number;
  topFactors: string[];
  rankingScore: number;
}

export interface CandidateMandi {
  rank: number;
  mandi: Mandi;
  distanceKm: number;
  commodityAvailable: boolean;
  currentPrice: number;
  forecast: ForecastOutput;
  transportCostPerQuintal: number;
  totalTransportCost: number;
  expectedRevenue: number;
  netReturn: number;
  riskScore: number;
  riskLevel: RiskLevel;
  riskAdjustedReturn: number;
  buyerSignal: BuyerSignal;
  weatherImpact: WeatherSignal;
  rankingBreakdown: RankingBreakdown;
  rankingScore: number;
  dataClassification: Record<string, any>;
}

export interface FarmerContext {
  stateId: string;
  districtId: string;
  latitude: number;
  longitude: number;
  quantityQuintals: number;
  radiusKm: number;
}

export interface SearchMetadata {
  candidateCount: number;
  searchStatus: string;
  crossBoundaryCandidatesIncluded: boolean;
}

export interface RiskSummary {
  overallRiskScore: number;
  riskLevel: RiskLevel;
  dataCompleteness: number;
  riskFactors: string[];
}

export interface DataProvenance {
  coverage: Record<string, any>;
  buyerDataClassification: DataClassification;
}

export interface DecisionOutput {
  baseDecision: BaseDecision;
  finalRecommendation: FinalRecommendation;
  riskOverrideApplied: boolean;
  recommendedMandi?: Mandi;
  reasonCodes: string[];
  humanReadableReason: string;
  decisionConfidence: number;
}

export interface AnalysisResult {
  commodity: Commodity;
  farmerContext: FarmerContext;
  search: SearchMetadata;
  localMandi?: Mandi;
  forecast: ForecastOutput;
  weather: WeatherSignal;
  riskSummary: RiskSummary;
  nearbyMandis: CandidateMandi[];
  dataProvenance: DataProvenance;
  decision: DecisionOutput;
}

export interface AnalysisRequest {
  stateId: string;
  districtId: string;
  latitude: number;
  longitude: number;
  commodityId: string;
  quantityQuintals: number;
  radiusKm: number;
  transportRatePerQuintalPerKm?: number;
}

export interface ErrorDetail {
  code: string;
  message: string;
}

export interface APIEnvelope<T> {
  success: boolean;
  data: T | null;
  error: ErrorDetail | null;
}
