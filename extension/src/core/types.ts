export type RiskLevel = 'safe' | 'suspicious' | 'dangerous' | 'unknown';
export type VoteValue = 'dangerous' | 'safe';

export interface ClassificationSinais {
  sender?: {
    status?: string;
    votos_perigosos?: number;
    votos_totais?: number;
  };
  links?: Record<string, string>;
  content?: {
    phishing_score?: number;
    indicators?: string[];
  };
}

export interface Classification {
  level: RiskLevel;
  score: number;
  reasons: string[];
  sinais?: ClassificationSinais;
  origem?: string;
}

export interface OpenedEmail {
  id: string | null;
  sender: string | null;
  subject: string | null;
  body: string;
}
