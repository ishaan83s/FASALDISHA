/**
 * AnalysisLoadingModal Component: Multi-step Intelligent Progress Experience.
 * SSOT Reference: Prompt Section 13 "Loading State".
 */
import React, { useEffect, useState, useMemo } from 'react';
import { Loader2, CheckCircle2, Circle, Sparkles, Sprout } from 'lucide-react';
import { useLanguage } from '../i18n';

interface AnalysisLoadingModalProps {
  commodityName?: string;
}

export const AnalysisLoadingModal: React.FC<AnalysisLoadingModalProps> = ({
  commodityName = 'Crop',
}) => {
  const { t, translateCrop } = useLanguage();
  const [activeStep, setActiveStep] = useState<number>(1);

  const steps = useMemo(
    () => [
      { id: 1, label: t('loading.step1') },
      { id: 2, label: t('loading.step2') },
      { id: 3, label: t('loading.step3') },
      { id: 4, label: t('loading.step4') },
      { id: 5, label: t('loading.step5') },
    ],
    [t]
  );

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev < steps.length ? prev + 1 : prev));
    }, 450);
    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm animate-fade-in">
      <div className="bg-white dark:bg-[#151c24] border border-earth-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl space-y-6">
        {/* Header with pulsing icon */}
        <div className="text-center space-y-2">
          <div className="w-14 h-14 rounded-2xl bg-agri-100 dark:bg-agri-950/80 border border-agri-300 dark:border-agri-800 text-agri-700 dark:text-agri-400 mx-auto flex items-center justify-center shadow-inner">
            <Sprout className="w-8 h-8 animate-bounce text-agri-600 dark:text-agri-400" />
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading">
            {t('loading.analyzingTitle', { commodity: translateCrop(commodityName) })}
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            {t('loading.subtitle')}
          </p>
        </div>

        {/* Step-by-Step Progress List */}
        <div className="space-y-3 bg-earth-50/70 dark:bg-slate-900/60 p-4 rounded-2xl border border-earth-200/80 dark:border-slate-800 text-xs">
          {steps.map((step) => {
            const isDone = activeStep > step.id;
            const isCurrent = activeStep === step.id;

            return (
              <div
                key={step.id}
                className={`flex items-center gap-3 transition-all duration-300 ${
                  isDone
                    ? 'text-agri-800 dark:text-agri-300 font-semibold'
                    : isCurrent
                    ? 'text-slate-900 dark:text-white font-bold scale-[1.02]'
                    : 'text-slate-400 dark:text-slate-500 opacity-60'
                }`}
              >
                {isDone ? (
                  <CheckCircle2 className="w-4 h-4 text-agri-600 dark:text-agri-400 flex-shrink-0" />
                ) : isCurrent ? (
                  <Loader2 className="w-4 h-4 text-agri-600 dark:text-agri-400 animate-spin flex-shrink-0" />
                ) : (
                  <Circle className="w-4 h-4 text-slate-300 dark:text-slate-700 flex-shrink-0" />
                )}
                <span className="text-[12px]">{step.label}</span>
              </div>
            );
          })}
        </div>

        {/* Footer info */}
        <div className="flex items-center justify-center gap-1.5 text-[11px] text-slate-400">
          <Sparkles className="w-3.5 h-3.5 text-amber-500" />
          <span>{t('loading.footerNote')}</span>
        </div>
      </div>
    </div>
  );
};

