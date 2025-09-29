from app import db
from datetime import datetime
from flask_bcrypt import check_password_hash, generate_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='psicologo')  # admin, psicologo, recepcionista
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    sessoes = db.relationship('Sessao', backref='psicologo', lazy=True)
    logs = db.relationship('Log', backref='usuario', lazy=True)
    
    def set_password(self, password):
        """Define a senha do usuário com hash bcrypt."""
        self.password_hash = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verifica se a senha fornecida está correta."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Converte o objeto Usuario para um dicionário."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Usuario {self.username}>'
