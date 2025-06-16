from functions.db_config import SessionLocal
from functions.hypnobox.auth import hy_url, hy_token
from sqlalchemy.orm import Session
from functions.hypnobox.log_handler import log_job_start, log_job_end
from functions.general import str_to_datetime, logging_config, timestamp_now_ddmmaa, str_to_bool
import json, requests
from models.hy_users import *
from datetime import datetime


# Criar instância de log
logger = logging_config()

# Função principal para atualizar produtos
def update(get_by_email=None):
    print(f"Função iniciada: update")
    print(f"get_by_email: {get_by_email}")
    
    try:
        db: Session = SessionLocal()
        date, hour = timestamp_now_ddmmaa()

        # Iniciar registro do LOG
        print("Iniciando log de atualização\n") 
        job_id = log_job_start("get users info", datetime.now(), datetime.now(), datetime.now(), "getusersinfo")

        # Realizar chamada para API e obter mensagens
        print("Realizando chamada para o Hypnobox\n")
        if get_by_email:
            api_results = api_call(get_by_email)
        else:
            api_results = api_call(get_by_email=None)

        #print(f"Resultado da chamada na API: \n{all_messages}")
        results_count = sum(1 for results in api_results if 'id_usuario' in results)
        print(f"Contando número de resultados obtidos: {results_count}\n")
                
        # Gravar mensagens no banco de dados
        print("Iniciando gravação dos resultados no BD\n")

        if get_by_email:
            get_by_email_id = db_add_bulk(db, api_results, get_by_email)
            print(f'teste do if get_by_email é TRUE {get_by_email}')
        else:
            get_by_email_id = db_add_bulk(db, api_results, get_by_email=None)
            print(f'teste do if get_by_email é FALSE {get_by_email}')

        # Finalizar registro do LOG
        log_job_end(job_id, results_count, None, None, "success")
        print("Atualizando log do UPDATE\n")
        print(f"\nNÚMERO DE MENSAGENS OBTIDAS: {results_count}\n")

    except Exception as e:
        logger.error(f"error in update_messages: {e} {date} ({hour})")
        print(f"error in update_messages: {e} {date} ({hour})")
        log_job_end(job_id, None, None, None, "error", e)

    finally:
        db.close()
        logger.info(f"update_messages fineshed {date} ({hour})")
        print(f"update_messages fineshed {date} ({hour})\n\n")

    if get_by_email:
        return get_by_email_id

# Função para realizar chamada na API de produtos
def api_call(get_by_email=None):
    print("Função iniciada: api_call")
    print(f"get_by_email: {get_by_email}")

    # Obter URL base
    base_url = hy_url()
    token = hy_token()
    
    # Endpoint para consulta
    hy_auth_endpoint = "getusersinfo"

    # Montando query string
    params = (
        f'?token={token}'
        f'&fields[]=email'
        f'&fields[]=creci'
        f'&fields[]=cpf'
        f'&fields[]=data_cadastro'
        f'&fields[]=id_usuario'
        f'&fields[]=id_perfil'
        f'&fields[]=id_usuario_gestor'
        f'&fields[]=id_usuario_gestor1'
        f'&fields[]=id_usuario_gestor2'
        f'&fields[]=id_usuario_gestor3'
        f'&fields[]=id_usuario_gestor4'
        f'&fields[]=id_usuario_gestor5'
        f'&fields[]=id_usuario_gestor6'
        f'&fields[]=nome'
        f'&fields[]=nome_guerra'
        f'&fields[]=telefone'
        f'&fields[]=creci_tipo'
        f'&fields[]=creci_validade'
        f'&fields[]=cpf'
        f'&fields[]=foto'
        f'&fields[]=data_cadastro'
        f'&fields[]=data_atualizacao'
        f'&fields[]=ativo'
        f'&fields[]=id_usuario_legado'
        f'&fields[]=descricao_status'
        f'&fields[]=dt_nascimento'
        f'&fields[]=dt_admissao'
        f'&fields[]=sexo'
        f'&fields[]=media_avaliacao'
        f'&fields[]=data_ultima_avaliacao_desempenho'
        f'&conditions[data_cadastro][]='
        f'&conditions[data_atualizacao][]='
        
        )
    
    # Adicionando o e-mail às condições se fornecido
    if get_by_email:
        params += f'&conditions[email][]={get_by_email}' 

    # URL final para requisição no ENDPOINT
    hy_conn = f'{base_url}/{hy_auth_endpoint}{params}'
    #print(f'valor de hy_conn: {hy_conn}')

    try:
        # Realiza a requisição para o Endpoint
        request = requests.get(hy_conn)

        # Se a resposta não for igual a "200" rtornar um "HTTPError"
        request.raise_for_status()

        # Captura a resposta e converte para um objeto Python/JSON
        response = request.json()
        #print(f'valor de response: {response}')

    except requests.RequestException as e:
        logger.error(f"Erro ao buscar mensagens: {e}")
        #print(f"Erro ao buscar mensagens: {e}")
        return None

    return response

# Função para inclusão de dados do DB em massa
def db_add_bulk(db: Session, model, get_by_email):
    print("Função iniciada: db_add_bulk")
    print(f'get_by_email: {get_by_email}')
    #print(f'model: {model}')
    

    model_instance = model_dict(db, model)

    try:
        for items in model_instance:
            try:
                db.merge(items)
                id = items.id
                Name = items.Name
                Email = items.Email
                print(f'Usuário adicionado com sucesso. id: {id} / Name: {Name} / Name: {Email}')
                
            except Exception as e:              
                print(f"ERRO DENTRO DO LOOPING:")
                print(f'Id da mensagem que gerou o erro: {items.id}')
                #print(f'Mensagem que gerou o erro: {items}')
                print(f"Exceção: {str(e)}")
                logger.error(f"Exceção: {str(e)}")
        db.commit()
        if get_by_email:
            return id

    except Exception as e:
        db.rollback()
        print(f"ERRO FORA DO LOOPING:")
        logger.error(f"add_users_in_bulk: {e}")
        #print(f"mensagem da Exception: {api_call_results}")
        print(f"mensagem da Exception: {model_instance['id_usuario']}")



# Função para inclusão de dados do DB em massa
def model_dict(db: Session, results):
    #print("Função iniciada: dict_model_messages")
    
    model = []

    if results:  # Verificação para garantir que há resultados
        for result in results:

            dict_obj = HyUser(
                id=                     result.get('id_usuario'),
                Email=                  result.get('email') or None,
                Creci=                  result.get('creci') or None,
                CreciType=              result.get('creci_tipo') or None,
                CreciValidity=          result.get('creci_validade') or None,
                CPF=                    result.get('cpf') or None,
                
                IdProfile=              result.get('id_perfil') or None,
                IdManager=              result.get('id_usuario_gestor') or None,
                IdManager1=             result.get('id_usuario_gestor1') or None,
                IdManager2=             result.get('id_usuario_gestor2') or None,
                IdManager3=             result.get('id_usuario_gestor3') or None,
                IdManager4=             result.get('id_usuario_gestor4') or None,
                IdManager5=             result.get('id_usuario_gestor5') or None,
                IdManager6=             result.get('id_usuario_gestor6') or None,
                
                Name=                   result.get('nome') or None,
                NickName=               result.get('nome_guerra') or None,
                Phone=                  result.get('telefone') or None,
                Photo=                  result.get('foto') or None,

                Active=                 str_to_bool(result.get('ativo')) or None,
                LegacyUserId=           result.get('id_usuario_legado') or None,
                DescriptionStatus=      result.get('descricao_status') or None,
                
                DateRegister=           str_to_datetime(result.get('data_cadastro')) or None,
                DateUpdate=             str_to_datetime(result.get('data_atualizacao')) or None,
                DateBirth=              str_to_datetime(result.get('dt_nascimento')) or None,
                DateAdmission=          str_to_datetime(result.get('dt_admissao')) or None,
                DateLastEvaluation=     str_to_datetime(result.get('media_avaliacao')) or None,

                Gender=                 result.get('sexo') or None,
                AverageRating=          result.get('data_ultima_avaliacao_desempenho') or None,
                
            )

            model.append(dict_obj)

    return model

# Utilize essa função para buscar e cadastrar um usuário, a partir do email. 
def get_user_id_by_email(email):
    print(f'iniciando get_user_id_by_email: {email}')
    user_data = update(get_by_email=email)
    if user_data:
        return user_data
    return None


# Teste de chamada da função que busca e cadastra um usuário específico na API de usuários.
""" email = "danielle.poliana@exto.com.br"
user_id = get_user_id_by_email(email)
if user_id:
    print(f'ID do usuário: {user_id}')
else:
    print(f'Usuário não encontrado: {user_id}') """
