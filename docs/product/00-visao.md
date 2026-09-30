# Visão do email-clear

## Proposta de valor

O **email-clear** protege o destinatário de e-mails maliciosos no momento em que ele lê a mensagem. Ele valida ativamente o remetente e o conteúdo, detecta riscos (phishing, engenharia social, e-mails suspeitos) e classifica a mensagem, informando o usuário diretamente na interface do webmail e organizando e-mails perigosos em pastas próprias (ex.: quarentena).

## Personas

1. **Usuário comum (free)** — pessoa física que quer saber se um e-mail é confiável antes de clicar. Não quer se cadastrar nem configurar nada.
2. **Profissional intensivo (pago)** — analisa grandes volumes de e-mail (sistemas, atendimento, financeiro) e precisa de processamento em lote, classificação automática e organização em pastas. Inclui o **cleaner**: criar pastas customizadas e rotear mensagens por conteúdo, limpando a caixa de entrada.
3. **Comunidade defensora** — usuários engajados que reportam a nota de risco de remetentes, alimentando de forma colaborativa a lista de bloqueio.

## Princípios

- **Proteção no momento da leitura**: agir quando o e-mail está aberto ao usuário.
- **Sem atrito no free**: funcionar sem login, sem bloqueio perceptível.
- **Classificação transparente**: explicar por que um e-mail foi sinalizado.
- **Colaboração**: a nota de risco da comunidade melhora a proteção geral.
- **Expansível**: Gmail primeiro, outros serviços depois.

## Limites de escopo (nesta fase)

- Extensão de navegador (Chrome MV3 inicialmente).
- Backend em Python (FastAPI) + PostgreSQL.
- Não inclui app mobile/página própria de consumo no início.
