from flask import request, jsonify
from app.api import bp
from app.api.auth import token_required
from app.services.ia_service import IAService
from app.models.log import Log
from app import db

@bp.route('/ia/alertas', methods=['GET'])
@token_required
def get_alertas_ia(current_user):
    """Endpoint para obter alertas gerados pela IA."""
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
    """Endpoint para obter análise de IA de um paciente específico."""
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
    """Endpoint para obter análise de padrões de cancelamento."""
    try:
        dias = request.args.get('dias', 60, type=int)
        psicologo_id = current_user.id if current_user.role == 'psicologo' else None
        
        if request.args.get('psicologo_id') and current_user.role == 'admin':
            psicologo_id = request.args.get('psicologo_id', type=int)
        
        analise = IAService.detectar_padroes_cancelamento(psicologo_id, dias)
        
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
