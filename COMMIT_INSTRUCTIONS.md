# Instruções para Commits - RegiFlex

## Estrutura de Commits Recomendada

Para manter o histórico do projeto organizado, siga esta estrutura de commits:

### 1. Commits de Refatoração Backend

```bash
# Commit 1: Estrutura de pastas
git add backend/app/api/v1/ backend/app/utils/ backend/app/middleware/
git commit -m "[Refactor] Reorganização da estrutura de pastas do backend

- Criada estrutura api/v1/ para endpoints organizados
- Adicionados módulos utils/ para utilitários
- Criado middleware/ para tratamento de erros
- Melhoria na organização e manutenibilidade"

# Commit 2: Validações
git add backend/app/utils/validators.py
git commit -m "[Feature] Sistema de validações robustas

- Implementadas validações para CPF, email, telefone
- Validação de data de nascimento com idade
- Validação de nome com caracteres permitidos
- Melhoria na segurança e consistência dos dados"

# Commit 3: Tratamento de erros
git add backend/app/middleware/ backend/app/utils/logger.py backend/app/utils/response.py
git commit -m "[Feature] Sistema de tratamento de erros e logging

- Middleware global de tratamento de erros
- Sistema de logging estruturado
- Respostas padronizadas da API
- Melhoria na experiência de debugging"

# Commit 4: Endpoints API v1
git add backend/app/api/v1/
git commit -m "[Feature] Implementação da API v1

- Endpoints organizados por funcionalidade
- Validação de entrada em todos os endpoints
- Logging de requisições e ações
- Melhoria na estrutura e manutenibilidade"
```

### 2. Commits de Refatoração Frontend

```bash
# Commit 5: Componentes padronizados
git add frontend/src/components/PatientForm.jsx frontend/src/components/ui/ErrorMessage.jsx
git commit -m "[Refactor] Padronização de componentes React

- Criado PatientForm.jsx unificado
- Componentes de mensagem reutilizáveis
- Remoção de arquivos duplicados
- Melhoria na consistência da UI"

# Commit 6: Hooks e utilitários
git add frontend/src/hooks/ frontend/src/lib/validators.js
git commit -m "[Feature] Sistema de validação e hooks customizados

- Hook useFormValidation para formulários
- Validadores e formatadores centralizados
- Melhoria na reutilização de código
- Validação em tempo real"
```

### 3. Commits de Testes

```bash
# Commit 7: Testes backend
git add backend/tests/ backend/requirements.txt
git commit -m "[Test] Implementação de testes unitários

- Testes para autenticação e pacientes
- Testes para validadores
- Cobertura de testes básica
- Melhoria na confiabilidade do código"
```

### 4. Commits de Documentação

```bash
# Commit 8: Documentação técnica
git add DOCUMENTATION.md CHANGELOG.md
git commit -m "[Docs] Documentação técnica completa

- Documentação detalhada da arquitetura
- Changelog com histórico de mudanças
- Instruções para futuras modificações
- Melhoria na manutenibilidade do projeto"
```

### 5. Commits de Dependências

```bash
# Commit 9: Atualização de dependências
git add backend/requirements.txt frontend/package.json
git commit -m "[Deps] Atualização de dependências

- Flask 2.3.2 → 3.0.0
- SQLAlchemy 2.0.21 → 2.0.23
- Pandas 2.1.1 → 2.1.4
- Melhoria na segurança e performance"
```

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
- **[Deps]**: Dependências
- **[Style]**: Formatação, espaços, etc.
- **[Perf]**: Melhoria de performance
- **[Security]**: Correções de segurança

### Exemplos de Boas Práticas:

```bash
# ✅ Bom
git commit -m "[Feature] Sistema de validação de CPF

- Implementada validação completa com dígitos verificadores
- Formatação automática no frontend
- Validação em tempo real
- Melhoria na experiência do usuário"

# ❌ Ruim
git commit -m "fix cpf"
```

## Sequência de Commits Recomendada

### 1. Primeiro: Estrutura Base
```bash
git add backend/app/api/v1/ backend/app/utils/ backend/app/middleware/
git commit -m "[Refactor] Reorganização da estrutura de pastas do backend"
```

### 2. Segundo: Validações
```bash
git add backend/app/utils/validators.py
git commit -m "[Feature] Sistema de validações robustas"
```

### 3. Terceiro: Tratamento de Erros
```bash
git add backend/app/middleware/ backend/app/utils/logger.py backend/app/utils/response.py
git commit -m "[Feature] Sistema de tratamento de erros e logging"
```

### 4. Quarto: API v1
```bash
git add backend/app/api/v1/
git commit -m "[Feature] Implementação da API v1"
```

### 5. Quinto: Frontend
```bash
git add frontend/src/components/PatientForm.jsx frontend/src/hooks/ frontend/src/lib/validators.js
git commit -m "[Refactor] Padronização de componentes e validações do frontend"
```

### 6. Sexto: Testes
```bash
git add backend/tests/
git commit -m "[Test] Implementação de testes unitários"
```

### 7. Sétimo: Documentação
```bash
git add DOCUMENTATION.md CHANGELOG.md
git commit -m "[Docs] Documentação técnica completa"
```

### 8. Oitavo: Dependências
```bash
git add backend/requirements.txt
git commit -m "[Deps] Atualização de dependências"
```

## Verificação Antes do Commit

### Checklist:
- [ ] Código testado localmente
- [ ] Mensagem de commit clara e descritiva
- [ ] Arquivos relacionados agrupados
- [ ] Não há arquivos desnecessários
- [ ] Documentação atualizada (se necessário)

### Comandos de Verificação:
```bash
# Verificar status
git status

# Verificar diferenças
git diff --cached

# Verificar histórico
git log --oneline -5
```

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
```

## Rollback (se necessário)

### Desfazer último commit (não pushado):
```bash
git reset --soft HEAD~1
```

### Desfazer mudanças em arquivo específico:
```bash
git checkout -- arquivo.py
```

### Desfazer todas as mudanças não commitadas:
```bash
git reset --hard HEAD
```

## Comandos Úteis

### Visualizar histórico:
```bash
git log --oneline --graph
```

### Verificar diferenças:
```bash
git diff HEAD~1
```

### Verificar arquivos modificados:
```bash
git diff --name-only
```

### Verificar status detalhado:
```bash
git status --porcelain
```

---

**Lembre-se**: Commits bem organizados facilitam a manutenção e colaboração no projeto. Siga sempre o padrão estabelecido para manter a consistência.
