from datetime import datetime
import time, secrets, pytz, os, re, json, logging
from dotenv import load_dotenv
from urllib.parse import unquote
from dotenv import load_dotenv

# Formata o tempo para hh:mm:ss.ms (com 3 dígitos para ms)
def format_time(seconds):
    time_str = datetime.fromtimestamp(seconds).strftime('%H:%M:%S.%f')
    return time_str[:-3]  # Trunca para obter apenas três dígitos dos milissegundos

# Gera um token seguro com o comprimento especificado
def generate_token(length=32):
    return secrets.token_hex(length)

# Retorna um timestamp já convertido para horário local
def timestamp_now():
    tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(tz)
    return now

# Retorna o valor da chave válida no sistema (obtido pelo ".env")
def system_key():
    load_dotenv()
    valid_key = os.getenv('API_KEY')
    return valid_key

def exec_time(start_time):
    end_time = time.time()
    total_time = format_time(end_time - start_time)
    return total_time

# Decodifica, substitui '+' por espaço e remove caracteres especiais não desejados
def clean_value(value):
    value = unquote(value).replace('+', ' ')
    clean_special_chars = re.sub(r'[^\w\s]', '', value)
    clean_double_spaces = re.sub(r'\s+', ' ', clean_special_chars).strip()
    return clean_double_spaces

# Converter uma data "string" para "date"
def str_to_datetime(date_str):
    if date_str:
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                pass
    return None

# Salvar resposta de API em arquivo JSON
def save_client_data_to_json(client_data):
    # Obter o timestamp atual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Nome do arquivo com base no timestamp
    file_name = f"client_data_{timestamp}.json"
    # Caminho onde o arquivo será salvo (pode ser ajustado conforme necessário)
    file_path = f"misc/{file_name}"
    
    # Salvar os dados no arquivo JSON
    with open(file_path, 'w') as json_file:
        json.dump(client_data, json_file, indent=4)
        
    return file_path

# Configuração do logger para gravar em um arquivo
def logging_config():
    
    load_dotenv()
    
    if os.getenv('RUNNING_IN_DOCKER') == 'true':
        log_path = "/var/log/api-exto.log"
    else:
        log_path = "api-exto.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    return logger    

# Timestamp regionalizado e com data/hora separados
def timestamp_now_ddmmaa():
    tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(tz)
    date_str = now.strftime('%d/%m/%Y')
    time_str = now.strftime('%H:%M')
    return date_str, time_str


def str_to_bool(value):
    true_values = ['1', "1", 'true', 'yes', 1]
    false_values = ['0', "0", 'false', 'no', 0]

    if str(value).lower() in true_values:
        return True
    elif str(value).lower() in false_values:
        return False
    return None  # Retorna None se o valor não corresponder a nenhuma das listas

def clean_value(value):
    if value in [None, "", "null", "Null", "0", "0.00", "0,00"]:
        return None
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return value


def not_empty(value):
    return value not in [None, "", "null", "Null"]


def filter_ddd(ddd):
    return None if ddd == '00' else ddd