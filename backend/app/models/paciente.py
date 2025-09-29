from app import db
from datetime import datetime
import uuid

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date)
    cpf = db.Column(db.String(14), unique=True)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    endereco = db.Column(db.Text)
    qr_code_data = db.Column(db.Text, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    sessoes = db.relationship('Sessao', backref='paciente', lazy=True)
    
    def __init__(self, **kwargs):
        super(Paciente, self).__init__(**kwargs)
        if not self.qr_code_data:
            self.qr_code_data = f"regiflex_patient_{uuid.uuid4().hex[:8]}"
    
    def to_dict(self):
        """Converte o objeto Paciente para um dicionário."""
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'qr_code_data': self.qr_code_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Paciente {self.nome_completo}>'
