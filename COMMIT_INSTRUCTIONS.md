# Instruções para Commits - RegiFlex

**Versão:** 2.0.0  
**Arquitetura:** Supabase + React.js

Este documento fornece diretrizes para manter o histórico do projeto organizado e consistente após a migração para Supabase.

---

## Estrutura de Commits Recomendada

### 1. Commits de Configuração Supabase

```bash
# Commit 1: Cliente Supabase
git add frontend/src/lib/supabaseClient.js frontend/.env.example
git commit -m "[Feature] Configuração do cliente Supabase

- Criado supabaseClient.js com configuração
- Adicionado .env.example com variáveis necessárias
- Integração com Supabase estabelecida
- Melhoria na arquitetura do projeto"

# Commit 2: Serviços de API
git add frontend/src/services/supabaseApi.js
git commit -m "[Feature] Implementação de serviços com Supabase

- Criado supabaseApi.js com operações CRUD
- Métodos para pacientes, sessões e usuários
- Tratamento de erros padronizado
- Melhoria na organização do código"

# Commit 3: Contexto de Autenticação
git add frontend/src/contexts/AuthContext.jsx
git commit -m "[Refactor] Atualização do contexto de autenticação

- Migrado para usar Supabase
- Implementada autenticação simplificada
- Gerenciamento de estado do usuário
- Melhoria na segurança"
```

### 2. Commits de Refatoração Frontend

```bash
# Commit 4: Componentes atualizados
git add frontend/src/components/
git commit -m "[Refactor] Atualização de componentes para Supabase

- Componentes adaptados para nova API
- Remoção de referências ao Flask
- Tratamento de erros aprimorado
- Melhoria na consistência da UI"

# Commit 5: Hooks e utilitários
git add frontend/src/hooks/ frontend/src/lib/validators.js
git commit -m "[Feature] Sistema de validação e hooks customizados

- Hook useFormValidation para formulários
- Validadores e formatadores centralizados
- Melhoria na reutilização de código
- Validação em tempo real"
```

### 3. Commits de Banco de Dados

```bash
# Commit 6: Schema do banco
git add database/schema.sql
git commit -m "[Database] Schema atualizado para Supabase

- Tabelas: usuarios, pacientes, sessoes, evolucao, logs
- Constraints e relacionamentos definidos
- Compatível com PostgreSQL do Supabase
- Melhoria na estrutura de dados"
```

### 4. Commits de Documentação

```bash
# Commit 7: README atualizado
git add README.md
git commit -m "[Docs] Atualização do README para arquitetura Supabase

- Instruções de instalação simplificadas
- Tecnologias atualizadas
- Remoção de referências a Docker
- Melhoria na clareza da documentação"

# Commit 8: Tutorial de instalação
git add docs/tutoriais/RegiFlex_Tutorial_Completo_Windows.md
git commit -m "[Docs] Tutorial de instalação atualizado

- Processo simplificado sem Docker
- Instruções para configuração do Supabase
- Solução de problemas comuns
- Melhoria na experiência do usuário"

# Commit 9: Documentação de integrações
git add docs/planos/INTEGRACOES_WIX_NOTION.md
git commit -m "[Docs] Documentação de integrações Wix e Notion

- Casos de uso e benefícios
- Implementação técnica
- Próximos passos
- Melhoria no planejamento do projeto"

# Commit 10: CHANGELOG
git add CHANGELOG.md
git commit -m "[Docs] Criação do CHANGELOG

- Histórico completo de versões
- Detalhamento da migração Supabase
- Benefícios e mudanças
- Melhoria na rastreabilidade"
```

### 5. Commits de Página de Marketing

```bash
# Commit 11: Atualização da página de marketing
git add index.html
git commit -m "[Docs] Atualização da página de marketing

- Tecnologias backend atualizadas para Supabase
- Remoção de Docker e Flask
- Adicionadas novas tecnologias
- Melhoria na apresentação do projeto"
```

---

## Padrão de Mensagens de Commit

### Formato:
```
[Tipo] Descrição breve

- Detalhe 1
- Detalhe 2
- Resultado esperado
```

### Tipos de Commit:
- **[Feature]**: Nova funcionalidade
- **[Fix]**: Correção de bug
- **[Refactor]**: Refatoração de código
- **[Test]**: Adição ou correção de testes
- **[Docs]**: Documentação
- **[Database]**: Alterações no banco de dados
- **[Style]**: Formatação, espaços, etc.
- **[Perf]**: Melhoria de performance
- **[Security]**: Correções de segurança
- **[Deploy]**: Configurações de deploy

### Exemplos de Boas Práticas:

```bash
# ✅ Bom
git commit -m "[Feature] Integração com Supabase Auth

- Implementada autenticação via Supabase
- Login e logout funcionais
- Gerenciamento de sessão
- Melhoria na segurança do sistema"

# ❌ Ruim
git commit -m "fix auth"
```

---

## Sequência de Commits Recomendada (Migração Supabase)

### 1. Primeiro: Configuração Base
```bash
git add frontend/src/lib/supabaseClient.js frontend/.env.example
git commit -m "[Feature] Configuração do cliente Supabase"
```

### 2. Segundo: Serviços de API
```bash
git add frontend/src/services/supabaseApi.js frontend/src/services/api.js
git commit -m "[Feature] Implementação de serviços com Supabase"
```

### 3. Terceiro: Autenticação
```bash
git add frontend/src/contexts/AuthContext.jsx
git commit -m "[Refactor] Atualização do contexto de autenticação"
```

### 4. Quarto: Componentes
```bash
git add frontend/src/components/
git commit -m "[Refactor] Atualização de componentes para Supabase"
```

### 5. Quinto: Documentação
```bash
git add README.md CHANGELOG.md docs/
git commit -m "[Docs] Atualização completa da documentação"
```

### 6. Sexto: Página de Marketing
```bash
git add index.html
git commit -m "[Docs] Atualização da página de marketing"
```

---

## Verificação Antes do Commit

### Checklist:
- [ ] Código testado localmente
- [ ] Mensagem de commit clara e descritiva
- [ ] Arquivos relacionados agrupados
- [ ] Não há arquivos desnecessários
- [ ] Documentação atualizada (se necessário)
- [ ] Variáveis de ambiente não commitadas (apenas .env.example)

### Comandos de Verificação:
```bash
# Verificar status
git status

# Verificar diferenças
git diff --cached

# Verificar histórico
git log --oneline -5

# Verificar se .env não está sendo commitado
git status | grep ".env"
```

---

## Push para o Repositório

### Após todos os commits:
```bash
# Push para o repositório
git push origin main

# Ou se for a primeira vez
git push -u origin main
```

### Verificação Final:
```bash
# Verificar se o push foi bem-sucedido
git log --oneline -10

# Verificar status do repositório remoto
git status
```

---

## Resolução de Conflitos

### Se houver conflitos:
```bash
# Puxar mudanças remotas
git pull origin main

# Resolver conflitos manualmente
# Adicionar arquivos resolvidos
git add .

# Fazer commit da resolução
git commit -m "[Fix] Resolução de conflitos de merge"

# Push das mudanças
git push origin main
```

---

## Rollback (se necessário)

### Desfazer último commit (não pushado):
```bash
git reset --soft HEAD~1
```

### Desfazer mudanças em arquivo específico:
```bash
git checkout -- arquivo.js
```

### Desfazer todas as mudanças não commitadas:
```bash
git reset --hard HEAD
```

### Reverter commit já pushado:
```bash
git revert <commit-hash>
git push origin main
```

---

## Comandos Úteis

### Visualizar histórico:
```bash
# Histórico gráfico
git log --oneline --graph --all

# Histórico detalhado
git log --stat

# Histórico de um arquivo específico
git log --follow -- arquivo.js
```

### Verificar diferenças:
```bash
# Diferenças não staged
git diff

# Diferenças staged
git diff --cached

# Diferenças com commit anterior
git diff HEAD~1
```

### Verificar arquivos modificados:
```bash
git diff --name-only
git status --porcelain
```

### Buscar em commits:
```bash
# Buscar por mensagem
git log --grep="Supabase"

# Buscar por autor
git log --author="nome"

# Buscar por data
git log --since="2025-10-01"
```

---

## Boas Práticas Específicas para Supabase

### 1. Nunca Commitar Credenciais

❌ **Nunca faça:**
```bash
git add frontend/.env
```

✅ **Sempre faça:**
```bash
git add frontend/.env.example
```

### 2. Documentar Mudanças no Schema

Sempre que alterar o schema do banco de dados:

```bash
git add database/schema.sql
git commit -m "[Database] Atualização do schema

- Adicionada coluna X na tabela Y
- Criado índice para melhorar performance
- Atualizado relacionamento entre tabelas
- Melhoria na estrutura de dados"
```

### 3. Atualizar Documentação Junto com Código

Quando adicionar uma nova funcionalidade:

```bash
# Commit do código
git add frontend/src/components/NovoComponente.jsx
git commit -m "[Feature] Novo componente de relatórios"

# Commit da documentação
git add README.md docs/
git commit -m "[Docs] Documentação do componente de relatórios"
```

---

## Integração Contínua

### Antes de fazer push:

```bash
# 1. Atualizar branch local
git pull origin main

# 2. Executar testes (se houver)
npm test

# 3. Verificar build
npm run build

# 4. Verificar lint (se configurado)
npm run lint

# 5. Push
git push origin main
```

---

## Trabalhando com Branches

### Criar branch para nova funcionalidade:
```bash
git checkout -b feature/nome-da-funcionalidade
```

### Fazer commits na branch:
```bash
git add .
git commit -m "[Feature] Descrição"
```

### Merge na main:
```bash
git checkout main
git merge feature/nome-da-funcionalidade
git push origin main
```

### Deletar branch:
```bash
git branch -d feature/nome-da-funcionalidade
```

---

## Conclusão

Commits bem organizados facilitam a manutenção e colaboração no projeto. Com a nova arquitetura Supabase, é ainda mais importante manter a documentação atualizada e as mensagens de commit claras.

**Lembre-se**: Cada commit deve contar uma história clara do que foi feito e por quê.

---

**Documento atualizado por:** Equipe RegiFlex  
**Versão:** 2.0.0  
**Data:** Outubro de 2025
