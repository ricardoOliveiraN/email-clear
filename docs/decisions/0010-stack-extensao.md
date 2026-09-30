# ADR-0010: Stack da extensão (linguagem, build e UI)

- **Status**: Aceito
- **Data**: 2026-09-17
- **Decisores**: time email-clear

## Contexto

A extensão é Chrome **Manifest V3** (ADR-0002), injeta UI no Gmail (ADR-0006), guarda um UUID local (ADR-0005) e conversa com o backend por HTTPS/REST (ADR-0001/0003). Nada disso define ainda **linguagem, bundler ou camada de UI**. O MV3 impõe restrições: service worker de vida curta, **sem código remoto** (CSP), sem `eval`, e custo de bundle importa.

## Decisão

- **Linguagem**: **TypeScript** (modo estrito), para contratos claros com o backend e segurança na manipulação de DOM.
- **Build/bundler**: **Vite** com **`@crxjs/vite-plugin`** (HMR no dev, empacota manifest/content/background).
- **UI**: **DOM nativo + Web Components com Shadow DOM**, sem framework. O aviso é pequeno e isolado; Shadow DOM isola o CSS do email-clear do CSS do Gmail (ADR-0006).
- **HTTP**: `fetch` nativo (sem axios).
- **Persistência local**: `chrome.storage.local` para o UUID de instalação e cache por mensagem.
- **Adaptador de webmail**: isolado em `src/adapters/gmail/` (ADR-0002).
- **Qualidade**: **ESLint + Prettier**; testes com **Vitest** (unitário) e **Playwright** (e2e no Gmail, fase F3).
- **Gerenciador de pacotes**: **npm**.

## Consequências

Positivas:
- TS evita erros de contrato com a API e no DOM do Gmail (que muda com frequência).
- Shadow DOM reduz conflito de estilo — manutenção mais barata do adaptador.
- Sem framework = bundle menor, alinhado às restrições do MV3.
- Vite/CRXJS dá HMR e build simples para extensões.

Negativas:
- Sem framework, UI rica (opções, painel, listas de votos) exige mais DOM manual.
- `@crxjs/vite-plugin` está em beta; atualizações podem exigir ajustes.
- Web Components exigem disciplina de encapsulamento (eventos, atributos).

## Alternativas descartadas

- **JavaScript puro**: menos segurança de tipo e refatoração mais arriscada nos seletores do Gmail.
- **React/Vue/Svelte**: bundle e complexidade maiores sem ganho para uma UI pequena e injetada; MV3 pune bundles grandes.
- **Sem bundler (arquivos soltos)**: sem TS, sem HMR e sem gestão de módulos confortável.
- **CSS injetado global (sem Shadow DOM)**: maior risco de conflito/regressão com o CSS do webmail.

## Quando rever

Se a UI crescer muito (painel de opções, histórico, quarentena visual) a ponto de justificar um framework — possivelmente introduzir Web Components mais estruturados ou framework leve mantendo o bundle pequeno. Reavaliar `@crxjs` se sair de beta com breaking changes.
