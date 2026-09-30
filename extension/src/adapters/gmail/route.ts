const THREAD_ID_PATTERN = /^[A-Za-z0-9_-]{12,}$/;
const NON_CONVERSATION_ROUTES = new Set(['settings', 'contacts', 'tasks']);

export function getThreadId(hash: string = location.hash): string | null {
  const path = hash.replace(/^#/, '').split('?')[0];
  const segments = path.split('/').filter(Boolean);

  if (segments.length < 2) {
    return null;
  }

  if (NON_CONVERSATION_ROUTES.has(segments[0])) {
    return null;
  }

  const candidate = segments[segments.length - 1];
  return THREAD_ID_PATTERN.test(candidate) ? candidate : null;
}

export function observeThread(callback: (threadId: string | null) => void): () => void {
  const emit = (): void => {
    callback(getThreadId());
  };

  window.addEventListener('hashchange', emit);
  emit();

  return () => {
    window.removeEventListener('hashchange', emit);
  };
}
