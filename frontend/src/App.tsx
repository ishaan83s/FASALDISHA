/**
 * Main Application Component: State and View Router.
 */
import React, { useState } from 'react';
import { AnalysisFormPage } from './pages/AnalysisFormPage';
import { ResultsDashboardPage } from './pages/ResultsDashboardPage';
import type { AnalysisResult } from './types';
import { Wheat, Sun, Moon } from 'lucide-react';

export const App: React.FC = () => {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    if (!isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  return (
    <div className={`min-h-screen ${isDarkMode ? 'dark bg-gray-950 text-gray-100' : 'bg-slate-50 text-gray-900'} transition-colors duration-200`}>
      {/* Top Navbar */}
      <header className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-emerald-600 flex items-center justify-center text-white shadow-md shadow-emerald-600/30">
              <Wheat className="w-5 h-5" />
            </div>
            <div>
              <span className="text-base font-extrabold text-gray-900 dark:text-white tracking-tight">
                FasalDisha
              </span>
              <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 ml-1.5 px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800">
                Round 2 v2.0
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={toggleDarkMode}
              className="p-2 rounded-xl bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition"
              title="Toggle Dark Mode"
            >
              {isDarkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-6xl mx-auto px-4 py-6 md:py-8">
        {analysisResult ? (
          <ResultsDashboardPage
            result={analysisResult}
            onModifySearch={() => setAnalysisResult(null)}
          />
        ) : (
          <AnalysisFormPage onAnalysisComplete={(res) => setAnalysisResult(res)} />
        )}
      </main>

      {/* Footer */}
      <footer className="max-w-6xl mx-auto px-4 py-6 text-center text-xs text-gray-500 dark:text-gray-400 border-t border-gray-200/60 dark:border-gray-800/60 mt-12">
        <p>
          FasalDisha — AI-Driven Crop Price Forecasting & Market Routing Decision System (v2.0)
        </p>
        <p className="mt-1 text-[11px] text-gray-400">
          Honest Architecture: Synthetic Buyers visibly labeled • Seeded Weather clearly disclosed • Direct ML & Fallback Models
        </p>
      </footer>
    </div>
  );
};

export default App;
