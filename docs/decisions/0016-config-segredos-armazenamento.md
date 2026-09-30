# ADR-0016: Configuração, segredos e armazenamento na extensão

- **Status**: Proposto
- **Data**: 2026-09-30
- **Decisores**: time email-clear

## Contexto

A extensão é um artefato **distribuído e desempacotável**: qualquer valor embutido no bundle é legível por quem instalar. Surgiram dúvidas sobre (a) valores estáticos no código (ex.: `INSTALL_ID_KEY` em `extension/src/core/config.ts`/`storage.ts`), (b) se tais valores deveriam vir de *env*, e (c) qual mecanismo de armazenamento usar.

Fatos relevantes:
- No Chrome MV3 **não há variáveis de ambiente em runtime**. O que o Vite expõe via `import.meta.env.VITE_*` é **inlined no bundle em build time** — ou seja, vira código legível, não um segredo.
- O [ADR-0005](0005-identidade-anonima-rate-limit.md) e o [ADR-0014](0014-identidade-servidor.md) já estabelecem que **segredo só no servidor** e que o UUID local é contabilidade, não credencial.
- O [ADR-0011](0011-seguranca-cadeia-suprimentos.md) proíbe segredos no repositório.

## Decisão proposta

1. **Nada secreto no cliente.** Chaves de assinatura, segredos HMAC e credenciais de IA vivem **apenas no backend** (env do servidor). Nunca em `config.ts`, em `import.meta.env` ou no `manifest.json`.
2. **Config não-secreta de ambiente via `import.meta.env.VITE_*`** (ex.: `API_BASE_URL`), com **default seguro** no código. Isso evita recompilar o código ao trocar de ambiente. Hoje `API_BASE_URL` está hardcoded vazio — migrar para env quando houver backend.
3. **Constantes de identificação ficam no código.** Literais como `INSTALL_ID_KEY = 'installId'`, nomes de header e paths de API **não são segredo**; residem em `config.ts` normalmente.
4. **`USE_MOCK` nunca em produção.** O modo mock (`USE_MOCK = true` em `config.ts`) deve ser desligado/omitido no build de produção; idealmente derivado de `import.meta.env.DEV` para não depender de edição manual.
5. **Armazenamento: só APIs da extensão.**
   - `chrome.storage.local` — persistente (identidade, cache L1).
   - `chrome.storage.session` — efêmero por sessão do navegador, se necessário.
   - **Proibido** `localStorage`/`sessionStorage` (pertencem à **origem do Gmail**, vazam entre scripts da página) e **cookies** (mecanismo de sessão HTTP, seriam enviados ao webmail).

## Consequências

Positivas:
- Elimina a classe de vazamento "segredo no pacote" (reforça ADR-0005/0011/0014).
- Config por ambiente sem recompilar; build reprodutível.
- Isola dados da extensão do domínio do webmail, evitando vazamento e colisão de chaves.

Negativas:
- Env de build exige cuidado: nada sensível pode cair em `VITE_*` por engano.
- Mais um passo de configuração no CI/build (definir `VITE_API_BASE_URL`).
- `chrome.storage` é assíncrono e tem limites de quota — exige tratamento (já adotado em `storage.ts`).

## Alternativas descartadas

- **Segredo/API key embutidos na extensão**: extraível do bundle; não é segredo ([ADR-0005](0005-identidade-anonima-rate-limit.md)).
- **"Env" no cliente como fonte de segredo**: em MV3 é apenas texto inlined no bundle; falsa sensação de segurança.
- **`localStorage`/`sessionStorage`**: pertencem ao Gmail, não à extensão; somem/colidem e vazam.
- **Cookies**: mecanismo de sessão HTTP; trafegam para o webmail e sofrem com SameSite/expiração.

## Quando rever

Ao criar o backend e o build de produção (definir `VITE_API_BASE_URL`, desligar o mock) e se surgir necessidade de armazenamento com dados grandes (avaliar `IndexedDB` via API da extensão).
