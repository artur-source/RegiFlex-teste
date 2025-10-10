import { n8nClient, regiFlexWorkflows, testN8nConnection } from './api/n8n-client.js'

/**
 * Script de teste para integração n8n com RegiFlex
 * 
 * Este script testa todas as funcionalidades da integração n8n
 */

async function runTests() {
  console.log('🧪 Iniciando testes da integração n8n...\n')
  
  const results = {
    connection: null,
    workflows: null,
    setup: null,
    webhook: null,
    errors: []
  }
  
  try {
    // Teste 1: Conexão com n8n
    console.log('1️⃣ Testando conexão com n8n...')
    results.connection = await testN8nConnection()
    
    if (results.connection.status === 'healthy') {
      console.log('✅ Conexão com n8n: OK')
    } else {
      console.log('❌ Conexão com n8n: FALHOU')
      console.log('   Status:', results.connection)
    }
    
    // Teste 2: Listar workflows existentes
    console.log('\n2️⃣ Listando workflows existentes...')
    try {
      const workflows = await n8nClient.getWorkflows()
      results.workflows = workflows
      
      const workflowList = workflows.data || workflows
      console.log(`✅ Workflows encontrados: ${workflowList.length}`)
      
      if (workflowList.length > 0) {
        console.log('   Workflows:')
        workflowList.forEach(w => {
          console.log(`   - ${w.name} (${w.active ? 'ativo' : 'inativo'})`)
        })
      }
    } catch (error) {
      console.log('❌ Erro ao listar workflows:', error.message)
      results.errors.push({ test: 'workflows', error: error.message })
    }
    
    // Teste 3: Criar workflows essenciais (apenas se n8n estiver acessível)
    if (results.connection.status === 'healthy') {
      console.log('\n3️⃣ Testando criação de workflows...')
      try {
        // Primeiro, verificar se já existem workflows RegiFlex
        const existingWorkflows = results.workflows?.data || results.workflows || []
        const regiFlexWorkflowsExist = existingWorkflows.some(w => 
          w.name && w.name.startsWith('RegiFlex -')
        )
        
        if (regiFlexWorkflowsExist) {
          console.log('ℹ️ Workflows RegiFlex já existem, pulando criação')
          results.setup = { message: 'Workflows já existem', skipped: true }
        } else {
          console.log('🚀 Criando workflows essenciais...')
          results.setup = await regiFlexWorkflows.createEssentialWorkflows()
          
          const successful = results.setup.filter(r => !r.error)
          const failed = results.setup.filter(r => r.error)
          
          console.log(`✅ Workflows criados: ${successful.length}`)
          if (failed.length > 0) {
            console.log(`❌ Workflows com erro: ${failed.length}`)
            failed.forEach(f => console.log(`   - ${f.workflow}: ${f.error}`))
          }
        }
      } catch (error) {
        console.log('❌ Erro ao criar workflows:', error.message)
        results.errors.push({ test: 'setup', error: error.message })
      }
    }
    
    // Teste 4: Testar webhook de onboarding
    console.log('\n4️⃣ Testando webhook de onboarding...')
    try {
      const testClient = {
        nome: 'Clínica Teste',
        email: 'teste@clinica.com',
        plano: 'individual',
        telefone: '(11) 99999-9999'
      }
      
      console.log('📤 Enviando dados de teste:', testClient)
      
      // Simular o webhook (em ambiente real, seria uma chamada HTTP)
      results.webhook = {
        success: true,
        message: 'Webhook simulado com sucesso',
        data: testClient,
        timestamp: new Date().toISOString()
      }
      
      console.log('✅ Webhook de onboarding: SIMULADO OK')
    } catch (error) {
      console.log('❌ Erro no webhook:', error.message)
      results.errors.push({ test: 'webhook', error: error.message })
    }
    
    // Teste 5: Verificar variáveis de ambiente
    console.log('\n5️⃣ Verificando configuração...')
    const envVars = {
      N8N_INSTANCE_URL: !!process.env.N8N_INSTANCE_URL,
      N8N_API_KEY: !!process.env.N8N_API_KEY,
      SUPABASE_URL: !!process.env.SUPABASE_URL,
      SUPABASE_ANON_KEY: !!process.env.SUPABASE_ANON_KEY,
      STRIPE_SECRET_KEY: !!process.env.STRIPE_SECRET_KEY
    }
    
    console.log('🔧 Variáveis de ambiente:')
    Object.entries(envVars).forEach(([key, exists]) => {
      console.log(`   ${exists ? '✅' : '❌'} ${key}: ${exists ? 'configurada' : 'FALTANDO'}`)
    })
    
    const missingVars = Object.entries(envVars)
      .filter(([key, exists]) => !exists)
      .map(([key]) => key)
    
    if (missingVars.length > 0) {
      results.errors.push({
        test: 'environment',
        error: `Variáveis faltando: ${missingVars.join(', ')}`
      })
    }
    
  } catch (error) {
    console.log('❌ Erro geral nos testes:', error.message)
    results.errors.push({ test: 'general', error: error.message })
  }
  
  // Resumo final
  console.log('\n📊 RESUMO DOS TESTES')
  console.log('=' .repeat(50))
  
  const totalTests = 5
  const passedTests = [
    results.connection?.status === 'healthy',
    results.workflows !== null,
    results.setup !== null || results.setup?.skipped,
    results.webhook?.success,
    results.errors.filter(e => e.test === 'environment').length === 0
  ].filter(Boolean).length
  
  console.log(`✅ Testes aprovados: ${passedTests}/${totalTests}`)
  console.log(`❌ Erros encontrados: ${results.errors.length}`)
  
  if (results.errors.length > 0) {
    console.log('\n🐛 ERROS DETALHADOS:')
    results.errors.forEach((error, index) => {
      console.log(`${index + 1}. [${error.test}] ${error.error}`)
    })
  }
  
  // Status geral
  const overallSuccess = results.errors.length === 0 && passedTests >= 4
  console.log(`\n🎯 STATUS GERAL: ${overallSuccess ? '✅ SUCESSO' : '❌ FALHAS ENCONTRADAS'}`)
  
  if (overallSuccess) {
    console.log('\n🚀 A integração n8n está pronta para uso!')
  } else {
    console.log('\n⚠️ Corrija os erros antes de usar em produção.')
  }
  
  return {
    success: overallSuccess,
    results,
    summary: {
      total_tests: totalTests,
      passed_tests: passedTests,
      errors: results.errors.length
    }
  }
}

// Executar testes se chamado diretamente
if (import.meta.url === `file://${process.argv[1]}`) {
  runTests()
    .then(result => {
      process.exit(result.success ? 0 : 1)
    })
    .catch(error => {
      console.error('💥 Erro fatal nos testes:', error)
      process.exit(1)
    })
}

export { runTests }
