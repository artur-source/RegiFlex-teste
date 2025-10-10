# RegiFlex - Sistema de Gestão para Clínicas de Psicologia

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)](https://github.com/artur-source/RegiFlex-teste)
[![Tecnologia](https://img.shields.io/badge/Frontend-React%2018.3.1-blue)](https://reactjs.org/)
[![Backend](https://img.shields.io/badge/Backend-Supabase-green)](https://supabase.com/)
[![Última Correção](https://img.shields.io/badge/Última%20Correção-2025--10--10-brightgreen)](./BUGFIXES.md)

## Sobre o Projeto

O RegiFlex é um sistema moderno de gestão para clínicas de psicologia, desenvolvido com foco na simplicidade, segurança e eficiência. Utilizando tecnologias de ponta como React e Supabase, oferece uma solução completa para o gerenciamento de pacientes, sessões e operações administrativas.

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
   cd RegiFlex-teste/frontend
   ```

2. **Instale as dependências**
   ```bash
   npm install
   ```

3. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   ```
   
   Edite o arquivo `.env` com suas credenciais do Supabase:
   ```env
   VITE_SUPABASE_URL=sua_url_do_supabase
   VITE_SUPABASE_ANON_KEY=sua_chave_anonima_do_supabase
   ```

4. **Execute o projeto**
   ```bash
   npm run dev
   ```

5. **Acesse o sistema**
   - URL: `http://localhost:5173`
   - Credenciais de teste:
     - **Admin:** admin / password
     - **Psicólogo:** psicologo1 / password
     - **Recepcionista:** recepcionista1 / password

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
