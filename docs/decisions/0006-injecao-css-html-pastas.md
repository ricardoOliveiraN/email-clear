# ADR-0006: Injeção do aviso, quarentena e resiliência do adaptador

- **Status**: Proposto
- **Data**: 2026-08-31 (fechado em 2026-09-30)
- **Decisores**: time email-clear (direção validada com o usuário)

## Contexto

A extensão precisa comunicar o resultado ao usuário (aviso visual ao abrir o e-mail) e, no plano pago, organizar e-mails perigosos movendo-os para pastas (quarentena, F09) ou pastas customizadas (cleaner, F13/ADR-0009). Faltava decidir os pontos de inserção, o comportamento free vs. pago, a mecânica de pastas e o tratamento de quebra do DOM do Gmail. Há ainda uma oportunidade de interação do usuário no free que reduz custo de IA.

## Decisão

### 1. Onde e como injetar o aviso

- **Aviso padrão (todos os níveis)**: **alerta não-bloqueante fixo no topo da tela** (toast), compacto e **dispensável**, no estilo de um `alert` nativo — **não** abre modal, **não** escurece a página e **não** impede o uso. Substitui o banner na conversa (retirado).
- **Cor por nível**: `safe` verde, `suspicious` âmbar, `dangerous` vermelho e `unknown` cinza; ícone e rótulo reforçam a leitura. O mesmo componente serve todos os casos.
- **Alerta desacoplado do layout**: renderizado em overlay de viewport (`position: fixed; top: 12px`) dentro de Shadow DOM, sem depender da estrutura/classes do Gmail — robusto a mudanças de DOM (ver §5).
- **Conteúdo**: rótulo + score (`risco X/100`); motivos disponíveis no `title` (tooltip). Ações (ex.: "marcar remetente como perigoso") devem ser anexadas depois, sem sobrecarregar o toast.
- **Acessibilidade**: `role="alert"`; fecha com `Esc` e botão `×`, com foco gerenciado; contraste AA e dark mode.
- **Renderização** via Shadow DOM, isolando o CSS da página.

### 2. Comportamento no free

- **Free = apenas o aviso.** Sem mover e-mails, sem criar pastas.
- Mover/organizar é exclusivo do **pago**.

### 3. Pastas: via API, com acionamento explícito

- Criar/mover pastas via **Gmail API + OAuth** no **backend (worker de lote)**, não pela extensão — consistente com o ADR-0001 (lote via API). Escopos: `gmail.modify` (labels) validados com o time.
- **Acionamento por botão**: ação **explícita do usuário** (botão na extensão) dispara o lote/quarentena. Nada de movimentação silenciosa.
- Labels no padrão `email-clear/<nome>` (ex.: `email-clear/quarentena`).
- Toda movimentação é **reversível** (undo) e registrada para auditoria (ADR-0009).

### 4. E-mails já classificados no lote

- Ao rodar o lote, mensagens **já classificadas** são enviadas para suas respectivas pastas (quarentena para perigosos; pasta de destino no cleaner).
- **Exceção**: mensagens na **lixeira nunca são tocadas** (não mover, não reclassificar).
- Precedência: **quarentena (F09) vence o cleaner (F13)** — perigosos nunca vão para pastas comuns (ADR-0009).

### 5. Resiliência do adaptador (o "refém do navegador")

Sim, no **free** dependemos do DOM do Gmail para ler o e-mail aberto. A estratégia é **conter o dano e falhar em silêncio**:

- **Isolamento**: seletores só em `extension/src/adapters/gmail/`; core/UI não conhecem o DOM.
- **Apresentação desacoplada**: banner e alerta são overlays próprios (Shadow DOM, `position: fixed`), independentes do layout do Gmail — o **alerta não depende do DOM** para renderizar.
- **Detecção por URL estável (implementada)**: `observeThread`/`getThreadId` em `extension/src/adapters/gmail/route.ts` observam o roteamento por hash do Gmail (`hashchange`) para saber **quando** uma conversa abriu e obter o `threadId` (usado como chave estável de cache/dedup). Sinal muito mais estável que classes; o `MutationObserver` permanece como fallback. Reduz (mas não elimina) a dependência de DOM.
- **Extração ainda depende do DOM no free**: remetente/assunto/corpo saem do DOM (sem OAuth). No pago, vêm da Gmail API. O modal melhora a **apresentação** e a **detecção**, não a extração.
- **Âncoras estáveis**: preferir atributos semânticos (`role`, `aria-label`, `data-message-id`, estrutura) — **evitar classes ofuscadas** do Gmail (mudam sem aviso).
- **Fallbacks em cascata**: lista de seletores alternativos; usa o primeiro que casar.
- **Degradação silenciosa**: se a extração falhar, **não injetar aviso** (ou "não avaliado" discreto) — nunca mostrar aviso errado.
- **Detecção de quebra (canário)**: *feature-detect* dos nós essenciais + **telemetria anônima de "selector miss"** (sem PII) para alertar o time; remote config para desligar um caminho quebrado sem esperar release.
- **Testes de contrato**: fixtures do DOM do Gmail + testes (Vitest/jsdom) que falham quando o shape muda; atualizados periodicamente.
- **Observer estreito**: observar apenas a raiz da conversa (não o `body` inteiro), com debounce — menos ruído/CPU.
- **Escape hatch no pago**: o lote já usa a **Gmail API** (independente do DOM). A dependência do DOM fica restrita à camada **visual** do free.

### 6. Interação do usuário no free (fonte de reputação)

- No free, o usuário pode **marcar o remetente como "perigoso"** a partir do aviso (botão). Isso alimenta a **base de remetentes perigosos do servidor** (F11/F12, [ADR-0008](0008-votos-risco-comunitario.md)).
- Efeito de longo prazo: acertos da base **evitam acionar a IA** (a lista/`F01` responde primeiro) — menos custo e mais rapidez.
- Regras anti-abuso/antiforga ficam no ADR-0008 (voto vinculado à instalação, thresholds ponderados). A decisão **local** do usuário tem peso de sinal, não de verdade absoluta.

## Consequências

Positivas:
- Comportamento free/pago claro e simples de comunicar (free avisa; pago organiza).
- Acionamento explícito evita surpresas (mover e-mail sem o usuário saber).
- Estratégia de resiliência reduz manutenção e evita avisos incorretos por quebra de DOM.
- Interação no free cria base de reputação que reduz custo de IA a longo prazo.

Negativas:
- Aviso no topo para **todos** os níveis exige cuidado para não virar ruído/fadiga (mitigar com regras de exibição e auto-dismiss).
- Lote via API exige OAuth, escopos e cotas (ADR-0009).
- Telemetria de "selector miss" precisa ser anônima (sem PII, ADR-0005).
- A base de perigosos por votos pode ser envenenada — mitigado no ADR-0008.

## Alternativas descartadas

- **Modal bloqueante**: testado e descartado — interrompe o uso e cobre o conteúdo; um alerta não-bloqueante no topo comunica o mesmo risco sem atrapalhar.
- **Banner injetado na conversa**: aposentado em favor do toast — dependia do ponto de injeção (mais frágil) e era menos visível.
- **Card ao lado / badge na lista**: mais visível, porém mais intrusivo e frágil (mais pontos de DOM).
- **Mover automaticamente sem botão**: risco de esconder mensagens legítimas; fere guardrails (ADR-0009).
- **Mover pastas pela extensão (DOM)**: inviável no MV3 e não escala para histórico (ADR-0001).
- **Aviso proeminente para todos os níveis**: vira ruído; reservado a `dangerous`.
- **Telemetria com conteúdo/PII**: viola ADR-0005; só sinais agregados e anônimos.

## Quando rever

Se o Gmail mudar a estrutura de forma agressiva (acionar remote config/adaptação), se a fadiga do alerta vermelho aparecer nas métricas, ou ao definir os escopos OAuth e os limites de cotas no backend.
