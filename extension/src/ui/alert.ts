import type { Classification, RiskLevel, VoteValue } from '../core/types';

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

const VOTE_LABELS: Record<VoteValue, string> = {
  dangerous: 'perigoso',
  safe: 'legítimo',
};

function pluralize(n: number, singular: string, plural: string): string {
  return `${n} ${n === 1 ? singular : plural}`;
}

function senderLinksSummary(classification: Classification): string {
  const parts: string[] = [];
  const sinais = classification.sinais;
  const sender = sinais?.sender;

  if (sender?.status === 'dangerous') {
    parts.push('histórico ruim');
  } else if (sender?.status === 'legitimate') {
    parts.push('histórico bom');
  } else if ((sender?.votos_totais ?? 0) > 0) {
    parts.push(pluralize(sender?.votos_totais ?? 0, 'voto', 'votos'));
  } else {
    parts.push('sem histórico');
  }

  const linkEntries = Object.entries(sinais?.links ?? {});
  if (linkEntries.length === 0) {
    parts.push('sem links');
  } else {
    const dangerous = linkEntries.filter(([, v]) => v === 'dangerous').length;
    const unknown = linkEntries.filter(([, v]) => v === 'unknown').length;
    const safe = linkEntries.length - dangerous - unknown;
    if (dangerous > 0) {
      parts.push(pluralize(dangerous, 'link perigoso', 'links perigosos'));
    } else if (safe > 0) {
      parts.push(pluralize(safe, 'link legítimo', 'links legítimos'));
    } else {
      parts.push(pluralize(unknown, 'link não verificado', 'links não verificados'));
    }
  }

  return parts.join(' · ');
}

export function isAlertMounted(): boolean {
  return document.getElementById(HOST_ID) !== null;
}

export function removeAlert(): void {
  document.getElementById(HOST_ID)?.remove();
}

export function renderAlert(
  classification: Classification,
  sender: string | null,
  existingVote: VoteValue | null,
  onVote: (valor: VoteValue) => Promise<void>,
  onClose?: () => void,
): void {
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
      display: flex;
      flex-direction: column;
      gap: 4px;
      max-width: min(560px, 92vw);
      box-sizing: border-box;
      padding: 8px 10px;
      border-left: 4px solid ${color.border};
      border-radius: 6px;
      background: ${color.background};
      color: ${color.text};
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
      font: 13px/1.4 Roboto, Arial, sans-serif;
    }
    .header {
      display: flex;
      align-items: center;
      gap: 8px;
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
      flex: 1 1 auto;
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
    .checks {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      font-size: 11px;
      opacity: 0.75;
    }
    .reasons {
      display: flex;
      align-items: baseline;
      gap: 6px;
      min-width: 0;
      font-size: 11px;
      opacity: 0.75;
    }
    .reasons-text {
      min-width: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .reasons.expanded .reasons-text {
      white-space: pre-line;
      overflow: visible;
    }
    .more {
      flex: none;
      border: none;
      background: transparent;
      color: ${color.text};
      font: 11px/1.4 Roboto, Arial, sans-serif;
      text-decoration: underline;
      cursor: pointer;
      padding: 0;
      white-space: nowrap;
    }
    .more:hover { opacity: 0.7; }
    .actions {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 2px;
    }
    .vote-btn {
      border: 1px solid ${color.border};
      background: transparent;
      color: ${color.text};
      font: 12px/1.2 Roboto, Arial, sans-serif;
      padding: 3px 8px;
      border-radius: 4px;
      cursor: pointer;
      white-space: nowrap;
    }
    .vote-btn:hover:not(:disabled) { background: rgba(0, 0, 0, 0.08); }
    .vote-btn:disabled { opacity: 0.5; cursor: default; }
    .status {
      font: 12px/1.2 Roboto, Arial, sans-serif;
      white-space: nowrap;
    }
    @media (prefers-color-scheme: dark) {
      .alert { background: #202124; color: ${color.border}; border-color: ${color.border}; }
      .close { color: ${color.border}; }
      .close:hover { background: rgba(255, 255, 255, 0.08); }
      .vote-btn { color: ${color.border}; border-color: ${color.border}; }
    }
  `;

  const alert = document.createElement('div');
  alert.className = 'alert';
  alert.setAttribute('role', 'alert');
  alert.title = classification.reasons.join(' · ');

  // linha 1 — ícone + título + fechar (topo)
  const header = document.createElement('div');
  header.className = 'header';

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

  header.append(icon, text, closeButton);

  // linha 2 — histórico + links
  const checks = document.createElement('div');
  checks.className = 'checks';
  checks.textContent = senderLinksSummary(classification);

  // linha 3 — o "porquê" da IA (com "ver mais")
  const reasonsEl = document.createElement('div');
  reasonsEl.className = 'reasons';

  const reasonsText = document.createElement('span');
  reasonsText.className = 'reasons-text';
  reasonsEl.append(reasonsText);

  let reasonsToggle: HTMLButtonElement | null = null;

  const indicators = classification.sinais?.content?.indicators ?? [];
  const collapsedText =
    indicators.length > 0 ? `indícios: ${indicators.join(', ')}` : 'sem indícios de phishing';
  const expandedText = indicators.map((item) => `• ${item}`).join('\n');
  reasonsText.textContent = collapsedText;

  if (indicators.length > 0) {
    reasonsToggle = document.createElement('button');
    reasonsToggle.className = 'more';
    reasonsToggle.type = 'button';
    reasonsToggle.textContent = 'ver mais';
    reasonsEl.append(reasonsToggle);

    let expandedState = false;
    reasonsToggle.addEventListener('click', () => {
      expandedState = !expandedState;
      reasonsText.textContent = expandedState ? expandedText : collapsedText;
      reasonsEl.classList.toggle('expanded', expandedState);
      reasonsToggle!.textContent = expandedState ? 'ver menos' : 'ver mais';
    });
  }

  // linha 4 — botões de voto
  const actions = document.createElement('div');
  actions.className = 'actions';
  const status = document.createElement('span');
  status.className = 'status';
  actions.append(status);

  if (sender) {
    const dangerBtn = document.createElement('button');
    dangerBtn.className = 'vote-btn';
    dangerBtn.type = 'button';
    dangerBtn.title = 'Marcar este remetente como perigoso';
    dangerBtn.textContent = 'Perigoso';

    const legitBtn = document.createElement('button');
    legitBtn.className = 'vote-btn';
    legitBtn.type = 'button';
    legitBtn.title = 'Marcar este remetente como legítimo';
    legitBtn.textContent = 'Legítimo';

    const changeBtn = document.createElement('button');
    changeBtn.className = 'vote-btn';
    changeBtn.type = 'button';
    changeBtn.title = 'Trocar seu voto neste remetente';
    changeBtn.textContent = 'trocar';

    const showButtons = (): void => {
      changeBtn.remove();
      status.textContent = '';
      dangerBtn.disabled = false;
      legitBtn.disabled = false;
      actions.append(dangerBtn, legitBtn);
    };

    const showVoted = (valor: VoteValue): void => {
      dangerBtn.remove();
      legitBtn.remove();
      status.textContent = `✓ marcado como ${VOTE_LABELS[valor]}`;
      actions.append(changeBtn);
    };

    if (existingVote) {
      showVoted(existingVote);
    } else {
      actions.append(dangerBtn, legitBtn);
    }

    changeBtn.addEventListener('click', showButtons);

    const doVote = async (valor: VoteValue): Promise<void> => {
      dangerBtn.disabled = true;
      legitBtn.disabled = true;
      status.textContent = '…';
      try {
        await onVote(valor);
        showVoted(valor);
      } catch {
        status.textContent = 'erro ao votar';
        dangerBtn.disabled = false;
        legitBtn.disabled = false;
      }
    };

    dangerBtn.addEventListener('click', () => {
      void doVote('dangerous');
    });
    legitBtn.addEventListener('click', () => {
      void doVote('safe');
    });
  }

  alert.append(header, checks, reasonsEl, actions);
  shadow.append(style, alert);
  document.body.append(host);

  // esconde o "ver mais" se o texto não estourar
  if (reasonsToggle && reasonsText.scrollWidth <= reasonsText.clientWidth) {
    reasonsToggle.style.display = 'none';
  }

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
