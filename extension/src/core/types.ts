export type RiskLevel = 'safe' | 'suspicious' | 'dangerous' | 'unknown';

export interface Classification {
  level: RiskLevel;
  score: number;
  reasons: string[];
}

export interface OpenedEmail {
  id: string | null;
  sender: string | null;
  subject: string | null;
  body: string;
}
