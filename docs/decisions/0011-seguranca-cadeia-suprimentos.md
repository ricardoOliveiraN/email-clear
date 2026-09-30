# ADR-0011: Segurança da cadeia de suprimentos (dependências)

- **Status**: Aceito
- **Data**: 2026-09-17
- **Decisores**: time email-clear

## Contexto

A extensão depende de pacotes npm de terceiros (Vite, `@crxjs/vite-plugin`, ESLint, Vitest…). Ataques de cadeia de suprimentos são reais: um pacote pode trazer código malicioso no **runtime** ou via **scripts de instalação** (`preinstall`/`install`/`postinstall`), que executam ao rodar `npm install`. O `npm audit` acusou vulnerabilidades conhecidas nas dependências de desenvolvimento (Vite/Vitest/esbuild) — falhas exploráveis no **dev server**, não no artefato final.

É preciso uma política para: confiar no que se baixa, corrigir vulnerabilidades e não levar isso ao usuário.

## Decisão

Adotar as seguintes regras, **o quê / como**:

1. **Lockfile versionado** (`package-lock.json`) e uso de **`npm ci`** em CI para instalações reproduzíveis.
2. **`npm audit` no fluxo** de desenvolvimento. Corrigir sempre que houver correção disponível; aceitar apenas o que não tiver correção e documentar.
3. **Separar dev de produção**: vulnerabilidades que só afetam ferramentas de dev **não** entram no `dist/` (artefato instalado no Chrome). Priorizar as que afetam runtime (`npm audit --omit=dev`).
4. **Poucas dependências e conhecidas**: preferir bibliotecas consolidadas; revisar (repositório, mantenedores, downloads) antes de adicionar.
5. **Inspeção de install scripts**: pacotes com `postinstall` desconhecido são vetados ou revisados. Exceção conhecida: `esbuild` (`node install.js`) — comportamento padrão.
6. **Atualizar majors** quando recomendado pelo audit, desde que compatível (ex.: `vite 8`, `vitest 5` — CRXJS declara suporte a Vite 8).
7. **Sem segredos no repositório**; sem PII (reforça ADR-0005).

**Por quê**: reduzir a superfície de ataque, garantir build reproduzível e manter o artefato do usuário livre de falhas conhecidas.

## Consequências

Positivas:
- Risco de malware/falha conhecida reduzido e rastreável.
- Build reproduzível (`npm ci`) e auditável.
- Dev e produção separados de forma explícita.

Negativas:
- Manutenção contínua (revisar audit, atualizar majors, quebrar compatibilidade).
- Repositório com poucas dependências pode significar mais código próprio.
- Inspeção manual de scripts não escala sozinha (mitigar com automação/Dependabot).

## Alternativas descartadas

- **Sem dependências (código 100% próprio)**: inviável para build/TS/CSS no MV3.
- **Congelar versões antigas**: mantém vulnerabilidades conhecidas.
- **Ignorar install scripts globalmente (`--ignore-scripts`)**: quebra o `esbuild`, que precisa do postinstall para o binário.
- **Trocar de gerenciador (pnpm/yarn)**: não resolve a origem do problema e adiciona ferramental.

## Quando rever

Ao adotar automação de atualização (Dependabot/Renovate) ou se surgir dependência de runtime (não-dev) que exija regras mais rígidas de pinagem e auditoria.
