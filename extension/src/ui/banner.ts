import type { Classification, RiskLevel } from '../core/types';

const HOST_ID = 'email-clear-banner';

const COLORS: Record<RiskLevel, { background: string; border: string; text: string }> = {
  safe: { background: '#e6f4ea', border: '#137333', text: '#0d652d' },
  suspicious: { background: '#fef7e0', border: '#b06000', text: '#7a4b00' },
  dangerous: { background: '#fce8e6', border: '#c5221f', text: '#a50e0e' },
  unknown: { background: '#f1f3f4', border: '#5f6368', text: '#3c4043' },
};

const LABELS: Record<RiskLevel, string> = {
  safe: 'Seguro',
  suspicious: 'Suspeito',
  dangerous: 'Perigoso',
  unknown: 'Não avaliado',
};

export function isBannerMounted(): boolean {
  return document.getElementById(HOST_ID) !== null;
}

export function removeBanner(): void {
  document.getElementById(HOST_ID)?.remove();
}

export function renderBanner(classification: Classification, anchor: HTMLElement): void {
  removeBanner();

  const host = document.createElement('div');
  host.id = HOST_ID;

  const shadow = host.attachShadow({ mode: 'open' });
  const color = COLORS[classification.level];

  const style = document.createElement('style');
  style.textContent = `
    .banner {
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 8px 0;
      padding: 8px 12px;
      border-left: 4px solid ${color.border};
      border-radius: 4px;
      background: ${color.background};
      color: ${color.text};
      font: 13px/1.4 Roboto, Arial, sans-serif;
    }
    .level { font-weight: 600; }
    .reasons { opacity: 0.85; }
  `;

  const banner = document.createElement('div');
  banner.className = 'banner';

  const level = document.createElement('span');
  level.className = 'level';
  level.textContent = `email-clear: ${LABELS[classification.level]} (${classification.score})`;

  const reasons = document.createElement('span');
  reasons.className = 'reasons';
  reasons.textContent = classification.reasons.join(' · ');

  banner.append(level, reasons);
  shadow.append(style, banner);
  anchor.prepend(host);
}
