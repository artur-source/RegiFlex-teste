from flask import request, jsonify
from app.api import bp
from app.api.auth import token_required
from app.models.paciente import Paciente
from app.models.log import Log
from app import db
import qrcode
import io
import base64

@bp.route('/qr/generate/<int:paciente_id>', methods=['GET'])
@token_required
def generate_qr_code(current_user, paciente_id):
    """Endpoint para gerar QR Code de um paciente."""
    try:
        paciente = Paciente.query.get_or_404(paciente_id)
        
        # Gerar QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(paciente.qr_code_data)
        qr.make(fit=True)
        
        # Criar imagem
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Converter para base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='GENERATE_QR',
            detalhes=f'QR Code gerado para paciente {paciente.nome_completo}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'qr_code': f'data:image/png;base64,{img_str}',
            'qr_data': paciente.qr_code_data,
            'paciente': paciente.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/qr/read', methods=['POST'])
@token_required
def read_qr_code(current_user):
    """Endpoint para ler/validar QR Code e obter dados do paciente."""
    try:
        data = request.get_json()
        
        if not data.get('qr_data'):
            return jsonify({'message': 'Dados do QR Code são obrigatórios!'}), 400
        
        # Buscar paciente pelo QR Code
        paciente = Paciente.query.filter_by(qr_code_data=data['qr_data']).first()
        
        if not paciente:
            # Registrar tentativa de leitura de QR inválido
            log = Log(
                usuario_id=current_user.id,
                acao='INVALID_QR_READ',
                detalhes=f'Tentativa de leitura de QR Code inválido: {data["qr_data"]}',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({'message': 'QR Code inválido!'}), 404
        
        # Registrar leitura bem-sucedida
        log = Log(
            usuario_id=current_user.id,
            acao='READ_QR',
            detalhes=f'QR Code lido com sucesso para paciente {paciente.nome_completo}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'QR Code válido!',
            'paciente': paciente.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/qr/validate/<qr_data>', methods=['GET'])
@token_required
def validate_qr_code(current_user, qr_data):
    """Endpoint para validar QR Code via URL."""
    try:
        # Buscar paciente pelo QR Code
        paciente = Paciente.query.filter_by(qr_code_data=qr_data).first()
        
        if not paciente:
            return jsonify({
                'valid': False,
                'message': 'QR Code inválido!'
            }), 404
        
        # Registrar validação
        log = Log(
            usuario_id=current_user.id,
            acao='VALIDATE_QR',
            detalhes=f'QR Code validado para paciente {paciente.nome_completo}',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'valid': True,
            'message': 'QR Code válido!',
            'paciente': paciente.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500
