import { validateEmail, voteSender } from '../core/api-client';
import { VALIDATE_EMAIL, VOTE_SENDER } from '../core/messaging';
import type {
  ExtensionMessage,
  ValidateEmailResponse,
  VoteSenderResponse,
} from '../core/messaging';
import { getInstallId } from '../core/storage';

chrome.runtime.onInstalled.addListener(() => {
  void getInstallId();
});

chrome.runtime.onMessage.addListener(
  (
    message: ExtensionMessage,
    _sender,
    sendResponse: (response: ValidateEmailResponse | VoteSenderResponse) => void,
  ) => {
    if (message.type === VALIDATE_EMAIL) {
      validateEmail(message.email)
        .then((classification) => sendResponse({ ok: true, classification }))
        .catch((error: unknown) => sendResponse({ ok: false, error: String(error) }));
      return true;
    }

    if (message.type === VOTE_SENDER) {
      voteSender(message.sender, message.valor)
        .then(() => sendResponse({ ok: true }))
        .catch((error: unknown) => sendResponse({ ok: false, error: String(error) }));
      return true;
    }

    return false;
  },
);
