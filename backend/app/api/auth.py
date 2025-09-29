from flask import request, jsonify
from app.api import bp
from app.models.usuario import Usuario
from app.models.log import Log
from app import db
import jwt
import datetime
from functools import wraps

def token_required(f):
    """Decorator para verificar se o token JWT é válido."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token inválido!'}), 401
        
        if not token:
            return jsonify({'message': 'Token é obrigatório!'}), 401
        
        try:
            data = jwt.decode(token, 'uma-chave-secreta-muito-segura', algorithms=['HS256'])
            current_user = Usuario.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token inválido!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@bp.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticação de usuários."""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Username e password são obrigatórios!'}), 400
        
        usuario = Usuario.query.filter_by(username=data['username']).first()
        
        if usuario and usuario.check_password(data['password']):
            # Gerar token JWT
            token = jwt.encode({
                'user_id': usuario.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, 'uma-chave-secreta-muito-segura', algorithm='HS256')
            
            # Registrar log de login
            log = Log(
                usuario_id=usuario.id,
                acao='LOGIN',
                detalhes=f'Login realizado com sucesso para o usuário {usuario.username}',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({
                'message': 'Login realizado com sucesso!',
                'token': token,
                'user': usuario.to_dict()
            }), 200
        else:
            # Registrar tentativa de login falhada
            log = Log(
                acao='LOGIN_FAILED',
                detalhes=f'Tentativa de login falhada para o usuário {data.get("username")}',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({'message': 'Credenciais inválidas!'}), 401
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Endpoint para logout de usuários."""
    try:
        # Registrar log de logout
        log = Log(
            usuario_id=current_user.id,
            acao='LOGOUT',
            detalhes=f'Logout realizado para o usuário {current_user.username}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'message': 'Logout realizado com sucesso!'}), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Endpoint para obter informações do usuário atual."""
    return jsonify({'user': current_user.to_dict()}), 200
