from flask import request, jsonify
from app.api import bp
from app.api.auth import token_required
from app.models.sessao import Sessao
from app.models.evolucao import Evolucao
from app.models.log import Log
from app import db
from datetime import datetime

@bp.route('/sessoes', methods=['GET'])
@token_required
def get_sessoes(current_user):
    """Endpoint para listar sessões."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        paciente_id = request.args.get('paciente_id', type=int)
        
        query = Sessao.query
        
        # Filtros
        if status:
            query = query.filter(Sessao.status == status)
        
        if paciente_id:
            query = query.filter(Sessao.paciente_id == paciente_id)
        
        # Psicólogos só veem suas próprias sessões
        if current_user.role == 'psicologo':
            query = query.filter(Sessao.psicologo_id == current_user.id)
        
        sessoes = query.order_by(Sessao.data_hora.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'sessoes': [sessao.to_dict() for sessao in sessoes.items],
            'total': sessoes.total,
            'pages': sessoes.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/sessoes', methods=['POST'])
@token_required
def create_sessao(current_user):
    """Endpoint para agendar uma nova sessão."""
    try:
        data = request.get_json()
        
        # Validações básicas
        required_fields = ['paciente_id', 'data_hora']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'Campo {field} é obrigatório!'}), 400
        
        # Converter data_hora
        try:
            data_hora = datetime.fromisoformat(data['data_hora'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'message': 'Formato de data/hora inválido!'}), 400
        
        # Verificar conflitos de horário
        conflito = Sessao.query.filter(
            Sessao.psicologo_id == current_user.id,
            Sessao.data_hora == data_hora,
            Sessao.status != 'cancelada'
        ).first()
        
        if conflito:
            return jsonify({'message': 'Já existe uma sessão agendada para este horário!'}), 400
        
        # Criar nova sessão
        nova_sessao = Sessao(
            paciente_id=data['paciente_id'],
            psicologo_id=current_user.id,
            data_hora=data_hora,
            duracao_minutos=data.get('duracao_minutos', 50),
            tipo_sessao=data.get('tipo_sessao'),
            observacoes=data.get('observacoes')
        )
        
        db.session.add(nova_sessao)
        db.session.commit()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='CREATE_SESSION',
            detalhes=f'Sessão agendada para {data_hora}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Sessão agendada com sucesso!',
            'sessao': nova_sessao.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/sessoes/<int:sessao_id>', methods=['GET'])
@token_required
def get_sessao(current_user, sessao_id):
    """Endpoint para obter uma sessão específica."""
    try:
        sessao = Sessao.query.get_or_404(sessao_id)
        
        # Verificar permissão
        if current_user.role == 'psicologo' and sessao.psicologo_id != current_user.id:
            return jsonify({'message': 'Acesso negado!'}), 403
        
        return jsonify({'sessao': sessao.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/sessoes/<int:sessao_id>', methods=['PUT'])
@token_required
def update_sessao(current_user, sessao_id):
    """Endpoint para atualizar uma sessão."""
    try:
        sessao = Sessao.query.get_or_404(sessao_id)
        
        # Verificar permissão
        if current_user.role == 'psicologo' and sessao.psicologo_id != current_user.id:
            return jsonify({'message': 'Acesso negado!'}), 403
        
        data = request.get_json()
        
        # Atualizar campos
        if data.get('data_hora'):
            try:
                nova_data_hora = datetime.fromisoformat(data['data_hora'].replace('Z', '+00:00'))
                
                # Verificar conflitos se a data/hora mudou
                if nova_data_hora != sessao.data_hora:
                    conflito = Sessao.query.filter(
                        Sessao.psicologo_id == sessao.psicologo_id,
                        Sessao.data_hora == nova_data_hora,
                        Sessao.status != 'cancelada',
                        Sessao.id != sessao_id
                    ).first()
                    
                    if conflito:
                        return jsonify({'message': 'Já existe uma sessão agendada para este horário!'}), 400
                
                sessao.data_hora = nova_data_hora
            except ValueError:
                return jsonify({'message': 'Formato de data/hora inválido!'}), 400
        
        if data.get('duracao_minutos'):
            sessao.duracao_minutos = data['duracao_minutos']
        
        if data.get('tipo_sessao'):
            sessao.tipo_sessao = data['tipo_sessao']
        
        if data.get('status'):
            sessao.status = data['status']
        
        if data.get('observacoes'):
            sessao.observacoes = data['observacoes']
        
        sessao.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='UPDATE_SESSION',
            detalhes=f'Sessão {sessao_id} atualizada',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Sessão atualizada com sucesso!',
            'sessao': sessao.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/sessoes/<int:sessao_id>/evolucao', methods=['POST'])
@token_required
def create_evolucao(current_user, sessao_id):
    """Endpoint para criar evolução de uma sessão."""
    try:
        sessao = Sessao.query.get_or_404(sessao_id)
        
        # Verificar permissão
        if current_user.role == 'psicologo' and sessao.psicologo_id != current_user.id:
            return jsonify({'message': 'Acesso negado!'}), 403
        
        data = request.get_json()
        
        if not data.get('conteudo'):
            return jsonify({'message': 'Conteúdo da evolução é obrigatório!'}), 400
        
        # Verificar se já existe evolução para esta sessão
        evolucao_existente = Evolucao.query.filter_by(sessao_id=sessao_id).first()
        if evolucao_existente:
            return jsonify({'message': 'Já existe uma evolução para esta sessão!'}), 400
        
        # Criar evolução
        nova_evolucao = Evolucao(
            sessao_id=sessao_id,
            conteudo=data['conteudo']
        )
        
        db.session.add(nova_evolucao)
        db.session.commit()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='CREATE_EVOLUTION',
            detalhes=f'Evolução criada para sessão {sessao_id}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Evolução criada com sucesso!',
            'evolucao': nova_evolucao.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/sessoes/<int:sessao_id>/evolucao', methods=['PUT'])
@token_required
def update_evolucao(current_user, sessao_id):
    """Endpoint para atualizar evolução de uma sessão."""
    try:
        sessao = Sessao.query.get_or_404(sessao_id)
        
        # Verificar permissão
        if current_user.role == 'psicologo' and sessao.psicologo_id != current_user.id:
            return jsonify({'message': 'Acesso negado!'}), 403
        
        evolucao = Evolucao.query.filter_by(sessao_id=sessao_id).first()
        if not evolucao:
            return jsonify({'message': 'Evolução não encontrada!'}), 404
        
        data = request.get_json()
        
        if not data.get('conteudo'):
            return jsonify({'message': 'Conteúdo da evolução é obrigatório!'}), 400
        
        evolucao.conteudo = data['conteudo']
        evolucao.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='UPDATE_EVOLUTION',
            detalhes=f'Evolução da sessão {sessao_id} atualizada',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Evolução atualizada com sucesso!',
            'evolucao': evolucao.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500
