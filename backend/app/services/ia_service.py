from app.models.sessao import Sessao
from app.models.paciente import Paciente
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import func

class IAService:
    """Serviço para funcionalidades de IA leve e análise de dados."""
    
    @staticmethod
    def analisar_frequencia_paciente(paciente_id, dias=30):
        """
        Analisa a frequência de sessões de um paciente nos últimos N dias.
        Retorna alertas se a frequência estiver abaixo do esperado.
        """
        try:
            data_inicio = datetime.now() - timedelta(days=dias)
            
            # Buscar sessões do paciente no período
            sessoes = Sessao.query.filter(
                Sessao.paciente_id == paciente_id,
                Sessao.data_hora >= data_inicio,
                Sessao.status.in_(['agendada', 'realizada'])
            ).all()
            
            total_sessoes = len(sessoes)
            sessoes_realizadas = len([s for s in sessoes if s.status == 'realizada'])
            
            # Análise básica
            frequencia_semanal = total_sessoes / (dias / 7)
            taxa_comparecimento = (sessoes_realizadas / total_sessoes * 100) if total_sessoes > 0 else 0
            
            alertas = []
            
            # Alertas de frequência
            if frequencia_semanal < 1:
                alertas.append({
                    'tipo': 'frequencia_baixa',
                    'severidade': 'media',
                    'mensagem': f'Paciente com baixa frequência: {frequencia_semanal:.1f} sessões por semana'
                })
            
            # Alertas de comparecimento
            if taxa_comparecimento < 70 and total_sessoes > 2:
                alertas.append({
                    'tipo': 'baixo_comparecimento',
                    'severidade': 'alta',
                    'mensagem': f'Taxa de comparecimento baixa: {taxa_comparecimento:.1f}%'
                })
            
            return {
                'paciente_id': paciente_id,
                'periodo_dias': dias,
                'total_sessoes': total_sessoes,
                'sessoes_realizadas': sessoes_realizadas,
                'frequencia_semanal': round(frequencia_semanal, 2),
                'taxa_comparecimento': round(taxa_comparecimento, 2),
                'alertas': alertas
            }
            
        except Exception as e:
            return {
                'erro': f'Erro na análise de frequência: {str(e)}',
                'paciente_id': paciente_id
            }
    
    @staticmethod
    def detectar_padroes_cancelamento(psicologo_id=None, dias=60):
        """
        Detecta padrões de cancelamento de sessões.
        Pode ser filtrado por psicólogo específico.
        """
        try:
            data_inicio = datetime.now() - timedelta(days=dias)
            
            # Query base
            query = Sessao.query.filter(
                Sessao.data_hora >= data_inicio,
                Sessao.status == 'cancelada'
            )
            
            if psicologo_id:
                query = query.filter(Sessao.psicologo_id == psicologo_id)
            
            sessoes_canceladas = query.all()
            
            if not sessoes_canceladas:
                return {
                    'total_cancelamentos': 0,
                    'padroes': [],
                    'recomendacoes': []
                }
            
            # Converter para DataFrame para análise
            data = []
            for sessao in sessoes_canceladas:
                data.append({
                    'paciente_id': sessao.paciente_id,
                    'psicologo_id': sessao.psicologo_id,
                    'dia_semana': sessao.data_hora.weekday(),
                    'hora': sessao.data_hora.hour,
                    'data': sessao.data_hora.date()
                })
            
            df = pd.DataFrame(data)
            
            # Análise de padrões
            padroes = []
            
            # Padrão por dia da semana
            cancelamentos_por_dia = df['dia_semana'].value_counts()
            if len(cancelamentos_por_dia) > 0:
                dia_mais_cancelado = cancelamentos_por_dia.index[0]
                dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
                padroes.append({
                    'tipo': 'dia_semana',
                    'descricao': f'Maior número de cancelamentos às {dias_semana[dia_mais_cancelado]}s',
                    'valor': int(cancelamentos_por_dia.iloc[0])
                })
            
            # Padrão por horário
            cancelamentos_por_hora = df['hora'].value_counts()
            if len(cancelamentos_por_hora) > 0:
                hora_mais_cancelada = cancelamentos_por_hora.index[0]
                padroes.append({
                    'tipo': 'horario',
                    'descricao': f'Maior número de cancelamentos às {hora_mais_cancelada}h',
                    'valor': int(cancelamentos_por_hora.iloc[0])
                })
            
            # Pacientes com mais cancelamentos
            cancelamentos_por_paciente = df['paciente_id'].value_counts()
            pacientes_problema = cancelamentos_por_paciente[cancelamentos_por_paciente >= 3]
            
            recomendacoes = []
            if len(pacientes_problema) > 0:
                recomendacoes.append({
                    'tipo': 'pacientes_frequentes',
                    'descricao': f'{len(pacientes_problema)} paciente(s) com 3+ cancelamentos',
                    'acao': 'Considerar conversa sobre compromisso com o tratamento'
                })
            
            return {
                'total_cancelamentos': len(sessoes_canceladas),
                'periodo_dias': dias,
                'padroes': padroes,
                'recomendacoes': recomendacoes
            }
            
        except Exception as e:
            return {
                'erro': f'Erro na análise de cancelamentos: {str(e)}'
            }
    
    @staticmethod
    def gerar_alertas_dashboard(psicologo_id=None):
        """
        Gera alertas para o dashboard baseados em análises de IA.
        """
        try:
            alertas = []
            
            # Análise de cancelamentos
            analise_cancelamentos = IAService.detectar_padroes_cancelamento(psicologo_id, dias=30)
            
            if analise_cancelamentos.get('total_cancelamentos', 0) > 5:
                alertas.append({
                    'tipo': 'cancelamentos_altos',
                    'severidade': 'media',
                    'titulo': 'Alto número de cancelamentos',
                    'mensagem': f'{analise_cancelamentos["total_cancelamentos"]} cancelamentos nos últimos 30 dias',
                    'acao': 'Revisar padrões de agendamento'
                })
            
            # Análise de sessões próximas sem confirmação
            hoje = datetime.now()
            amanha = hoje + timedelta(days=1)
            
            query = Sessao.query.filter(
                Sessao.data_hora >= hoje,
                Sessao.data_hora <= amanha,
                Sessao.status == 'agendada'
            )
            
            if psicologo_id:
                query = query.filter(Sessao.psicologo_id == psicologo_id)
            
            sessoes_proximas = query.count()
            
            if sessoes_proximas > 0:
                alertas.append({
                    'tipo': 'sessoes_proximas',
                    'severidade': 'baixa',
                    'titulo': 'Sessões próximas',
                    'mensagem': f'{sessoes_proximas} sessão(ões) agendada(s) para amanhã',
                    'acao': 'Confirmar presença dos pacientes'
                })
            
            return alertas
            
        except Exception as e:
            return [{
                'tipo': 'erro_sistema',
                'severidade': 'alta',
                'titulo': 'Erro no sistema de alertas',
                'mensagem': f'Erro: {str(e)}',
                'acao': 'Contatar suporte técnico'
            }]
