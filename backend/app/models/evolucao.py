from app import db
from datetime import datetime

class Evolucao(db.Model):
    __tablename__ = 'evolucao'
    
    id = db.Column(db.Integer, primary_key=True)
    sessao_id = db.Column(db.Integer, db.ForeignKey('sessoes.id'), unique=True, nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte o objeto Evolucao para um dicionário."""
        return {
            'id': self.id,
            'sessao_id': self.sessao_id,
            'conteudo': self.conteudo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Evolucao {self.id} - Sessao {self.sessao_id}>'
