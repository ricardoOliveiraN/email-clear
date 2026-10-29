import type { RiskLevel } from './types';

// URL do backend (ADR-0016). Sobrescreva com VITE_API_BASE_URL se necessário.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';
export const API_VALIDATE_PATH = '/v1/validate';

// Modo mock: apenas quando VITE_USE_MOCK=true (ex.: testar a UI sem backend).
export const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';

// Força um nível no modo mock (ex.: 'dangerous' para testar o alerta). `null` = aleatório pelo hash.
export const MOCK_FORCE_LEVEL: RiskLevel | null = null;
