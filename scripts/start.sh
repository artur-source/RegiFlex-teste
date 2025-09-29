#!/bin/bash

echo "Iniciando o ambiente RegiFlex com Docker Compose..."

# Navega para o diretório raiz do projeto
cd "$(dirname "$0")"/..

# Inicia os serviços Docker em segundo plano
docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo "
Ambiente RegiFlex iniciado com sucesso!"
    echo "Frontend disponível em: http://localhost:3000"
    echo "Backend API disponível em: http://localhost:5000"
    echo "Banco de Dados PostgreSQL disponível na porta 5432"
else
    echo "
Erro ao iniciar o ambiente RegiFlex."
    exit 1
fi

# Opcional: Exibir logs dos serviços (pode ser removido ou modificado)
# docker-compose logs -f

