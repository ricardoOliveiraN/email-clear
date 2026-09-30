import type { Classification, RiskLevel } from '../core/types';

const HOST_ID = 'email-clear-alert';

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

export function isAlertMounted(): boolean {
  return document.getElementById(HOST_ID) !== null;
}

export function removeAlert(): void {
  document.getElementById(HOST_ID)?.remove();
}

export function renderAlert(classification: Classification, onClose?: () => void): void {
  removeAlert();

  const previousFocus = document.activeElement as HTMLElement | null;
  const color = COLORS[classification.level];

  const host = document.createElement('div');
  host.id = HOST_ID;

  const shadow = host.attachShadow({ mode: 'open' });

  const style = document.createElement('style');
  style.textContent = `
    :host { all: initial; }
    .alert {
      position: fixed;
      top: 12px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 2147483647;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      max-width: min(560px, 92vw);
      box-sizing: border-box;
      padding: 8px 10px 8px 12px;
      border-left: 4px solid ${color.border};
      border-radius: 6px;
      background: ${color.background};
      color: ${color.text};
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
      font: 13px/1.4 Roboto, Arial, sans-serif;
    }
    .icon {
      flex: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: ${color.border};
      color: #ffffff;
      font-weight: 700;
      font-size: 12px;
      line-height: 18px;
      text-align: center;
    }
    .text {
      min-width: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .text strong { font-weight: 600; }
    .close {
      flex: none;
      border: none;
      background: transparent;
      color: ${color.text};
      font-size: 16px;
      line-height: 1;
      cursor: pointer;
      padding: 2px 4px;
      border-radius: 4px;
    }
    .close:hover { background: rgba(0, 0, 0, 0.08); }
    @media (prefers-color-scheme: dark) {
      .alert { background: #202124; color: ${color.border}; border-color: ${color.border}; }
      .close { color: ${color.border}; }
      .close:hover { background: rgba(255, 255, 255, 0.08); }
    }
  `;

  const alert = document.createElement('div');
  alert.className = 'alert';
  alert.setAttribute('role', 'alert');
  alert.title = classification.reasons.join(' · ');

  const icon = document.createElement('span');
  icon.className = 'icon';
  icon.setAttribute('aria-hidden', 'true');
  icon.textContent = '!';

  const text = document.createElement('span');
  text.className = 'text';

  const strong = document.createElement('strong');
  strong.textContent = LABELS[classification.level];

  text.replaceChildren(
    document.createTextNode('email-clear: '),
    strong,
    document.createTextNode(` · risco ${classification.score}/100`),
  );

  const closeButton = document.createElement('button');
  closeButton.className = 'close';
  closeButton.type = 'button';
  closeButton.setAttribute('aria-label', 'Fechar aviso');
  closeButton.textContent = '×';

  alert.append(icon, text, closeButton);
  shadow.append(style, alert);
  document.body.append(host);

  let closed = false;
  const close = (): void => {
    if (closed) {
      return;
    }
    closed = true;
    document.removeEventListener('keydown', onKeydown, true);
    removeAlert();
    previousFocus?.focus?.();
    onClose?.();
  };

  function onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Escape') {
      close();
    }
  }

  closeButton.addEventListener('click', close);
  document.addEventListener('keydown', onKeydown, true);
}
