import { API_BASE_URL, API_VALIDATE_PATH, USE_MOCK } from './config';
import { mockClassification } from './mock';
import { getInstallToken, setInstall } from './storage';
import type { Classification, OpenedEmail, VoteValue } from './types';

const API_INSTALL_PATH = '/v1/install';
const API_VOTE_PATH = '/v1/vote';

const UNCONFIGURED: Classification = {
  level: 'unknown',
  score: 0,
  reasons: ['backend não configurado'],
};

async function ensureInstallToken(): Promise<string> {
  const existing = await getInstallToken();
  if (existing) {
    return existing;
  }

  const response = await fetch(`${API_BASE_URL}${API_INSTALL_PATH}`, { method: 'POST' });
  if (!response.ok) {
    throw new Error(`Falha ao obter token de instalação: ${response.status}`);
  }

  const data = (await response.json()) as { install_id: string; token: string };
  await setInstall(data.install_id, data.token);
  return data.token;
}

export async function validateEmail(email: OpenedEmail): Promise<Classification> {
  if (USE_MOCK) {
    return mockClassification(email);
  }

  if (!API_BASE_URL) {
    return UNCONFIGURED;
  }

  const token = await ensureInstallToken();

  const response = await fetch(`${API_BASE_URL}${API_VALIDATE_PATH}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Install-Token': token,
    },
    body: JSON.stringify({
      sender: email.sender,
      subject: email.subject,
      body: email.body,
    }),
  });

  if (!response.ok) {
    throw new Error(`Falha na validação: ${response.status}`);
  }

  return (await response.json()) as Classification;
}

export async function voteSender(sender: string, valor: VoteValue): Promise<void> {
  if (USE_MOCK) {
    return;
  }

  const token = await ensureInstallToken();

  const response = await fetch(`${API_BASE_URL}${API_VOTE_PATH}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Install-Token': token,
    },
    body: JSON.stringify({ sender, valor }),
  });

  if (!response.ok) {
    throw new Error(`Falha ao votar: ${response.status}`);
  }
}
