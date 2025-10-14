-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'psicologo', -- admin, psicologo, recepcionista
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id SERIAL PRIMARY KEY,
    nome_completo VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    cpf VARCHAR(14) UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(120),
    endereco TEXT,
    qr_code_data TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Sessões
CREATE TABLE IF NOT EXISTS sessoes (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id),
    psicologo_id INTEGER NOT NULL REFERENCES usuarios(id),
    data_hora TIMESTAMP NOT NULL,
    duracao_minutos INTEGER DEFAULT 50,
    tipo_sessao VARCHAR(50), -- ex: terapia individual, casal, grupo
    status VARCHAR(20) NOT NULL DEFAULT 'agendada', -- agendada, realizada, cancelada
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Evolução (para registrar o progresso do paciente em cada sessão)
CREATE TABLE IF NOT EXISTS evolucao (
    id SERIAL PRIMARY KEY,
    sessao_id INTEGER UNIQUE NOT NULL REFERENCES sessoes(id),
    conteudo TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Logs de Auditoria
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    acao VARCHAR(100) NOT NULL,
    detalhes TEXT,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- Tabela de Clínicas
CREATE TABLE IF NOT EXISTS clinicas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    admin_usuario_id INTEGER REFERENCES usuarios(id) UNIQUE,
    stripe_customer_id VARCHAR(255) UNIQUE,
    plano_atual VARCHAR(50) DEFAULT 'individual',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Adicionando clinica_id à tabela usuarios
ALTER TABLE usuarios
ADD COLUMN clinica_id INTEGER REFERENCES clinicas(id);

-- Adicionando clinica_id à tabela pacientes
ALTER TABLE pacientes
ADD COLUMN clinica_id INTEGER REFERENCES clinicas(id);



-- Habilitar RLS para tabelas relevantes
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE pacientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE evolucao ENABLE ROW LEVEL SECURITY;
ALTER TABLE logs ENABLE ROW LEVEL SECURITY;

-- Política RLS para a tabela 'usuarios': Usuários só podem ver e modificar usuários da sua própria clínica
CREATE POLICY "Users can view their own clinic users" ON usuarios FOR SELECT USING (clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()));
CREATE POLICY "Users can modify their own clinic users" ON usuarios FOR UPDATE USING (clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()));
CREATE POLICY "Users can insert their own clinic users" ON usuarios FOR INSERT WITH CHECK (clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()));
CREATE POLICY "Users can delete their own clinic users" ON usuarios FOR DELETE USING (clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()));

-- Política RLS para a tabela 'pacientes': Usuários só podem ver e modificar pacientes da sua própria clínica
CREATE POLICY "Users can view their own clinic patients" ON pacientes FOR SELECT USING (clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()));
CREATE POLICY "Users can modify their own clinic patients" ON pacientes FOR UPDATE USING (clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()));
CREATE POLICY "Users can insert their own clinic patients" ON pacientes FOR INSERT WITH CHECK (clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()));
CREATE POLICY "Users can delete their own clinic patients" ON pacientes FOR DELETE USING (clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()));

-- Política RLS para a tabela 'sessoes': Usuários só podem ver e modificar sessões de pacientes da sua própria clínica
CREATE POLICY "Users can view their own clinic sessions" ON sessoes FOR SELECT USING (paciente_id IN (SELECT id FROM pacientes WHERE clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid())));
CREATE POLICY "Users can modify their own clinic sessions" ON sessoes FOR UPDATE USING (paciente_id IN (SELECT id FROM pacientes WHERE clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid())));
CREATE POLICY "Users can insert their own clinic sessions" ON sessoes FOR INSERT WITH CHECK (paciente_id IN (SELECT id FROM pacientes WHERE clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid())));
CREATE POLICY "Users can delete their own clinic sessions" ON sessoes FOR DELETE USING (paciente_id IN (SELECT id FROM pacientes WHERE clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid())));

-- Política RLS para a tabela 'evolucao': Usuários só podem ver e modificar evoluções de sessões de pacientes da sua própria clínica
CREATE POLICY "Users can view their own clinic evolutions" ON evolucao FOR SELECT USING (sessao_id IN (SELECT id FROM sessoes WHERE paciente_id IN (SELECT id FROM pacientes WHERE clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()))));
CREATE POLICY "Users can modify their own clinic evolutions" ON evolucao FOR UPDATE USING (sessao_id IN (SELECT id FROM sessoes WHERE paciente_id IN (SELECT id FROM pacientes WHERE clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()))));
CREATE POLICY "Users can insert their own clinic evolutions" ON evolucao FOR INSERT WITH CHECK (sessao_id IN (SELECT id FROM sessoes WHERE paciente_id IN (SELECT id FROM pacientes WHERE clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()))));
CREATE POLICY "Users can delete their own clinic evolutions" ON evolucao FOR DELETE USING (sessao_id IN (SELECT id FROM sessoes WHERE paciente_id IN (SELECT id FROM pacientes WHERE clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid()))));

-- Política RLS para a tabela 'logs': Usuários só podem ver logs da sua própria clínica
CREATE POLICY "Users can view their own clinic logs" ON logs FOR SELECT USING (usuario_id IN (SELECT id FROM usuarios WHERE clinica_id = (SELECT clinica_id FROM usuarios WHERE auth_user_id = auth.uid())));

