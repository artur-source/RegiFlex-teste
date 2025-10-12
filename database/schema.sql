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

