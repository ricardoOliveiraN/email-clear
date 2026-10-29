import type { Classification, OpenedEmail, VoteValue } from './types';

export const VALIDATE_EMAIL = 'VALIDATE_EMAIL';
export const VOTE_SENDER = 'VOTE_SENDER';

export interface ValidateEmailMessage {
  type: typeof VALIDATE_EMAIL;
  email: OpenedEmail;
}

export interface VoteSenderMessage {
  type: typeof VOTE_SENDER;
  sender: string;
  valor: VoteValue;
}

export type ExtensionMessage = ValidateEmailMessage | VoteSenderMessage;

export interface ValidateEmailResponse {
  ok: boolean;
  classification?: Classification;
  error?: string;
}

export interface VoteSenderResponse {
  ok: boolean;
  error?: string;
}

export function sendMessage<T>(message: ExtensionMessage): Promise<T> {
  return chrome.runtime.sendMessage(message) as Promise<T>;
}
