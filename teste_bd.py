import psycopg

URL_BD = "postgresql://postgres:estacao@localhost:5433/estacao"

with psycopg.connect(URL_BD) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM leituras;")
        resultado = cur.fetchone()
        print("Linhas na tabela:", resultado[0])