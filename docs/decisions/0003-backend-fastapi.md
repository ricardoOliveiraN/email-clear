# ADR-0003: Backend em FastAPI

- **Status**: Aceito
- **Data**: 2026-08-31

## Contexto

O backend precisa servir requisições de validação em tempo real, lidar com processamento em lote (assíncrono) e expor APIs simples para a extensão. Escolha do framework Python.

## Decisão

Usar **FastAPI** (ASGI):

- **Tipado** com Pydantic para contratos de API claros e validação de entrada.
- **Assíncrono** para volume de requisições de validação e tolerância a chamadas de IA/rede externa.
- **Documentação automática** (OpenAPI) que facilita o desenvolvimento da extensão e dos testes.
- Boa integração com **filas/job queues** para o lote (pago).

## Consequências

Positivas:
- Alto desempenho para cargas assíncronas.
- Menos código repetido (modelos de entrada/saída).
- Fácil de testar e gerar contrato documentado.

Negativas:
- Equipe precisa estar confortável com async em Python.
- ORM assíncrono (ex.: SQLAlchemy async) adiciona alguma curva de aprendizado.
- Não traz painel admin embutido (como Django); se necessário, será adicionado à parte.

## Alternativas descartadas

- **Flask**: síncrono, simples para MVP, porém menos adequado a chamadas concorrentes/rede e assíncrono.
- **Django**: traz ORM/admin prontos, porém mais pesado para uma API assíncrona focada; adotado apenas se um painel administrativo robusto virar requisito forte.

## Quando rever

Se um painel administrativo rico se tornar central e o overhead do Django passar a valer a pena.
