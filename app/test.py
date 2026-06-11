from app.services.database import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute('SELECT * FROM clientes ORDER BY id DESC LIMIT 10;')
resultados = cur.fetchall()

for cliente in resultados:
    print(cliente)

cur.close()
conn.close()