from flask import request, jsonify
from app.api import bp
from app.api.auth import token_required
from app.models.usuario import Usuario
from app.models.log import Log
from app import db

@bp.route('/usuarios', methods=['GET'])
@token_required
def get_usuarios(current_user):
    """Endpoint para listar todos os usuários (apenas admin)."""
    if current_user.role != 'admin':
        return jsonify({'message': 'Acesso negado!'}), 403
    
    try:
        usuarios = Usuario.query.all()
        return jsonify({
            'usuarios': [usuario.to_dict() for usuario in usuarios]
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/usuarios', methods=['POST'])
@token_required
def create_usuario(current_user):
    """Endpoint para criar um novo usuário (apenas admin)."""
    if current_user.role != 'admin':
        return jsonify({'message': 'Acesso negado!'}), 403
    
    try:
        data = request.get_json()
        
        # Validações básicas
        required_fields = ['username', 'email', 'password', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'Campo {field} é obrigatório!'}), 400
        
        # Verificar se username ou email já existem
        if Usuario.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username já existe!'}), 400
        
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email já existe!'}), 400
        
        # Criar novo usuário
        novo_usuario = Usuario(
            username=data['username'],
            email=data['email'],
            role=data['role']
        )
        novo_usuario.set_password(data['password'])
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='CREATE_USER',
            detalhes=f'Usuário {novo_usuario.username} criado com sucesso',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário criado com sucesso!',
            'usuario': novo_usuario.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/usuarios/<int:user_id>', methods=['GET'])
@token_required
def get_usuario(current_user, user_id):
    """Endpoint para obter um usuário específico."""
    if current_user.role != 'admin' and current_user.id != user_id:
        return jsonify({'message': 'Acesso negado!'}), 403
    
    try:
        usuario = Usuario.query.get_or_404(user_id)
        return jsonify({'usuario': usuario.to_dict()}), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/usuarios/<int:user_id>', methods=['PUT'])
@token_required
def update_usuario(current_user, user_id):
    """Endpoint para atualizar um usuário."""
    if current_user.role != 'admin' and current_user.id != user_id:
        return jsonify({'message': 'Acesso negado!'}), 403
    
    try:
        usuario = Usuario.query.get_or_404(user_id)
        data = request.get_json()
        
        # Atualizar campos permitidos
        if data.get('email'):
            # Verificar se o novo email já existe
            existing_user = Usuario.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({'message': 'Email já existe!'}), 400
            usuario.email = data['email']
        
        if data.get('password'):
            usuario.set_password(data['password'])
        
        # Apenas admin pode alterar role
        if data.get('role') and current_user.role == 'admin':
            usuario.role = data['role']
        
        db.session.commit()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='UPDATE_USER',
            detalhes=f'Usuário {usuario.username} atualizado',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário atualizado com sucesso!',
            'usuario': usuario.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/usuarios/<int:user_id>', methods=['DELETE'])
@token_required
def delete_usuario(current_user, user_id):
    """Endpoint para deletar um usuário (apenas admin)."""
    if current_user.role != 'admin':
        return jsonify({'message': 'Acesso negado!'}), 403
    
    if current_user.id == user_id:
        return jsonify({'message': 'Você não pode deletar sua própria conta!'}), 400
    
    try:
        usuario = Usuario.query.get_or_404(user_id)
        username = usuario.username
        
        db.session.delete(usuario)
        db.session.commit()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='DELETE_USER',
            detalhes=f'Usuário {username} deletado',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'message': 'Usuário deletado com sucesso!'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500
