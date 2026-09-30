# Glossário

Termos usados no projeto. Referencie este arquivo para manter consistência.

- **Remetente perigoso**: e-mail ou domínio confirmado como malicioso (lista de bloqueio).
- **Remetente conhecido**: contato confiável/verificado.
- **E-mail suspeito**: candidato a risco por comportamento/reputação, ainda sem confirmação.
- **Risco (score)**: valor numérico que representa o quão perigoso é um e-mail; alimenta a classificação.
- **Classificação**: rótulo atribuído à mensagem (ex.: seguro, suspeito, perigoso, phishing).
- **Validação de conteúdo**: inspeção do corpo do e-mail buscando phishing, engenharia social, links e anexos maliciosos.
- **Heurística**: regra de detecção baseada em padrões/pontuação (não em lista estática).
- **Injeção CSS/HTML**: inserção de elementos visuais no webmail para comunicar o resultado ao usuário.
- **Quarentena**: pasta onde e-mails classificados como perigosos são movidos.
- **Processamento em lote**: varredura de vários e-mails de uma vez (Pago).
- **Pasta customizada**: pasta (label) criada pelo próprio assinante para a qual mensagens são roteadas por conteúdo/regra (Pago, F13).
- **Cleaner (limpeza da caixa de entrada)**: movimentação automática de mensagens da caixa de entrada para pastas com base na classificação de conteúdo, deixando a entrada organizada (Pago, F13).
- **Nota de risco (input do usuário)**: avaliação manual atribuída por um usuário a um remetente (F11).
- **Lista de bloqueio**: conjunto de remetentes que, após votos suficientes, é considerado perigoso.
- **UUID de instalação**: identificador gerado pela extensão, sem PII, usado apenas para quota de rate-limit (contabilidade best-effort; não é credencial).
- **Token de instalação**: credencial anônima emitida pelo servidor (assinada com HMAC) que permite ao backend verificar a instalação sem login (ADR-0014).
- **Quota / rate-limit**: limite de requisições por usuário/instalação para evitar abuso do uso de IA.
- **Free tier**: plano sem custo, sem login, com limite de uso.
- **Pago / Premium**: plano com processamento em lote e automação.
