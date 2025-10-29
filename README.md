# RegiFlex - Sistema de Gestão para Clínicas de Psicologia

[![Status](https://img.shields.io/badge/Status-Comercialização-brightgreen)](https://github.com/artur-source/RegiFlex-teste)
[![Tecnologia](https://img.shields.io/badge/Frontend-React%2018.3.1-blue)](https://reactjs.org/)
[![Backend](https://img.shields.io/badge/Backend-Supabase-green)](https://supabase.com/)
[![Última Correção](https://img.shields.io/badge/Última%20Correção-2025--10--10-brightgreen)](./BUGFIXES.md)

## Sobre o Projeto

O RegiFlex é uma **solução SaaS completa** para gestão de clínicas de psicologia, desenvolvida com arquitetura **multi-tenant** e **provisionamento automatizado**. O sistema foi projetado para ser comercializado como uma startup de **custo zero**, utilizando serviços com planos gratuitos robustos.

### 💰 Modelo de Negócio Validado
- **Custo Operacional:** Apenas **R$ 3,33/mês** (domínio)
- **Break-Even:** 1 cliente (R$ 34,90 > R$ 3,33)
- **Planos:** Individual (R$ 34,90/mês) e Clínica (R$ 99,90/mês)
- **Provisionamento:** 100% automatizado para novos clientes

### 🔗 Links Importantes
- **Página de Marketing:** [https://artur-source.github.io/RegiFlex/](https://artur-source.github.io/RegiFlex/)
- **Contato Comercial:** regiflex.contato@gmail.com

## 🚀 Tecnologias Utilizadas

### Frontend
- **React 18.3.1** - Biblioteca para construção de interfaces
- **Vite 5.2.0** - Build tool e servidor de desenvolvimento
- **Tailwind CSS** - Framework CSS utilitário
- **Lucide React** - Biblioteca de ícones

### Backend e Infraestrutura
- **Supabase** - Backend-as-a-Service
  - PostgreSQL com Row Level Security (RLS)
  - Autenticação JWT integrada
  - APIs RESTful geradas automaticamente
  - Armazenamento de arquivos

## ✅ Status das Funcionalidades

| Funcionalidade | Status | Descrição |
|---|---|---|
| 🏥 **Gestão de Pacientes** | ✅ Completa | Cadastro, edição e histórico completo |
| 📅 **Gestão de Sessões** | ✅ Completa | Agendamento e controle de sessões |
| 🔐 **Autenticação** | ✅ Completa | Sistema seguro com diferentes perfis |
| 📱 **QR Code** | ✅ Completa | Geração de códigos para check-in |
| 📊 **Dashboard** | ✅ Completa | Visão geral e métricas principais |
| 📈 **Relatórios Avançados** | 🚧 Em Desenvolvimento | Análises detalhadas e exportação |
| 🤖 **IA Integrada** | 🚧 Em Desenvolvimento | Assistente inteligente e alertas |
| 📱 **Mobile App** | 📋 Planejado | Aplicativo nativo para dispositivos móveis |

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Node.js 18+ 
- npm ou yarn
- Conta no Supabase

### Passos para Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/artur-source/RegiFlex-teste.git
   cd RegiFlex-teste
   ```

2. **Instale as dependências (Frontend)**
   ```bash
   cd frontend && npm install && cd ..
   ```

3. **Configure as variáveis de ambiente (Frontend)**
   ```bash
   cp frontend/.env.example frontend/.env
   ```
   
   Edite o arquivo `frontend/.env` com suas credenciais do Supabase:
   ```env
   VITE_SUPABASE_URL=sua_url_do_supabase
   VITE_SUPABASE_ANON_KEY=sua_chave_anonima_do_supabase
   ```

4. **Configure o Banco de Dados (Supabase)**
   ```bash
   - Crie um novo projeto no Supabase.
- No seu projeto Supabase, vá em **SQL Editor** e execute o script `supabase/schema.sql` para criar a estrutura de tabelas, RLS e dados de teste.
- **Importante:** O script `schema.sql` inclui um `tenant_id` de teste ('00000000-0000-0000-0000-000000000001'). Para testar o login, você precisará criar um usuário de teste no Supabase Auth (ex: `admin@regiflex.com` com a senha `password`) e garantir que o `id` deste usuário esteja associado ao `tenant_id` de teste na tabela `profiles`.

5. **Execute o projeto (Frontend)**
   ```bash
   cd frontend
   npm run dev
   ```
   ```

6. **Acesse o sistema**
   - URL: `http://localhost:5173` (ou a porta indicada pelo Vite)
   - Credenciais de teste:
     - **Admin:** admin@regiflex.com / password (após configurar o usuário no Supabase Auth)
     - **Psicólogo:** psicologo1@regiflex.com / password (após configurar o usuário no Supabase Auth)
     - **Recepcionista:** recepcionista1@regiflex.com / password (após configurar o usuário no Supabase Auth)

## 🔧 Correções Recentes

### Outubro 2025
- **✅ Corrigido:** Erro de sintaxe em `Sessoes.jsx` que impedia a execução do servidor
- **✅ Melhorado:** Documentação de instalação e configuração
- **✅ Adicionado:** Histórico de correções em `BUGFIXES.md`

Para ver o histórico completo de correções, consulte [BUGFIXES.md](./BUGFIXES.md).

## 🏗️ Arquitetura do Sistema

O RegiFlex utiliza uma arquitetura moderna e escalável:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │   Supabase      │    │   PostgreSQL    │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Componentes Principais
- **AuthContext:** Gerenciamento de autenticação e sessões
- **Dashboard:** Painel principal com métricas e navegação
- **Pacientes:** CRUD completo para gestão de pacientes
- **Sessões:** Agendamento e controle de sessões terapêuticas
- **QRCode:** Geração de códigos para facilitar check-ins

## 🔒 Segurança

- **Autenticação JWT** via Supabase Auth
- **Row Level Security (RLS)** no PostgreSQL
- **Criptografia** de dados sensíveis
- **Controle de acesso** baseado em perfis (admin, psicólogo, recepcionista)

## 📚 Documentação Adicional

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detalhes da arquitetura do sistema
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Guia para contribuidores
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Instruções de deploy
- [BUGFIXES.md](./BUGFIXES.md) - Histórico de correções

## 🤝 Contribuindo

Este projeto está em desenvolvimento ativo. Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Para dúvidas, sugestões ou reportar problemas:
- Abra uma [issue](https://github.com/artur-source/RegiFlex-teste/issues)
- Entre em contato através do [repositório principal](https://github.com/artur-source/RegiFlex)

---

**RegiFlex** - Transformando a gestão de clínicas de psicologia com tecnologia moderna e segura.
