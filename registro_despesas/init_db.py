import sqlite3

conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

# Cria tabela de compras
cursor.execute('''
CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT,
    valor_total REAL,
    num_parcelas INTEGER,
    data_compra TEXT,
    forma_pagamento TEXT,
    categoria TEXT,
    subcategoria TEXT
)
''')

# Cria tabela de parcelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS parcelas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    compra_id INTEGER,
    numero_parcela INTEGER,
    valor_parcela REAL,
    data_parcela TEXT,
    FOREIGN KEY (compra_id) REFERENCES compras(id)
)
''')

conn.commit()
conn.close()
print("Banco de dados criado com sucesso!")
