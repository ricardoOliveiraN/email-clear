import type { Classification, OpenedEmail, RiskLevel } from './types';

const LEVELS: RiskLevel[] = ['safe', 'suspicious', 'dangerous'];

export function mockClassification(email: OpenedEmail): Classification {
  const seed = `${email.sender ?? ''}${email.subject ?? ''}`;
  const index = [...seed].reduce((total, char) => total + char.charCodeAt(0), 0) % LEVELS.length;
  return {
    level: LEVELS[index],
    score: (index + 1) * 30,
    reasons: ['modo mock (sem backend)'],
  };
}
