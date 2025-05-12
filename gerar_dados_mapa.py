from datetime import datetime, timedelta
import psycopg2
import json

# Parâmetro da regra de negócio
DATA_CRITICA_DIAS = 30


# Acesso ao Banco de dados da Empresa
def conectar_banco():
    return psycopg2.connect(
        dbname="...",
        user="...",
        password="...",
        host="..."
    )

def buscar_lojas(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, nome, latitude, longitude FROM lojas")
        return cursor.fetchall()

def contar_produtos_criticos(conn, loja_id, data_inicio, data_fim):
    query = """
        SELECT COUNT(*)
        FROM produtos p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.loja_id = %s
        AND p.validade BETWEEN %s AND %s
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (loja_id, data_inicio, data_fim))
        return cursor.fetchone()[0]

def montar_dados_para_mapa(lojas, contagens):
    dados_mapa = []

    for loja in lojas:
        loja_id, nome, lat, long = loja
        qtd_criticos = contagens.get(loja_id, 0)

        ponto = {
            "loja_id": loja_id,
            "loja_nome": nome,
            "latitude": lat,
            "longitude": long,
            "quantidade_produtos_criticos": qtd_criticos,
            "cor": "vermelho" if qtd_criticos > 0 else "azul",
            "raio": calcular_raio(qtd_criticos)
        }
        dados_mapa.append(ponto)

    return dados_mapa

def calcular_raio(qtd):
    if qtd == 0:
        return 3  # pequeno para lojas sem risco
    elif qtd < 10:
        return 6
    elif qtd < 50:
        return 10
    else:
        return 15  # mais risco, maior o ponto

def main():
    hoje = datetime.now().date()
    data_limite = hoje + timedelta(days=DATA_CRITICA_DIAS)

    try:
        conn = conectar_banco()
        lojas = buscar_lojas(conn)

        contagens = {}
        for loja in lojas:
            loja_id = loja[0]
            qtd = contar_produtos_criticos(conn, loja_id, hoje, data_limite)
            contagens[loja_id] = qtd

        dados_para_mapa = montar_dados_para_mapa(lojas, contagens)

        with open("dados_mapa_lojas.json", "w") as f:
            json.dump(dados_para_mapa, f, indent=2)

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
