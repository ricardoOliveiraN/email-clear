import type { Classification, OpenedEmail } from './types';

export const VALIDATE_EMAIL = 'VALIDATE_EMAIL';

export interface ValidateEmailMessage {
  type: typeof VALIDATE_EMAIL;
  email: OpenedEmail;
}

export type ExtensionMessage = ValidateEmailMessage;

export interface ValidateEmailResponse {
  ok: boolean;
  classification?: Classification;
  error?: string;
}

export function sendMessage<T>(message: ExtensionMessage): Promise<T> {
  return chrome.runtime.sendMessage(message) as Promise<T>;
}
