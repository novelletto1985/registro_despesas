from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from parcelas import gerar_parcelas
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    dados = request.form
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO compras (descricao, valor_total, num_parcelas, data_compra, forma_pagamento, categoria, subcategoria)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        dados['descricao'],
        float(dados['valor_total']),
        int(dados['num_parcelas']),
        dados['data_compra'],
        dados['forma_pagamento'],
        dados['categoria'],
        dados['subcategoria']
    ))
    compra_id = cursor.lastrowid
    conn.commit()
    conn.close()

    gerar_parcelas(compra_id)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect("banco.db")
    df = pd.read_sql_query("SELECT * FROM compras", conn)
    conn.close()

    total = df["valor_total"].sum()

    # Gráfico de pizza: soma de valores por categoria
    categorias = df["categoria"].fillna("Outros").unique().tolist()
    valores_por_categoria = df.groupby("categoria")["valor_total"].sum().tolist()

    # Gráfico de linha: soma por data de compra
    df["data_compra"] = pd.to_datetime(df["data_compra"])
    df_linha = df.groupby(df["data_compra"].dt.date)["valor_total"].sum().sort_index()
    datas = df_linha.index.astype(str).tolist()
    valores_por_data = df_linha.tolist()

    return render_template(
        "dashboard.html",
        despesas=df.to_dict(orient="records"),
        total=round(total, 2),
        categorias=categorias,
        valores_por_categoria=valores_por_categoria,
        datas=datas,
        valores_por_data=valores_por_data
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
