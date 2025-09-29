from app import db
from datetime import datetime

class Log(db.Model):
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    acao = db.Column(db.String(100), nullable=False)
    detalhes = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converte o objeto Log para um dicionário."""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'acao': self.acao,
            'detalhes': self.detalhes,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'usuario': self.usuario.to_dict() if self.usuario else None
        }
    
    def __repr__(self):
        return f'<Log {self.id} - {self.acao}>'
