# ADRs — Arquitecture Decision Records

Cada arquivo registra uma decisão do projeto. Veja o formato e as regras em [`docs/README.md`](../README.md).

## Índice

| ADR | Título | Status |
|-----|--------|--------|
| [0001](0001-arquitetura-geral.md) | Arquitetura geral (extensão + backend + banco + filas) | Aceito |
| [0002](0002-extensao-gmail-mv3.md) | Extensão de navegador / Gmail (Chrome MV3) | Aceito |
| [0003](0003-backend-fastapi.md) | Backend em FastAPI | Aceito |
| [0004](0004-banco-postgresql.md) | Banco PostgreSQL | Aceito |
| [0005](0005-identidade-anonima-rate-limit.md) | Identidade anônima e quota sem login | Proposto |
| [0006](0006-injecao-css-html-pastas.md) | Injeção do aviso, quarentena e resiliência do adaptador | Proposto |
| [0007](0007-classificacao-risco.md) | Classificação e score de risco | Proposto |
| [0008](0008-votos-risco-comunitario.md) | Votos de risco comunitário → lista de bloqueio | Proposto |
| [0009](0009-pastas-customizadas-conteudo.md) | Pastas customizadas por conteúdo (cleaner) | Rascunho |
| [0010](0010-stack-extensao.md) | Stack da extensão (TS + Vite + Web Components) | Aceito |
| [0011](0011-seguranca-cadeia-suprimentos.md) | Segurança da cadeia de suprimentos (dependências) | Aceito |
| [0012](0012-convencoes-agentes.md) | Convenções e comandos para agentes (AGENTS.md) | Aceito |
| [0013](0013-gerenciador-pacotes-npm-pnpm.md) | Gerenciador de pacotes — npm vs pnpm | Rascunho |
| [0014](0014-identidade-servidor.md) | Token de instalação emitido pelo servidor | Proposto |
| [0015](0015-cache-duas-camadas-hash.md) | Cache em duas camadas e pré-checagem por hash de conteúdo | Proposto |
| [0016](0016-config-segredos-armazenamento.md) | Configuração, segredos e armazenamento na extensão | Proposto |

## Como criar um novo ADR

1. Crie o arquivo com o próximo número (`0009-titulo.md`).
2. Preencha título, status, contexto, decisão, consequências, alternativas e "quando rever".
3. Adicione a linha no índice acima.
4. Registre o status corretamente (`[Aceito]`, `[Proposto]`, `[Rascunho]`, `[Substituído por XXXX]`).
