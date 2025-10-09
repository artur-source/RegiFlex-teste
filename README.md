# RegiFlex - Sistema de Gestão para Clínicas de Psicologia

![RegiFlex Logo](frontend/src/assets/regiflex-logo.jpg)

## 🎯 Visão Geral

O RegiFlex é um **sistema moderno e completo** de gestão para clínicas de psicologia, desenvolvido para simplificar o registro, acompanhamento e análise de informações de pacientes e sessões. Com uma interface intuitiva e responsiva, oferece funcionalidades que abrangem desde o cadastro de pacientes até a geração de relatórios avançados.

**Arquitetura Moderna:** Totalmente baseada em **Supabase** como Backend-as-a-Service, eliminando a complexidade de gerenciar servidores próprios e oferecendo escalabilidade automática, segurança robusta e banco de dados real-time.

## ✨ Funcionalidades Principais

- **👥 Gestão de Pacientes** - Cadastro completo com informações demográficas, contato e histórico médico
- **📅 Gestão de Sessões** - Agendamento inteligente, registro detalhado e acompanhamento da evolução
- **🔐 Autenticação Segura** - Sistema de login robusto com diferentes perfis (Admin, Psicólogo, Recepcionista)
- **📱 QR Code** - Geração e leitura de QR Codes para acesso rápido às informações dos pacientes
- **📊 Dashboard Intuitivo** - Visão geral com métricas importantes e gráficos interativos
- **🤖 IA Integrada** - Análise de padrões e alertas inteligentes (em desenvolvimento)

## 🚀 Tecnologias Utilizadas

### Backend (Supabase)
- **Plataforma:** [Supabase](https://supabase.com) - Backend-as-a-Service
- **Banco de Dados:** PostgreSQL com Row Level Security (RLS)
- **Autenticação:** Supabase Auth com JWT
- **API:** RESTful API gerada automaticamente
- **Real-time:** Subscriptions em tempo real

### Frontend (React.js)
- **Framework:** React 18.3.1 com Hooks
- **Build Tool:** Vite 5.2.0 para desenvolvimento rápido
- **Estilização:** Tailwind CSS 3.4.4 para design responsivo
- **Componentes:** Shadcn/ui para interface consistente
- **Roteamento:** React Router 7.6.1
- **Gráficos:** Recharts para visualizações
- **Ícones:** Lucide React

## 📁 Estrutura do Projeto

```
RegiFlex-teste/
├── 📂 frontend/                  # Aplicação React.js
│   ├── 📂 public/               # Arquivos estáticos
│   ├── 📂 src/                  # Código fonte
│   │   ├── 📂 components/       # Componentes React reutilizáveis
│   │   ├── 📂 contexts/         # Context API (AuthContext)
│   │   ├── 📂 lib/              # Configurações (Supabase client)
│   │   ├── 📂 services/         # Serviços de API
│   │   ├── 📂 assets/           # Imagens e recursos
│   │   └── 📄 App.jsx           # Componente principal
│   └── 📄 package.json          # Dependências do projeto
├── 📂 database/                 # Schema do banco de dados
├── 📂 docs/                     # Documentação técnica
├── 📄 ARCHITECTURE.md           # Documentação da arquitetura
├── 📄 CONTRIBUTING.md           # Guia de contribuição
├── 📄 DEPLOYMENT.md             # Instruções de deploy
└── 📄 README.md                 # Este arquivo
```

## ⚡ Início Rápido

### Pré-requisitos

- **Node.js** 18.0+ e npm
- **Conta Supabase** (gratuita) - [Criar conta](https://supabase.com)
- **Git** para clonagem do repositório

### 🛠️ Configuração Local

```bash
# 1. Clone o repositório
git clone https://github.com/artur-source/RegiFlex-teste.git
cd RegiFlex-teste

# 2. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais do Supabase

# 3. Instale as dependências
cd frontend
npm install

# 4. Inicie o servidor de desenvolvimento
npm run dev
```

A aplicação estará disponível em `http://localhost:5173`

### 🗄️ Configuração do Banco de Dados

1. **Crie um projeto no Supabase:**
   - Acesse [supabase.com](https://supabase.com)
   - Clique em "New Project"
   - Anote a URL e a chave pública do projeto

2. **Configure o schema:**
   - Vá para o SQL Editor no dashboard do Supabase
   - Execute o conteúdo do arquivo `database/schema.sql`

3. **Atualize o arquivo `.env`:**
   ```env
   VITE_SUPABASE_URL=https://seu-projeto.supabase.co
   VITE_SUPABASE_ANON_KEY=sua-chave-publica-aqui
   ```

### 👤 Primeiro Acesso

Para criar o primeiro usuário administrador, execute no SQL Editor do Supabase:

```sql
INSERT INTO usuarios (username, email, password_hash, role) 
VALUES ('admin', 'admin@regiflex.com', 'temp_password', 'admin');
```

**Login:** `admin` | **Senha:** Qualquer senha (autenticação simplificada para desenvolvimento)

## 🚀 Deploy em Produção

### Opções de Hospedagem

**Frontend (Recomendado: Vercel)**
- ✅ **Vercel** - Deploy automático via Git, otimizado para React
- ✅ **Netlify** - Alternativa robusta com recursos similares  
- ✅ **GitHub Pages** - Gratuito para projetos open source

**Backend**
- ✅ **Supabase** - Totalmente gerenciado, sem configuração adicional necessária

### Deploy Rápido na Vercel

1. **Conecte seu repositório GitHub à Vercel**
2. **Configure as variáveis de ambiente:**
   ```
   VITE_SUPABASE_URL=https://seu-projeto.supabase.co
   VITE_SUPABASE_ANON_KEY=sua-chave-publica
   ```
3. **Deploy automático** - Cada push na branch main fará deploy automaticamente

📖 **Guia Completo:** Consulte [DEPLOYMENT.md](DEPLOYMENT.md) para instruções detalhadas

## 📚 Documentação

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Documentação técnica da arquitetura
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guia para contribuidores
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Instruções completas de deploy
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de versões

## 🤝 Contribuição

Contribuições são muito bem-vindas! Este é um projeto open source e toda ajuda é apreciada.

### Como Contribuir

1. **Fork** o repositório
2. **Crie uma branch** para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -m 'feat: adicionar nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra um Pull Request**

📖 **Guia Detalhado:** Consulte [CONTRIBUTING.md](CONTRIBUTING.md)

## 🐛 Reportar Bugs

Encontrou um bug? Ajude-nos a melhorar!

1. **Verifique** se o bug já foi reportado nas [Issues](https://github.com/artur-source/RegiFlex-teste/issues)
2. **Crie uma nova Issue** com detalhes sobre o problema
3. **Inclua** passos para reproduzir e screenshots se possível

## 💡 Solicitar Funcionalidades

Tem uma ideia para melhorar o RegiFlex?

1. **Abra uma Issue** com o label "enhancement"
2. **Descreva** detalhadamente a funcionalidade desejada
3. **Explique** como ela beneficiaria os usuários

## 📊 Status do Projeto

- ✅ **Gestão de Pacientes** - Completo
- ✅ **Gestão de Sessões** - Completo  
- ✅ **Autenticação** - Completo
- ✅ **QR Code** - Completo
- ✅ **Dashboard** - Completo
- 🚧 **Relatórios Avançados** - Em desenvolvimento
- 🚧 **IA Integrada** - Em desenvolvimento
- 📋 **Mobile App** - Planejado

## 🏆 Reconhecimentos

- **[Supabase](https://supabase.com)** - Backend-as-a-Service incrível
- **[Shadcn/ui](https://ui.shadcn.com)** - Componentes UI elegantes
- **[Tailwind CSS](https://tailwindcss.com)** - Framework CSS utilitário
- **Comunidade Open Source** - Por todas as bibliotecas utilizadas

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">

**Desenvolvido com ❤️ para simplificar a gestão de clínicas de psicologia**

[🌟 Star no GitHub](https://github.com/artur-source/RegiFlex-teste) • [🐛 Reportar Bug](https://github.com/artur-source/RegiFlex-teste/issues) • [💡 Solicitar Feature](https://github.com/artur-source/RegiFlex-teste/issues)

</div>

