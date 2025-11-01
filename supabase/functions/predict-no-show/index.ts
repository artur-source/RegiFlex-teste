import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

// IA: O cliente Supabase foi inicializado para interagir com o banco de dados.
// Inicializa o cliente Supabase
const supabase = createClient(
  Deno.env.get("SUPABASE_URL") ?? "",
  Deno.env.get("SUPABASE_ANON_KEY") ?? ""
)

serve(async (req) => {
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" },
    })
  }

  try {
    const { session_id } = await req.json()

    if (!session_id) {
      return new Response(JSON.stringify({ error: "Missing session_id" }), {
        status: 400,
        headers: { "Content-Type": "application/json" },
      })
    }

    // 1. Buscar dados da sessão no Supabase
    const { data: sessionData, error: sessionError } = await supabase
      .from("sessoes")
      .select("data_hora, created_at, duracao_minutos")
      .eq("id", session_id)
      .single()

    if (sessionError || !sessionData) {
      console.error("Error fetching session data:", sessionError?.message)
      return new Response(JSON.stringify({ error: "Session not found or database error" }), {
        status: 404,
        headers: { "Content-Type": "application/json" },
      })
    }

    // 2. Pré-processamento e Feature Engineering
    const dataHora = new Date(sessionData.data_hora)
    const createdAt = new Date(sessionData.created_at)

    // Calcula a diferença em dias (antecedência)
    const diffTime = Math.abs(dataHora.getTime() - createdAt.getTime())
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    const features = {
      dia_da_semana: dataHora.getDay(), // 0 (Dom) a 6 (Sáb)
      hora_do_dia: dataHora.getHours(),
      antecedencia_agendamento: diffDays,
      duracao_minutos: sessionData.duracao_minutos,
    }

    // 3. Simulação de Predição de IA (Modelo treinado em Python não pode ser importado diretamente)
    // IA: Esta seção simula a lógica de predição de risco de no-show. O modelo original foi treinado em Python, e esta é uma adaptação em TypeScript para a Edge Function.
    // Artur: A IA fez um bom trabalho em replicar a lógica do modelo. Vamos testar a acurácia.
    // Guilherme: A IA poderia sugerir melhorias para este modelo? Por exemplo, usar mais features?
    // IA: Sim, podemos adicionar features como o histórico de no-shows do paciente e a sazonalidade (mês do ano). Isso pode melhorar a acurácia do modelo.
    // Em um cenário real, o modelo seria re-implementado em JS/TS ou acessado via um serviço externo.
    // Para fins de demonstração, simularemos uma Regressão Logística simples baseada nas features.
    
    // Simulação de risco: Maior risco se for agendado com pouca antecedência,
    // em um final de semana (0 ou 6), ou em horários de pico.
    let risk_score = 0
    
    // Peso para antecedência (menos dias = mais risco)
    risk_score += Math.max(0, 10 - features.antecedencia_agendamento) * 0.1

    // Peso para dia da semana (fim de semana tem mais risco)
    if (features.dia_da_semana === 0 || features.dia_da_semana === 6) {
      risk_score += 0.5
    }
    
    // Peso para horário (fora do horário comercial tem mais risco)
    if (features.hora_do_dia < 9 || features.hora_do_dia > 18) {
      risk_score += 0.3
    }
    
    // Normaliza o score para um percentual de 0 a 100
    const risk_percentage = Math.min(100, Math.round(risk_score * 10))

    const is_high_risk = risk_percentage > 50

    const prediction_result = {
      session_id: session_id,
      risk_percentage: risk_percentage,
      is_high_risk: is_high_risk,
      features_used: features,
      alert_message: is_high_risk
        ? `ALERTA: Alto risco de no-show (${risk_percentage}%). Considere um lembrete.`
        : `Risco de no-show baixo (${risk_percentage}%).`,
    }

    // 4. Retornar o resultado
    return new Response(JSON.stringify(prediction_result), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })
  } catch (error) {
    console.error(error)
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    })
  }
})
