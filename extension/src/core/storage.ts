import type { VoteValue } from './types';

const INSTALL_ID_KEY = 'installId';
const INSTALL_TOKEN_KEY = 'installToken';
const VOTE_PREFIX = 'vote:';

export async function getInstallId(): Promise<string> {
  const stored = await chrome.storage.local.get(INSTALL_ID_KEY);
  const existing = stored[INSTALL_ID_KEY];
  if (typeof existing === 'string') {
    return existing;
  }
  const id = crypto.randomUUID();
  await chrome.storage.local.set({ [INSTALL_ID_KEY]: id });
  return id;
}

export async function getInstallToken(): Promise<string | null> {
  const stored = await chrome.storage.local.get(INSTALL_TOKEN_KEY);
  const value = stored[INSTALL_TOKEN_KEY];
  return typeof value === 'string' ? value : null;
}

export async function setInstall(installId: string, token: string): Promise<void> {
  await chrome.storage.local.set({
    [INSTALL_ID_KEY]: installId,
    [INSTALL_TOKEN_KEY]: token,
  });
}

function voteKey(sender: string): string {
  return `${VOTE_PREFIX}${sender.trim().toLowerCase()}`;
}

export async function getSenderVote(sender: string): Promise<VoteValue | null> {
  const key = voteKey(sender);
  const stored = await chrome.storage.local.get(key);
  const value = stored[key];
  return value === 'dangerous' || value === 'safe' ? value : null;
}

export async function setSenderVote(sender: string, valor: VoteValue): Promise<void> {
  await chrome.storage.local.set({ [voteKey(sender)]: valor });
}

export async function getCachedClassification(messageId: string): Promise<unknown | null> {
  const key = `classification:${messageId}`;
  const stored = await chrome.storage.local.get(key);
  return stored[key] ?? null;
}

export async function setCachedClassification(messageId: string, value: unknown): Promise<void> {
  const key = `classification:${messageId}`;
  await chrome.storage.local.set({ [key]: value });
}
