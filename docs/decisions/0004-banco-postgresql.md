# ADR-0004: Banco PostgreSQL

- **Status**: Aceito
- **Data**: 2026-08-31

## Contexto

O email-clear precisa persistir dados relacionais com integridade e também consultas de classificação/listas. Dados: remetentes e domínios perigosos, verificações realizadas, decisões, votos de risco, planos/usuários.

## Decisão

Usar **PostgreSQL** como banco principal.

- Modelo relacional e transacional: listas de perigosos, verificações, votos, planos.
- Índices para consultas rápidas de domínios/remetentes (lookup por e-mail/domínio).
- Suporte a extensões e tipos (arrays, JSONB) para guardar detalhes da classificação e payloads de verificação.

## Consequências

Positivas:
- Integridade e consultas complexas bem-sucedidas.
- Conforto para crescer: particionamento, índices, réplicas.

Negativas:
- Operação gerenciada (hosted) ou custo de infraestrutura.
- Mais setup que bancos embutidos (SQLite) para desenvolvimento local.

## Alternativas descartadas

- **SQLite**: ótimo para protótipo local, mas sem concorrência/colaboração.
- **Banco NoSQL (ex.: MongoDB)**: menos natural para relações domínio→remetente→votos e integridade.

## Quando rever

Se o volume de escrita exigir dimensionamento horizontal pesado (possível particionamento), mantendo o PostgreSQL.
