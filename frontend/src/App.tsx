/**
 * App Component: Modern Indian AgriTech Application Shell.
 * SSOT Reference: 06_FRONTEND_CONTRACT.md, Prompt Section 9 "Visual Style".
 */
import React, { useState } from 'react';
import { AnalysisFormPage } from './pages/AnalysisFormPage';
import { ResultsDashboardPage } from './pages/ResultsDashboardPage';
import type { AnalysisResult } from './types';
import { Sprout, Sun, Moon, Sparkles, RefreshCw } from 'lucide-react';

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
    <div className={`min-h-screen ${isDarkMode ? 'dark bg-[#0f141c] text-slate-100' : 'bg-[#faf8f5] text-slate-900'} font-sans antialiased transition-colors duration-200`}>
      {/* Top Navbar */}
      <header className="sticky top-0 z-40 bg-white/90 dark:bg-[#151c24]/90 backdrop-blur-md border-b border-earth-200 dark:border-slate-800 shadow-2xs">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-agri-700 dark:bg-agri-800 flex items-center justify-center text-white shadow-sm shadow-agri-700/30 flex-shrink-0">
              <Sprout className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg font-black tracking-tight text-slate-900 dark:text-white font-heading">
                  FasalDisha <span className="text-agri-700 dark:text-agri-400 font-normal text-sm sm:inline hidden font-sans">| फसल दिशा</span>
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-agri-100 dark:bg-agri-950/80 text-agri-800 dark:text-agri-300 border border-agri-200 dark:border-agri-800 hidden sm:inline-block">
                  AI Decision Engine
                </span>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 hidden sm:block">
                AI Mandi Price Forecasting & Cross-Boundary Market Routing
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {analysisResult && (
              <button
                type="button"
                onClick={() => setAnalysisResult(null)}
                className="inline-flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-xl bg-agri-50 dark:bg-agri-950/50 hover:bg-agri-100 text-agri-800 dark:text-agri-300 border border-agri-200 dark:border-agri-800 transition cursor-pointer shadow-2xs"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>New Search</span>
              </button>
            )}

            <button
              type="button"
              onClick={toggleDarkMode}
              className="p-2 rounded-xl bg-earth-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-earth-200 dark:hover:bg-slate-700 transition cursor-pointer"
              title="Toggle Theme"
            >
              {isDarkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
            </button>
          </div>
        </div>
      </header>

      {/* Main Body */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-6 md:py-8">
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
      <footer className="max-w-6xl mx-auto px-4 sm:px-6 py-6 text-center text-xs text-slate-400 dark:text-slate-500 border-t border-earth-200 dark:border-slate-800/80 mt-12">
        <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-1">
          <span className="flex items-center gap-1 font-semibold text-slate-600 dark:text-slate-400">
            <Sparkles className="w-3 h-3 text-agri-600 dark:text-agri-400" />
            FasalDisha Intelligence Core
          </span>
          <span>•</span>
          <span>APMC Mandi Real Pricing</span>
          <span>•</span>
          <span>7-Day ML Price Forecasting</span>
          <span>•</span>
          <span>Weather & Transport Optimization</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
