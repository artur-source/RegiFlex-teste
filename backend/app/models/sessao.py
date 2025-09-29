from app import db
from datetime import datetime

class Sessao(db.Model):
    __tablename__ = 'sessoes'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    psicologo_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    duracao_minutos = db.Column(db.Integer, default=50)
    tipo_sessao = db.Column(db.String(50))  # ex: terapia individual, casal, grupo
    status = db.Column(db.String(20), nullable=False, default='agendada')  # agendada, realizada, cancelada
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    evolucao = db.relationship('Evolucao', backref='sessao', uselist=False, lazy=True)
    
    def to_dict(self):
        """Converte o objeto Sessao para um dicionário."""
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'psicologo_id': self.psicologo_id,
            'data_hora': self.data_hora.isoformat() if self.data_hora else None,
            'duracao_minutos': self.duracao_minutos,
            'tipo_sessao': self.tipo_sessao,
            'status': self.status,
            'observacoes': self.observacoes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'paciente': self.paciente.to_dict() if self.paciente else None,
            'psicologo': self.psicologo.to_dict() if self.psicologo else None
        }
    
    def __repr__(self):
        return f'<Sessao {self.id} - {self.data_hora}>'
