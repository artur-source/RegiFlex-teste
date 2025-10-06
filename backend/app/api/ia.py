from flask import request, jsonify
from app.api import bp
from app.api.auth import token_required
from app.services.ia_service import IAService
from app.models.log import Log
from app import db

@bp.route('/ia/alertas', methods=['GET'])
@token_required
def get_alertas_ia(current_user):
    """
    Endpoint para obter alertas gerados pela IA.
    Retorna alertas consolidados com análises estatísticas e preditivas.
    """
    try:
        psicologo_id = current_user.id if current_user.role == 'psicologo' else None
        alertas = IAService.gerar_alertas_dashboard(psicologo_id)
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='GET_IA_ALERTS',
            detalhes=f'{len(alertas)} alertas de IA gerados',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'alertas': alertas,
            'total': len(alertas)
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/ia/analise-paciente/<int:paciente_id>', methods=['GET'])
@token_required
def get_analise_paciente(current_user, paciente_id):
    """
    Endpoint para obter análise de IA de um paciente específico.
    Inclui análise de frequência inteligente, variação de tendência e índice de engajamento.
    
    Query params:
        - dias: Período de análise em dias (padrão: 30)
    """
    try:
        dias = request.args.get('dias', 30, type=int)
        analise = IAService.analisar_frequencia_paciente(paciente_id, dias)
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='ANALYZE_PATIENT',
            detalhes=f'Análise de IA realizada para paciente {paciente_id}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(analise), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/ia/padroes-cancelamento', methods=['GET'])
@token_required
def get_padroes_cancelamento(current_user):
    """
    Endpoint para obter análise de padrões de cancelamento.
    Utiliza K-Means clustering para identificar padrões e clusters.
    
    Query params:
        - dias: Período de análise em dias (padrão: 60)
        - psicologo_id: ID do psicólogo (apenas para admin)
        - usar_cache: Se deve usar cache (padrão: true)
    """
    try:
        dias = request.args.get('dias', 60, type=int)
        usar_cache = request.args.get('usar_cache', 'true').lower() == 'true'
        psicologo_id = current_user.id if current_user.role == 'psicologo' else None
        
        if request.args.get('psicologo_id') and current_user.role == 'admin':
            psicologo_id = request.args.get('psicologo_id', type=int)
        
        analise = IAService.detectar_padroes_cancelamento(psicologo_id, dias, usar_cache)
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='ANALYZE_CANCELLATIONS',
            detalhes=f'Análise de padrões de cancelamento realizada',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(analise), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/ia/prever-cancelamento', methods=['POST'])
@token_required
def prever_cancelamento(current_user):
    """
    Endpoint para prever probabilidade de cancelamento de uma sessão.
    Utiliza modelo de Regressão Logística treinado com dados históricos.
    
    Body JSON:
        - sessao_id: ID da sessão (opcional, busca dados automaticamente)
        - paciente_id: ID do paciente (obrigatório se sessao_id não fornecido)
        - psicologo_id: ID do psicólogo (obrigatório se sessao_id não fornecido)
        - data_hora: Data e hora da sessão ISO format (obrigatório se sessao_id não fornecido)
        - retreinar: Se deve retreinar o modelo (padrão: false)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'Dados não fornecidos'}), 400
        
        sessao_id = data.get('sessao_id')
        paciente_id = data.get('paciente_id')
        psicologo_id = data.get('psicologo_id')
        data_hora_str = data.get('data_hora')
        retreinar = data.get('retreinar', False)
        
        # Converter data_hora se fornecida
        from datetime import datetime
        data_hora = None
        if data_hora_str:
            try:
                data_hora = datetime.fromisoformat(data_hora_str.replace('Z', '+00:00'))
            except:
                return jsonify({'message': 'Formato de data_hora inválido. Use ISO format'}), 400
        
        # Fazer previsão
        previsao = IAService.prever_cancelamento(
            sessao_id=sessao_id,
            paciente_id=paciente_id,
            psicologo_id=psicologo_id,
            data_hora=data_hora,
            retreinar=retreinar
        )
        
        if 'erro' in previsao:
            return jsonify(previsao), 400
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='PREDICT_CANCELLATION',
            detalhes=f'Previsão de cancelamento realizada (prob: {previsao.get("percentual", 0):.1f}%)',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(previsao), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/ia/prever-cancelamento/<int:sessao_id>', methods=['GET'])
@token_required
def prever_cancelamento_sessao(current_user, sessao_id):
    """
    Endpoint simplificado para prever cancelamento de uma sessão específica.
    
    Query params:
        - retreinar: Se deve retreinar o modelo (padrão: false)
    """
    try:
        retreinar = request.args.get('retreinar', 'false').lower() == 'true'
        
        previsao = IAService.prever_cancelamento(sessao_id=sessao_id, retreinar=retreinar)
        
        if 'erro' in previsao:
            return jsonify(previsao), 400
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='PREDICT_CANCELLATION',
            detalhes=f'Previsão de cancelamento para sessão {sessao_id} (prob: {previsao.get("percentual", 0):.1f}%)',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(previsao), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/ia/treinar-modelo', methods=['POST'])
@token_required
def treinar_modelo(current_user):
    """
    Endpoint para forçar retreinamento do modelo preditivo.
    Apenas administradores podem executar esta ação.
    """
    try:
        # Verificar permissão
        if current_user.role != 'admin':
            return jsonify({'message': 'Acesso negado. Apenas administradores podem treinar modelos.'}), 403
        
        # Forçar retreinamento
        previsao = IAService.prever_cancelamento(
            sessao_id=1,  # Dummy, apenas para forçar treinamento
            retreinar=True
        )
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='TRAIN_MODEL',
            detalhes='Modelo de previsão de cancelamento retreinado',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Modelo retreinado com sucesso',
            'status': 'success'
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/ia/estatisticas', methods=['GET'])
@token_required
def get_estatisticas(current_user):
    """
    Endpoint para obter estatísticas gerais do sistema de IA.
    Retorna informações sobre cache, modelos e performance.
    """
    try:
        import os
        from pathlib import Path
        
        # Verificar existência de modelos
        model_dir = Path(__file__).parent.parent.parent / 'cache' / 'models'
        modelo_existe = (model_dir / 'cancelamento_model.pkl').exists()
        scaler_existe = (model_dir / 'cancelamento_scaler.pkl').exists()
        
        # Carregar estatísticas salvas
        stats = IAService._load_stats()
        
        estatisticas = {
            'modelo_treinado': modelo_existe and scaler_existe,
            'cache_ativo': True,
            'estatisticas_salvas': stats,
            'recursos_disponiveis': [
                'analise_frequencia_inteligente',
                'deteccao_padroes_kmeans',
                'previsao_cancelamentos',
                'aprendizado_incremental',
                'alertas_preditivos'
            ]
        }
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='GET_IA_STATS',
            detalhes='Estatísticas do sistema de IA consultadas',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(estatisticas), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/ia/atualizar-estatisticas', methods=['POST'])
@token_required
def atualizar_estatisticas(current_user):
    """
    Endpoint para atualizar estatísticas incrementais.
    
    Body JSON:
        - paciente_id: ID do paciente (opcional, se não fornecido atualiza estatísticas gerais)
    """
    try:
        data = request.get_json() or {}
        paciente_id = data.get('paciente_id')
        
        IAService.atualizar_estatisticas_incrementais(paciente_id)
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='UPDATE_STATS',
            detalhes=f'Estatísticas atualizadas (paciente: {paciente_id or "geral"})',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Estatísticas atualizadas com sucesso',
            'status': 'success'
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/ia/limpar-cache', methods=['POST'])
@token_required
def limpar_cache(current_user):
    """
    Endpoint para limpar cache expirado.
    Apenas administradores podem executar esta ação.
    """
    try:
        # Verificar permissão
        if current_user.role != 'admin':
            return jsonify({'message': 'Acesso negado. Apenas administradores podem limpar cache.'}), 403
        
        IAService.limpar_cache()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='CLEAR_CACHE',
            detalhes='Cache do sistema de IA limpo',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Cache limpo com sucesso',
            'status': 'success'
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500
