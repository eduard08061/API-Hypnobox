from functions.db_config import SessionLocal
from functions.hypnobox.auth import hy_url, hy_token
from sqlalchemy.orm import Session
from functions.hypnobox.log_handler import log_job_start, log_job_end
from functions.general import str_to_datetime, logging_config, timestamp_now_ddmmaa, str_to_bool, not_empty, filter_ddd
import json, requests
from datetime import datetime, timedelta
from models.hy_messages import *
from models.hy_dimensions import *
from pprint import pprint


# Criar instância de log
logger = logging_config()

# Função principal para atualizar produtos
def update_messages(start_time, end_time, delta):
    print("Função iniciada: update_messages")
    
    try:
        db: Session = SessionLocal()
        date, hour = timestamp_now_ddmmaa()

        # Obtém última Data/hora do lead mais recente no DB
        last_interaction_date = get_latest_interaction_date(db)

        # Se não existir uma data no banco, usar valores padrão
        if not last_interaction_date:
            last_interaction_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            print("NENHUMA DATA ENCONTRADA NO DB -> USANDO DATA DO GATILHO")

        # Define intervalo de datas para chamada na API do Hypnobox
        start_date = last_interaction_date  + timedelta(seconds=1)
        end_date = start_date + timedelta(days=delta)
        #print(f"DATA MAIS ATUAL NO DB: {last_interaction_date}.\nINICIANDO UPDATE...\nDATA INICIO: {start_date}\nDATA FINAL: {end_date}.\nDELTA: {delta} dias.\n")
        print(f"\nINTERVALO: {start_date} - {end_date}. (DELTA: {delta} dias.)\n")

        # Iniciar registro do LOG
        print("Iniciando log de atualização\n") 
        job_id = log_job_start("update messages", datetime.now(), start_date, end_date, "consultamensagens.json")

        # Realizar chamada para API e obter mensagens
        print("Realizando chamada para o Hypnobox\n")
        # Definindo datas de atualização manualmente (comente as linhas abaixo para desativar)
        #start_date=     "2018-03-01 00:00:00"
        #end_date=       "2018-03-06 00:00:00"
        #print(f"\nDatas alteradas para: {start_date} - {end_date}. (DELTA: {delta} dias.)\n")
        all_messages = hy_get_messages_from_api_loop(start_date, end_date)
        total_results = sum(1 for message in all_messages if 'IDCliente' in message)
        print(f"Contando número de resultados obtidos: {total_results}\n")
        #pprint(all_messages)  # Imprime um JSON dos resultuados no console
                
        # Gravar mensagens no banco de dados
        print("Iniciando gravação dos resultados no BD\n")
        add_messages_in_bulk(db, all_messages)

        # Finalizar registro do LOG
        log_job_end(job_id, total_results, None, None, "success")
        print("Atualizando log do UPDATE\n")
        print(f"\nNÚMERO DE MENSAGENS OBTIDAS: {total_results}\n")

    except Exception as e:
        logger.error(f"error in update_messages: {e} {date} ({hour})")
        print(f"error in update_messages: {e} {date} ({hour})")
        #log_job_end(job_id, None, None, e, "error")

    finally:
        db.close()
        logger.info(f"update_messages fineshed {date} ({hour})")
        print(f"update_messages fineshed {date} ({hour})\n\n")

# Cria a lógica de campos DIMENSÂO a serem criados / consultados
def process_message_dimensions(db: Session, message: dict) -> dict:
    #print(f"Função iniciada: process_message_dimensions: {message}")
    dimensions_ids = {}

    def is_valid(value):
        return value not in [None, "", "null", "Null"]

    # CAMPOS QUE TÊM ID EXTERNO (is_external_id=True)

    if not_empty(message.get('IDCanal')):
        db_class= HyDimChannel
        make_id_for= "Channel"
        make_id_from= message.get('NomeCanal')
        additional_fields={'idHyCRM': message.get('IDCanal')}
        dimensions_ids['IdChannel'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)
    
    if not_empty(message.get('IDSubCanal')):
        db_class= HyDimSubChannel
        make_id_for= "SubChannel"
        make_id_from= message.get('NomeSubCanal')
        additional_fields={'idHyCRM': message.get('IDSubCanal')}
        dimensions_ids['IdSubChannel'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('IDMomento')):
        db_class= HyDimMoment
        make_id_for= "Moment"
        make_id_from= message.get('NomeMomento')
        additional_fields={'idHyCRM': message.get('IDMomento')}
        dimensions_ids['IdMoment'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('IDSubMomento')):
        db_class= HyDimSubMoment
        make_id_for= "SubMoment"
        make_id_from= message.get('NomeSubMomento')
        additional_fields={'idHyCRM': message.get('IDSubMomento')}
        dimensions_ids['IdSubMoment'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('IDTemperatura')):
        db_class= HyDimTemperature
        make_id_for= "Temperature"
        make_id_from= message.get('NomeTemperatura')
        additional_fields={'idHyCRM': message.get('IDTemperatura')}
        dimensions_ids['IdTemperature'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('IDCorretorResponsavel')):
        db_class= HyMessageUser
        make_id_for= "Email"
        make_id_from= message.get('EmailCorretorResponsavel')
        additional_fields={'Name':      message.get('NomeCorretorResponsavel') or None,  
                           'idHyCRM':   message.get('IDCorretorResponsavel') or None, 
                           
                           }
        dimensions_ids['IdBrokerResponsible'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields )

    if not_empty(message.get('IDGerenteCorretorResponsavel')):
        db_class= HyMessageUser
        make_id_for= "Email"
        make_id_from= message.get('EmailGerenteCorretorResponsavel')
        additional_fields={'Name':      message.get('NomeGerenteCorretorResponsavel') or None,  
                           'idHyCRM':   message.get('IDGerenteCorretorResponsavel') or None, 
                           
                           }
        dimensions_ids['IdBrokerManager'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields )

    if not_empty(message.get('IDProduto')):
        db_class= HyDimProduct
        make_id_for= "Product"
        make_id_from= message.get('NomeProduto') or "Produto Nulo"
        additional_fields={'idHyCRM': message.get('IDProduto')}
        dimensions_ids['IdProduct'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    # CAMPOS QUE SEM ID EXTERNO (será criado via SCRIPT)

    if not_empty(message.get('Midia')):
        db_class= HyDimMedia
        make_id_for= "Media"
        make_id_from= message.get('Midia')
        dimensions_ids['IdMedia'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('GrupoMidia')):
        db_class= HyDimMediaGroup
        make_id_for= "MediaGroup"
        make_id_from= message.get('GrupoMidia')
        dimensions_ids['IdMediaGroup'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('StatusMenssagem')):
        db_class= HyMessageDimStatus
        make_id_for= "MessageStatus"
        make_id_from= message.get('StatusMenssagem')
        dimensions_ids['IdMessageStatus'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('TipoMensagem')):
        db_class= HyMessageDimTipo
        make_id_for= "MessageType"
        make_id_from= message.get('TipoMensagem')
        dimensions_ids['IdMessageType'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)
    
    return dimensions_ids

# Verifica se ID é interno / Externo e realiza a chamada de "fetch_or_create_id_handle_db" 
def fetch_or_create_id(db: Session, model, field_name: str, field_value, default_values=None, is_external_id=False):
    #print(f"Função iniciada: fetch_or_create_id / field_value={field_value} / default_values={default_values} ")
    # SOBRE
    # Processa um campo específico para verificar se já existe no banco de dados e, se não, cria um novo registro.
    # Obtém o ID da dimensão correspondente, distinguindo entre IDs fornecidos externamente e IDs gerados internamente.

    # VERIFICAÇÃO DO VALOR DO CAMPO
    # Se o valor do campo é fornecido, procedemos com a verificação/criação da dimensão.
    if field_value:
        # Prepara os argumentos para a consulta ao banco de dados
        kwargs = {field_name: field_value}
        
        # Se o ID não é fornecido externamente, usamos default_values para a criação/atualização
        if not is_external_id:
            default_values = default_values or kwargs

        # Verificação adicional para garantir que default_values não contenha None
        if default_values:
            for key, value in default_values.items():
                if value is None:
                    raise ValueError(f"Error: '{key}' value cannot be None")
        
        # Obtém ou cria a dimensão e retorna o ID
        field_id = fetch_or_create_id_handle_db(db, model, default_values=default_values, **kwargs)
        return field_id
    else:
        # Levanta um erro se o valor do campo for None
        raise ValueError(f"Error: '{field_name}' value cannot be None")

# Função para gravação/gerar ID de dimensão e retornar um ID
def fetch_or_create_id_handle_db(db: Session, model, default_values=None, **kwargs):
    #print("Função iniciada: fetch_or_create_id_handle_db")
    # SOBRE
    # Facilita a chamada de "fetch_or_create_id_handle_db" com os parâmetros corretos,
    # distinguindo entre campos com IDs fornecidos externamente e campos que precisam de IDs gerados internamente.

    # INICIANDO O PROCESSO
    # A linha abaixo consulta o banco de dados para verificar se já existe um registro que corresponde
    # aos critérios especificados em kwargs. Se o registro existir, ele é carregado na memória como uma instância do modelo (instance),
    # permitindo que seus atributos sejam modificados.
    instance = db.query(model).filter_by(**kwargs).first()

    # INICIANDO VERIFICAÇÕES PARA ATUALIZAÇÃO CONDICIONAL
    # Se um registro existente é encontrado (instance não é None), verificamos se default_values foi fornecido.
    if instance: # Se o registro existir
        if default_values: # Se valores padrão forem fornecidos
            needs_update = False # Flag para verificar se há necessidade de atualização

            for key, value in default_values.items(): # Loop nos valores padrão fornecidos
                if getattr(instance, key) != value: # Verifica se valores atuais diferem dos valores padrão
                    setattr(instance, key, value) # Atualiza o valor do atributo no objeto instance
                    needs_update = True # Sinaliza que é necessária uma atualização no DB

            if needs_update: # Se houver necessidade de atualização
                db.add(instance) # Adiciona a instância modificada à sessão
                db.commit() # Confirma as alterações no banco de dados

        return instance.id # Retorna o ID do registro existente

    # CRIAÇÃO DE UM NOVO REGISTRO
    # Se nenhum registro correspondente for encontrado, combinamos kwargs e default_values (se fornecidos) para criar um novo registro.
    else:
        params = {**kwargs, **default_values} if default_values else {**kwargs} # Combina kwargs e default_values
        instance = model(**params) # Cria uma nova instância do modelo com os parâmetros combinados
        db.add(instance) # Adiciona a nova instância à sessão
        db.commit() # Confirma a nova instância no banco de dados
        return instance.id # Retorna o ID do novo registro criado

# Função para realizar chamada na API de produtos
def hy_get_messages_from_api(start_time, end_time, page=1):
    #print("Função iniciada: hy_get_messages_from_api")

    # Obter URL base
    base_url = hy_url()
    token = hy_token()
    
    # Endpoint para consulta
    hy_auth_endpoint = "consultamensagens.json"

    # Parâmetros da requisição
    id_cliente = ""
    id_corretor = ""
    email_corretor = ""
    data_cadastro_de = start_time
    data_cadastro_ate = end_time
    pagina = page
    id_mensagem = ""

    # Montando query string
    params = (
        f'?token={token}'
        f'&id_cliente={id_cliente}'
        f'&id_corretor={id_corretor}'
        f'&email_corretor={email_corretor}'
        f'&data_cadastro_de={data_cadastro_de}'
        f'&data_cadastro_ate={data_cadastro_ate}'
        f'&pagina={pagina}'
        f'&id_mensagem={id_mensagem}'
    )

    # URL final para requisição no ENDPOINT
    hy_conn = f'{base_url}/{hy_auth_endpoint}{params}'

    try:
        # Realiza a requisição para o Endpoint
        request = requests.get(hy_conn)

        # Se a resposta não for igual a "200" rtornar um "HTTPError"
        request.raise_for_status()

        # Captura a resposta e converte para um objeto Python/JSON
        response = request.json()

        # Verificação para garantir que Paginacao esteja presente na resposta
        if 'Paginacao' not in response:
            response['Paginacao'] = {
                'PaginaAtual': 1,
                'NumerodePaginas': 1
            }

    except requests.RequestException as e:
        logger.error(f"Erro ao buscar mensagens: {e}")
        print(f"Erro ao buscar mensagens: {e}")
        return None

    return response

# Função para inclusão de dados do DB em massa
def add_messages_in_bulk(db: Session, messages_data):
    #print("Função iniciada: add_messages_in_bulk")

    messages = dict_model_messages(db, messages_data)


    try:
        for message in messages:
            try:
                db.merge(message)
                id_cliente =    message.IdClient
                id_mensagem =   message.id
                client_new =     message.ClientNew
                print(f'Mensagem adicionada com sucesso. IDCliente: {id_cliente} e IdMensagem: {id_mensagem} (cliente novo {client_new})')
            except Exception as e:              
                print(f"ERRO DENTRO DO LOOPING:")
                print(f'Id da mensagem que gerou o erro: {message.IdClient}')
                print(f'Mensagem que gerou o erro: {message}')
                print(f"Exceção: {str(e)}")
                logger.error(f"Exceção: {str(e)}")
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"ERRO FORA DO LOOPING:")
        logger.error(f"add_users_in_bulk: {e}")
        print(f"mensagem da Exception: {messages_data}")
        print(f"mensagem da Exception: {messages_data['IDProduto']}")

# Realiza o looping na resposta da API e chama a função "hy_get_messages"
def hy_get_messages_from_api_loop(start_time, end_time):
    #print("Função iniciada: hy_get_messages_from_api_loop")
    all_messages = []
    page = 1
    while True:
        response = hy_get_messages_from_api(start_time, end_time, page)
        if response is None or 'Mensagens' not in response:
            break
        
        messages = response['Mensagens']
        all_messages.extend(messages)
        
        pagination = response['Paginacao']
        current_page = pagination['PaginaAtual']
        total_pages = pagination['NumerodePaginas']

        # Verificar se current_page e total_pages são válidos
        if current_page is None or total_pages is None:
            break

        if current_page >= total_pages:
            break
        
        page += 1

    return all_messages

# Função para inclusão de dados do DB em massa
def dict_model_messages(db: Session, all_messages):
    #print("Função iniciada: dict_model_messages")
    messages = []

    for message in all_messages:
        dimensions_ids=process_message_dimensions(db, message)
        
        message_obj = HyMessage(
            id=                         message.get('IDMensagemCliente'),
            IdClient=                   message.get('IDCliente') or None,
            ClientName=                 message.get('NomeCliente') or None,
            ClientNew=                  str_to_bool(message.get('ClienteNovo')),
            CNA=                        str_to_bool(message.get('CNA')),
            AssignmentDate=             str_to_datetime(message.get('DataAtribuicao')) or None,
            Message=                    message.get('Mensagem') or None,
            Subject=                    message.get('Assunto') or None,            
            MessageDate=                str_to_datetime(message.get('Datamensagem')) or None,
            IdBrokerResponsible=        dimensions_ids.get('IdBrokerResponsible') or None,
            IdBrokerManager=            dimensions_ids.get('IdBrokerManager') or None,
            IdProduct=                  dimensions_ids.get('IdProduct') or 43,
            IdChannel=                  dimensions_ids.get('IdChannel') or None,
            IdSubChannel=               dimensions_ids.get('IdSubChannel') or None,
            IdMoment=                   dimensions_ids.get('IdMoment') or None,
            IdSubMoment=                dimensions_ids.get('IdSubMoment') or None,
            IdMedia=                    dimensions_ids.get('IdMedia') or None,
            IdMediaGroup=               dimensions_ids.get('IdMediaGroup') or None,
            IdTemperature=              dimensions_ids.get('IdTemperature') or None,
            IdStatusMessage=            dimensions_ids.get('IdMessageStatus') or None,
            IdMessageType=              dimensions_ids.get('IdMessageType') or None,
            IdResponsibleClient=        dimensions_ids.get('IDResponsavelCliente') or None,
            IdResponsibleClientShared=  dimensions_ids.get('IDResponsavelClienteCompartilhado') or None,
        )

        # Mapeando emails
        emails = [
            HyMessageEmail(email=message.get('Email1Cliente'), 
                           IdClientMessage=message.get('IDMensagemCliente'), 
                           email_type=1),

            HyMessageEmail(email=message.get('Email2Cliente'), 
                           IdClientMessage=message.get('IDMensagemCliente'), 
                           email_type=2),

            HyMessageEmail(email=message.get('Email3Cliente'), 
                           IdClientMessage=message.get('IDMensagemCliente'), 
                           email_type=3)
        ]
        message_obj.message_email.extend([e for e in emails if e.email])

        # Mapeando telefones
        phones = [
            HyMessageTel(
                IdClientMessage=    message.get('IDMensagemCliente'),
                phone=              filter_ddd(message.get('TelResidencial')),
                phone_ddd=          filter_ddd(message.get('TelDDDResidencial')), 
                phone_type=         "Residencial"
                ),

            HyMessageTel(
                IdClientMessage=        message.get('IDMensagemCliente'),
                phone=                  message.get('TelCelular'),
                phone_ddd=              message.get('TelDDDCelular'), 
                phone_type=             "Celular"
                ),
        ]
        message_obj.message_tel.extend([p for p in phones if p.phone])

        messages.append(message_obj)

    return messages

# Consultar o banco de dados e descobrir última data de atualização captada
def get_latest_interaction_date(db: Session):
    #print("Função iniciada: get_latest_interaction_date")
    latest_date = db.query(HyMessage).order_by(HyMessage.MessageDate.desc()).first()
    if latest_date:
        return latest_date.MessageDate
    return None


# Verifica se ID é interno / Externo e realiza a chamada de "fetch_or_create_id_handle_db" 
def is_external_id(db: Session, model, field_name: str, field_value, default_values=None, is_external_id=False, additional_fields=None):
    if field_value:
        kwargs = {field_name: field_value}
        
        if not is_external_id:
            default_values = default_values or kwargs

        if default_values:
            for key, value in default_values.items():
                if value is None:
                    model_column = getattr(model, key)
                    if not model_column.nullable:
                        raise ValueError(f"Error: '{key}' value cannot be None")
        if additional_fields:
            default_values.update(additional_fields)
        
        field_id = save_dim_on_db(db, model, default_values=default_values, **kwargs)
        return field_id
    else:
        raise ValueError(f"Error: '{field_name}' value cannot be None")
    
# Função para gravação/gerar ID de dimensão e retornar um ID
def save_dim_on_db(db: Session, model, default_values=None, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()

    if instance:
        if default_values:
            needs_update = False

            for key, value in default_values.items():
                if getattr(instance, key) != value:
                    setattr(instance, key, value)
                    needs_update = True 

            if needs_update:
                db.add(instance)
                db.commit()

        return instance.id

    else:
        params = {**kwargs, **default_values} if default_values else {**kwargs} 
        instance = model(**params)
        db.add(instance)
        db.commit()
        return instance.id