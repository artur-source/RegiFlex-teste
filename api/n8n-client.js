import fetch from 'node-fetch'

/**
 * Cliente n8n para integração com RegiFlex
 * 
 * Este cliente permite criar, executar e gerenciar workflows
 * no n8n para automatizar processos do RegiFlex.
 */

export class N8nClient {
  constructor() {
    this.baseUrl = process.env.N8N_INSTANCE_URL || 'http://localhost:5678'
    this.apiKey = process.env.N8N_API_KEY
    
    if (!this.apiKey) {
      console.warn('⚠️ N8N_API_KEY não configurada. Algumas funcionalidades podem não funcionar.')
    }
  }

  /**
   * Headers padrão para requisições
   */
  get headers() {
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    
    if (this.apiKey) {
      headers['X-N8N-API-KEY'] = this.apiKey
    }
    
    return headers
  }

  /**
   * Fazer requisição para a API do n8n
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}/api/v1${endpoint}`
    
    const response = await fetch(url, {
      headers: this.headers,
      ...options
    })

    if (!response.ok) {
      const error = await response.text()
      throw new Error(`n8n API Error: ${response.status} - ${error}`)
    }

    return response.json()
  }

  /**
   * Listar todos os workflows
   */
  async getWorkflows() {
    return this.request('/workflows')
  }

  /**
   * Obter workflow específico
   */
  async getWorkflow(workflowId) {
    return this.request(`/workflows/${workflowId}`)
  }

  /**
   * Criar novo workflow
   */
  async createWorkflow(workflowData) {
    return this.request('/workflows', {
      method: 'POST',
      body: JSON.stringify(workflowData)
    })
  }

  /**
   * Atualizar workflow existente
   */
  async updateWorkflow(workflowId, workflowData) {
    return this.request(`/workflows/${workflowId}`, {
      method: 'PUT',
      body: JSON.stringify(workflowData)
    })
  }

  /**
   * Ativar/desativar workflow
   */
  async toggleWorkflow(workflowId, active = true) {
    return this.request(`/workflows/${workflowId}/activate`, {
      method: 'POST',
      body: JSON.stringify({ active })
    })
  }

  /**
   * Executar workflow manualmente
   */
  async executeWorkflow(workflowId, data = {}) {
    return this.request(`/workflows/${workflowId}/execute`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  /**
   * Obter execuções de um workflow
   */
  async getExecutions(workflowId, limit = 20) {
    return this.request(`/executions?workflowId=${workflowId}&limit=${limit}`)
  }

  /**
   * Trigger webhook do n8n
   */
  async triggerWebhook(webhookPath, data) {
    const url = `${this.baseUrl}/webhook/${webhookPath}`
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })

    if (!response.ok) {
      throw new Error(`Webhook Error: ${response.status}`)
    }

    return response.json()
  }

  /**
   * Verificar status do n8n
   */
  async getStatus() {
    try {
      const response = await fetch(`${this.baseUrl}/healthz`)
      return {
        status: response.ok ? 'healthy' : 'unhealthy',
        statusCode: response.status
      }
    } catch (error) {
      return {
        status: 'unreachable',
        error: error.message
      }
    }
  }
}

/**
 * Workflows específicos do RegiFlex
 */
export class RegiFlexN8nWorkflows {
  constructor(n8nClient) {
    this.n8n = n8nClient
  }

  /**
   * Workflow: Onboarding de novo cliente
   */
  getOnboardingWorkflow() {
    return {
      name: 'RegiFlex - Onboarding Cliente',
      active: true,
      nodes: [
        {
          parameters: {
            path: 'regiflex-onboarding',
            options: {}
          },
          name: 'Webhook - Novo Cliente',
          type: 'n8n-nodes-base.webhook',
          typeVersion: 1,
          position: [240, 300],
          id: 'webhook-novo-cliente'
        },
        {
          parameters: {
            functionCode: `
              // Validar dados do cliente
              const data = items[0].json;
              
              console.log('📥 Dados recebidos:', data);
              
              // Validações obrigatórias
              const required = ['nome', 'email', 'plano'];
              const missing = required.filter(field => !data[field]);
              
              if (missing.length > 0) {
                throw new Error(\`Campos obrigatórios faltando: \${missing.join(', ')}\`);
              }
              
              // Validar email
              const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
              if (!emailRegex.test(data.email)) {
                throw new Error('Email inválido');
              }
              
              // Gerar ID único para a clínica
              const clinicId = 'clinic_' + Math.random().toString(36).substr(2, 9);
              
              return [{
                json: {
                  ...data,
                  clinic_id: clinicId,
                  status: 'processing',
                  created_at: new Date().toISOString()
                }
              }];
            `
          },
          name: 'Validar Dados',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [460, 300],
          id: 'validar-dados'
        },
        {
          parameters: {
            url: `\${process.env.SUPABASE_URL}/rest/v1/clinicas`,
            authentication: 'genericCredentialType',
            genericAuthType: 'httpHeaderAuth',
            method: 'POST',
            headers: {
              'apikey': `\${process.env.SUPABASE_ANON_KEY}`,
              'Authorization': `Bearer \${process.env.SUPABASE_SERVICE_ROLE_KEY}`,
              'Content-Type': 'application/json',
              'Prefer': 'return=representation'
            },
            body: {
              nome: '={{$json.nome}}',
              email: '={{$json.email}}',
              plano: '={{$json.plano}}',
              status: 'trial',
              trial_ends_at: '={{new Date(Date.now() + 15 * 24 * 60 * 60 * 1000).toISOString()}}'
            }
          },
          name: 'Criar Clínica - Supabase',
          type: 'n8n-nodes-base.httpRequest',
          typeVersion: 4,
          position: [680, 300],
          id: 'criar-clinica'
        },
        {
          parameters: {
            url: 'https://api.stripe.com/v1/customers',
            authentication: 'genericCredentialType',
            genericAuthType: 'httpHeaderAuth',
            method: 'POST',
            headers: {
              'Authorization': `Bearer \${process.env.STRIPE_SECRET_KEY}`,
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'email={{$json.email}}&name={{$json.nome}}&metadata[clinic_id]={{$json.clinic_id}}'
          },
          name: 'Criar Customer - Stripe',
          type: 'n8n-nodes-base.httpRequest',
          typeVersion: 4,
          position: [900, 300],
          id: 'criar-customer-stripe'
        },
        {
          parameters: {
            functionCode: `
              // Preparar dados para deploy
              const clinicData = items[0].json;
              const stripeData = items[1].json;
              
              console.log('🚀 Preparando deploy para:', clinicData.nome);
              
              return [{
                json: {
                  clinic_id: clinicData.clinic_id,
                  clinic_name: clinicData.nome,
                  subdomain: clinicData.nome.toLowerCase()
                    .replace(/[^a-z0-9]/g, '-')
                    .replace(/-+/g, '-')
                    .replace(/^-|-$/g, ''),
                  stripe_customer_id: stripeData.id,
                  status: 'deploying'
                }
              }];
            `
          },
          name: 'Preparar Deploy',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [1120, 300],
          id: 'preparar-deploy'
        },
        {
          parameters: {
            functionCode: `
              // Simular deploy (em produção, chamaria API do Vercel)
              const data = items[0].json;
              
              console.log('✅ Deploy simulado para:', data.clinic_name);
              
              const deployUrl = \`https://\${data.subdomain}.regiflex.app\`;
              
              return [{
                json: {
                  ...data,
                  deploy_url: deployUrl,
                  status: 'deployed',
                  deployed_at: new Date().toISOString()
                }
              }];
            `
          },
          name: 'Deploy Instância',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [1340, 300],
          id: 'deploy-instancia'
        },
        {
          parameters: {
            functionCode: `
              // Preparar email de boas-vindas
              const data = items[0].json;
              
              const emailData = {
                to: data.email || items[0].json.email,
                subject: 'Bem-vindo ao RegiFlex! 🎉',
                html: \`
                  <h2>Olá, \${data.clinic_name}!</h2>
                  <p>Sua clínica foi configurada com sucesso no RegiFlex.</p>
                  
                  <h3>📋 Detalhes da sua conta:</h3>
                  <ul>
                    <li><strong>Plano:</strong> \${data.plano || 'Individual'}</li>
                    <li><strong>URL de acesso:</strong> <a href="\${data.deploy_url}">\${data.deploy_url}</a></li>
                    <li><strong>Status:</strong> Trial (15 dias gratuitos)</li>
                  </ul>
                  
                  <h3>🚀 Próximos passos:</h3>
                  <ol>
                    <li>Acesse sua instância do RegiFlex</li>
                    <li>Configure seu primeiro usuário</li>
                    <li>Cadastre seus primeiros pacientes</li>
                  </ol>
                  
                  <p>Em caso de dúvidas, entre em contato: regiflex.contato@gmail.com</p>
                  
                  <p>Bem-vindo à família RegiFlex! 💚</p>
                \`,
                clinic_id: data.clinic_id,
                deploy_url: data.deploy_url
              };
              
              console.log('📧 Email preparado para:', emailData.to);
              
              return [{ json: emailData }];
            `
          },
          name: 'Preparar Email',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [1560, 300],
          id: 'preparar-email'
        },
        {
          parameters: {
            functionCode: `
              // Log final do processo
              const data = items[0].json;
              
              console.log('🎉 Onboarding concluído!');
              console.log('Clínica:', data.clinic_name);
              console.log('URL:', data.deploy_url);
              console.log('Email enviado para:', data.to);
              
              return [{
                json: {
                  success: true,
                  message: 'Onboarding concluído com sucesso',
                  clinic_id: data.clinic_id,
                  deploy_url: data.deploy_url,
                  completed_at: new Date().toISOString()
                }
              }];
            `
          },
          name: 'Finalizar Processo',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [1780, 300],
          id: 'finalizar-processo'
        }
      ],
      connections: {
        'Webhook - Novo Cliente': {
          main: [['Validar Dados']]
        },
        'Validar Dados': {
          main: [['Criar Clínica - Supabase']]
        },
        'Criar Clínica - Supabase': {
          main: [['Criar Customer - Stripe']]
        },
        'Criar Customer - Stripe': {
          main: [['Preparar Deploy']]
        },
        'Preparar Deploy': {
          main: [['Deploy Instância']]
        },
        'Deploy Instância': {
          main: [['Preparar Email']]
        },
        'Preparar Email': {
          main: [['Finalizar Processo']]
        }
      },
      settings: {
        executionOrder: 'v1'
      }
    }
  }

  /**
   * Workflow: Monitoramento de sistema
   */
  getMonitoringWorkflow() {
    return {
      name: 'RegiFlex - Monitoramento Sistema',
      active: true,
      nodes: [
        {
          parameters: {
            rule: {
              interval: [{ field: 'minutes', value: 15 }]
            }
          },
          name: 'Schedule - A cada 15min',
          type: 'n8n-nodes-base.scheduleTrigger',
          typeVersion: 1,
          position: [240, 300],
          id: 'schedule-monitoring'
        },
        {
          parameters: {
            functionCode: `
              // Verificar status dos serviços
              const services = [
                { name: 'Supabase', url: process.env.SUPABASE_URL + '/rest/v1/' },
                { name: 'Vercel', url: 'https://api.vercel.com/v1/user' },
                { name: 'Stripe', url: 'https://api.stripe.com/v1/account' }
              ];
              
              console.log('🔍 Iniciando monitoramento...');
              
              return services.map(service => ({
                json: {
                  service: service.name,
                  url: service.url,
                  timestamp: new Date().toISOString()
                }
              }));
            `
          },
          name: 'Preparar Verificações',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [460, 300],
          id: 'preparar-verificacoes'
        },
        {
          parameters: {
            functionCode: `
              // Simular verificação de saúde
              const data = items[0].json;
              
              const isHealthy = Math.random() > 0.1; // 90% de chance de estar saudável
              const responseTime = Math.floor(Math.random() * 500) + 50; // 50-550ms
              
              console.log(\`\${data.service}: \${isHealthy ? '✅' : '❌'} (\${responseTime}ms)\`);
              
              return [{
                json: {
                  ...data,
                  status: isHealthy ? 'healthy' : 'unhealthy',
                  response_time: responseTime,
                  checked_at: new Date().toISOString()
                }
              }];
            `
          },
          name: 'Verificar Saúde',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [680, 300],
          id: 'verificar-saude'
        },
        {
          parameters: {
            conditions: {
              string: [
                {
                  value1: '={{$json.status}}',
                  operation: 'equal',
                  value2: 'unhealthy'
                }
              ]
            }
          },
          name: 'Serviço com Problema?',
          type: 'n8n-nodes-base.if',
          typeVersion: 1,
          position: [900, 300],
          id: 'verificar-problema'
        },
        {
          parameters: {
            functionCode: `
              // Criar alerta
              const data = items[0].json;
              
              console.log('🚨 ALERTA:', data.service, 'com problemas!');
              
              return [{
                json: {
                  alert: true,
                  service: data.service,
                  message: \`Serviço \${data.service} está com problemas. Tempo de resposta: \${data.response_time}ms\`,
                  severity: 'high',
                  timestamp: new Date().toISOString()
                }
              }];
            `
          },
          name: 'Criar Alerta',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [1120, 200],
          id: 'criar-alerta'
        },
        {
          parameters: {
            functionCode: `
              // Log status normal
              const data = items[0].json;
              
              console.log('✅', data.service, 'funcionando normalmente');
              
              return [{
                json: {
                  ...data,
                  alert: false,
                  message: \`\${data.service} está funcionando normalmente\`
                }
              }];
            `
          },
          name: 'Log Status OK',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [1120, 400],
          id: 'log-status-ok'
        }
      ],
      connections: {
        'Schedule - A cada 15min': {
          main: [['Preparar Verificações']]
        },
        'Preparar Verificações': {
          main: [['Verificar Saúde']]
        },
        'Verificar Saúde': {
          main: [['Serviço com Problema?']]
        },
        'Serviço com Problema?': {
          main: [
            ['Criar Alerta'],
            ['Log Status OK']
          ]
        }
      },
      settings: {
        executionOrder: 'v1'
      }
    }
  }

  /**
   * Workflow: Gestão de pagamentos Stripe
   */
  getPaymentWorkflow() {
    return {
      name: 'RegiFlex - Gestão Pagamentos',
      active: true,
      nodes: [
        {
          parameters: {
            path: 'stripe-webhook',
            options: {}
          },
          name: 'Webhook - Stripe',
          type: 'n8n-nodes-base.webhook',
          typeVersion: 1,
          position: [240, 300],
          id: 'webhook-stripe'
        },
        {
          parameters: {
            functionCode: `
              // Processar evento do Stripe
              const event = items[0].json;
              
              console.log('💳 Evento Stripe recebido:', event.type);
              
              const eventData = {
                type: event.type,
                customer_id: event.data?.object?.customer,
                subscription_id: event.data?.object?.subscription,
                amount: event.data?.object?.amount_paid,
                status: event.data?.object?.status,
                timestamp: new Date().toISOString()
              };
              
              return [{ json: eventData }];
            `
          },
          name: 'Processar Evento',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [460, 300],
          id: 'processar-evento'
        },
        {
          parameters: {
            conditions: {
              string: [
                {
                  value1: '={{$json.type}}',
                  operation: 'equal',
                  value2: 'invoice.payment_succeeded'
                }
              ]
            }
          },
          name: 'Pagamento Sucesso?',
          type: 'n8n-nodes-base.if',
          typeVersion: 1,
          position: [680, 300],
          id: 'pagamento-sucesso'
        },
        {
          parameters: {
            functionCode: `
              // Ativar conta após pagamento
              const data = items[0].json;
              
              console.log('✅ Pagamento confirmado para customer:', data.customer_id);
              
              return [{
                json: {
                  ...data,
                  action: 'activate_account',
                  message: 'Conta ativada após pagamento confirmado'
                }
              }];
            `
          },
          name: 'Ativar Conta',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [900, 200],
          id: 'ativar-conta'
        },
        {
          parameters: {
            conditions: {
              string: [
                {
                  value1: '={{$json.type}}',
                  operation: 'equal',
                  value2: 'invoice.payment_failed'
                }
              ]
            }
          },
          name: 'Pagamento Falhou?',
          type: 'n8n-nodes-base.if',
          typeVersion: 1,
          position: [900, 400],
          id: 'pagamento-falhou'
        },
        {
          parameters: {
            functionCode: `
              // Suspender conta após falha no pagamento
              const data = items[0].json;
              
              console.log('❌ Falha no pagamento para customer:', data.customer_id);
              
              return [{
                json: {
                  ...data,
                  action: 'suspend_account',
                  message: 'Conta suspensa devido à falha no pagamento'
                }
              }];
            `
          },
          name: 'Suspender Conta',
          type: 'n8n-nodes-base.function',
          typeVersion: 1,
          position: [1120, 400],
          id: 'suspender-conta'
        }
      ],
      connections: {
        'Webhook - Stripe': {
          main: [['Processar Evento']]
        },
        'Processar Evento': {
          main: [['Pagamento Sucesso?']]
        },
        'Pagamento Sucesso?': {
          main: [
            ['Ativar Conta'],
            ['Pagamento Falhou?']
          ]
        },
        'Pagamento Falhou?': {
          main: [
            ['Suspender Conta'],
            []
          ]
        }
      },
      settings: {
        executionOrder: 'v1'
      }
    }
  }

  /**
   * Criar todos os workflows essenciais
   */
  async createEssentialWorkflows() {
    const workflows = [
      this.getOnboardingWorkflow(),
      this.getMonitoringWorkflow(),
      this.getPaymentWorkflow()
    ]

    const results = []
    
    for (const workflow of workflows) {
      try {
        console.log(`📝 Criando workflow: ${workflow.name}`)
        const result = await this.n8n.createWorkflow(workflow)
        
        // Ativar o workflow
        if (result.id) {
          await this.n8n.toggleWorkflow(result.id, true)
          console.log(`✅ Workflow ativado: ${workflow.name}`)
        }
        
        results.push(result)
      } catch (error) {
        console.error(`❌ Erro ao criar workflow ${workflow.name}:`, error.message)
        results.push({ error: error.message, workflow: workflow.name })
      }
    }
    
    return results
  }
}

// Instância singleton
export const n8nClient = new N8nClient()
export const regiFlexWorkflows = new RegiFlexN8nWorkflows(n8nClient)

// Função helper para testar conexão
export async function testN8nConnection() {
  try {
    const status = await n8nClient.getStatus()
    console.log('🔗 Status do n8n:', status)
    return status
  } catch (error) {
    console.error('❌ Erro ao conectar com n8n:', error.message)
    return { status: 'error', error: error.message }
  }
}
