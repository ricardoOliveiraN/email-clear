import { getOpenedEmail, getConversationRoot, isGmail } from '../adapters/gmail';
import { sendMessage, VALIDATE_EMAIL } from '../core/messaging';
import type { ValidateEmailResponse } from '../core/messaging';
import { getCachedClassification, setCachedClassification } from '../core/storage';
import type { Classification, OpenedEmail } from '../core/types';
import { isBannerMounted, removeBanner, renderBanner } from '../ui/banner';

const DEBOUNCE_MS = 500;

let currentKey: string | null = null;
let currentClassification: Classification | null = null;
let inFlightKey: string | null = null;
let timer: number | undefined;

async function requestClassification(email: OpenedEmail): Promise<Classification> {
  const response = await sendMessage<ValidateEmailResponse>({ type: VALIDATE_EMAIL, email });
  if (!response.ok || !response.classification) {
    throw new Error(response.error ?? 'sem classificação');
  }
  return response.classification;
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
    removeBanner();
    currentKey = null;
    currentClassification = null;
    return;
  }

  const key = `${email.sender ?? ''}|${email.subject ?? ''}`;

  if (key === currentKey && isBannerMounted()) {
    return;
  }

  if (key !== currentKey) {
    currentKey = key;
    currentClassification = null;
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
    renderBanner(classification, root);
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

  const observer = new MutationObserver(() => {
    scheduleCheck();
  });
  observer.observe(document.body, { childList: true, subtree: true });

  scheduleCheck();
}

start();
