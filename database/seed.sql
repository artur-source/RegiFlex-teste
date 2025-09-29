-- Inserir um usuário de exemplo (admin)
INSERT INTO usuarios (username, email, password_hash, role) VALUES
(
    'admin',
    'admin@regiflex.com',
    '$2b$12$DeGPdyYjRURj2pJO1g4lxelnjgUeQkTmAFIo/jpYUJVM6LA2HcFY2', -- Senha: password (hash gerado com bcrypt)
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- Inserir um psicólogo de exemplo
INSERT INTO usuarios (username, email, password_hash, role) VALUES
(
    'psicologo1',
    'psicologo1@regiflex.com',
    '$2b$12$DeGPdyYjRURj2pJO1g4lxelnjgUeQkTmAFIo/jpYUJVM6LA2HcFY2',
    'psicologo'
) ON CONFLICT (username) DO NOTHING;

-- Inserir um recepcionista de exemplo
INSERT INTO usuarios (username, email, password_hash, role) VALUES
(
    'recepcionista1',
    'recepcionista1@regiflex.com',
    '$2b$12$DeGPdyYjRURj2pJO1g4lxelnjgUeQkTmAFIo/jpYUJVM6LA2HcFY2',
    'recepcionista'
) ON CONFLICT (username) DO NOTHING;

-- Inserir um paciente de exemplo
INSERT INTO pacientes (nome_completo, data_nascimento, cpf, telefone, email, endereco, qr_code_data) VALUES
(
    'Maria Silva',
    '1990-05-15',
    '111.222.333-44',
    '11987654321',
    'maria.silva@example.com',
    'Rua Exemplo, 123, São Paulo - SP',
    'regiflex_patient_1'
) ON CONFLICT (qr_code_data) DO NOTHING;

-- Inserir uma sessão de exemplo
INSERT INTO sessoes (paciente_id, psicologo_id, data_hora, status) VALUES
(
    (SELECT id FROM pacientes WHERE qr_code_data = 'regiflex_patient_1'),
    (SELECT id FROM usuarios WHERE username = 'psicologo1'),
    '2025-10-01 10:00:00',
    'agendada'
) ON CONFLICT DO NOTHING;

-- Inserir uma evolução de exemplo para a sessão
INSERT INTO evolucao (sessao_id, conteudo) VALUES
(
    (SELECT id FROM sessoes WHERE paciente_id = (SELECT id FROM pacientes WHERE qr_code_data = 'regiflex_patient_1') AND data_hora = '2025-10-01 10:00:00'),
    'Paciente apresentou melhora significativa na última semana, com redução da ansiedade e aumento da proatividade.'
) ON CONFLICT DO NOTHING;

