import { validateEmail } from '../core/api-client';
import { VALIDATE_EMAIL } from '../core/messaging';
import type { ValidateEmailMessage, ValidateEmailResponse } from '../core/messaging';
import { getInstallId } from '../core/storage';

chrome.runtime.onInstalled.addListener(() => {
  void getInstallId();
});

chrome.runtime.onMessage.addListener(
  (message: ValidateEmailMessage, _sender, sendResponse: (response: ValidateEmailResponse) => void) => {
    if (message.type !== VALIDATE_EMAIL) {
      return false;
    }

    validateEmail(message.email)
      .then((classification) => sendResponse({ ok: true, classification }))
      .catch((error: unknown) => sendResponse({ ok: false, error: String(error) }));

    return true;
  },
);
