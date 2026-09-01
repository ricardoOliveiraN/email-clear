# ADR-0005: Identidade anônima e quota sem login

- **Status**: Proposto
- **Data**: 2026-08-31

## Contexto

A validação ao abrir e-mail deve funcionar no **free tier sem exigir conta**. Isso cria uma dúvida: como limitar o uso de requisições (e consequentemente o custo de IA) por usuário/instalação, sem o usuário estar logado?

Requisitos:
- Não coletar PII.
- Aplicar quota por "usuário" (instalação/device).
- Não servir como autenticação de segurança.
- Limitar abuso (muitas requisições).

## Decisão proposta

Aplicar quota via **UUID de instalação**:

1. A extensão gera (e persiste localmente) um **UUID aleatório** na primeira execução — sem PII, sem email.
2. Cada requisição ao backend envia esse UUID (ex.: header `X-Install-Id` ou campo no body).
3. O backend registra o uso por UUID e aplica **quota e rate-limit** (ex.: N verificações/dia).
4. O UUID **não é credencial**: serve apenas para quota. Recomenda-se **hashear** o valor e, se necessário, usar assinatura/chave da extensão para evitar falsificação grosseira.
5. Permanecer sem login no free; o login passa a ser opcional (para sincronizar/upgrade).

## Consequências

Positivas:
- Free tier funcional sem atrito.
- Controle de custo de IA por instalação.
- Base para migrar a conta paga depois.

Negativas:
- UUID é forjável; quem quiser burlar pode reescrever o ID (mitigação: também hash por instalação + limite global por IP).
- Instalações múltiplas = quotas múltiplas (aceitável no free).
- Necessário gerenciar quota de forma justa (ex.: janelas de tempo).

## Alternativas descartadas

- **API key por download**: vaza facilmente e é distribuída em pacote.
- **Somente IP**: não confiável (NAT, proxies; afeta usuários legítimos).
- **Conta obrigatória**: fere o requisito de "sem login" no free.

## Quando rever

Se a falsificação de UUID gerar abuso relevante, ou se o login se tornar default. Validar junto ao time antes de implementar o rate-limit em produção.
