# Dicionário de dados

Arquivo contendo os metadados do dataset final gerado na ETL.

## Tabela: fake_store_analytics

### Colunas

1. **user_id**
    - **Descrição**: Identificador único (ID) do(a) usuário(a) que adicionou produtos no carrinho na loja Fake Store. 
    - **Tipo de dado**: Integer
    - **Exemplo**: `1`

2. **most_relevant_category**
    - **Descrição**: Nome da categoria do produto em que o(a) usuário(a) possui maior volume de produtos no carrinho.
    - **Tipo de dado**: String
    - **Exemplo**:`men's clothing`

3. **last_date_added_to_cart**
    - **Descrição**: Data mais recente em que o(a) usuário(a) adicionou produtos no carrinho da loja Fake Store.
    - **Tipo de dado**: Timestamp
    - **Formato**: `yyyy-MM-dd HH:mm:ss`
    - **Exemplo**:`2020-02-29 21:00:00`

4. **processind_date**
    - **Descrição**: Data em que ocorreu o processamento dos dados no processo de ETL.
    - **Tipo de dado**: Timestamp
    - **Formato**: `yyyy-MM-dd HH:mm:ss`
    - **Exemplo**: `2024-11-08 14:01:25`