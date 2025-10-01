# Tutorial Completo: Executando o RegiFlex no Windows com Docker Compose

Este tutorial fornecerá um guia passo a passo detalhado para configurar e executar o sistema RegiFlex em seu ambiente Windows. Utilizaremos o Docker Compose, a ferramenta mais robusta e recomendada para gerenciar todas as dependências e serviços do projeto (banco de dados, backend e frontend) de forma consistente e isolada.

## 1. O que é o RegiFlex?

O RegiFlex é um sistema completo de gestão para clínicas de psicologia. Ele foi desenvolvido para simplificar o registro, acompanhamento e análise de informações de pacientes e sessões, oferecendo funcionalidades como:

*   **Gestão de Pacientes:** Cadastro completo de informações demográficas, contato e histórico.
*   **Gestão de Sessões:** Agendamento, registro de sessões e evolução do paciente.
*   **Autenticação e Autorização:** Sistema de login seguro com diferentes perfis de usuário (Admin, Psicólogo, Recepcionista).
*   **QR Code:** Geração e leitura de QR Codes para acesso rápido a informações de pacientes e sessões.
*   **Inteligência Artificial Leve:** Geração de alertas inteligentes e análise de padrões (ex: cancelamentos).
*   **Relatórios e Dashboard:** Visão geral e detalhada das atividades da clínica.

### Tecnologias Principais:

*   **Backend:** Python 3.11, Flask, PostgreSQL, SQLAlchemy
*   **Frontend:** React.js, pnpm, Vite, Tailwind CSS
*   **Infraestrutura:** Docker, Docker Compose

## 2. Pré-requisitos Essenciais

Para executar o RegiFlex, você precisará instalar os seguintes softwares em seu sistema Windows. É crucial que eles estejam instalados e configurados corretamente antes de prosseguir.

### 2.1. Docker Desktop para Windows

O Docker Desktop é a ferramenta fundamental que permite executar contêineres Docker no Windows, incluindo o Docker Engine, Docker CLI e Docker Compose. Ele é responsável por criar um ambiente isolado para o RegiFlex.

*   **Download:** Baixe o instalador mais recente em [Docker Desktop Official Website](https://www.docker.com/products/docker-desktop/).
*   **Instalação:** Siga as instruções do instalador. Durante a instalação, o Docker Desktop pode solicitar que você habilite o **WSL 2 (Windows Subsystem for Linux 2)**. É **altamente recomendado** habilitar o WSL 2 para melhor desempenho e compatibilidade. Se você não tiver o WSL 2 instalado, o Docker Desktop geralmente oferece a opção de instalá-lo automaticamente. Caso contrário, você pode seguir o guia oficial da Microsoft: [Instalar WSL](https://learn.microsoft.com/pt-br/windows/wsl/install).
*   **Verificação:** Após a instalação, inicie o Docker Desktop. Ele pode levar alguns minutos para iniciar completamente. Verifique se o ícone do Docker na bandeja do sistema está verde (indicando que está em execução).

### 2.2. Git for Windows

O Git for Windows inclui o Git Bash, um terminal que oferece uma experiência de linha de comando semelhante ao Linux no Windows, o que é muito útil para executar comandos Git e scripts shell. Ele também instala o comando `git` que será usado para clonar o repositório.

*   **Download:** Baixe o instalador em [Git for Windows Official Website](https://git-scm.com/download/win).
*   **Instalação:** Siga as instruções padrão do instalador. As opções padrão geralmente são suficientes.

## 3. Obtendo o Código do RegiFlex

Você pode obter o código-fonte do RegiFlex clonando o repositório atualizado do GitHub:

1.  **Abra o Git Bash:** Inicie o Git Bash (procure por "Git Bash" no menu Iniciar do Windows).
2.  **Clone o Repositório:** No Git Bash, navegue até o diretório onde deseja armazenar o projeto (ex: `cd /c/Projetos`) e execute o comando para clonar o repositório:
    ```bash
    git clone https://github.com/artur-source/RefiFlex-teste.git
    ```
3.  **Navegue para a Pasta do Projeto:** Após clonar, entre no diretório do projeto:
    ```bash
    cd RefiFlex-teste
    ```

## 4. Configuração e Inicialização com Docker Compose

Esta é a etapa principal onde o Docker Compose irá construir e iniciar todos os serviços do RegiFlex.

### 4.1. Verifique o Arquivo `.env`

O projeto utiliza um arquivo `.env` para armazenar variáveis de ambiente, como as credenciais do banco de dados. Este arquivo já foi atualizado no repositório com a senha que você forneceu. É crucial que este arquivo esteja presente na raiz do projeto (`RefiFlex-teste`) e salvo com a codificação correta.

1.  **Localize o arquivo:** Verifique se existe um arquivo chamado `.env` na pasta raiz do projeto `RefiFlex-teste`.
2.  **Conteúdo do `.env`:** O arquivo `.env` deve conter o seguinte:
    ```
    POSTGRES_USER=regiflex_user
    POSTGRES_PASSWORD=regiflex@123
    POSTGRES_DB=regiflex_db
    ```
3.  **Codificação:** **Muito importante:** Certifique-se de que o arquivo `.env` está salvo com a codificação **UTF-8 (sem BOM)**. Muitos editores de texto permitem escolher a codificação ao salvar. Se o arquivo for salvo com outra codificação (como UTF-16), o Docker Compose pode ter problemas para lê-lo, resultando em erros como `unexpected character`. No VS Code, por exemplo, você pode clicar em "UTF-8" na barra de status inferior e selecionar "Salvar com Codificação" para escolher "UTF-8 sem BOM".

### 4.2. Iniciando os Serviços com Docker Compose

Com o Docker Desktop em execução e o arquivo `.env` configurado corretamente, você pode iniciar todos os serviços do RegiFlex com um único comando.

1.  **Abra o Terminal:** No Git Bash (ou PowerShell/CMD), certifique-se de estar no diretório raiz do projeto `RefiFlex-teste`.
2.  **Execute o Comando:** Digite o seguinte comando e pressione Enter:
    ```bash
    docker compose up --build -d
    ```

    *   `docker compose up`: Inicia os serviços definidos no arquivo `docker-compose.yml`.
    *   `--build`: Garante que as imagens Docker para o backend e frontend sejam construídas (ou reconstruídas, se houver alterações no código ou nos Dockerfiles). Isso é importante na primeira execução e sempre que houver atualizações no projeto.
    *   `-d`: Executa os contêineres em modo "detached" (segundo plano). Isso libera seu terminal para outros comandos enquanto os serviços continuam rodando.

### O que Acontece Após Executar o Comando?

1.  **Construção de Imagens:** O Docker irá construir as imagens para o backend (Python/Flask) e frontend (React.js) com base nos `Dockerfile`s e nas dependências especificadas.
2.  **Inicialização do Banco de Dados:** O contêiner do PostgreSQL será iniciado. O `docker-compose.yml` está configurado para inicializar o banco de dados com o esquema e dados iniciais (se presentes em `database/schema.sql` e `database/seed.sql`).
3.  **Inicialização do Backend:** O contêiner do backend será iniciado e aguardará o banco de dados estar saudável antes de se conectar.
4.  **Inicialização do Frontend:** O contêiner do frontend será iniciado, configurando o servidor de desenvolvimento do React.

### 4.3. Aguardando a Inicialização dos Serviços

O processo de construção e inicialização pode levar alguns minutos, especialmente na primeira vez. Você pode monitorar o status dos seus contêineres com o seguinte comando:

```bash
docker compose ps
```

Espere até que todos os serviços (`db`, `backend`, `frontend`) estejam com o status `running` e, idealmente, `healthy` (indicado pelo `healthcheck` do banco de dados).

### 4.4. Acessando a Aplicação

Após todos os serviços estarem em execução, abra seu navegador e acesse:

*   **Frontend (Interface do Usuário):** `http://localhost:3000`
*   **Backend (API):** `http://localhost:5000/api` (usado internamente pelo frontend)

### 4.5. Credenciais de Teste

Para testar a aplicação, você pode usar as seguintes credenciais:

*   **Admin:** `admin` / `regiflex@123`
*   **Psicólogo:** `psicologo1` / `regiflex@123`
*   **Recepcionista:** `recepcionista1` / `regiflex@123`

## 5. Parando e Removendo os Serviços

Quando você terminar de usar o RegiFlex, é importante parar e remover os contêineres para liberar recursos do sistema. No diretório raiz do projeto (`RefiFlex-teste`), execute:

```bash
docker compose down -v
```

### Explicação do Comando:

*   `docker compose down`: Para e remove os contêineres, redes e volumes padrão criados pelo `docker compose up`.
*   `-v`: Remove também os volumes de dados (`db_data` neste caso). Isso é útil se você quiser iniciar com um banco de dados completamente limpo na próxima vez.

## 6. Solução de Problemas Comuns

Se você encontrar problemas, verifique os seguintes pontos:

*   **"docker compose: command not found"**: Certifique-se de que o Docker Desktop está instalado, em execução e que você reiniciou seu terminal após a instalação. A sintaxe `docker compose` (sem hífen) é a mais recente; se não funcionar, tente `docker-compose` (com hífen).
*   **Portas em uso**: Se você receber erros como `Error: listen EADDRINUSE: address already in use :::3000` ou `:::5000`, significa que outra aplicação em seu sistema já está usando essas portas. Você precisará fechar a aplicação que está usando a porta ou alterar as portas no arquivo `docker-compose.yml`.
*   **Problemas com o `.env`**: Como mencionado, o arquivo `.env` deve estar na raiz do projeto e salvo com codificação **UTF-8 (sem BOM)**. Verifique isso com um editor de texto.
*   **Contêineres não iniciam ou param inesperadamente**: Verifique os logs dos contêineres para obter mais informações. Você pode ver os logs de um serviço específico (ex: `backend`) com:
    ```bash
docker compose logs backend
    ```
*   **Problemas de conexão com o banco de dados**: Certifique-se de que o serviço `db` está `healthy` (saudável) ao executar `docker compose ps`. Se não estiver, verifique os logs do contêiner `db`.

Se, após seguir este tutorial, você ainda enfrentar dificuldades, por favor, compartilhe os logs de erro completos do seu terminal (especialmente os logs do `docker compose up --build -d` e `docker compose logs <nome_do_servico>`) para que eu possa ajudar a diagnosticar o problema com mais precisão.

---

**Autor:** Manus AI
**Data:** 01 de Outubro de 2025
