# Visão Arquitetural

Visão macro dos componentes. Para decisões detalhadas veja os [ADRs](../decisions/README.md).

## Componentes

```
┌────────────────────────┐
│   Extensão (Chrome MV3)│
│  - content script      │
│  - adaptador Gmail      │
│  - injeção CSS/HTML     │
│  - UUID de instalação   │
└─────────┬──────────────┘
          │ HTTPS (REST)
          ▼
┌────────────────────────┐
│   Backend FastAPI      │
│  - API validação/score │
│  - quota / rate-limit  │
│  - orquestração IA     │
│  - fábrica de filas    │
└────┬───────────────┬───┘
     │               │
     ▼               ▼
┌──────────────┐  ┌──────────────────┐
│ PostgreSQL   │  │ Worker (lote)    │
│  listas,     │  │  - processa em   │
│  decisões,   │  │    massa (pago)  │
│  votos       │  │  - move p/ pasta │
└──────────────┘  └──────────────────┘
```

## Fluxo Free (MVP)

1. Usuário abre o e-mail no Gmail.
2. Content script detecta a abertura e extrai remetente/conteúdo.
3. Content script envia a mensagem ao **service worker** (background), que faz a chamada HTTPS ao backend (evita o CORS da página no MV3 e centraliza a identidade) com o token de instalação (ADR-0005/0014).
4. Backend valida: tabela de perigosos + heurísticas + IA (conteúdo).
5. Backend aplica quota e devolve classificação/score.
6. Extensão injeta aviso visual (CSS/HTML) e cacheia o resultado (cache local e, no servidor, por mensagem).

## Fluxo Pago (lote via API de e-mail)

O lote **não** é feito pela extensão: o navegador carrega os e-mails sob demanda e tem limite de interação, e o service worker do MV3 tem tempo de execução curto. Por isso o lote opera pela **API do serviço de e-mail (Gmail API/REST)** autenticada via OAuth no backend.

1. Usuário autoriza o acesso ao e-mail (OAuth) e dispara o lote.
2. Backend consulta a Gmail API: lista mensagens (label, período, etc.) em páginas.
3. Worker busca o conteúdo de cada mensagem via API (com paginação/limite).
4. Classifica, arma a score e (opcional) **move/quarentena** usando labels/API (ex.: addLabel).
5. Notifica/atualiza o usuário (resultado no lote e na extensão).

> **Ponto de atenção (em mapeamento)**: a Gmail API tem escopos (readonly vs. modificar), cotas de requisição e requisições paginadas. O volume do lote deve respeitar as cotas e o custo de tempo (backoff, retries). A extensão segue usada para o **free** (validação no momento da abertura) e para **injetar o resultado visual** no webmail.

## Colaboração (votos)

1. Usuário atribui nota de risco a um remetente.
2. Backend registra voto (deduplicado por instalação).
3. Após threshold, remetente entra na lista de bloqueio global.

## Camadas

- **Extensão**: interação com o webmail, extração de dados, apresentação.
- **API**: contratos, validação, quota, orquestração.
- **Regras de negócio**: classificação, score, listas, votos.
- **Dados**: PostgreSQL.

## Considerações transversais

- **Conexão de rede**: latência/offline — cachear resultado por mensagem.
- **Chamadas à API**: feitas pelo **service worker** (background), não pelo content script — no MV3 o `fetch` do content script está sujeito ao **CORS da página**; o background usa `host_permissions`. O content script apenas troca mensagens com o background.
- **Identidade**: token de instalação emitido pelo servidor; o cliente é tratado como **não confiável** (ADR-0005/0014).
- **Custo de IA**: controlar por quota (ADR-0005), por mensagem (ADR-0007) e por cache (por mensagem, no servidor).
- **Privacidade**: sem PII; UUID/token anônimos apenas para quota.
- **Integração de e-mails**: Gmail primeiro; adaptadores isolados (ADR-0002).
