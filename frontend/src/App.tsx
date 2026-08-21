/**
 * App Component: Google Stitch-inspired AI AgTech Application Shell.
 */
import React, { useState } from 'react';
import { AnalysisFormPage } from './pages/AnalysisFormPage';
import { ResultsDashboardPage } from './pages/ResultsDashboardPage';
import type { AnalysisResult } from './types';
import { Wheat, Sun, Moon, Sparkles } from 'lucide-react';

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
    <div className={`min-h-screen ${isDarkMode ? 'dark bg-[#0e1318] text-slate-100' : 'bg-[#f6f8fa] text-slate-900'} font-sans antialiased transition-colors duration-200`}>
      {/* Stitch-style Glassmorphic Top Navbar */}
      <header className="sticky top-0 z-50 bg-white/85 dark:bg-[#151b23]/85 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800/80 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-500/20">
              <Wheat className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-base font-extrabold tracking-tight text-slate-900 dark:text-white font-heading">
                  FasalDisha
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                  AI Decision Engine
                </span>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 hidden sm:block">
                Crop Price Forecasting & Cross-Boundary Market Routing
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            {analysisResult && (
              <button
                type="button"
                onClick={() => setAnalysisResult(null)}
                className="text-xs font-semibold px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition"
              >
                New Analysis
              </button>
            )}

            <button
              type="button"
              onClick={toggleDarkMode}
              className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition"
              title="Toggle Theme"
            >
              {isDarkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
            </button>
          </div>
        </div>
      </header>

      {/* Main App Body */}
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

      {/* Stitch-style Minimal Footer */}
      <footer className="max-w-6xl mx-auto px-4 sm:px-6 py-6 text-center text-xs text-slate-400 dark:text-slate-500 border-t border-slate-200/60 dark:border-slate-800/60 mt-12">
        <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-1">
          <span className="flex items-center gap-1 font-medium">
            <Sparkles className="w-3 h-3 text-emerald-500" />
            FasalDisha Intelligence Core (Round 2 v2.0)
          </span>
          <span>•</span>
          <span>Synthetic Buyers Aggregation</span>
          <span>•</span>
          <span>Seeded Weather Radar</span>
          <span>•</span>
          <span>Direct ML Horizons</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
