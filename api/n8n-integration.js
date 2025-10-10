import express from 'express'
import { n8nClient, regiFlexWorkflows, testN8nConnection } from './n8n-client.js'

const router = express.Router()

/**
 * API de Integração n8n para RegiFlex
 * 
 * Endpoints para gerenciar workflows e automações
 */

/**
 * GET /api/n8n/status
 * Verificar status da conexão com n8n
 */
router.get('/status', async (req, res) => {
  try {
    const status = await testN8nConnection()
    res.json({
      success: true,
      n8n_status: status,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    })
  }
})

/**
 * GET /api/n8n/workflows
 * Listar todos os workflows
 */
router.get('/workflows', async (req, res) => {
  try {
    const workflows = await n8nClient.getWorkflows()
    res.json({
      success: true,
      workflows: workflows.data || workflows,
      count: workflows.data?.length || workflows.length || 0
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
})

/**
 * POST /api/n8n/setup
 * Configurar workflows essenciais do RegiFlex
 */
router.post('/setup', async (req, res) => {
  try {
    console.log('🚀 Iniciando setup dos workflows essenciais...')
    
    const results = await regiFlexWorkflows.createEssentialWorkflows()
    
    const successful = results.filter(r => !r.error)
    const failed = results.filter(r => r.error)
    
    res.json({
      success: true,
      message: 'Setup dos workflows concluído',
      results: {
        successful: successful.length,
        failed: failed.length,
        details: results
      },
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    })
  }
})

/**
 * POST /api/n8n/trigger/onboarding
 * Trigger manual do workflow de onboarding
 */
router.post('/trigger/onboarding', async (req, res) => {
  try {
    const clientData = req.body
    
    // Validar dados obrigatórios
    const required = ['nome', 'email', 'plano']
    const missing = required.filter(field => !clientData[field])
    
    if (missing.length > 0) {
      return res.status(400).json({
        success: false,
        error: `Campos obrigatórios faltando: ${missing.join(', ')}`
      })
    }
    
    // Trigger do webhook de onboarding
    const result = await n8nClient.triggerWebhook('regiflex-onboarding', clientData)
    
    res.json({
      success: true,
      message: 'Processo de onboarding iniciado',
      data: result,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    })
  }
})

/**
 * POST /api/n8n/webhook/stripe
 * Webhook para eventos do Stripe
 */
router.post('/webhook/stripe', async (req, res) => {
  try {
    const stripeEvent = req.body
    
    console.log('💳 Evento Stripe recebido:', stripeEvent.type)
    
    // Trigger do webhook de pagamentos
    const result = await n8nClient.triggerWebhook('stripe-webhook', stripeEvent)
    
    res.json({
      success: true,
      message: 'Evento Stripe processado',
      event_type: stripeEvent.type,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('❌ Erro ao processar webhook Stripe:', error)
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
})

/**
 * GET /api/n8n/executions/:workflowId
 * Obter execuções de um workflow
 */
router.get('/executions/:workflowId', async (req, res) => {
  try {
    const { workflowId } = req.params
    const limit = parseInt(req.query.limit) || 20
    
    const executions = await n8nClient.getExecutions(workflowId, limit)
    
    res.json({
      success: true,
      workflow_id: workflowId,
      executions: executions.data || executions,
      count: executions.data?.length || executions.length || 0
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
})

/**
 * POST /api/n8n/execute/:workflowId
 * Executar workflow manualmente
 */
router.post('/execute/:workflowId', async (req, res) => {
  try {
    const { workflowId } = req.params
    const data = req.body
    
    const result = await n8nClient.executeWorkflow(workflowId, data)
    
    res.json({
      success: true,
      workflow_id: workflowId,
      execution: result,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
})

/**
 * GET /api/n8n/health
 * Health check completo do sistema
 */
router.get('/health', async (req, res) => {
  try {
    const checks = {
      n8n: await testN8nConnection(),
      timestamp: new Date().toISOString()
    }
    
    // Verificar se há workflows ativos
    try {
      const workflows = await n8nClient.getWorkflows()
      checks.workflows = {
        total: workflows.data?.length || workflows.length || 0,
        active: workflows.data?.filter(w => w.active).length || 0
      }
    } catch (error) {
      checks.workflows = { error: error.message }
    }
    
    const isHealthy = checks.n8n.status === 'healthy'
    
    res.status(isHealthy ? 200 : 503).json({
      success: isHealthy,
      health: isHealthy ? 'healthy' : 'unhealthy',
      checks,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    res.status(503).json({
      success: false,
      health: 'unhealthy',
      error: error.message,
      timestamp: new Date().toISOString()
    })
  }
})

/**
 * Middleware de tratamento de erros
 */
router.use((error, req, res, next) => {
  console.error('❌ Erro na API n8n:', error)
  
  res.status(500).json({
    success: false,
    error: 'Erro interno do servidor',
    message: error.message,
    timestamp: new Date().toISOString()
  })
})

export default router

/**
 * Função para inicializar a integração n8n
 */
export async function initializeN8nIntegration() {
  try {
    console.log('🔧 Inicializando integração n8n...')
    
    // Testar conexão
    const status = await testN8nConnection()
    
    if (status.status !== 'healthy') {
      console.warn('⚠️ n8n não está acessível:', status)
      return false
    }
    
    console.log('✅ Conexão com n8n estabelecida')
    
    // Verificar se workflows já existem
    const workflows = await n8nClient.getWorkflows()
    const existingWorkflows = workflows.data || workflows
    
    const regiFlexWorkflows = existingWorkflows.filter(w => 
      w.name && w.name.startsWith('RegiFlex -')
    )
    
    console.log(`📋 Workflows RegiFlex encontrados: ${regiFlexWorkflows.length}`)
    
    if (regiFlexWorkflows.length === 0) {
      console.log('🚀 Criando workflows essenciais...')
      // Os workflows serão criados via endpoint /setup quando necessário
    }
    
    return true
  } catch (error) {
    console.error('❌ Erro ao inicializar n8n:', error.message)
    return false
  }
}
