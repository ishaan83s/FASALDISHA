import { createContext } from 'react';
import type { LanguageContextValue } from './types';

export const LanguageContext = createContext<LanguageContextValue | null>(null);
