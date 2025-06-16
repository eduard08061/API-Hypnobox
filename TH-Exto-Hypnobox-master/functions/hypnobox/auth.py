from dotenv import load_dotenv
import json, requests, os

load_dotenv()

# Montar para chamada do Hypnobox
def hy_url():
    hy_url = os.getenv('HYPNOBOX_URL')
    hy_uri = os.getenv('HYPNOBOX_URI')
    hy_portal = os.getenv('HYPNOBOX_PORTAL')
    hy_base_url = f'https://{hy_portal}.{hy_url}/{hy_uri}'

    return hy_base_url

def hy_token():
    
    # Obter URL base
    base_url = hy_url()
    
    # Endpoint de autenticação
    hy_auth_endpoint = "auth"

    # Dados de autenticação
    login = os.getenv('HYPNOBOX_USER')
    password = os.getenv('HYPNOBOX_PASS')

    # Parâmetros da requisição
    returnType = "json"

    # Montando query string
    params = f'?login={login}&password={password}&returnType={returnType}'
    
    # URL final para requisição no ENDPOINT
    hy_conn = f'{base_url}/{hy_auth_endpoint}/{params}'

    # Realiza a requisição para o Endpoint    
    request = requests.get(hy_conn)

    # Captura valores da resposta e converte para JSON
    response = json.loads(request.text)

    # Armazena apenas o Token
    token = response['token']
    return token