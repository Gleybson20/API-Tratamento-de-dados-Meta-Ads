import requests
import json
import time
from datetime import datetime, timedelta

def fetch_insights_yesterday(account_id, access_token):
    """
    Coleta os dados de anúncios do dia anterior para uma conta específica,
    lida com a paginação e salva os resultados em um único arquivo JSON.
    """

    # 1. Identificar a data de ontem no formato YYYY-MM-DD
    ontem = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # 2. Montar a URL de requisição para o dia de ontem
    url_base = (
        f"https://graph.facebook.com/v22.0/act_{account_id}/insights?time_increment=1"
        f"&time_range={{\"since\":\"{ontem}\",\"until\":\"{ontem}\"}}"
        f"&level=ad&fields=impressions,reach,spend,adset_id,adset_name,ad_id,ad_name,actions&action_breakdowns=action_type"
        f"&access_token={access_token}"
    )

    # Lista que irá conter todos os registros de todas as páginas
    todos_os_dados = []

    # URL inicial para começar a requisição
    url_atual = url_base

    while url_atual:
        print(f"Fazendo requisição para: {url_atual}")
        resposta = requests.get(url_atual)
        
        if resposta.status_code != 200:
            print(f"Erro na requisição. Código: {resposta.status_code}")
            print(f"Resposta: {resposta.text}")
            break

        # Carrega os dados JSON
        dados = resposta.json()

        # Verifica se a resposta possui o campo "data"
        if "data" in dados:
            # "data" normalmente é uma lista de objetos de insights
            todos_os_dados.extend(dados["data"])
        else:
            print("Nenhum campo 'data' encontrado nessa resposta. Encerrando.")
            break

        # 3. Verificar se existe próximo link em "paging.next"
        #    (em vez de "pagination", a Graph API usa "paging")
        if "paging" in dados and "next" in dados["paging"]:
            url_atual = dados["paging"]["next"]
            
            # Espera 5 ms antes de fazer a próxima requisição
            time.sleep(0.005)
        else:
            # Não há próxima página
            url_atual = None

    # Por fim, salva tudo em um único arquivo JSON
    nome_arquivo = f"{account_id}arquivo.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(todos_os_dados, f, indent=4, ensure_ascii=False)

    print(f"Coleta finalizada! Dados salvos em '{nome_arquivo}'.")


if __name__ == "__main__":
    # Exemplo de uso:
    # Se tiver apenas uma conta, basta chamar a função para aquela conta.
    # Caso tenha várias, repita para cada ID.

    # Defina seu token de acesso (Access Token do Meta)
    ACCESS_TOKEN = "Token de acesso"

    # Caso você tenha apenas UMA conta:
    # fetch_insights_yesterday("1234567890", ACCESS_TOKEN)

    # Caso tenha VÁRIAS contas, itere sobre elas:
    lista_de_contas = [
        "1234567890",
        "2345678901",
        "345678..."
    ]

    for account_id in lista_de_contas:
        print(f"\n--- Coletando dados da conta: {account_id} ---")
        fetch_insights_yesterday(account_id, ACCESS_TOKEN)


