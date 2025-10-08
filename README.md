# RegiFlex - Sistema de Gestão para Clínicas de Psicologia

![RegiFlex Logo](frontend/src/assets/regiflex-logo.jpg)

## Visão Geral

O RegiFlex é um sistema completo de gestão para clínicas de psicologia, desenvolvido para simplificar o registro, acompanhamento e análise de informações de pacientes e sessões. Ele oferece uma interface intuitiva e moderna, com funcionalidades que abrangem desde o cadastro de pacientes e agendamento de sessões até a geração de relatórios.

Esta versão foi totalmente migrada para usar **Supabase** como backend, eliminando a necessidade de um servidor próprio e aproveitando os benefícios de um backend gerenciado, escalável e com banco de dados real-time.

## Funcionalidades Principais

- **Gestão de Pacientes:** Cadastro completo de informações demográficas, contato e histórico.
- **Gestão de Sessões:** Agendamento, registro de sessões e evolução do paciente.
- **Autenticação e Autorização:** Sistema de login seguro com diferentes perfis de usuário (Admin, Psicólogo, Recepcionista) gerenciado pelo Supabase.
- **QR Code:** Geração de QR Codes para acesso rápido a informações de pacientes.
- **Backend Gerenciado:** Utiliza Supabase para banco de dados, autenticação e APIs, garantindo escalabilidade e segurança.

## Tecnologias Utilizadas

### Backend (Supabase)

- **Plataforma:** Supabase
- **Banco de Dados:** PostgreSQL
- **Autenticação:** Supabase Auth
- **API:** API RESTful gerada automaticamente pelo Supabase

### Frontend (React.js)

- **Framework:** React.js
- **Gerenciador de Pacotes:** npm
- **Build Tool:** Vite
- **Cliente Supabase:** `@supabase/supabase-js`
- **Estilização:** Tailwind CSS
- **Componentes UI:** Shadcn/ui
- **Ícones:** Lucide React
- **Gráficos:** Recharts

## Estrutura do Projeto

```
RegiFlex-teste/
├── frontend/                     # Aplicação React.js
│   ├── public/                   # Arquivos estáticos
│   ├── src/                      # Código fonte do React
│   │   ├── assets/               # Imagens e outros assets
│   │   ├── components/           # Componentes reutilizáveis (Login, Layout, etc.)
│   │   ├── contexts/             # Contextos React (AuthContext)
│   │   ├── lib/                  # Bibliotecas e clientes, como o supabaseClient.js
│   │   ├── services/             # Serviços de API para comunicação com o Supabase
│   │   ├── App.jsx               # Componente principal da aplicação
│   │   ├── main.jsx              # Ponto de entrada do React
│   │   └── index.css             # Estilos globais
│   ├── .env.example              # Exemplo de variáveis de ambiente
│   ├── .gitignore                # Arquivos ignorados pelo Git
│   └── package.json              # Dependências do Node.js/React
├── docs/                         # Documentação e arquivos de texto organizados
├── .gitignore                    # Arquivos e diretórios a serem ignorados pelo Git
└── README.md                     # Este arquivo
```

## Como Executar (Ambiente de Desenvolvimento)

Para configurar e executar o projeto localmente:

1.  **Pré-requisitos:**
    *   Node.js e npm instalados.
    *   Uma conta no [Supabase](https://supabase.com) com um projeto criado.

2.  **Clone o repositório:**
    ```bash
    git clone https://github.com/artur-source/RegiFlex-teste.git
    cd RegiFlex-teste/frontend
    ```

3.  **Instale as dependências:**
    ```bash
    npm install
    ```

4.  **Configure as Variáveis de Ambiente:**
    - Crie um arquivo `.env` na pasta `frontend/`.
    - Adicione as credenciais do seu projeto Supabase, usando o `.env.example` como referência:
      ```env
      VITE_SUPABASE_URL=https://your-project-id.supabase.co
      VITE_SUPABASE_ANON_KEY=your-public-anon-key
      ```

5.  **Configure o Banco de Dados:**
    - Acesse o seu projeto no Supabase.
    - Vá para o "SQL Editor" e execute o script encontrado em `RegiFlex-teste/database/schema.sql` para criar as tabelas necessárias.

6.  **Inicie o servidor de desenvolvimento:**
    ```bash
    npm run dev
    ```
    - A aplicação estará disponível em `http://localhost:5173`.

7.  **Credenciais de Teste:**
    - Para testar, crie um usuário na tabela `usuarios` do seu banco de dados Supabase. A autenticação simplificada atual buscará o usuário por `username` e não validará a senha.
    - **Exemplo:** `username: admin`

## Deploy

- **Backend:** O backend já está "deployado" e gerenciado pelo Supabase.
- **Frontend:** A aplicação frontend é um site estático e pode ser facilmente "deployada" em serviços como Vercel, Netlify ou GitHub Pages.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT.

