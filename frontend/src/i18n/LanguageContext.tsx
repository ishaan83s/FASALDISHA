import React, { useState, useEffect, useMemo, useCallback } from 'react';
import type { Language, TranslationParams } from './types';
import { LanguageContext } from './context';
import { en } from './locales/en';
import { hi } from './locales/hi';
import * as translators from './translators';

const STORAGE_KEY = 'fasaldisha_lang';

function getNestedValue(obj: any, path: string): string | undefined {
  if (!obj || !path) return undefined;
  const keys = path.split('.');
  let current = obj;
  for (const k of keys) {
    if (current && typeof current === 'object' && k in current) {
      current = current[k];
    } else {
      return undefined;
    }
  }
  return typeof current === 'string' ? current : undefined;
}

function interpolate(text: string, params?: TranslationParams): string {
  if (!params || !text) return text;
  return text.replace(/\{(\w+)\}/g, (match, key) => {
    return key in params ? String(params[key]) : match;
  });
}

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [language, setLanguageState] = useState<Language>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored === 'hi' || stored === 'en') {
        return stored;
      }
    } catch {
      // ignore storage access error
    }
    return 'en';
  });

  const setLanguage = useCallback((lang: Language) => {
    setLanguageState(lang);
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch {
      // ignore
    }
  }, []);

  const toggleLanguage = useCallback(() => {
    setLanguage(language === 'en' ? 'hi' : 'en');
  }, [language, setLanguage]);

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  const dict = useMemo(() => (language === 'hi' ? hi : en), [language]);

  const t = useCallback(
    (keyPath: string, params?: TranslationParams): string => {
      let rawText = getNestedValue(dict, keyPath);
      if (rawText === undefined && language !== 'en') {
        // Fallback to English dictionary if key missing in Hindi
        rawText = getNestedValue(en, keyPath);
      }
      if (rawText === undefined) {
        return keyPath;
      }
      return interpolate(rawText, params);
    },
    [dict, language]
  );

  const boundTranslateCrop = useCallback(
    (cropName: string) => translators.translateCrop(cropName, language),
    [language]
  );

  const boundTranslateCategory = useCallback(
    (category: string) => translators.translateCategory(category, language),
    [language]
  );

  const boundTranslatePerishability = useCallback(
    (pClass: string) => translators.translatePerishability(pClass, language),
    [language]
  );

  const boundTranslateRiskLevel = useCallback(
    (riskLevel: string) => translators.translateRiskLevel(riskLevel, language),
    [language]
  );

  const boundTranslateDemand = useCallback(
    (demand: string) => translators.translateDemand(demand, language),
    [language]
  );

  const boundTranslateClassification = useCallback(
    (classification: string) => translators.translateClassification(classification, language),
    [language]
  );

  const boundTranslateState = useCallback(
    (stateIdOrName: string) => translators.translateState(stateIdOrName, language),
    [language]
  );

  const boundTranslateDistrict = useCallback(
    (districtIdOrName: string) => translators.translateDistrict(districtIdOrName, language),
    [language]
  );

  const boundGetLocalizedDecisionTitle = useCallback(
    (rec: string, mandiName: string, cropName: string, isRiskOverride?: boolean) =>
      translators.getLocalizedDecisionTitle(rec, mandiName, cropName, language, isRiskOverride),
    [language]
  );

  const boundGetLocalizedDecisionReason = useCallback(
    (rec: string, rawReason: string, mandiName: string, cropName: string, isRiskOverride?: boolean) =>
      translators.getLocalizedDecisionReason(rec, rawReason, mandiName, cropName, language, isRiskOverride),
    [language]
  );

  const boundTranslateTopFactor = useCallback(
    (factor: string) => translators.translateTopFactor(factor, language),
    [language]
  );

  const contextValue = useMemo(
    () => ({
      language,
      setLanguage,
      toggleLanguage,
      t,
      dict,
      translateCrop: boundTranslateCrop,
      translateCategory: boundTranslateCategory,
      translatePerishability: boundTranslatePerishability,
      translateRiskLevel: boundTranslateRiskLevel,
      translateDemand: boundTranslateDemand,
      translateClassification: boundTranslateClassification,
      translateState: boundTranslateState,
      translateDistrict: boundTranslateDistrict,
      getLocalizedDecisionTitle: boundGetLocalizedDecisionTitle,
      getLocalizedDecisionReason: boundGetLocalizedDecisionReason,
      translateTopFactor: boundTranslateTopFactor,
    }),
    [
      language,
      setLanguage,
      toggleLanguage,
      t,
      dict,
      boundTranslateCrop,
      boundTranslateCategory,
      boundTranslatePerishability,
      boundTranslateRiskLevel,
      boundTranslateDemand,
      boundTranslateClassification,
      boundTranslateState,
      boundTranslateDistrict,
      boundGetLocalizedDecisionTitle,
      boundGetLocalizedDecisionReason,
      boundTranslateTopFactor,
    ]
  );

  return <LanguageContext.Provider value={contextValue}>{children}</LanguageContext.Provider>;
};

