from flask import request, jsonify
from app.api import bp
from app.api.auth import token_required
from app.models.paciente import Paciente
from app.models.log import Log
from app import db
from datetime import datetime

@bp.route('/pacientes', methods=['GET'])
@token_required
def get_pacientes(current_user):
    """Endpoint para listar todos os pacientes."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        pacientes = Paciente.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'pacientes': [paciente.to_dict() for paciente in pacientes.items],
            'total': pacientes.total,
            'pages': pacientes.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/pacientes', methods=['POST'])
@token_required
def create_paciente(current_user):
    """Endpoint para criar um novo paciente."""
    try:
        data = request.get_json()
        
        # Validações básicas
        if not data.get('nome_completo'):
            return jsonify({'message': 'Nome completo é obrigatório!'}), 400
        
        # Verificar se CPF já existe (se fornecido)
        if data.get('cpf'):
            existing_paciente = Paciente.query.filter_by(cpf=data['cpf']).first()
            if existing_paciente:
                return jsonify({'message': 'CPF já cadastrado!'}), 400
        
        # Criar novo paciente
        novo_paciente = Paciente(
            nome_completo=data['nome_completo'],
            data_nascimento=datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date() if data.get('data_nascimento') else None,
            cpf=data.get('cpf'),
            telefone=data.get('telefone'),
            email=data.get('email'),
            endereco=data.get('endereco')
        )
        
        db.session.add(novo_paciente)
        db.session.commit()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='CREATE_PATIENT',
            detalhes=f'Paciente {novo_paciente.nome_completo} cadastrado com sucesso',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Paciente cadastrado com sucesso!',
            'paciente': novo_paciente.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/pacientes/<int:paciente_id>', methods=['GET'])
@token_required
def get_paciente(current_user, paciente_id):
    """Endpoint para obter um paciente específico."""
    try:
        paciente = Paciente.query.get_or_404(paciente_id)
        return jsonify({'paciente': paciente.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/pacientes/<int:paciente_id>', methods=['PUT'])
@token_required
def update_paciente(current_user, paciente_id):
    """Endpoint para atualizar um paciente."""
    try:
        paciente = Paciente.query.get_or_404(paciente_id)
        data = request.get_json()
        
        # Atualizar campos
        if data.get('nome_completo'):
            paciente.nome_completo = data['nome_completo']
        
        if data.get('data_nascimento'):
            paciente.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        
        if data.get('cpf'):
            # Verificar se o novo CPF já existe
            existing_paciente = Paciente.query.filter_by(cpf=data['cpf']).first()
            if existing_paciente and existing_paciente.id != paciente_id:
                return jsonify({'message': 'CPF já cadastrado!'}), 400
            paciente.cpf = data['cpf']
        
        if data.get('telefone'):
            paciente.telefone = data['telefone']
        
        if data.get('email'):
            paciente.email = data['email']
        
        if data.get('endereco'):
            paciente.endereco = data['endereco']
        
        paciente.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='UPDATE_PATIENT',
            detalhes=f'Paciente {paciente.nome_completo} atualizado',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Paciente atualizado com sucesso!',
            'paciente': paciente.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/pacientes/<int:paciente_id>', methods=['DELETE'])
@token_required
def delete_paciente(current_user, paciente_id):
    """Endpoint para deletar um paciente (apenas admin)."""
    if current_user.role != 'admin':
        return jsonify({'message': 'Acesso negado!'}), 403
    
    try:
        paciente = Paciente.query.get_or_404(paciente_id)
        nome_paciente = paciente.nome_completo
        
        db.session.delete(paciente)
        db.session.commit()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='DELETE_PATIENT',
            detalhes=f'Paciente {nome_paciente} deletado',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'message': 'Paciente deletado com sucesso!'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/pacientes/search', methods=['GET'])
@token_required
def search_pacientes(current_user):
    """Endpoint para buscar pacientes por nome ou CPF."""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'message': 'Parâmetro de busca é obrigatório!'}), 400
        
        pacientes = Paciente.query.filter(
            db.or_(
                Paciente.nome_completo.ilike(f'%{query}%'),
                Paciente.cpf.ilike(f'%{query}%')
            )
        ).all()
        
        return jsonify({
            'pacientes': [paciente.to_dict() for paciente in pacientes]
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500
