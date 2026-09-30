# Estrutura de pastas

Árvore de diretórios alvo do repositório. Define onde cada camada (ADR-0001) vive no código. Os diretórios de código ainda **não existem** — fazem parte da Fase F1 (ver [`../roadmap/0001-marcos.md`](../roadmap/0001-marcos.md)).

## Árvore alvo

```
email-clear/
├── README.md
├── docs/                          # documentação (visão, ADRs, arquitetura, roadmap, handoff)
├── extension/                     # extensão Chrome MV3 (ADR-0002)
│   ├── manifest.json              # Manifest V3
│   ├── src/
│   │   ├── background/            # service worker: faz as chamadas à API (evita CORS) e gera a identidade + token
│   │   ├── content/               # content script + injeção CSS/HTML (ADR-0006)
│   │   ├── adapters/
│   │   │   └── gmail/             # adaptador Gmail isolado (detecção/extração)
│   │   ├── core/                  # cliente de API, cache por mensagem, UUID de instalação (ADR-0005)
│   │   └── ui/                    # estilos/componentes do aviso
│   ├── assets/
│   └── tests/
├── backend/                       # FastAPI (ADR-0003) + PostgreSQL (ADR-0004)
│   ├── app/
│   │   ├── main.py                # bootstrap ASGI
│   │   ├── api/                   # rotas (ex.: v1/) — contrato consumido pela extensão
│   │   ├── core/                  # config/settings, segurança, quota
│   │   ├── domain/                # regras de negócio: score, listas, votos (ADR-0007/0008)
│   │   ├── services/              # validação, orquestração de IA, filas
│   │   ├── models/                # modelos SQLAlchemy
│   │   ├── schemas/               # contratos Pydantic
│   │   └── db/                    # sessão/engine
│   ├── worker/                    # processamento em lote (pago — Gmail API/OAuth)
│   ├── alembic/                   # migrations
│   ├── tests/
│   └── pyproject.toml
├── docker-compose.yml             # dev: PostgreSQL + backend
└── .github/workflows/             # CI (lint + testes)
```

## Regras

- **`extension/` e `backend/` são independentes** — sem build cruzado nem imports entre eles; a integração é só via HTTP (HTTPS REST).
- **Adaptadores isolados**: todo código específico de webmail fica em `extension/src/adapters/<servico>/`; adicionar um webmail novo não deve tocar no `core` (ADR-0002).
- **Lote não vive na extensão**: `backend/worker/` processa em lote via API (ADR-0001); a extensão não faz varredura.
- **Entradas com nomes únicos**: os arquivos de entrada (`background/service-worker.ts`, `content/content.ts`) **não** podem se chamar `index.ts` — o CRXJS/Vite colide o nome e pode ligar o service worker ao chunk errado. Manter nomes distintos por entrypoint.
- **Rede só no background**: o content script **não** faz `fetch` direto ao backend; envia mensagem ao service worker, que faz a chamada (evita CORS no MV3 e centraliza a identidade). Ver [arch/0001](0001-visao-arquitetural.md).
- **Regras de negócio fora das rotas**: `api/` só recebe/devolve contratos e delega para `domain/`/`services/`.
- **Sem PII**: `core/` da extensão guarda apenas o UUID anônimo de instalação (ADR-0005).

## Quando rever

Ao adicionar o segundo webmail (novo adaptador) ou se o worker ganhar ciclo de vida/deploy próprio e justificar repositório/serviço separado.

<!-- Referências: ADR-0001 (arquitetura geral), ADR-0002 (extensão MV3), ADR-0003 (FastAPI), ADR-0004 (PostgreSQL), ADR-0005 (identidade/quota), ADR-0006 (injeção/pastas), ADR-0007 (score), ADR-0008 (votos). -->
