import { getOpenedEmail, getConversationRoot, getThreadId, isGmail, observeThread } from '../adapters/gmail';
import { sendMessage, VALIDATE_EMAIL, VOTE_SENDER } from '../core/messaging';
import type { ValidateEmailResponse, VoteSenderResponse } from '../core/messaging';
import { getCachedClassification, getSenderVote, setCachedClassification, setSenderVote } from '../core/storage';
import type { Classification, OpenedEmail, VoteValue } from '../core/types';
import { isAlertMounted, removeAlert, renderAlert } from '../ui/alert';

const DEBOUNCE_MS = 500;

let currentKey: string | null = null;
let currentClassification: Classification | null = null;
let inFlightKey: string | null = null;
let dismissedKey: string | null = null;
let timer: number | undefined;

async function requestClassification(email: OpenedEmail): Promise<Classification> {
  const response = await sendMessage<ValidateEmailResponse>({ type: VALIDATE_EMAIL, email });
  if (!response.ok || !response.classification) {
    throw new Error(response.error ?? 'sem classificação');
  }
  return response.classification;
}

async function requestVote(sender: string, valor: VoteValue): Promise<void> {
  const response = await sendMessage<VoteSenderResponse>({ type: VOTE_SENDER, sender, valor });
  if (!response.ok) {
    throw new Error(response.error ?? 'falha ao votar');
  }
}

async function resolveClassification(email: OpenedEmail, key: string): Promise<Classification | null> {
  if (currentClassification) {
    return currentClassification;
  }

  const cached = (await getCachedClassification(key)) as Classification | null;
  if (cached) {
    return cached;
  }

  try {
    const classification = await requestClassification(email);
    await setCachedClassification(key, classification);
    return classification;
  } catch (error) {
    console.warn('[email-clear] validação falhou', error);
    return null;
  }
}

async function handleEmailOpen(): Promise<void> {
  const email = getOpenedEmail();
  const root = getConversationRoot();

  if (!email || !root) {
    removeAlert();
    currentKey = null;
    currentClassification = null;
    dismissedKey = null;
    return;
  }

  const key = getThreadId() ?? `${email.sender ?? ''}|${email.subject ?? ''}`;

  if (key === currentKey && isAlertMounted()) {
    return;
  }

  if (key === currentKey && dismissedKey === key) {
    return;
  }

  if (key !== currentKey) {
    currentKey = key;
    currentClassification = null;
    dismissedKey = null;
  }

  if (inFlightKey === key) {
    return;
  }

  inFlightKey = key;
  try {
    const classification = await resolveClassification(email, key);
    if (!classification || key !== currentKey) {
      return;
    }
    currentClassification = classification;
    const sender = email.sender;
    const existingVote = sender ? await getSenderVote(sender) : null;
    renderAlert(
      classification,
      sender,
      existingVote,
      async (valor) => {
        if (sender) {
          await requestVote(sender, valor);
          await setSenderVote(sender, valor);
        }
      },
      () => {
        dismissedKey = key;
      },
    );
  } finally {
    if (inFlightKey === key) {
      inFlightKey = null;
    }
  }
}

function scheduleCheck(): void {
  window.clearTimeout(timer);
  timer = window.setTimeout(() => {
    void handleEmailOpen();
  }, DEBOUNCE_MS);
}

function start(): void {
  if (!isGmail()) {
    return;
  }

  observeThread(() => {
    scheduleCheck();
  });

  const observer = new MutationObserver(() => {
    scheduleCheck();
  });
  observer.observe(document.body, { childList: true, subtree: true });

  scheduleCheck();
}

start();
