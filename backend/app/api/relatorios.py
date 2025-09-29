from flask import request, jsonify
from app.api import bp
from app.api.auth import token_required
from app.models.sessao import Sessao
from app.models.paciente import Paciente
from app.models.usuario import Usuario
from app.models.log import Log
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func, and_

@bp.route('/relatorios/dashboard', methods=['GET'])
@token_required
def get_dashboard_data(current_user):
    """Endpoint para obter dados do dashboard."""
    try:
        # Data atual
        hoje = datetime.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        inicio_mes = hoje.replace(day=1)
        
        # Filtrar por psicólogo se necessário
        sessoes_query = Sessao.query
        if current_user.role == 'psicologo':
            sessoes_query = sessoes_query.filter(Sessao.psicologo_id == current_user.id)
        
        # Estatísticas básicas
        total_pacientes = Paciente.query.count()
        total_sessoes_hoje = sessoes_query.filter(func.date(Sessao.data_hora) == hoje).count()
        total_sessoes_semana = sessoes_query.filter(func.date(Sessao.data_hora) >= inicio_semana).count()
        total_sessoes_mes = sessoes_query.filter(func.date(Sessao.data_hora) >= inicio_mes).count()
        
        # Próximas sessões (próximos 7 dias)
        proximas_sessoes = sessoes_query.filter(
            and_(
                Sessao.data_hora >= datetime.now(),
                Sessao.data_hora <= datetime.now() + timedelta(days=7),
                Sessao.status == 'agendada'
            )
        ).order_by(Sessao.data_hora).limit(5).all()
        
        # Sessões por status
        sessoes_por_status = db.session.query(
            Sessao.status,
            func.count(Sessao.id).label('count')
        ).filter(
            func.date(Sessao.data_hora) >= inicio_mes
        )
        
        if current_user.role == 'psicologo':
            sessoes_por_status = sessoes_por_status.filter(Sessao.psicologo_id == current_user.id)
        
        sessoes_por_status = sessoes_por_status.group_by(Sessao.status).all()
        
        # Sessões por dia da semana (últimos 30 dias)
        inicio_periodo = hoje - timedelta(days=30)
        sessoes_por_dia = db.session.query(
            func.extract('dow', Sessao.data_hora).label('dia_semana'),
            func.count(Sessao.id).label('count')
        ).filter(
            func.date(Sessao.data_hora) >= inicio_periodo
        )
        
        if current_user.role == 'psicologo':
            sessoes_por_dia = sessoes_por_dia.filter(Sessao.psicologo_id == current_user.id)
        
        sessoes_por_dia = sessoes_por_dia.group_by(func.extract('dow', Sessao.data_hora)).all()
        
        # Mapear dias da semana
        dias_semana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
        sessoes_por_dia_formatado = [
            {'dia': dias_semana[int(dia)], 'count': count} 
            for dia, count in sessoes_por_dia
        ]
        
        return jsonify({
            'estatisticas': {
                'total_pacientes': total_pacientes,
                'sessoes_hoje': total_sessoes_hoje,
                'sessoes_semana': total_sessoes_semana,
                'sessoes_mes': total_sessoes_mes
            },
            'proximas_sessoes': [sessao.to_dict() for sessao in proximas_sessoes],
            'sessoes_por_status': [
                {'status': status, 'count': count} 
                for status, count in sessoes_por_status
            ],
            'sessoes_por_dia': sessoes_por_dia_formatado
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/relatorios/sessoes', methods=['GET'])
@token_required
def get_relatorio_sessoes(current_user):
    """Endpoint para gerar relatório de sessões com filtros."""
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        paciente_id = request.args.get('paciente_id', type=int)
        psicologo_id = request.args.get('psicologo_id', type=int)
        status = request.args.get('status')
        
        # Query base
        query = Sessao.query
        
        # Aplicar filtros
        if data_inicio:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
                query = query.filter(Sessao.data_hora >= data_inicio_dt)
            except ValueError:
                return jsonify({'message': 'Formato de data de início inválido!'}), 400
        
        if data_fim:
            try:
                data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Sessao.data_hora < data_fim_dt)
            except ValueError:
                return jsonify({'message': 'Formato de data de fim inválido!'}), 400
        
        if paciente_id:
            query = query.filter(Sessao.paciente_id == paciente_id)
        
        if psicologo_id:
            query = query.filter(Sessao.psicologo_id == psicologo_id)
        elif current_user.role == 'psicologo':
            query = query.filter(Sessao.psicologo_id == current_user.id)
        
        if status:
            query = query.filter(Sessao.status == status)
        
        # Executar query
        sessoes = query.order_by(Sessao.data_hora.desc()).all()
        
        # Estatísticas do relatório
        total_sessoes = len(sessoes)
        sessoes_realizadas = len([s for s in sessoes if s.status == 'realizada'])
        sessoes_canceladas = len([s for s in sessoes if s.status == 'cancelada'])
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='GENERATE_REPORT',
            detalhes=f'Relatório de sessões gerado com {total_sessoes} registros',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'sessoes': [sessao.to_dict() for sessao in sessoes],
            'estatisticas': {
                'total_sessoes': total_sessoes,
                'sessoes_realizadas': sessoes_realizadas,
                'sessoes_canceladas': sessoes_canceladas,
                'taxa_realizacao': round((sessoes_realizadas / total_sessoes * 100) if total_sessoes > 0 else 0, 2)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/relatorios/pacientes', methods=['GET'])
@token_required
def get_relatorio_pacientes(current_user):
    """Endpoint para gerar relatório de pacientes."""
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        # Query base
        query = Paciente.query
        
        # Aplicar filtros de data de cadastro
        if data_inicio:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
                query = query.filter(Paciente.created_at >= data_inicio_dt)
            except ValueError:
                return jsonify({'message': 'Formato de data de início inválido!'}), 400
        
        if data_fim:
            try:
                data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Paciente.created_at < data_fim_dt)
            except ValueError:
                return jsonify({'message': 'Formato de data de fim inválido!'}), 400
        
        # Executar query
        pacientes = query.order_by(Paciente.created_at.desc()).all()
        
        # Estatísticas adicionais
        total_pacientes = len(pacientes)
        pacientes_com_sessoes = len([
            p for p in pacientes 
            if len(p.sessoes) > 0
        ])
        
        # Registrar log
        log = Log(
            usuario_id=current_user.id,
            acao='GENERATE_PATIENT_REPORT',
            detalhes=f'Relatório de pacientes gerado com {total_pacientes} registros',
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'pacientes': [paciente.to_dict() for paciente in pacientes],
            'estatisticas': {
                'total_pacientes': total_pacientes,
                'pacientes_com_sessoes': pacientes_com_sessoes,
                'pacientes_sem_sessoes': total_pacientes - pacientes_com_sessoes
            }
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500

@bp.route('/relatorios/logs', methods=['GET'])
@token_required
def get_relatorio_logs(current_user):
    """Endpoint para gerar relatório de logs de auditoria (apenas admin)."""
    if current_user.role != 'admin':
        return jsonify({'message': 'Acesso negado!'}), 403
    
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        usuario_id = request.args.get('usuario_id', type=int)
        acao = request.args.get('acao')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Query base
        query = Log.query
        
        # Aplicar filtros
        if data_inicio:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
                query = query.filter(Log.timestamp >= data_inicio_dt)
            except ValueError:
                return jsonify({'message': 'Formato de data de início inválido!'}), 400
        
        if data_fim:
            try:
                data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Log.timestamp < data_fim_dt)
            except ValueError:
                return jsonify({'message': 'Formato de data de fim inválido!'}), 400
        
        if usuario_id:
            query = query.filter(Log.usuario_id == usuario_id)
        
        if acao:
            query = query.filter(Log.acao.ilike(f'%{acao}%'))
        
        # Executar query com paginação
        logs = query.order_by(Log.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'logs': [log.to_dict() for log in logs.items],
            'total': logs.total,
            'pages': logs.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro interno do servidor: {str(e)}'}), 500
