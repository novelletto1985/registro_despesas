from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
import plotly.express as px
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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    ano = request.args.get('ano', default='Todos')
    mes = request.args.get('mes', default='Todos')

    conn = sqlite3.connect('banco.db')
    df = pd.read_sql_query('SELECT * FROM parcelas INNER JOIN compras ON parcelas.compra_id = compras.id', conn)
    conn.close()

    df['data_parcela'] = pd.to_datetime(df['data_parcela'])
    df['mes'] = df['data_parcela'].dt.month
    df['ano'] = df['data_parcela'].dt.year

    anos_disponiveis = sorted(df['ano'].unique())

    if ano != 'Todos':
        df = df[df['ano'] == int(ano)]
    if mes != 'Todos':
        df = df[df['mes'] == int(mes)]

    if df.empty:
        return render_template('dashboard.html', grafico1=None, grafico2=None, grafico3=None, grafico4=None, anos=anos_disponiveis, ano=ano, mes=mes)

    fig1 = px.histogram(df, x='data_parcela', y='valor_parcela', histfunc='sum', title='Gastos por Mês')
    fig2 = px.pie(df, names='forma_pagamento', values='valor_parcela', title='Gastos por Forma de Pagamento')
    fig3 = px.pie(df, names='categoria', values='valor_parcela', title='Gastos por Categoria')
    fig4 = px.pie(df, names='subcategoria', values='valor_parcela', title='Gastos por Subcategoria')

    return render_template('dashboard.html',
                           grafico1=fig1.to_html(full_html=False),
                           grafico2=fig2.to_html(full_html=False),
                           grafico3=fig3.to_html(full_html=False),
                           grafico4=fig4.to_html(full_html=False),
                           anos=anos_disponiveis,
                           ano=ano,
                           mes=mes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
from flask import Flask, render_template, request, redirect
import sqlite3
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
    app.run(host='0.0.0.0', port=10000)
