# ADR-0002: Extensão de navegador (Gmail, Chrome MV3)

- **Status**: Aceito
- **Data**: 2026-08-31

## Contexto

A validação do e-mail aberto e a injeção do aviso acontecem na interface do webmail. A tecnologia depende do serviço de e-mail; no início o alvo é o Gmail, com intenção de expansão para outros.

## Decisão

- Construir extensão para navegador **Chrome (Manifest V3)**, compatível com navegadores que seguem o padrão (Edge, Brave, Opera).
- Focar no **Gmail web** em primeiro lugar: injetar um content script e detectar o e-mail aberto para disparar a validação e exibir o aviso (CSS/HTML).
- Estruturar o código de forma que o **adaptador do webmail** (detecção de elemento, extração de remetente/conteúdo) fique isolado, permitindo adicionar outros serviços depois.

## Consequências

Positivas:
- MV3 é o padrão atual e facilita a publicação na Chrome Web Store.
- Injeção visual direta e de baixa latência no fluxo do usuário.

Negativas:
- Manutenção contínua por mudanças no DOM do Gmail.
- MV3 traz restrições (service workers, limites de execução) que exigem cuidado com chamadas de rede.
- Cada webmail novo exige um adaptador específico.

## Alternativas descartadas

- **Genérico (qualquer webmail via DOM)**: mais abrangente, porém frágil e com esforço alto por serviço.
- **Somente via API de e-mail**: não cobre injeção visual no momento da abertura.

## Quando rever

Ao adicionar o segundo webmail significativo ou se o Gmail mudar a estrutura de forma agressiva.
