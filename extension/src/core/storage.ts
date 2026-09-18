const INSTALL_ID_KEY = 'installId';

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

export async function getCachedClassification(messageId: string): Promise<unknown | null> {
  const key = `classification:${messageId}`;
  const stored = await chrome.storage.local.get(key);
  return stored[key] ?? null;
}

export async function setCachedClassification(messageId: string, value: unknown): Promise<void> {
  const key = `classification:${messageId}`;
  await chrome.storage.local.set({ [key]: value });
}
