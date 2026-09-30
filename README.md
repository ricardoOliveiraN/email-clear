# email-clear

Proteção contra e-mails maliciosos enquanto você lê. O email-clear valida o remetente e o conteúdo da mensagem (phishing, engenharia social, e-mails suspeitos) e avisa o usuário no próprio webmail, além de organizar mensagens perigosas em pastas (ex.: quarentena).

Extensão de navegador (Chrome MV3, Gmail primeiro) + backend em Python (FastAPI) + PostgreSQL.

> Status: em desenvolvimento. Este README descreverá, futuramente, **como usar a aplicação** (instalação, configuração e uso para quem consome o projeto open source).

## Documentação

As decisões de projeto (o quê, porquê, como, quando), arquitetura, estimativas e roadmap estão em [`docs/`](docs/README.md).

- [Visão do produto](docs/product/00-visao.md)
- [Funcionalidades (Free/Pago)](docs/product/01-features.md)
- [Decisões — ADRs](docs/decisions/README.md)
- [Arquitetura](docs/architecture/0001-visao-arquitetural.md)
- [Estrutura de pastas](docs/architecture/0002-estrutura-de-pastas.md)
- [Estimativas e custos](docs/planning/0001-estimativas.md)
- [Roadmap](docs/roadmap/0001-marcos.md)
- [Handoff — estado atual](docs/handoff/0001-estado-atual.md)

## Estrutura

```
docs/        Documentação (decisões, arquitetura, roadmap, handoff)
extension/   Extensão Chrome MV3 (a criar — ver docs/architecture/0002)
backend/     API FastAPI + worker (a criar — ver docs/architecture/0002)
```
