from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from parcelas import gerar_parcelas

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
    import pandas as pd
    import plotly.express as px

    conn = sqlite3.connect('banco.db')
    df = pd.read_sql_query('SELECT * FROM parcelas', conn)
    conn.close()

    fig = px.histogram(df, x='data_parcela', y='valor_parcela', histfunc='sum', title='Gastos por mês')
    fig_html = fig.to_html(full_html=False)

    return render_template('dashboard.html', grafico=fig_html)

if __name__ == '__main__':
    app.run(debug=True)
