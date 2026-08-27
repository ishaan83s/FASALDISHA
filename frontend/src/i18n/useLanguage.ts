import { useContext } from 'react';
import { LanguageContext } from './context';
import type { LanguageContextValue } from './types';

export function useLanguage(): LanguageContextValue {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}

export function useTranslation() {
  const { t, language, dict } = useLanguage();
  return { t, language, dict };
}
