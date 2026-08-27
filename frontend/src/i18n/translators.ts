/**
 * Centralized Domain Translators for FasalDisha.
 * Translates known API enums, crops, perishability, decisions, risk levels, and locations.
 */
import type { Language } from './types';
import type {
  FinalRecommendation,
  BaseDecision,
  RiskLevel,
  DemandLevel,
  PerishabilityClass,
  DataClassification,
} from '../types';

// Supported Crop Names Dictionary
const CROP_MAP: Record<string, { en: string; hi: string }> = {
  onion: { en: 'Onion', hi: 'प्याज' },
  tomato: { en: 'Tomato', hi: 'टमाटर' },
  wheat: { en: 'Wheat', hi: 'गेहूं' },
  potato: { en: 'Potato', hi: 'आलू' },
  soybean: { en: 'Soybean', hi: 'सोयाबीन' },
  mustard: { en: 'Mustard', hi: 'सरसों' },
  cotton: { en: 'Cotton', hi: 'कपास' },
  gram: { en: 'Gram (Chana)', hi: 'चना' },
  maize: { en: 'Maize', hi: 'मक्का' },
  paddy: { en: 'Paddy / Rice', hi: 'धान / चावल' },
};

// Commodity Categories
const CATEGORY_MAP: Record<string, { en: string; hi: string }> = {
  vegetable: { en: 'Vegetable', hi: 'सब्जी' },
  cereal: { en: 'Cereal', hi: 'अनाज' },
  oilseed: { en: 'Oilseed', hi: 'तिलहन' },
  'cash crop': { en: 'Cash Crop', hi: 'नकदी फसल' },
  tuber: { en: 'Tuber', hi: 'कंद' },
  pulse: { en: 'Pulse', hi: 'दलहन' },
};

// Perishability Classes
const PERISHABILITY_MAP: Record<PerishabilityClass | string, { en: string; hi: string; descEn: string; descHi: string }> = {
  HIGHLY_PERISHABLE: {
    en: 'Highly Perishable',
    hi: 'अति शीघ्र खराब होने वाली',
    descEn: '1-3 day holding limit; high spoilage risk',
    descHi: '1-3 दिन की भंडारण सीमा; खराब होने का उच्च जोखिम',
  },
  MODERATELY_PERISHABLE: {
    en: 'Moderately Perishable',
    hi: 'मध्यम शीघ्र खराब होने वाली',
    descEn: '1-2 week storage with proper ventilation',
    descHi: 'उचित हवादार स्थान में 1-2 सप्ताह भंडारण संभव',
  },
  NON_PERISHABLE: {
    en: 'Non-Perishable / Durable',
    hi: 'टिकाऊ / गैर-खराब होने वाली',
    descEn: 'Extended holding allowed for peak price capture',
    descHi: 'उच्चतम कीमत पाने के लिए अधिक समय तक रोका जा सकता है',
  },
};

// Known Risk Levels
const RISK_MAP: Record<RiskLevel | string, { en: string; hi: string }> = {
  LOW: { en: 'LOW RISK', hi: 'कम जोखिम' },
  MODERATE: { en: 'MODERATE RISK', hi: 'मध्यम जोखिम' },
  HIGH: { en: 'HIGH RISK', hi: 'उच्च जोखिम' },
  CRITICAL: { en: 'CRITICAL RISK', hi: 'अत्यधिक जोखिम' },
};

// Known Demand Levels
const DEMAND_MAP: Record<DemandLevel | string, { en: string; hi: string }> = {
  LOW: { en: 'Low Demand', hi: 'कम मांग' },
  MEDIUM: { en: 'Medium Demand', hi: 'मध्यम मांग' },
  HIGH: { en: 'High Demand', hi: 'उच्च मांग' },
};

// Known Data Classifications
const CLASSIFICATION_MAP: Record<DataClassification | string, { en: string; hi: string }> = {
  REAL: { en: 'REAL', hi: 'वास्तविक (REAL)' },
  CACHED_REAL: { en: 'CACHED', hi: 'कैश्ड (CACHED)' },
  SEEDED: { en: 'SEEDED', hi: 'सीडेड (SEEDED)' },
  SYNTHETIC: { en: 'SYNTHETIC', hi: 'सिंथेटिक (SYNTHETIC)' },
  DERIVED: { en: 'DERIVED', hi: 'व्युत्पन्न (DERIVED)' },
  UNAVAILABLE: { en: 'UNAVAILABLE', hi: 'अनुपलब्ध' },
};

// Known States
const STATE_MAP: Record<string, { en: string; hi: string }> = {
  maharashtra: { en: 'Maharashtra', hi: 'महाराष्ट्र' },
  rajasthan: { en: 'Rajasthan', hi: 'राजस्थान' },
  gujarat: { en: 'Gujarat', hi: 'गुजरात' },
  madhyapradesh: { en: 'Madhya Pradesh', hi: 'मध्य प्रदेश' },
  punjab: { en: 'Punjab', hi: 'पंजाब' },
  haryana: { en: 'Haryana', hi: 'हरियाणा' },
};

// Known Major Districts
const DISTRICT_MAP: Record<string, { en: string; hi: string }> = {
  pune: { en: 'Pune', hi: 'पुणे' },
  nashik: { en: 'Nashik', hi: 'नासिक' },
  ahmednagar: { en: 'Ahmednagar', hi: 'अहमदनगर' },
  solapur: { en: 'Solapur', hi: 'सोलापुर' },
  nagpur: { en: 'Nagpur', hi: 'नागपुर' },
  kota: { en: 'Kota', hi: 'कोटा' },
  jaipur: { en: 'Jaipur', hi: 'जयपुर' },
  jodhpur: { en: 'Jodhpur', hi: 'जोधपुर' },
  bikaner: { en: 'Bikaner', hi: 'बीकानेर' },
  ahmedabad: { en: 'Ahmedabad', hi: 'अहमदाबाद' },
  surat: { en: 'Surat', hi: 'सूरत' },
  rajkot: { en: 'Rajkot', hi: 'राजकोट' },
  vadodara: { en: 'Vadodara', hi: 'वडोदरा' },
};

/**
 * Translates crop name. Falls back to original name if unknown.
 */
export function translateCrop(cropName: string, lang: Language): string {
  if (!cropName) return '';
  const key = cropName.toLowerCase().trim();
  if (CROP_MAP[key]) {
    return CROP_MAP[key][lang];
  }
  return cropName;
}

/**
 * Translates crop category.
 */
export function translateCategory(category: string, lang: Language): string {
  if (!category) return '';
  const key = category.toLowerCase().trim();
  if (CATEGORY_MAP[key]) {
    return CATEGORY_MAP[key][lang];
  }
  return category;
}

/**
 * Translates perishability badge text & description.
 */
export function translatePerishability(pClass: PerishabilityClass | string, lang: Language) {
  const item = PERISHABILITY_MAP[pClass];
  if (item) {
    return {
      label: item[lang],
      desc: lang === 'hi' ? item.descHi : item.descEn,
    };
  }
  return {
    label: pClass ? pClass.replace(/_/g, ' ') : '',
    desc: '',
  };
}

/**
 * Translates risk level.
 */
export function translateRiskLevel(riskLevel: RiskLevel | string, lang: Language): string {
  if (RISK_MAP[riskLevel]) {
    return RISK_MAP[riskLevel][lang];
  }
  return riskLevel || '';
}

/**
 * Translates demand level.
 */
export function translateDemand(demand: DemandLevel | string, lang: Language): string {
  if (DEMAND_MAP[demand]) {
    return DEMAND_MAP[demand][lang];
  }
  return demand || '';
}

/**
 * Translates data classification tag.
 */
export function translateClassification(classification: DataClassification | string, lang: Language): string {
  if (CLASSIFICATION_MAP[classification]) {
    return CLASSIFICATION_MAP[classification][lang];
  }
  return classification || '';
}

/**
 * Translates state name.
 */
export function translateState(stateIdOrName: string, lang: Language): string {
  if (!stateIdOrName) return '';
  const key = stateIdOrName.toLowerCase().replace(/\s+/g, '');
  if (STATE_MAP[key]) {
    return STATE_MAP[key][lang];
  }
  return stateIdOrName.charAt(0).toUpperCase() + stateIdOrName.slice(1);
}

/**
 * Translates district name.
 */
export function translateDistrict(districtIdOrName: string, lang: Language): string {
  if (!districtIdOrName) return '';
  const key = districtIdOrName.toLowerCase().replace(/\s+/g, '');
  if (DISTRICT_MAP[key]) {
    return DISTRICT_MAP[key][lang];
  }
  return districtIdOrName.charAt(0).toUpperCase() + districtIdOrName.slice(1);
}

/**
 * Formats a localized action headline for DecisionHeroCard / RecommendationBanner.
 */
export function getLocalizedDecisionTitle(
  rec: FinalRecommendation | BaseDecision | string,
  mandiName: string,
  cropName: string,
  lang: Language,
  isRiskOverride = false
): string {
  const safeMandi = mandiName || (lang === 'hi' ? 'सुझाई गई मंडी' : 'Recommended Mandi');
  const safeCrop = translateCrop(cropName, lang);

  if (isRiskOverride || rec === 'SELL_EARLY_DUE_TO_RISK') {
    return lang === 'hi'
      ? `${safeMandi} में जल्दी बेचें`
      : `Sell Early at ${safeMandi}`;
  }
  if (rec === 'SELL_AT_RECOMMENDED_MANDI' || rec === 'TRAVEL') {
    return lang === 'hi'
      ? `${safeMandi} में बेचें`
      : `Sell at ${safeMandi}`;
  }
  if (rec === 'HOLD') {
    return lang === 'hi'
      ? `उच्चतम मूल्य के लिए ${safeCrop} रोकें (प्रतीक्षा करें)`
      : `Hold ${safeCrop} for Expected Peak Price`;
  }
  if (rec === 'AVOID_MANDI_OR_ROUTE') {
    return lang === 'hi'
      ? `उच्च जोखिम के कारण यह मार्ग टालें`
      : `Avoid Transit Corridor (High Risk)`;
  }
  // Default SELL_NOW
  return lang === 'hi'
    ? `${safeMandi} में अभी बेचें`
    : `Sell Now at ${safeMandi}`;
}

/**
 * Localizes top factor bullet strings for Mandi ranking cards.
 */
export function translateTopFactor(factor: string, lang: Language): string {
  if (lang !== 'hi' || !factor) return factor;
  const fLower = factor.toLowerCase();
  if (fLower.includes('risk-adjusted') || fLower.includes('high net return')) {
    return 'उच्च जोखिम-समायोजित शुद्ध लाभ';
  }
  if (fLower.includes('buyer demand') || fLower.includes('traders')) {
    return 'मजबूत खरीदार मांग और सक्रिय व्यापारी';
  }
  if (fLower.includes('proximity') || fLower.includes('logistics')) {
    return 'निकटता से परिवहन लागत न्यूनतम';
  }
  if (fLower.includes('price')) {
    return 'आकर्षक मंडी भाव';
  }
  return factor;
}

/**
 * Returns localized farmer-friendly explanation prose for the decision.
 */
export function getLocalizedDecisionReason(
  rec: FinalRecommendation | BaseDecision | string,
  rawReason: string,
  mandiName: string,
  cropName: string,
  lang: Language,
  isRiskOverride = false
): string {
  if (lang !== 'hi') {
    return rawReason;
  }
  const safeMandi = mandiName || 'सुझाई गई मंडी';
  const safeCrop = translateCrop(cropName, lang);

  if (isRiskOverride || rec === 'SELL_EARLY_DUE_TO_RISK') {
    return `खराब मौसम और फसल की शेल्फ-लाइफ के जोखिम को देखते हुए, माल खराब होने से पहले ${safeMandi} में तत्काल बिक्री सबसे सुरक्षित विकल्प है।`;
  }
  if (rec === 'SELL_AT_RECOMMENDED_MANDI' || rec === 'TRAVEL') {
    return `${safeMandi} में परिवहन लागत निकालने के बाद भी आपको अपने ${safeCrop} के लिए अधिकतम शुद्ध लाभ प्राप्त होगा।`;
  }
  if (rec === 'HOLD') {
    return `अगले 7 दिनों में ${safeCrop} के मूल्य में वृद्धि का अनुमान है। उच्चतम मूल्य पाने के लिए फसल को रोककर रखने की सलाह दी जाती है।`;
  }
  if (rec === 'AVOID_MANDI_OR_ROUTE') {
    return `परिवहन मार्ग पर मौसम या उच्च जोखिम के कारण इस मंडी में जाने से बचें और सुरक्षित विकल्प चुनें।`;
  }
  if (rec === 'SELL_NOW') {
    return `स्थानीय मंडी में वर्तमान भाव अनुकूल हैं और तुरंत बिक्री करने से अतिरिक्त परिवहन जोखिम से बचा जा सकता है।`;
  }
  return rawReason;
}

