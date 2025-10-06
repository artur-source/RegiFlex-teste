# Documentação do Módulo de IA Aprimorado - RegiFlex

## Visão Geral

Este documento detalha a arquitetura e o funcionamento do novo módulo de Inteligência Artificial (IA) do RegiFlex. O módulo foi reestruturado para incorporar aprendizado leve, análise adaptativa e insights preditivos, mantendo a compatibilidade com o backend existente e sem adicionar dependências pesadas.

O foco é fornecer valor prático e interpretável para clínicas de psicologia, com alertas mais inteligentes e contextualizados, baseados em padrões e tendências reais dos dados.

## Arquitetura

O módulo de IA está contido em dois arquivos principais:

- `backend/app/services/ia_service.py`: Contém toda a lógica de negócio, incluindo análises, processamento de dados, treinamento de modelos e geração de insights.
- `backend/app/api/ia.py`: Expõe os serviços de IA através de uma API RESTful segura, com endpoints para consumo pelo frontend.

### Cache e Modelos

Para garantir a eficiência e a responsividade, o sistema utiliza um diretório de cache (`backend/cache/`) para armazenar:

- **Resultados de Análises:** Análises computacionalmente intensas, como a detecção de padrões de cancelamento, são cacheadas para evitar reprocessamento.
- **Modelos de Machine Learning:** Modelos treinados (ex: Regressão Logística) são salvos para uso em previsões futuras.
- **Estatísticas Incrementais:** Dados estatísticos são atualizados de forma incremental para evitar o reprocessamento de todo o histórico.

## Melhorias Técnicas Implementadas

### 1. Análise de Frequência Inteligente

- **Detecção de Variação de Frequência:** Compara a frequência de sessões de um paciente em semanas consecutivas para identificar tendências de "queda" ou "melhora" na assiduidade.
- **Índice de Engajamento:** Um novo índice (0-100) é calculado para cada paciente, combinando a taxa de comparecimento e a frequência semanal normalizada. A fórmula é:
  ```
  índice = (taxa_comparecimento * 0.6) + (frequência_semanal_normalizada * 0.4)
  ```
- **Alertas Contextualizados:** Alertas são gerados para baixa frequência, baixo comparecimento, tendências de queda e baixo índice de engajamento.

### 2. Padrões de Cancelamento com Agrupamento (K-Means)

- **Clusterização com K-Means:** O algoritmo K-Means é aplicado para identificar clusters de cancelamentos, agrupando-os por características como dia da semana e horário.
- **Resumo Interpretável:** Os clusters são traduzidos em descrições claras e acionáveis, como "Cluster 1: cancelamentos noturnos" ou "Cluster 2: segundas e quartas".
- **Cache de Resultados:** Os resultados da clusterização são armazenados em cache para otimizar o desempenho.

### 3. Previsão de Cancelamentos (Regressão Logística)

- **Modelo Preditivo Leve:** Um modelo de Regressão Logística (Scikit-learn) foi implementado para prever a probabilidade de cancelamento de uma sessão.
- **Features Utilizadas:** O modelo utiliza as seguintes features:
  - `dia_semana`
  - `hora`
  - `paciente_id`
  - `psicologo_id`
  - `cancelamentos_passados`
- **Treinamento Rápido:** O treinamento é realizado em pequenos lotes de dados recentes, garantindo agilidade e adaptação contínua.
- **Alerta Preditivo:** Um alerta é gerado se a probabilidade de cancelamento de uma sessão futura for superior a 60%.

### 4. Geração de Alertas Aprimorada

- **Consolidação de Alertas:** Os alertas de análises estatísticas e previsões são consolidados em um único endpoint.
- **Nível de Confiança:** Cada alerta agora possui um nível de confiança (baixa, média, alta), ajudando os usuários a priorizar ações.
- **Mensagens Claras:** As mensagens de alerta são geradas automaticamente e de forma clara para o dashboard, como: `"Alta chance de cancelamento amanhã às 18h (72%)"`. 

### 5. Camada de Aprendizado Incremental

- **Cache de Estatísticas:** Estatísticas chave, como a média de comparecimento de um paciente, são salvas em cache.
- **Atualização Automática:** Essas estatísticas são atualizadas incrementalmente à medida que novas sessões são registradas, eliminando a necessidade de reprocessar todo o histórico a cada requisição.

### 6. Logs e Segurança

- **Logs Detalhados:** Todas as ações e execuções dos modelos de IA são registradas em logs para auditoria e depuração.
- **Autenticação JWT:** Todos os endpoints da API de IA são protegidos e requerem um token de autenticação (JWT) válido, garantindo que apenas usuários autenticados possam acessá-los.

## Endpoints da API

A seguir, a descrição dos principais endpoints disponíveis em `backend/app/api/ia.py`.

| Método | Endpoint                               | Descrição                                                                                             |
| :----- | :------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| GET    | `/ia/alertas`                          | Retorna uma lista consolidada de alertas para o dashboard.                                            |
| GET    | `/ia/analise-paciente/<int:paciente_id>` | Obtém a análise de frequência inteligente para um paciente específico.                                  |
| GET    | `/ia/padroes-cancelamento`             | Analisa e retorna padrões e clusters de cancelamentos.                                                 |
| POST   | `/ia/prever-cancelamento`              | Prevê a probabilidade de cancelamento de uma sessão com base nos dados fornecidos no corpo da requisição. |
| GET    | `/ia/prever-cancelamento/<int:sessao_id>` | Endpoint simplificado para prever o cancelamento de uma sessão específica.                             |
| POST   | `/ia/treinar-modelo`                   | Força o retreinamento do modelo de previsão de cancelamentos (apenas para administradores).             |
| GET    | `/ia/estatisticas`                     | Retorna estatísticas gerais sobre o estado do sistema de IA (modelos, cache, etc.).                   |
| POST   | `/ia/atualizar-estatisticas`           | Atualiza as estatísticas incrementais (para um paciente ou gerais).                                   |
| POST   | `/ia/limpar-cache`                     | Limpa o cache expirado do sistema de IA (apenas para administradores).                                |

## Como Usar

1. **Consumo pelo Frontend:** O frontend pode consumir os endpoints da API para exibir alertas, análises e previsões no dashboard do usuário.
2. **Manutenção:** O sistema foi projetado para baixa manutenção. O cache é limpo automaticamente e os modelos são retreinados conforme necessário.
3. **Evolução Futura:** A base de código atual é sólida e modular, permitindo a fácil implementação de futuras funcionalidades, como previsão de evolução terapêutica e análise de sentimento.

