# email-clear

**Proteção contra e-mails maliciosos no momento em que você lê.**

O email-clear é uma extensão de navegador (Chrome, Gmail primeiro) que analisa o e-mail aberto — **remetente**, **conteúdo** e **links** — e mostra um aviso no próprio Gmail dizendo se a mensagem é **segura**, **suspeita** ou **perigosa**, com a explicação do porquê. A comunidade ainda pode votar se um remetente é perigoso ou legítimo, melhorando a proteção para todos.

---

## O que ele faz

Ao abrir um e-mail no Gmail, aparece um aviso no topo:

```
⚠ email-clear: Suspeito · risco 64/100                    [×]
   sem histórico · sem links
   indícios: urgência, domínio suspeito            ver mais
   [Perigoso]  [Legítimo]
```

A classificação combina **três sinais**:

| Sinal | Fonte | Efeito |
|-------|-------|--------|
| **Conteúdo** | IA (OpenRouter) detecta phishing/engenharia social | sinal dominante (0–70) |
| **Links** | Google Safe Browsing | link em blocklist → `perigoso` (piso 85) |
| **Remetente** | votos da comunidade (perigoso/legítimo) | perigoso → piso 80; legítimo → reduz risco |

O score vai de 0 a 100 → **seguro** (0–39), **suspeito** (40–69), **perigoso** (70–100).

## Arquitetura

```
extension/   Extensão Chrome MV3 (TypeScript + Vite + CRXJS)
backend/     API FastAPI (Python) + PostgreSQL (SQLAlchemy + Alembic)
docker-compose.yml   sobe o Postgres + a API
```

A extensão não fala direto com o banco: o **content script** detecta o e-mail no Gmail e envia para o **service worker**, que chama a API (`POST /v1/validate`). A identidade é anônima (token HMAC), sem login.

## Status

Em desenvolvimento, mas já funcional de ponta a ponta para uso pessoal:

- ✅ Validação em tempo real no Gmail (conteúdo + links + remetente)
- ✅ Votos da comunidade (perigoso/legítimo) com anti-abuso
- ✅ Cache por hash de conteúdo (economiza chamadas de IA)
- ⬜ Processamento em lote, quarentena/pastas automáticas e plano pago (roadmap)

Veja o [roadmap](docs/roadmap/0001-marcos.md) para o que está planejado.

## Pré-requisitos

- [Docker](https://www.docker.com/) + Docker Compose (para o backend/Postgres)
- [Node.js](https://nodejs.org/) 20+ (para a extensão)
- Chaves de API **opcionais** (o sistema degrada sem elas):
  - [OpenRouter](https://openrouter.ai/) — para a análise de conteúdo por IA
  - [Google Safe Browsing](https://developers.google.com/safe-browsing) — para validar links

## Como rodar (uso pessoal)

### 1. Fork e clone

Fork o repositório no GitHub e clone:

```bash
git clone https://github.com/<seu-usuario>/email-clear.git
cd email-clear
```

### 2. Suba o backend

```bash
# (opcional) configure as chaves — copie o exemplo
cp .env.example .env
#   edite .env e preencha OPENROUTER_API_KEY e/ou SAFEBROWSING_API_KEY

docker compose up -d --build
```

Confira que está no ar:

```bash
curl http://127.0.0.1:8000/v1/healthz
# → {"status":"ok","database":"ok"}
```

Sem as chaves, a IA é substituída por uma heurística simples e os links ficam "não verificados" — dá pra testar tudo mesmo assim.

### 3. Rode a extensão

```bash
cd extension
npm install
npm run build        # gera a pasta extension/dist
```

No Chrome:

1. Abra `chrome://extensions`
2. Ative o **"Modo do desenvolvedor"** (canto superior direito)
3. Clique em **"Carregar sem compactação"** e selecione a pasta `extension/dist`

> Para desenvolvimento, use `npm run dev` (modo watch) e recarregue a extensão a cada mudança.

### 4. Teste

Abra `mail.google.com` (recarregue a página) e abra qualquer e-mail. O aviso aparece no topo.

Para ver um e-mail ser flagrado, envie para você mesmo algo como:

- Assunto: `URGENTE: sua conta foi bloqueada`
- Corpo: `Detectamos acesso suspeito. Confirme sua senha e dados bancários no link abaixo em até 12 horas.`

Ou use um link de teste do Safe Browsing (sempre dá `perigoso`):
`http://testsafebrowsing.appspot.com/s/malware.html`

## Configuração (variáveis de ambiente)

| Variável | Onde | Obrigatória? | Descrição |
|----------|------|--------------|-----------|
| `OPENROUTER_API_KEY` | `.env` (raiz) | não | chave do OpenRouter (IA de conteúdo) |
| `OPENROUTER_MODEL` | `.env` (raiz) | não | modelo (padrão `openai/gpt-4o-mini`) |
| `SAFEBROWSING_API_KEY` | `.env` (raiz) | não | chave do Google Safe Browsing (links) |
| `INSTALL_TOKEN_SECRET` | `.env` (raiz) | não | segredo para assinar tokens de instalação |
| `VITE_API_BASE_URL` | `extension/.env` | não | URL do backend (padrão `http://127.0.0.1:8000`) |
| `VITE_USE_MOCK` | `extension/.env` | não | `true` p/ testar a UI sem backend |

Os arquivos `.env` **nunca** vão para o git (estão no `.gitignore`).

## Estrutura do repositório

```
docs/        Documentação: decisões (ADRs), arquitetura, roadmap, handoff
extension/   Extensão Chrome MV3 (src/ + manifest)
backend/     API FastAPI (app/ + alembic/ + tests/)
```

## Documentação

- [Visão do produto](docs/product/00-visao.md)
- [Funcionalidades (Free/Pago)](docs/product/01-features.md)
- [Decisões de arquitetura (ADRs)](docs/decisions/README.md)
- [Arquitetura](docs/architecture/0001-visao-arquitetural.md)
- [Roadmap](docs/roadmap/0001-marcos.md)

## Licença

A definir. Por ora, uso pessoal e estudo.
