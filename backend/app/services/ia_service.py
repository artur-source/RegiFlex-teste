from app.models.sessao import Sessao
from app.models.paciente import Paciente
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy import func
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pickle
import os
import json
from pathlib import Path

class IAService:
    """
    Serviço aprimorado para funcionalidades de IA leve e análise de dados.
    Incorpora aprendizado incremental, análise adaptativa e insights preditivos.
    """
    
    # Diretório para cache e modelos
    CACHE_DIR = Path(__file__).parent.parent.parent / 'cache'
    MODEL_DIR = CACHE_DIR / 'models'
    STATS_FILE = CACHE_DIR / 'stats.json'
    
    def __init__(self):
        """Inicializa diretórios de cache e modelos."""
        self.CACHE_DIR.mkdir(exist_ok=True)
        self.MODEL_DIR.mkdir(exist_ok=True)
    
    # ========== ANÁLISE DE FREQUÊNCIA INTELIGENTE ==========
    
    @staticmethod
    def analisar_frequencia_paciente(paciente_id, dias=30):
        """
        Analisa a frequência de sessões de um paciente nos últimos N dias.
        Inclui detecção de variação de frequência e índice de engajamento.
        
        Args:
            paciente_id: ID do paciente
            dias: Período de análise em dias (padrão: 30)
            
        Returns:
            dict: Análise completa com alertas, tendências e índice de engajamento
        """
        try:
            data_inicio = datetime.now() - timedelta(days=dias)
            
            # Buscar sessões do paciente no período
            sessoes = Sessao.query.filter(
                Sessao.paciente_id == paciente_id,
                Sessao.data_hora >= data_inicio,
                Sessao.status.in_(['agendada', 'realizada'])
            ).order_by(Sessao.data_hora).all()
            
            total_sessoes = len(sessoes)
            sessoes_realizadas = len([s for s in sessoes if s.status == 'realizada'])
            
            # Análise básica
            frequencia_semanal = total_sessoes / (dias / 7)
            taxa_comparecimento = (sessoes_realizadas / total_sessoes * 100) if total_sessoes > 0 else 0
            
            # === NOVO: Detecção de variação de frequência ===
            variacao_frequencia = IAService._calcular_variacao_frequencia(sessoes, dias)
            
            # === NOVO: Índice de engajamento (0-100) ===
            # Fórmula: (taxa_comparecimento * 0.6) + (frequência_semanal_normalizada * 0.4)
            frequencia_normalizada = min(frequencia_semanal / 2 * 100, 100)  # Normalizar para 0-100 (2 sessões/semana = 100)
            indice_engajamento = (taxa_comparecimento * 0.6) + (frequencia_normalizada * 0.4)
            
            alertas = []
            
            # Alertas de frequência
            if frequencia_semanal < 1:
                alertas.append({
                    'tipo': 'frequencia_baixa',
                    'severidade': 'media',
                    'confianca': 'alta',
                    'mensagem': f'Paciente com baixa frequência: {frequencia_semanal:.1f} sessões por semana'
                })
            
            # Alertas de comparecimento
            if taxa_comparecimento < 70 and total_sessoes > 2:
                alertas.append({
                    'tipo': 'baixo_comparecimento',
                    'severidade': 'alta',
                    'confianca': 'alta',
                    'mensagem': f'Taxa de comparecimento baixa: {taxa_comparecimento:.1f}%'
                })
            
            # === NOVO: Alertas de tendência ===
            if variacao_frequencia['tendencia'] == 'queda':
                alertas.append({
                    'tipo': 'tendencia_queda',
                    'severidade': 'alta',
                    'confianca': 'media',
                    'mensagem': f'Queda na assiduidade: {variacao_frequencia["variacao_percentual"]:.1f}% nas últimas semanas'
                })
            elif variacao_frequencia['tendencia'] == 'melhora':
                alertas.append({
                    'tipo': 'tendencia_melhora',
                    'severidade': 'baixa',
                    'confianca': 'media',
                    'mensagem': f'Melhora na assiduidade: {variacao_frequencia["variacao_percentual"]:.1f}% nas últimas semanas'
                })
            
            # === NOVO: Alerta de índice de engajamento baixo ===
            if indice_engajamento < 50:
                alertas.append({
                    'tipo': 'engajamento_baixo',
                    'severidade': 'alta',
                    'confianca': 'alta',
                    'mensagem': f'Índice de engajamento baixo: {indice_engajamento:.1f}/100'
                })
            
            return {
                'paciente_id': paciente_id,
                'periodo_dias': dias,
                'total_sessoes': total_sessoes,
                'sessoes_realizadas': sessoes_realizadas,
                'frequencia_semanal': round(frequencia_semanal, 2),
                'taxa_comparecimento': round(taxa_comparecimento, 2),
                'indice_engajamento': round(indice_engajamento, 2),
                'variacao_frequencia': variacao_frequencia,
                'alertas': alertas
            }
            
        except Exception as e:
            return {
                'erro': f'Erro na análise de frequência: {str(e)}',
                'paciente_id': paciente_id
            }
    
    @staticmethod
    def _calcular_variacao_frequencia(sessoes, dias_totais):
        """
        Calcula a variação de frequência comparando semanas consecutivas.
        
        Args:
            sessoes: Lista de sessões ordenadas por data
            dias_totais: Total de dias do período de análise
            
        Returns:
            dict: Informações sobre variação e tendência
        """
        if len(sessoes) < 2:
            return {
                'tendencia': 'estavel',
                'variacao_percentual': 0,
                'semanas_comparadas': 0
            }
        
        # Dividir sessões em semanas
        df = pd.DataFrame([{
            'data': s.data_hora.date(),
            'semana': (datetime.now().date() - s.data_hora.date()).days // 7
        } for s in sessoes])
        
        # Contar sessões por semana
        sessoes_por_semana = df.groupby('semana').size()
        
        if len(sessoes_por_semana) < 2:
            return {
                'tendencia': 'estavel',
                'variacao_percentual': 0,
                'semanas_comparadas': len(sessoes_por_semana)
            }
        
        # Comparar últimas 2 semanas
        semanas_ordenadas = sorted(sessoes_por_semana.index)
        ultima_semana = sessoes_por_semana[semanas_ordenadas[0]]
        penultima_semana = sessoes_por_semana[semanas_ordenadas[1]]
        
        variacao = ((ultima_semana - penultima_semana) / penultima_semana * 100) if penultima_semana > 0 else 0
        
        if variacao < -20:
            tendencia = 'queda'
        elif variacao > 20:
            tendencia = 'melhora'
        else:
            tendencia = 'estavel'
        
        return {
            'tendencia': tendencia,
            'variacao_percentual': round(abs(variacao), 2),
            'semanas_comparadas': len(sessoes_por_semana),
            'ultima_semana_sessoes': int(ultima_semana),
            'penultima_semana_sessoes': int(penultima_semana)
        }
    
    # ========== PADRÕES DE CANCELAMENTO COM K-MEANS ==========
    
    @staticmethod
    def detectar_padroes_cancelamento(psicologo_id=None, dias=60, usar_cache=True):
        """
        Detecta padrões de cancelamento usando K-Means clustering.
        Identifica clusters de cancelamentos por horários, dias e psicólogos.
        
        Args:
            psicologo_id: ID do psicólogo (opcional)
            dias: Período de análise em dias
            usar_cache: Se True, usa resultados em cache quando disponível
            
        Returns:
            dict: Análise com clusters e padrões interpretáveis
        """
        try:
            # Verificar cache
            cache_key = f'cancelamentos_{psicologo_id}_{dias}'
            if usar_cache:
                cached = IAService._load_from_cache(cache_key)
                if cached:
                    return cached
            
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
                    'clusters': [],
                    'recomendacoes': []
                }
            
            # Converter para DataFrame
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
            
            # === NOVO: Aplicar K-Means para clustering ===
            clusters_info = IAService._aplicar_kmeans_cancelamentos(df)
            
            # Análise de padrões (mantido do código original)
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
                    'acao': 'Considerar conversa sobre compromisso com o tratamento',
                    'confianca': 'alta'
                })
            
            # Recomendações baseadas em clusters
            for cluster in clusters_info:
                if cluster['tamanho'] >= 3:
                    recomendacoes.append({
                        'tipo': 'cluster_identificado',
                        'descricao': cluster['descricao'],
                        'acao': 'Revisar agendamentos neste perfil',
                        'confianca': 'media'
                    })
            
            resultado = {
                'total_cancelamentos': len(sessoes_canceladas),
                'periodo_dias': dias,
                'padroes': padroes,
                'clusters': clusters_info,
                'recomendacoes': recomendacoes
            }
            
            # Salvar em cache
            IAService._save_to_cache(cache_key, resultado, ttl_hours=6)
            
            return resultado
            
        except Exception as e:
            return {
                'erro': f'Erro na análise de cancelamentos: {str(e)}'
            }
    
    @staticmethod
    def _aplicar_kmeans_cancelamentos(df):
        """
        Aplica K-Means clustering nos dados de cancelamento.
        
        Args:
            df: DataFrame com dados de cancelamentos
            
        Returns:
            list: Lista de clusters com descrições interpretáveis
        """
        if len(df) < 3:
            return []
        
        # Preparar features para clustering
        X = df[['dia_semana', 'hora']].values
        
        # Determinar número ideal de clusters (máximo 4)
        n_clusters = min(3, len(df) // 2)
        
        if n_clusters < 2:
            return []
        
        # Aplicar K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(X)
        
        # Interpretar clusters
        clusters_info = []
        dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        for cluster_id in range(n_clusters):
            cluster_data = df[df['cluster'] == cluster_id]
            
            # Calcular características do cluster
            dia_medio = int(cluster_data['dia_semana'].mode()[0]) if len(cluster_data) > 0 else 0
            hora_media = int(cluster_data['hora'].mean())
            tamanho = len(cluster_data)
            
            # Determinar período do dia
            if hora_media < 12:
                periodo = 'manhã'
            elif hora_media < 18:
                periodo = 'tarde'
            else:
                periodo = 'noite'
            
            descricao = f'Cluster {cluster_id + 1}: cancelamentos na {periodo}'
            
            # Adicionar dia da semana se houver padrão claro
            if cluster_data['dia_semana'].nunique() <= 2:
                dias_principais = cluster_data['dia_semana'].mode().values
                dias_nomes = [dias_semana[d] for d in dias_principais[:2]]
                descricao += f' ({", ".join(dias_nomes)})'
            
            clusters_info.append({
                'cluster_id': cluster_id,
                'descricao': descricao,
                'tamanho': tamanho,
                'hora_media': hora_media,
                'dia_predominante': dias_semana[dia_medio],
                'periodo': periodo
            })
        
        return clusters_info
    
    # ========== PREVISÃO DE CANCELAMENTOS ==========
    
    @staticmethod
    def prever_cancelamento(sessao_id=None, paciente_id=None, psicologo_id=None, 
                           data_hora=None, retreinar=False):
        """
        Prevê a probabilidade de cancelamento de uma sessão usando Regressão Logística.
        
        Args:
            sessao_id: ID da sessão (opcional, se fornecido busca dados automaticamente)
            paciente_id: ID do paciente
            psicologo_id: ID do psicólogo
            data_hora: Data e hora da sessão
            retreinar: Se True, retreina o modelo
            
        Returns:
            dict: Probabilidade de cancelamento e alerta preditivo
        """
        try:
            # Se sessao_id fornecido, buscar dados
            if sessao_id:
                sessao = Sessao.query.get(sessao_id)
                if not sessao:
                    return {'erro': 'Sessão não encontrada'}
                paciente_id = sessao.paciente_id
                psicologo_id = sessao.psicologo_id
                data_hora = sessao.data_hora
            
            if not all([paciente_id, psicologo_id, data_hora]):
                return {'erro': 'Dados insuficientes para previsão'}
            
            # Carregar ou treinar modelo
            modelo, scaler = IAService._carregar_ou_treinar_modelo(retreinar)
            
            if modelo is None:
                return {
                    'erro': 'Dados insuficientes para treinamento',
                    'mensagem': 'É necessário histórico de pelo menos 20 sessões'
                }
            
            # Calcular features
            features = IAService._extrair_features_sessao(
                paciente_id, psicologo_id, data_hora
            )
            
            # Fazer previsão
            X = np.array([[
                features['dia_semana'],
                features['hora'],
                features['cancelamentos_passados_paciente'],
                features['cancelamentos_passados_psicologo']
            ]])
            
            X_scaled = scaler.transform(X)
            probabilidade = modelo.predict_proba(X_scaled)[0][1]  # Probabilidade de cancelamento
            
            # Gerar alerta preditivo
            alertas = []
            nivel_confianca = 'baixa'
            
            if probabilidade > 0.7:
                nivel_confianca = 'alta'
                alertas.append({
                    'tipo': 'risco_alto_cancelamento',
                    'severidade': 'alta',
                    'confianca': nivel_confianca,
                    'mensagem': f'Alta chance de cancelamento ({probabilidade*100:.0f}%)'
                })
            elif probabilidade > 0.5:
                nivel_confianca = 'media'
                alertas.append({
                    'tipo': 'risco_medio_cancelamento',
                    'severidade': 'media',
                    'confianca': nivel_confianca,
                    'mensagem': f'Chance moderada de cancelamento ({probabilidade*100:.0f}%)'
                })
            
            return {
                'probabilidade_cancelamento': round(probabilidade, 3),
                'percentual': round(probabilidade * 100, 1),
                'nivel_confianca': nivel_confianca,
                'alertas': alertas,
                'features_utilizadas': features
            }
            
        except Exception as e:
            return {
                'erro': f'Erro na previsão de cancelamento: {str(e)}'
            }
    
    @staticmethod
    def _carregar_ou_treinar_modelo(retreinar=False):
        """
        Carrega modelo existente ou treina um novo.
        
        Args:
            retreinar: Se True, força retreinamento
            
        Returns:
            tuple: (modelo, scaler) ou (None, None) se não houver dados suficientes
        """
        modelo_path = IAService.MODEL_DIR / 'cancelamento_model.pkl'
        scaler_path = IAService.MODEL_DIR / 'cancelamento_scaler.pkl'
        
        # Tentar carregar modelo existente
        if not retreinar and modelo_path.exists() and scaler_path.exists():
            try:
                with open(modelo_path, 'rb') as f:
                    modelo = pickle.load(f)
                with open(scaler_path, 'rb') as f:
                    scaler = pickle.load(f)
                return modelo, scaler
            except:
                pass  # Se falhar, treinar novo modelo
        
        # Treinar novo modelo
        return IAService._treinar_modelo_cancelamento()
    
    @staticmethod
    def _treinar_modelo_cancelamento():
        """
        Treina modelo de Regressão Logística para previsão de cancelamentos.
        
        Returns:
            tuple: (modelo, scaler) ou (None, None) se não houver dados suficientes
        """
        try:
            # Buscar dados recentes (últimos 180 dias)
            data_inicio = datetime.now() - timedelta(days=180)
            sessoes = Sessao.query.filter(
                Sessao.data_hora >= data_inicio,
                Sessao.status.in_(['realizada', 'cancelada'])
            ).all()
            
            if len(sessoes) < 20:
                return None, None
            
            # Preparar dados de treinamento
            X_data = []
            y_data = []
            
            for sessao in sessoes:
                features = IAService._extrair_features_sessao(
                    sessao.paciente_id,
                    sessao.psicologo_id,
                    sessao.data_hora,
                    excluir_sessao_id=sessao.id
                )
                
                X_data.append([
                    features['dia_semana'],
                    features['hora'],
                    features['cancelamentos_passados_paciente'],
                    features['cancelamentos_passados_psicologo']
                ])
                
                y_data.append(1 if sessao.status == 'cancelada' else 0)
            
            X = np.array(X_data)
            y = np.array(y_data)
            
            # Normalizar features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Treinar modelo
            modelo = LogisticRegression(random_state=42, max_iter=1000)
            modelo.fit(X_scaled, y)
            
            # Salvar modelo e scaler
            modelo_path = IAService.MODEL_DIR / 'cancelamento_model.pkl'
            scaler_path = IAService.MODEL_DIR / 'cancelamento_scaler.pkl'
            
            with open(modelo_path, 'wb') as f:
                pickle.dump(modelo, f)
            with open(scaler_path, 'wb') as f:
                pickle.dump(scaler, f)
            
            return modelo, scaler
            
        except Exception as e:
            print(f'Erro ao treinar modelo: {e}')
            return None, None
    
    @staticmethod
    def _extrair_features_sessao(paciente_id, psicologo_id, data_hora, excluir_sessao_id=None):
        """
        Extrai features de uma sessão para o modelo preditivo.
        
        Args:
            paciente_id: ID do paciente
            psicologo_id: ID do psicólogo
            data_hora: Data e hora da sessão
            excluir_sessao_id: ID da sessão a excluir (para evitar data leakage)
            
        Returns:
            dict: Features extraídas
        """
        # Features temporais
        dia_semana = data_hora.weekday()
        hora = data_hora.hour
        
        # Cancelamentos passados do paciente
        query_paciente = Sessao.query.filter(
            Sessao.paciente_id == paciente_id,
            Sessao.status == 'cancelada',
            Sessao.data_hora < data_hora
        )
        if excluir_sessao_id:
            query_paciente = query_paciente.filter(Sessao.id != excluir_sessao_id)
        
        cancelamentos_paciente = query_paciente.count()
        
        # Cancelamentos passados do psicólogo
        query_psicologo = Sessao.query.filter(
            Sessao.psicologo_id == psicologo_id,
            Sessao.status == 'cancelada',
            Sessao.data_hora < data_hora
        )
        if excluir_sessao_id:
            query_psicologo = query_psicologo.filter(Sessao.id != excluir_sessao_id)
        
        cancelamentos_psicologo = query_psicologo.count()
        
        return {
            'dia_semana': dia_semana,
            'hora': hora,
            'cancelamentos_passados_paciente': cancelamentos_paciente,
            'cancelamentos_passados_psicologo': cancelamentos_psicologo
        }
    
    # ========== GERAÇÃO DE ALERTAS APRIMORADA ==========
    
    @staticmethod
    def gerar_alertas_dashboard(psicologo_id=None):
        """
        Gera alertas consolidados para o dashboard com níveis de confiança.
        Combina análises estatísticas e preditivas.
        
        Args:
            psicologo_id: ID do psicólogo (opcional)
            
        Returns:
            list: Lista de alertas com mensagens automáticas claras
        """
        try:
            alertas = []
            
            # Análise de cancelamentos
            analise_cancelamentos = IAService.detectar_padroes_cancelamento(psicologo_id, dias=30)
            
            if analise_cancelamentos.get('total_cancelamentos', 0) > 5:
                alertas.append({
                    'tipo': 'cancelamentos_altos',
                    'severidade': 'media',
                    'confianca': 'alta',
                    'titulo': 'Alto número de cancelamentos',
                    'mensagem': f'{analise_cancelamentos["total_cancelamentos"]} cancelamentos nos últimos 30 dias',
                    'acao': 'Revisar padrões de agendamento'
                })
            
            # === NOVO: Alertas preditivos para sessões próximas ===
            hoje = datetime.now()
            amanha = hoje + timedelta(days=1)
            
            query = Sessao.query.filter(
                Sessao.data_hora >= hoje,
                Sessao.data_hora <= amanha,
                Sessao.status == 'agendada'
            )
            
            if psicologo_id:
                query = query.filter(Sessao.psicologo_id == psicologo_id)
            
            sessoes_proximas = query.all()
            
            # Prever cancelamentos para sessões próximas
            sessoes_alto_risco = []
            for sessao in sessoes_proximas:
                previsao = IAService.prever_cancelamento(sessao_id=sessao.id)
                if previsao.get('probabilidade_cancelamento', 0) > 0.6:
                    sessoes_alto_risco.append({
                        'sessao_id': sessao.id,
                        'paciente_id': sessao.paciente_id,
                        'data_hora': sessao.data_hora,
                        'probabilidade': previsao['percentual']
                    })
            
            if sessoes_alto_risco:
                for sessao_risco in sessoes_alto_risco[:3]:  # Limitar a 3 alertas
                    hora_formatada = sessao_risco['data_hora'].strftime('%H:%M')
                    alertas.append({
                        'tipo': 'previsao_cancelamento',
                        'severidade': 'alta',
                        'confianca': 'media',
                        'titulo': 'Alta chance de cancelamento',
                        'mensagem': f'Sessão às {hora_formatada} com {sessao_risco["probabilidade"]:.0f}% de chance de cancelamento',
                        'acao': 'Confirmar presença do paciente',
                        'sessao_id': sessao_risco['sessao_id']
                    })
            
            # Alertas de sessões próximas (mantido)
            if len(sessoes_proximas) > 0 and not sessoes_alto_risco:
                alertas.append({
                    'tipo': 'sessoes_proximas',
                    'severidade': 'baixa',
                    'confianca': 'alta',
                    'titulo': 'Sessões próximas',
                    'mensagem': f'{len(sessoes_proximas)} sessão(ões) agendada(s) para amanhã',
                    'acao': 'Confirmar presença dos pacientes'
                })
            
            # === NOVO: Alertas de engajamento baixo ===
            # Buscar pacientes com sessões recentes
            data_inicio = datetime.now() - timedelta(days=30)
            pacientes_ativos = Sessao.query.filter(
                Sessao.data_hora >= data_inicio
            ).with_entities(Sessao.paciente_id).distinct()
            
            if psicologo_id:
                pacientes_ativos = pacientes_ativos.filter(Sessao.psicologo_id == psicologo_id)
            
            pacientes_baixo_engajamento = 0
            for (paciente_id,) in pacientes_ativos.all()[:10]:  # Limitar análise
                analise = IAService.analisar_frequencia_paciente(paciente_id, dias=30)
                if analise.get('indice_engajamento', 100) < 50:
                    pacientes_baixo_engajamento += 1
            
            if pacientes_baixo_engajamento > 0:
                alertas.append({
                    'tipo': 'engajamento_baixo_geral',
                    'severidade': 'media',
                    'confianca': 'alta',
                    'titulo': 'Pacientes com baixo engajamento',
                    'mensagem': f'{pacientes_baixo_engajamento} paciente(s) com índice de engajamento abaixo de 50',
                    'acao': 'Revisar plano terapêutico e motivação'
                })
            
            return alertas
            
        except Exception as e:
            return [{
                'tipo': 'erro_sistema',
                'severidade': 'alta',
                'confianca': 'alta',
                'titulo': 'Erro no sistema de alertas',
                'mensagem': f'Erro: {str(e)}',
                'acao': 'Contatar suporte técnico'
            }]
    
    # ========== CAMADA DE APRENDIZADO INCREMENTAL ==========
    
    @staticmethod
    def atualizar_estatisticas_incrementais(paciente_id=None):
        """
        Atualiza estatísticas em cache de forma incremental.
        Evita reprocessar todo o histórico.
        
        Args:
            paciente_id: ID do paciente (se None, atualiza estatísticas gerais)
        """
        try:
            stats = IAService._load_stats()
            
            if paciente_id:
                # Atualizar estatísticas do paciente
                analise = IAService.analisar_frequencia_paciente(paciente_id, dias=90)
                
                if 'pacientes' not in stats:
                    stats['pacientes'] = {}
                
                stats['pacientes'][str(paciente_id)] = {
                    'taxa_comparecimento': analise.get('taxa_comparecimento', 0),
                    'frequencia_semanal': analise.get('frequencia_semanal', 0),
                    'indice_engajamento': analise.get('indice_engajamento', 0),
                    'ultima_atualizacao': datetime.now().isoformat()
                }
            else:
                # Atualizar estatísticas gerais
                total_sessoes = Sessao.query.count()
                total_canceladas = Sessao.query.filter(Sessao.status == 'cancelada').count()
                taxa_cancelamento_geral = (total_canceladas / total_sessoes * 100) if total_sessoes > 0 else 0
                
                stats['geral'] = {
                    'total_sessoes': total_sessoes,
                    'total_canceladas': total_canceladas,
                    'taxa_cancelamento': taxa_cancelamento_geral,
                    'ultima_atualizacao': datetime.now().isoformat()
                }
            
            IAService._save_stats(stats)
            
        except Exception as e:
            print(f'Erro ao atualizar estatísticas: {e}')
    
    @staticmethod
    def _load_stats():
        """Carrega estatísticas do arquivo de cache."""
        if IAService.STATS_FILE.exists():
            try:
                with open(IAService.STATS_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    @staticmethod
    def _save_stats(stats):
        """Salva estatísticas no arquivo de cache."""
        try:
            with open(IAService.STATS_FILE, 'w') as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            print(f'Erro ao salvar estatísticas: {e}')
    
    @staticmethod
    def _load_from_cache(key):
        """Carrega dados do cache."""
        cache_file = IAService.CACHE_DIR / f'{key}.json'
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    # Verificar TTL
                    if 'expires_at' in data:
                        expires_at = datetime.fromisoformat(data['expires_at'])
                        if datetime.now() > expires_at:
                            cache_file.unlink()
                            return None
                    return data.get('content')
            except:
                pass
        return None
    
    @staticmethod
    def _save_to_cache(key, content, ttl_hours=24):
        """Salva dados no cache com TTL."""
        try:
            cache_file = IAService.CACHE_DIR / f'{key}.json'
            expires_at = datetime.now() + timedelta(hours=ttl_hours)
            data = {
                'content': content,
                'expires_at': expires_at.isoformat()
            }
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f'Erro ao salvar cache: {e}')
    
    @staticmethod
    def limpar_cache():
        """Remove todos os arquivos de cache expirados."""
        try:
            for cache_file in IAService.CACHE_DIR.glob('*.json'):
                try:
                    with open(cache_file, 'r') as f:
                        data = json.load(f)
                        if 'expires_at' in data:
                            expires_at = datetime.fromisoformat(data['expires_at'])
                            if datetime.now() > expires_at:
                                cache_file.unlink()
                except:
                    pass
        except Exception as e:
            print(f'Erro ao limpar cache: {e}')
