/**
 * TypeScript Type Definitions for FasalDisha Internationalization (i18n).
 */

export type Language = 'en' | 'hi';

export type TranslationParams = Record<string, string | number>;

export interface TranslationDictionary {
  // Navigation & App Shell
  nav: {
    brandName: string;
    brandHindiSuffix: string;
    aiEngineBadge: string;
    tagline: string;
    newSearch: string;
    toggleTheme: string;
    languageAriaLabel: string;
    switchToEnglish: string;
    switchToHindi: string;
  };

  // Footer
  footer: {
    coreIntelligence: string;
    apmcPricing: string;
    mlForecasting: string;
    weatherOptimization: string;
  };

  // Input Form & Hero
  form: {
    badge: string;
    heroTitle: string;
    heroSubtitle: string;
    step1Title: string;
    step2Title: string;
    step3Title: string;
    step4Title: string;
    harvestQuantityLabel: string;
    harvestQuantityUnit: string;
    customTransportLabel: string;
    customTransportPlaceholder: string;
    radiusLabel: string;
    maxRadiusNote: string;
    kmUnit: string;
    ctaButton: string;
    validations: {
      selectStateDistrictCrop: string;
      quantityPositive: string;
      failedCatalogs: string;
      failedDistricts: string;
      analysisFailed: string;
    };
  };

  // Geography Selector
  geography: {
    stateLabel: string;
    districtLabel: string;
    loadingStates: string;
    selectStatePrompt: string;
    loadingDistricts: string;
    selectDistrictPrompt: string;
    selectStateFirst: string;
    coordinateSearchNote: string;
  };

  // Location Picker & GPS
  location: {
    authorityCoordsLabel: string;
    useGps: string;
    acquiringGps: string;
    latLabel: string;
    lonLabel: string;
    latPlaceholder: string;
    lonPlaceholder: string;
    sourceGps: string;
    sourcePreset: string;
    sourceManual: string;
    tryPresetScenario: string;
    selectedBadge: string;
    readyBadge: string;
    loadedPrefix: string;
    gpsMatchedNotice: string;
    gpsOutOfBoundsError: string;
    gpsCatalogError: string;
    gpsDeniedError: string;
    gpsNotSupported: string;
    presets: {
      puneOnionTitle: string;
      puneOnionDesc: string;
      puneOnionBadge: string;
      nashikTomatoTitle: string;
      nashikTomatoDesc: string;
      nashikTomatoBadge: string;
      kotaWheatTitle: string;
      kotaWheatDesc: string;
      kotaWheatBadge: string;
      ahmedabadCottonTitle: string;
      ahmedabadCottonDesc: string;
      ahmedabadCottonBadge: string;
    };
  };

  // Commodity Selector & Perishability
  commodity: {
    label: string;
    loadingCatalog: string;
    selectPrompt: string;
    perishability: {
      highlyPerishable: string;
      moderatelyPerishable: string;
      nonPerishable: string;
      standard: string;
      highlyPerishableDesc: string;
      moderatelyPerishableDesc: string;
      nonPerishableDesc: string;
    };
  };

  // Loading Progress Modal
  loading: {
    analyzingTitle: string;
    subtitle: string;
    step1: string;
    step2: string;
    step3: string;
    step4: string;
    step5: string;
    footerNote: string;
  };

  // Results Dashboard - Top Context Bar
  contextBar: {
    changeInputs: string;
    bestDayPill: string;
    quintals: string;
    kmRadius: string;
  };

  // Decision Hero Card (Level 1 & 2)
  decisionHero: {
    bestDecisionEyebrow: string;
    analysisConfidence: string;
    riskOverrideTag: string;
    recommendedMarketTag: string;
    optimalRoutingTag: string;
    strategicHoldTag: string;
    sellNowTag: string;
    riskOverrideNotice: string;
    netReturnLabel: string;
    netReturnSubtext: string;
    bestSellingDay: string;
    dayLabel: string;
    expectedPeakPrice: string;
    targetMandi: string;
    kmAway: string;
    grossTransitFormula: string;
  };

  // Forecast Trend Chart (Level 3)
  forecast: {
    title: string;
    subtitle: string;
    peakAlertBadge: string;
    peakExpectedBadge: string;
    steadyTrajectoryBadge: string;
    currentModalLabel: string;
    todayBaseline: string;
    day1Horizon: string;
    day3Horizon: string;
    day1Label: string;
    day3Label: string;
    day3Subtext: string;
    expectedPeakLabel: string;
    dailyTrajectoryHeading: string;
    modelReliability: string;
    dayLabel: string;
    basisPrefix: string;
    modelTypeLive: string;
    modelTypePrecomputed: string;
    sevenDayTitle: string;
    normalTrajectory: string;
  };

  // Mandi Rankings List & Card (Level 4)
  rankings: {
    sectionTitle: string;
    sectionSubtitle: string;
    crossDistrictActive: string;
    emptyTitle: string;
    emptySubtitle: string;
    recommendedBadge: string;
    bestChoiceBadge: string;
    kmAway: string;
    expectedNetReturn: string;
    riskAdjustedReturn: string;
    grossTransitBreakdown: string;
    grossTransportBreakdown: string;
    predictedPrice: string;
    currentPrice: string;
    sevenDayHorizon: string;
    buyerDemand: string;
    buyersCount: string;
    routeRisk: string;
    overallRankScore: string;
    whyThisRank: string;
    hideScoreBreakdown: string;
    returnScore70: string;
    buyerScore20: string;
    dataQuality10: string;
    keyDecisionDrivers: string;
    explainScore: string;
    hideScoreMath: string;
    transitCostNote: string;
  };

  // Radar Map Visualizer
  radar: {
    title: string;
    subtitle: string;
    marketsCount: string;
    yourFarm: string;
    bestBadge: string;
    recommendedRouteLegend: string;
    candidateRoutesLegend: string;
    disclaimer: string;
    marketPrice: string;
    transitImpact: string;
    netReturn: string;
    topRecommendationBadge: string;
    kmAway: string;
  };

  // Analysis Confidence Card (Level 5)
  confidence: {
    title: string;
    highConfidence: string;
    moderateConfidence: string;
    baselineHeuristic: string;
    compositeScoreDesc: string;
    decisionSignalsTitle: string;
    priceForecastSignal: string;
    modelReliabilitySub: string;
    marketDensitySignal: string;
    apmcCandidatesSub: string;
    weatherRouteSignal: string;
    riskMonitoredSub: string;
    dataQualitySignal: string;
    verifiedSub: string;
  };

  // Weather Impact Card & Alert (Level 7)
  weather: {
    title: string;
    subtitle: string;
    clearBadge: string;
    clearAdvice: string;
    moderateBadge: string;
    moderateAdvice: string;
    highImpactBadge: string;
    highImpactAdvice: string;
    farmerSellingImpact: string;
    activeAdvisory: string;
    sourcePrefix: string;
    unavailableTitle: string;
    unavailableDesc: string;
    severeWeatherRoadAlert: string;
    moderateWeatherCaution: string;
    optimalConditions: string;
    noDisruptions: string;
    heavyRainAlert: string;
  };

  // Why Recommendation Drawer & Reasoning Panel (Level 6)
  audit: {
    drawerTitle: string;
    drawerSubtitle: string;
    viewAuditTrail: string;
    collapseDetails: string;
    hideAuditTrail: string;
    pillar1Title: string;
    pillar1Desc: string;
    pillar1Formula: string;
    netReturnSubscore: string;
    buyerSignalSubscore: string;
    dataQualitySubscore: string;
    compositeFinalScore: string;
    pillar2Title: string;
    pillar2Desc: string;
    pillar2Formula: string;
    activeVerifiedBuyers: string;
    demandCategory: string;
    offerReliabilityIndex: string;
    classification: string;
    pillar3Title: string;
    pillar3Desc: string;
    baseAlgorithmDecision: string;
    riskOverrideTriggered: string;
    overrideYes: string;
    overrideNo: string;
    finalActionableAdvice: string;
    pillar4Title: string;
    pillar4Desc: string;
    modelEngineType: string;
    trainingDataBasis: string;
    dataSourceLabel: string;
    forecastScope: string;
    syntheticBaseline: string;
    seededBaseline: string;
    historicalBaseline: string;
    daySeries: string;
    systemAuditTitle: string;
    systemAuditDesc: string;
    bestLocationProofTitle: string;
    noCandidateInRadius: string;
    buyerIntelligenceTitle: string;
    noActiveBuyers: string;
    weatherSourceTitle: string;
    forcedSafeSelling: string;
    normalHoldSell: string;
    mlProvenanceTitle: string;
    peakPriceLabel: string;
    onDayLabel: string;
    peakAlertActive: string;
    peakAlertOff: string;
  };

  // Risk Panel (Auxiliary)
  riskPanel: {
    title: string;
    overallScore: string;
    activeOverrideNotice: string;
    weatherSignal: string;
    perishabilitySpoilage: string;
    cropClass: string;
    dataCompleteness: string;
    multiFactorSupport: string;
  };
}

export type TranslationKeyPath = string;

export interface LanguageContextValue {
  language: Language;
  setLanguage: (lang: Language) => void;
  toggleLanguage: () => void;
  t: (keyPath: string, params?: TranslationParams) => string;
  dict: TranslationDictionary;

  // Domain Helper Functions bound to current language
  translateCrop: (cropName: string) => string;
  translateCategory: (category: string) => string;
  translatePerishability: (pClass: string) => { label: string; desc: string };
  translateRiskLevel: (riskLevel: string) => string;
  translateDemand: (demand: string) => string;
  translateClassification: (classification: string) => string;
  translateState: (stateIdOrName: string) => string;
  translateDistrict: (districtIdOrName: string) => string;
  getLocalizedDecisionTitle: (
    rec: string,
    mandiName: string,
    cropName: string,
    isRiskOverride?: boolean
  ) => string;
  getLocalizedDecisionReason: (
    rec: string,
    rawReason: string,
    mandiName: string,
    cropName: string,
    isRiskOverride?: boolean
  ) => string;
  translateTopFactor: (factor: string) => string;
}
