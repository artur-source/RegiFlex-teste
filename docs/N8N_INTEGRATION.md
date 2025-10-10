# Integração n8n com RegiFlex

## Visão Geral

A integração n8n permite automatizar completamente o pipeline de onboarding, gestão de pagamentos e monitoramento do RegiFlex. Esta documentação detalha como configurar e usar a integração.

## Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   RegiFlex      │    │      n8n        │    │   Serviços      │
│   Frontend      │    │   Workflows     │    │  Externos       │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Formulário  │◄┼────┼►│ Onboarding  │◄┼────┼►│  Supabase   │ │
│ │ Marketing   │ │    │ │  Workflow   │ │    │ │             │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   Admin     │◄┼────┼►│Monitoramento│◄┼────┼►│   Vercel    │ │
│ │ Dashboard   │ │    │ │  Workflow   │ │    │ │             │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│                 │    │                 │    │                 │
│                 │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│                 │◄───┼►│ Pagamentos  │◄┼────┼►│   Stripe    │ │
│                 │    │ │  Workflow   │ │    │ │             │ │
│                 │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Workflows Implementados

### 1. RegiFlex - Onboarding Cliente

**Trigger:** Webhook `/webhook/regiflex-onboarding`

**Fluxo:**
1. Recebe dados do formulário de marketing
2. Valida informações obrigatórias
3. Cria registro da clínica no Supabase
4. Cria customer no Stripe
5. Provisiona instância no Vercel
6. Envia email de boas-vindas
7. Registra conclusão do processo

**Dados de entrada:**
```json
{
  "nome": "Nome da Clínica",
  "email": "contato@clinica.com",
  "plano": "individual|clinica",
  "telefone": "(11) 99999-9999",
  "cnpj": "12.345.678/0001-90" // opcional
}
```

### 2. RegiFlex - Monitoramento Sistema

**Trigger:** Schedule (a cada 15 minutos)

**Fluxo:**
1. Verifica status dos serviços (Supabase, Vercel, Stripe)
2. Mede tempo de resposta
3. Identifica problemas
4. Cria alertas quando necessário
5. Registra métricas de saúde

### 3. RegiFlex - Gestão Pagamentos

**Trigger:** Webhook `/webhook/stripe-webhook`

**Fluxo:**
1. Recebe eventos do Stripe
2. Processa diferentes tipos de evento:
   - `invoice.payment_succeeded`: Ativa conta
   - `invoice.payment_failed`: Suspende conta
   - `customer.subscription.deleted`: Cancela conta
3. Atualiza status no Supabase
4. Envia notificações apropriadas

## Configuração

### 1. Variáveis de Ambiente

```bash
# n8n
N8N_INSTANCE_URL=https://your-n8n-instance.com
N8N_API_KEY=your-api-key

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Stripe
STRIPE_SECRET_KEY=sk_live_your-secret-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
```

### 2. Setup Inicial

```bash
# 1. Instalar dependências
npm install

# 2. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# 3. Testar conexão
node test-n8n-integration.js

# 4. Criar workflows (via API)
curl -X POST http://localhost:3000/api/n8n/setup
```

## API Endpoints

### GET /api/n8n/status
Verifica status da conexão com n8n.

**Resposta:**
```json
{
  "success": true,
  "n8n_status": {
    "status": "healthy",
    "statusCode": 200
  },
  "timestamp": "2025-10-09T21:00:00.000Z"
}
```

### POST /api/n8n/setup
Cria todos os workflows essenciais do RegiFlex.

**Resposta:**
```json
{
  "success": true,
  "message": "Setup dos workflows concluído",
  "results": {
    "successful": 3,
    "failed": 0,
    "details": [...]
  }
}
```

### POST /api/n8n/trigger/onboarding
Inicia processo de onboarding para novo cliente.

**Corpo da requisição:**
```json
{
  "nome": "Clínica Exemplo",
  "email": "contato@exemplo.com",
  "plano": "individual"
}
```

### GET /api/n8n/health
Health check completo do sistema.

## Webhooks

### Onboarding: `/webhook/regiflex-onboarding`

Usado pelo formulário de marketing para iniciar onboarding automático.

**Exemplo de uso:**
```javascript
fetch('https://your-n8n-instance.com/webhook/regiflex-onboarding', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    nome: 'Clínica ABC',
    email: 'contato@clinicaabc.com',
    plano: 'individual'
  })
})
```

### Stripe: `/webhook/stripe-webhook`

Configurado no dashboard do Stripe para receber eventos de pagamento.

**Eventos suportados:**
- `invoice.payment_succeeded`
- `invoice.payment_failed`
- `customer.subscription.deleted`
- `customer.subscription.created`

## Monitoramento

### Logs

Todos os workflows geram logs detalhados:

```
📥 Dados recebidos: { nome: "Clínica ABC", ... }
🚀 Preparando deploy para: Clínica ABC
✅ Deploy simulado para: Clínica ABC
📧 Email preparado para: contato@clinicaabc.com
🎉 Onboarding concluído!
```

### Métricas

O workflow de monitoramento coleta:
- Status de saúde dos serviços
- Tempo de resposta
- Número de onboardings por dia
- Taxa de sucesso dos workflows

### Alertas

Alertas são criados para:
- Serviços indisponíveis (> 5 minutos)
- Tempo de resposta alto (> 2 segundos)
- Falhas em workflows críticos
- Problemas de pagamento

## Troubleshooting

### Erro: "Cannot GET /api/v1/workflows"

**Causa:** n8n não está configurado para aceitar API calls ou URL incorreta.

**Solução:**
1. Verificar se `N8N_INSTANCE_URL` está correto
2. Confirmar que n8n está rodando
3. Verificar se API está habilitada no n8n

### Erro: "n8n API Error: 401"

**Causa:** API key inválida ou não configurada.

**Solução:**
1. Verificar `N8N_API_KEY` no arquivo .env
2. Gerar nova API key no n8n se necessário

### Workflows não executam

**Causa:** Workflows podem estar inativos ou com erros.

**Solução:**
1. Verificar se workflows estão ativos: `GET /api/n8n/workflows`
2. Verificar logs de execução: `GET /api/n8n/executions/:workflowId`
3. Recriar workflows: `POST /api/n8n/setup`

## Desenvolvimento

### Adicionando Novos Workflows

1. Criar definição do workflow em `api/n8n-client.js`
2. Adicionar ao método `createEssentialWorkflows()`
3. Testar com `node test-n8n-integration.js`
4. Documentar no README

### Testando Localmente

```bash
# Executar testes
npm test

# Testar integração específica
node test-n8n-integration.js

# Testar webhook específico
curl -X POST http://localhost:5678/webhook/regiflex-onboarding \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","email":"teste@teste.com","plano":"individual"}'
```

## Segurança

### Autenticação

- API key obrigatória para todas as chamadas
- Webhooks validados por assinatura
- HTTPS obrigatório em produção

### Dados Sensíveis

- Credenciais armazenadas em variáveis de ambiente
- Logs não expõem informações sensíveis
- Dados de clientes isolados por RLS

### Rate Limiting

- Webhooks limitados a 100 req/min por IP
- API calls limitadas a 1000 req/hora
- Retry automático com backoff exponencial

## Próximos Passos

1. **Integração WhatsApp:** Notificações via WhatsApp Business API
2. **IA Insights:** Análise automática de dados com OpenAI
3. **Backup Automático:** Backup diário de dados críticos
4. **Prevenção Churn:** Identificação automática de clientes em risco
5. **Relatórios Automáticos:** Geração semanal de relatórios executivos

## Suporte

Para dúvidas sobre a integração n8n:

1. Verificar logs dos workflows
2. Executar `node test-n8n-integration.js`
3. Consultar documentação oficial do n8n
4. Contatar: regiflex.contato@gmail.com
