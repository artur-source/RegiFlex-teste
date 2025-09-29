#!/bin/bash

echo "🚀 Iniciando ambiente de desenvolvimento RegiFlex..."

# Função para verificar se uma porta está em uso
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Porta $port já está em uso"
        return 1
    fi
    return 0
}

# Verificar portas necessárias
echo "🔍 Verificando portas disponíveis..."
check_port 5432 || echo "   PostgreSQL pode estar rodando"
check_port 5000 || echo "   Backend pode estar rodando"
check_port 3000 || echo "   Frontend pode estar rodando"

# Navegar para o diretório do projeto
cd "$(dirname "$0")/.."

echo "📦 Instalando dependências do backend..."
cd backend
pip install -r requirements.txt
cd ..

echo "📦 Instalando dependências do frontend..."
cd frontend
pnpm install
cd ..

echo "🐳 Iniciando banco de dados com Docker..."
docker-compose up -d db

# Aguardar o banco estar pronto
echo "⏳ Aguardando banco de dados..."
sleep 10

echo "🔧 Configurando banco de dados (via Docker)..."
docker-compose exec backend python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print(\'✅ Tabelas criadas com sucesso!\')
"

echo "
🎉 Ambiente configurado com sucesso!

Para iniciar os serviços:

Terminal 1 - Backend:
cd backend && python wsgi.py

Terminal 2 - Frontend:
cd frontend && pnpm run dev

Ou use Docker Compose:
docker-compose up

URLs:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Banco: localhost:5432

Credenciais de teste:
- Admin: admin / password
- Psicólogo: psicologo1 / password
- Recepcionista: recepcionista1 / password
"
