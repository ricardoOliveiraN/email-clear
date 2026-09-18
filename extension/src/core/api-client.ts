import { API_BASE_URL, API_VALIDATE_PATH, USE_MOCK } from './config';
import { mockClassification } from './mock';
import { getInstallId } from './storage';
import type { Classification, OpenedEmail } from './types';

const UNCONFIGURED: Classification = {
  level: 'unknown',
  score: 0,
  reasons: ['backend não configurado'],
};

export async function validateEmail(email: OpenedEmail): Promise<Classification> {
  if (!API_BASE_URL) {
    return USE_MOCK ? mockClassification(email) : UNCONFIGURED;
  }

  const installId = await getInstallId();
  const response = await fetch(`${API_BASE_URL}${API_VALIDATE_PATH}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Install-Id': installId,
    },
    body: JSON.stringify(email),
  });

  if (!response.ok) {
    throw new Error(`Falha na validação: ${response.status}`);
  }

  return (await response.json()) as Classification;
}
