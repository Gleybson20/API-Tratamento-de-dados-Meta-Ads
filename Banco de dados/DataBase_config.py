import psycopg2

DB_CONFIG = {
    "dbname": "Database",
    "user": "postgres",
    "password": "senha",
    "host": "localhost",
    "port": "5432"
}

def criar_tabelas():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_meta (
            id_conta BIGINT PRIMARY KEY,   -- ID da conta
            nome_unidade TEXT NOT NULL     -- Nome da unidade (ex: 'Cabo', 'Cacoal', etc.)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dad0s_json (
            id SERIAL PRIMARY KEY,           -- Identificador único para cada entrada
            id_conta BIGINT NOT NULL,        -- ID da conta
            id_conjunto BIGINT,              -- ID do conjunto de anúncios
            nome_conjunto TEXT,              -- Nome do conjunto de anúncios
            id_anuncio BIGINT NOT NULL,      -- ID do anúncio
            nome_anuncio TEXT,               -- Nome do anúncio
            data DATE,                -- Data de início do anúncio
            investimento NUMERIC(10,2),      -- Investimento total
            cliques INT,                     -- Total de cliques
            leads INT,                       -- Total de leads
            cadastro_meta INT,               -- Total de cadastros meta
            conversas_iniciadas INT         -- Total de conversas iniciadas
        );
        """)
        conn.commit()
        print("✅ Tabela criadas com sucesso!")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Erro ao criar as tabela: {e}")

if __name__ == "__main__":
    criar_tabelas()


conn = psycopg2.connect(
    dbname="databases",
    user="postgres",
    password="senha",
    host="localhost",
    port="5432"
)
conn.autocommit = True
cursor = conn.cursor()
DATABASE_NAME = "Database"

try:
    cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
    print(f"✅ Banco de dados '{DATABASE_NAME}' criado com sucesso!")
except psycopg2.errors.DuplicateDatabase:
    print(f"⚠️ O banco de dados '{DATABASE_NAME}' já existe.")
cursor.close()
conn.close()
