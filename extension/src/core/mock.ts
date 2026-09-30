import { MOCK_FORCE_LEVEL } from './config';
import type { Classification, OpenedEmail, RiskLevel } from './types';

const LEVELS: RiskLevel[] = ['safe', 'suspicious', 'dangerous'];
const SCORES: Record<RiskLevel, number> = { safe: 30, suspicious: 60, dangerous: 90, unknown: 0 };

export function mockClassification(email: OpenedEmail): Classification {
  const seed = `${email.sender ?? ''}${email.subject ?? ''}`;
  const index = [...seed].reduce((total, char) => total + char.charCodeAt(0), 0) % LEVELS.length;
  const level = MOCK_FORCE_LEVEL ?? LEVELS[index];
  return {
    level,
    score: SCORES[level],
    reasons: ['modo mock (sem backend)'],
  };
}
