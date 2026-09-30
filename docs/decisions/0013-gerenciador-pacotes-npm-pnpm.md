# ADR-0013: Gerenciador de pacotes — npm vs pnpm

- **Status**: Rascunho
- **Data**: 2026-09-17
- **Decisores**: time email-clear

## Contexto

A extensão usa **npm** (ADR-0010) com `package-lock.json`, `npm ci` em CI e `npm audit` (ADR-0011). Surgiu a dúvida se o **pnpm** seria melhor, sobretudo como reforço de segurança da cadeia de suprimentos (preocupação do time com "pegar vírus" de pacote npm).

Este ADR apenas **registra o estudo**; a decisão está em aberto.

## Comparação (o quê)

| Critério | npm | pnpm |
|---|---|---|
| Disco/velocidade | baixa cópias | store global + hardlinks (economiza disco, instala mais rápido) |
| Rigor de dependências | "achata" `node_modules`; pode mascarar dep fantasma | `node_modules` não-achatado; acusa import não declarado |
| Scripts de instalação | **roda por padrão** | **não roda por padrão** — exige allowlist (`onlyBuiltDependencies`) |
| Monorepo (workspaces) | ok | melhor |
| Compatibilidade | universal | alguns pacotes exigem `shamefully-hoist` |
| Onipresença/CI | total | exige `corepack`/setup; lockfile próprio |
| Familiaridade | máxima | adicional a aprender |

## Opções

**Opção A — Manter npm (status quo)**
- Vantagens: zero mudança; compatibilidade total; já configurado e validado.
- Desvantagens: roda install scripts por padrão (menos seguro); `node_modules` achatado pode esconder dependências faltantes.

**Opção B — Adotar pnpm**
- Vantagens: bloqueio de install scripts por padrão (alinha com ADR-0011); rigor contra dep fantasma; economia de disco; instalação mais rápida. `esbuild` entraria em `onlyBuiltDependencies` explícito.
- Desvantagens: tooling extra (`corepack`/pnpm) e curva; lockfile incompatível (migração); alguns pacotes exigem `public-hoist-pattern`/`shamefully-hoist`; precisa atualizar comandos em `AGENTS.md`/README e os ADR-0010/0011; como o backend é Python, não há monorepo JS que justifique workspaces agora.

## Decisão

**Adiada.** Manter **npm** provisoriamente (o status quo de ADR-0010/0011) e reavaliar. Este ADR sobe para `Aceito` quando o time decidir; se a escolha for pnpm, ele **substitui o item "gerenciador de pacotes: npm" do ADR-0010** e ajusta o ADR-0011.

## Consequências

- Nenhuma mudança imediata no repositório.
- O time mantém ciência do trade-off e evita retrabalho se a decisão for por pnpm (migrar agora seria mais barato que depois).
- Fica registrado que a motivação principal de uma eventual troca é **segurança** (bloqueio de scripts), não desempenho.

## Quando rever

Ao configurar o CI (F1) ou antes de aumentar o número de dependências. Se a decisão for migrar, fazer enquanto a extensão é pequena.
