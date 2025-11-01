# RegiFlex - Sistema de Gestão para Clínicas de Psicologia

[![GitHub Pages Status](https://github.com/artur-source/RegiFlex-teste/actions/workflows/pages/pages-build-deployment/badge.svg)](https://artur-source.github.io/RegiFlex-teste/)

O RegiFlex é um sistema de gestão SaaS (Software as a Service) para clínicas e psicólogos autônomos, desenvolvido como um projeto de extensão acadêmica. Ele utiliza uma arquitetura moderna e escalável baseada no Supabase.

## Status Atual do Projeto

O projeto está **funcional** e as principais funcionalidades (Gestão de Pacientes, Agendamento, Relatórios e a Edge Function de IA) foram implementadas e sincronizadas.

| Funcionalidade | Status | Observação |
| :--- | :--- | :--- |
| **Instalação** | **Funcional** | O processo de setup foi corrigido com scripts SQL para inicialização do banco de dados. |
| **IA Integrada** | **Funcional** | Edge Function de previsão de *no-show* implantada e conectada ao frontend. (Modelo de simulação). |
| **Relatórios** | **Funcional** | Módulo de relatórios avançados (gráficos e estatísticas) implementado. |
| **Multi-Tenancy** | **Funcional** | Infraestrutura de banco de dados (tabela `clinicas` e RLS) e código de provisionamento automático (Edge Function) implementados. |

## 1. Tecnologias

- **Frontend:** React.js, Vite, Tailwind CSS, Shadcn/ui, Recharts
- **Backend/Database:** Supabase (PostgreSQL, Auth, Edge Functions)

## 2. Instalação e Setup (Ambiente de Desenvolvimento)

Siga os passos abaixo para configurar o projeto localmente:

### 2.1. Clone o Repositório

```bash
git clone https://github.com/artur-source/RegiFlex-teste.git
cd RegiFlex-teste
```

### 2.2. Configure o Supabase CLI

Certifique-se de ter a [Supabase CLI](https://supabase.com/docs/guides/cli) instalada e logada.

```bash
# Instalar a CLI (se necessário)
# curl -L https://github.com/supabase/cli/releases/latest/download/supabase_linux_amd64.tar.gz | tar -xz && sudo mv supabase /usr/local/bin
# supabase login
```

### 2.3. Vincule ao Projeto Remoto

Vincule seu ambiente local ao projeto Supabase remoto.

- **Project Ref:** `upbsldljfejaieuveknr`

```bash
supabase link --project-ref upbsldljfejaieuveknr
```

### 2.4. Inicialize o Banco de Dados

Execute os scripts SQL para criar o schema e popular com dados de teste.

```bash
# Cria as tabelas e políticas de segurança (RLS)
supabase db reset --local
# O script `schema.sql` e `seed.sql` serão aplicados automaticamente.
```
**Nota:** O comando `supabase db reset --local` é usado para desenvolvimento local. Para aplicar o schema no projeto remoto, use o Dashboard ou o comando `supabase migration up`.

### 2.5. Instale as Dependências do Frontend e Inicie

```bash
cd frontend
npm install
npm run dev
```

O frontend estará acessível em `http://localhost:5173` (ou porta similar).

### 2.6. Credenciais de Teste

Use as seguintes credenciais para acessar o sistema após a inicialização do banco de dados:

| Campo | Valor |
| :--- | :--- |
| **Email** | `admin@regiflex.com` |
| **Senha** | `password` |

## 3. Edge Functions

As Edge Functions foram implantadas no projeto remoto.

| Função | Descrição | Status |
| :--- | :--- | :--- |
| `predict-no-show` | Previsão de risco de *no-show* em sessões agendadas. | **Deploy Feito** |
| `provision-new-tenant` | Lógica de provisionamento automático de novos clientes. | **Deploy Feito** |

## 4. Próximos Passos Críticos

Os próximos passos para a viabilidade comercial do RegiFlex são:

1.  **Refinamento da IA:** Substituir o modelo de simulação (`predict-no-show/index.ts`) por um modelo treinado com dados reais.
2.  **Conclusão dos Relatórios Avançados:** Implementar a funcionalidade de exportação de dados (CSV/PDF) no módulo de relatórios.
