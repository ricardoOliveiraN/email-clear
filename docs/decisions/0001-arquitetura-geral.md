# ADR-0001: Arquitetura geral

- **Status**: Aceito
- **Data**: 2026-08-31
- **Decisores**: time email-clear (validado com usuário)

## Contexto

O email-clear precisa validar e-mails no momento em que o usuário os abre e, no plano pago, processar em lote e classificar, organizando mensagens perigosas. A solução combina trabalho no navegador (extensão) e processamento central (backend) com persistência relacional.

## Decisão

Adotar três camadas principais:

1. **Extensão de navegador** — capta o e-mail aberto, aciona a validação, injeta o aviso ao usuário (CSS/HTML) e, no pago, move e-mails para pastas.
2. **Backend (FastAPI)** — recebe as requisições de validação, aplica as regras (tabela de perigosos, heurísticas, IA), classifica e devolve o resultado. Gerencia quota/rate-limit.
3. **PostgreSQL** — persiste tabela de remetentes/domínios perigosos, verificações, decisões, votos e plano do usuário.

Para o processamento em lote (pago), usa-se **fila de trabalhos** (léase: worker/job queue) para não travar as requisições síncronas.

## Fluxo (resumo)

- **Free**: abrir e-mail → extensão envia remetente/content → backend valida → retorna classificação → extensão injeta aviso.
- **Pago (lote)**: usuário autoriza OAuth → backend consulta a **Gmail API (REST)** em páginas → enfileira → worker busca conteúdo → classifica → (opcional) move via labels → notifica.

> **Lote via API, não pela extensão.** O navegador carrega e-mails sob demanda e limita interações; o service worker do MV3 tem execução curta. Portanto o lote usa a Gmail API autenticada no backend (ver `architecture/0001`). A extensão segue usada no free (validação na abertura) e para injetar o resultado visual.

## Consequências

Positivas:
- Validação centralizada (listas e heurísticas em um só lugar).
- Extensão leve, responsável só pela interação com o webmail.
- Base pronta para venda do plano pago.

Negativas:
- Dependência de rede/backend no momento da leitura.
- Necessita estratégia de cache/modo offline para queda de conectividade.
- Extensão precisa acompanhar mudanças do DOM do webmail.

## Alternativas descartadas

- **Tudo no navegador**: sem backend; inviável para colaboração, listas globais e lote.
- **Backend acessa e-mail via API (sem extensão)**: descartado como fluxo **principal** por não cobrir a validação "no momento da abertura" nem a injeção visual no webmail. Porém é a via adotada **especificamente para o lote (pago)** — os dois convivem.
- **Tudo pela extensão (mesmo no lote)**: descartado; limites de interação do navegador e tempo curto do service worker MV3 inviabilizam varreduras grandes no cliente.

## Quando rever

Se suportar muitos webmails com DOM divergente, ou se o modo offline se tornar requisito de produto.
