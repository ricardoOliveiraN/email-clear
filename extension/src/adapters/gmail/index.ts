import type { OpenedEmail } from '../../core/types';

const SUBJECT_SELECTOR = 'h2.hP';
const SENDER_SELECTOR = 'span.gD[email]';
const BODY_SELECTOR = 'div.a3s.aiL';
const CONVERSATION_SELECTOR = 'div[role="main"]';

export function isGmail(): boolean {
  return location.hostname === 'mail.google.com';
}

export function getConversationRoot(): HTMLElement | null {
  return document.querySelector<HTMLElement>(CONVERSATION_SELECTOR);
}

export function getOpenedEmail(): OpenedEmail | null {
  const subject = document.querySelector<HTMLElement>(SUBJECT_SELECTOR);
  const sender = document.querySelector<HTMLElement>(SENDER_SELECTOR);
  const body = document.querySelector<HTMLElement>(BODY_SELECTOR);

  if (!subject || !body) {
    return null;
  }

  return {
    id: null,
    sender: sender?.getAttribute('email') ?? sender?.textContent ?? null,
    subject: subject.textContent,
    body: body.innerText,
  };
}
