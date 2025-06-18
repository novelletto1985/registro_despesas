import sqlite3
from datetime import datetime, timedelta

def gerar_parcelas(compra_id):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()

    cursor.execute('SELECT valor_total, num_parcelas, data_compra FROM compras WHERE id = ?', (compra_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        print(f"Nenhuma compra encontrada com id={compra_id}")
        return

    valor_total, num_parcelas, data_compra = resultado
    data_base = datetime.strptime(data_compra, '%Y-%m-%d')
    valor_parcela = round(valor_total / num_parcelas, 2)

    for i in range(num_parcelas):
        data_vencimento = (data_base.replace(day=15) + timedelta(days=30 * i)).strftime('%Y-%m-%d')

        cursor.execute('''
            INSERT INTO parcelas (compra_id, numero_parcela, valor_parcela, data_parcela)
            VALUES (?, ?, ?, ?)
        ''', (
            compra_id,
            i + 1,
            valor_parcela,
            data_vencimento
        ))

    conn.commit()
    conn.close()

