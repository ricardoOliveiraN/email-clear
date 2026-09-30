import type { RiskLevel } from './types';

export const API_BASE_URL = '';
export const API_VALIDATE_PATH = '/v1/validate';

export const USE_MOCK = true;

// Força um nível no modo mock (ex.: 'dangerous' para testar o alerta). `null` = aleatório pelo hash.
export const MOCK_FORCE_LEVEL: RiskLevel | null = null;
