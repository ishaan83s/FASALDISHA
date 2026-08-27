/**
 * LanguageToggle Component: Compact, Polished Segmented Language Switcher.
 * Matches FasalDisha AgriTech visual conventions in light & dark mode.
 */
import React from 'react';
import { useLanguage } from '../i18n';

export const LanguageToggle: React.FC = () => {
  const { language, setLanguage, t } = useLanguage();

  return (
    <div
      role="group"
      aria-label={t('nav.languageAriaLabel')}
      className="inline-flex items-center p-0.5 rounded-xl bg-earth-100 dark:bg-slate-800 border border-earth-200/80 dark:border-slate-700 shadow-2xs"
    >
      <button
        type="button"
        onClick={() => setLanguage('en')}
        className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all duration-150 cursor-pointer ${
          language === 'en'
            ? 'bg-agri-700 dark:bg-agri-600 text-white shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
        }`}
        aria-pressed={language === 'en'}
        title="Switch to English"
      >
        EN
      </button>

      <button
        type="button"
        onClick={() => setLanguage('hi')}
        className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all duration-150 cursor-pointer ${
          language === 'hi'
            ? 'bg-agri-700 dark:bg-agri-600 text-white shadow-xs'
            : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
        }`}
        aria-pressed={language === 'hi'}
        title="हिन्दी में बदलें"
      >
        हिं
      </button>
    </div>
  );
};
