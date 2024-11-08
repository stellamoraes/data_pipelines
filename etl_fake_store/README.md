# ETL: Pipeline Fake Store API

Este repositório contém o código e a documentação para o projeto de ETL (Extract, Transform, Load) dos dados da API Fake Store, que possui dados fictícios de acessos de usuários a uma loja, bem como registros de produtos que foram adicionados ao carrinho. A documentação da API pode ser acessada no link: https://fakestoreapi.com/doc

Os dados foram transformados com o objetivo de responder as seguintes perguntas:
    - Qual a categoria de produto o(a) usuário(a) mais adicionou produtos ao carrinho?
    - Qual a data mais recente em que o(a) usuário(a) adicionou produtos ao carrinho?

## Modelo de arquitetura para automação

Modelo pensado para extração dos dados de uma API e armazenamento desses dados brutos em camada da Cloud Store (o equivalete ao Amazon S3 na AWS); o armazenamento dos dados brutos faciliam a criação de novas tabelas analíticas e reprocessamentos. Na etapa de transformação, são realizados relacionamentos entre datasets, agregações e limpezas visando atender as necessidades do negócio. Após a transformação é feito o carregamento do dado analítico no data warehouse/data lake para consumo dos(as) usuários(as).


### Componentes
1- **Google Storage**: Armazenamento de dados brutos e dados tratados em difetentes camadas.
2- **Apache Airflow**: Automação do fluxo do pipeline utilizando o `schedule_interval` para agendamento diário.
3- **Looker**: Criação de dashoboars e métricas utilizando LookerML. 
