from functions.db_config import SessionLocal
from functions.hypnobox.auth import hy_url, hy_token
from sqlalchemy.orm import Session
from functions.hypnobox.log_handler import log_job_start, log_job_end
from functions.general import str_to_datetime, logging_config, timestamp_now_ddmmaa, str_to_bool, clean_value, not_empty, filter_ddd
import json, requests
from datetime import datetime, timedelta

from models.hy_dimensions import *
from models.hy_client_v2 import *
import logging
from pprint import pprint


# Criar instância de log
logger = logging_config()

# Função principal para atualizar produtos
def update(start_time, end_time, delta):
    print(f"Função iniciada: update\nstart_time={start_time}\nend_time={end_time}")
    
    try:
        db: Session = SessionLocal()
        date, hour = timestamp_now_ddmmaa()

        # Obtém última Data/hora do lead mais recente no DB
        last_interaction_date = find_last_record(db)

        # Se não existir uma data no banco, usar valores padrão
        if not last_interaction_date:
            last_interaction_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            print("NENHUMA DATA ENCONTRADA NO DB -> USANDO DATA DO GATILHO")

        # Define intervalo de datas para chamada na API do Hypnobox
        start_date = last_interaction_date  + timedelta(seconds=1)
        end_date = start_date + timedelta(days=delta)
        print(f"\nINTERVALO: {start_date} - {end_date}. (DELTA: {delta} dias.)\n")

        # Iniciar registro do LOG
        print("Iniciando log de atualização\n") 
        job_id = log_job_start("update messages", datetime.now(), start_date, end_date, "consultamensagens.json")

        # Realizar chamada para API e obter mensagens
        print("Realizando chamada para o Hypnobox\n")
        all_messages = api_pagination(start_date, end_date)
        #print(f"Resultado da chamada na API: \n{all_messages}")
        total_results = sum(1 for message in all_messages if 'CodCliente' in message)
        print(f"Contando número de resultados obtidos: {total_results}\n")
        
        #for message in all_messages:
        #    print(f"CLIENTE OBTIDO: \n\n {message}\n")
                
        # Gravar mensagens no banco de dados
        print("Iniciando gravação dos resultados no BD\n")
        db_add_bulk(db, all_messages)

        # Finalizar registro do LOG
        log_job_end(job_id, total_results, None, None, "success")
        print("Atualizando log do UPDATE\n")
        print(f"\nNÚMERO DE MENSAGENS OBTIDAS: {total_results}\n")

    except Exception as e:
        logger.error(f"error in update_messages: {e} {date} ({hour})")
        print(f"error in update_messages: {e} {date} ({hour})")
        log_job_end(job_id, None, None, None, "error", e)

    finally:
        db.close()
        logger.info(f"update_messages fineshed {date} ({hour})")
        print(f"update_messages fineshed {date} ({hour})\n\n")

# Cria a lógica de campos DIMENSÂO a serem criados / consultados
def create_dimensions(db: Session, message: dict) -> dict:
    #print(f"Função iniciada: process_message_dimensions: {message}")
    dimensions_ids = {}

    # CAMPOS QUE TÊM ID EXTERNO (is_external_id=True)
    # Nenhum cadastrado

    # CAMPOS SEM ID EXTERNO (será criado via SCRIPT)

    if not_empty(message.get('Objetivo')):
        db_class= HyDimObjective
        make_id_for= "Objective"
        make_id_from= message.get('Objetivo')
        dimensions_ids['IdObjective'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('Momento')):
        db_class= HyDimMoment
        make_id_for= "Moment"
        make_id_from= message.get('Momento')
        additional_fields = {'idHyCRM': message.get('IDMomento')} if message.get('IDMomento') else None
        dimensions_ids['IdMoment'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('SubMomento')):
        db_class= HyDimSubMoment
        make_id_for= "SubMoment"
        make_id_from= message.get('SubMomento')
        additional_fields = {'idHyCRM': message.get('IDSubMomento')} if message.get('IDSubMomento') else None
        dimensions_ids['IdSubMoment'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('Temperatura')):
        db_class= HyDimTemperature
        make_id_for= "Temperature"
        make_id_from= message.get('Temperatura')
        additional_fields = {'idHyCRM': message.get('IDTemperatura')} if message.get('IDTemperatura') else None
        dimensions_ids['IdTemperature'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('Status')):
        db_class= HyDimStatus
        make_id_for= "Status"
        make_id_from= message.get('Status')
        additional_fields = {'idHyCRM': message.get('IDTemperatura')} if message.get('IDTemperatura') else None
        dimensions_ids['IdStatus'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('InactiveState')):
        db_class= HyDimInactiveState
        make_id_for= "InactiveState"
        make_id_from= message.get('InactiveState')
        additional_fields={'idHyCRM': message.get('InactiveStateId')}
        dimensions_ids['IdInactiveState'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('ProdutoOrigem')):
        db_class= HyDimProduct
        make_id_for= "Product"
        make_id_from= message.get('ProdutoOrigem')
        dimensions_ids['IdProductOrigin'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('ProdutoInteresse')):
        db_class= HyDimProduct
        make_id_for= "Product"
        make_id_from= message.get('ProdutoInteresse')
        additional_fields={'idHyCRM': message.get('CodProdutoInteresse')}
        dimensions_ids['IdProductInterest'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('CanalOrigem')):
        db_class= HyDimChannel
        make_id_for= "Channel"
        make_id_from= message.get('CanalOrigem')
        dimensions_ids['IdSourceChannel'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('MidiaOrigem')):
        db_class= HyDimMedia
        make_id_for= "Media"
        make_id_from= message.get('MidiaOrigem')
        dimensions_ids['IdSourceMedia'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('MidiaAtual')):
        db_class= HyDimMedia
        make_id_for= "Media"
        make_id_from= message.get('MidiaAtual')
        dimensions_ids['IdCurrentMedia'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('GrupoMidiaOrigem')):
        db_class= HyDimMediaGroup
        make_id_for= "MediaGroup"
        make_id_from= message.get('GrupoMidiaOrigem')
        dimensions_ids['IdMediaOriginGroup'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('GrupoMidiaAtual')):
        db_class= HyDimMediaGroup
        make_id_for= "MediaGroup"
        make_id_from= message.get('GrupoMidiaAtual')
        dimensions_ids['IdCurrentMediaGroup'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('EmailCorretor')):
        db_class= HyDimUser
        make_id_for= "Email"
        make_id_from= message.get('EmailCorretor')
        additional_fields={'Name':      message.get('NomeCorretor') or None, 
                           'CPF':       message.get('CpfCorretor') or None,
                           'Regional':  message.get('RegionalCorretor') or None, 
                           }
        dimensions_ids['IdBroker'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields )


    if not_empty(message.get('EmailCorretorOrigem')):
        db_class= HyDimUser
        make_id_for= "Email"
        make_id_from= message.get('EmailCorretorOrigem')
        additional_fields={'Name': message.get('NomeCorretorOrigem')}
        dimensions_ids['IdBrokerOrigin'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields )

    if not_empty(message.get('EmailGerente')):
        db_class= HyDimUser
        make_id_for= "Email"
        make_id_from= message.get('EmailGerente')
        additional_fields={'Name':      message.get('NomeGerente'), 
                           'CPF':       message.get('CpfGerente') }
        dimensions_ids['IdManager'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields )

    if not_empty(message.get('EmailGerenteGeral')):
        db_class= HyDimUser
        make_id_for= "Email"
        make_id_from= message.get('EmailGerenteGeral')
        additional_fields={'Name': message.get('NomeGerenteGeral')}
        dimensions_ids['IdGeneralManager'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('EmailGerenteOrigem')):
        db_class= HyDimUser
        make_id_for= "Email"
        make_id_from= message.get('EmailGerenteOrigem')
        additional_fields={'Name': message.get('NomeGerenteOrigem')}
        dimensions_ids['EmailManagerOrigin'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('EmailCorretorCompartilhado')):
        db_class= HyDimUser
        make_id_for= "Email"
        make_id_from= message.get('EmailCorretorCompartilhado')
        additional_fields={'Name': message.get('NomeCorretorCompartilhado')}
        dimensions_ids['IdBrokerShared'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields)

    if not_empty(message.get('Sexo')):
        db_class= HyDimGender
        make_id_for= "Gender"
        make_id_from= message.get('Sexo')
        dimensions_ids['IdCoordinator'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('estadoCivil')):
        db_class= HyDimMaritalStatus
        make_id_for= "MaritalStatus"
        make_id_from= message.get('estadoCivil')
        dimensions_ids['IdMaritalStatus'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('PrimeiroImovel')):
        db_class= HyDimFirstProperty
        make_id_for= "FirstProperty"
        make_id_from= message.get('PrimeiroImovel')
        dimensions_ids['IdFirstProperty'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    # Dimensões de Região

    if not_empty(message.get('Estado')):
        db_class= HyDimState
        make_id_for= "State"
        make_id_from= message.get('Estado')
        dimensions_ids['IdState'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('Cidade')):
        db_class= HyDimCity
        make_id_for= "City"
        make_id_from= message.get('Cidade')
        dimensions_ids['IdCity'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    if not_empty(message.get('Bairro')):
        db_class= HyDimNeighborhood
        make_id_for= "Neighborhood"
        make_id_from= message.get('Bairro')
        dimensions_ids['IdNeighborhood'] = is_external_id(db, db_class, make_id_for, make_id_from, additional_fields=None)

    #logging.info(f"Dimensões criadas na função create_dimensions: {dimensions_ids}")

    return dimensions_ids

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

# Função para realizar chamada na API de produtos
def api_call(start_time, end_time, page=1):

    # Obter URL base
    base_url = hy_url()
    token = hy_token()
    
    # Endpoint para consulta
    hy_auth_endpoint = "clients-v2.json"

    # Parâmetros da requisição
    data_inicio = ""
    data_final = ""
    data_atualizacao_inicio = start_time
    data_atualizacao_final = end_time
    pagina = page
    id_produto_atual = ""
    id_produto_origem = ""
    id_corretor = ""
    email_cliente = ""
    id_submomento = ""
    paginacao_registros_por_pagina = 300
    id_cliente = ""


    # Montando query string
    params = (
        f'?token={token}'
        f'&data_inicio={data_inicio}'
        f'&data_final={data_final}'
        f'&data_atualizacao_inicio={data_atualizacao_inicio}'
        f'&data_atualizacao_final={data_atualizacao_final}'
        f'&id_produto_atual={id_produto_atual}'
        f'&id_produto_origem={id_produto_origem}'
        f'&id_corretor={id_corretor}'
        f'&email_cliente={email_cliente}'
        f'&id_submomento={id_submomento}'
        f'&paginacao_registros_por_pagina={paginacao_registros_por_pagina}'
        f'&id_cliente={id_cliente}'
        f'&pagina={pagina}'
    )

    # URL final para requisição no ENDPOINT
    hy_conn = f'{base_url}/{hy_auth_endpoint}{params}'
    print(f'Calling to API: {hy_conn}')

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
def db_add_bulk(db: Session, api_call_results):
    #pprint(api_call_results)
    model_instance = model_dict(db, api_call_results)

    try:
        for items in model_instance:
            try:
                db.merge(items)
                db.commit()

                id = items.id
                name = items.Name
                register_date = items.DateRegister
                print(f'Adicionado -> IDCliente: {id} | Nome: {name} | Data Cadastro: {register_date} ')
            
            except Exception as e:
                db.rollback()
                print(f"ERRO DENTRO DO LOOPING:")
                print(f'Id da mensagem que gerou o erro: {items.id}')
                print(f"Exceção: {str(e)}")
                logger.error(f"Exceção: {str(e)}")
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"ERRO FORA DO LOOPING:")
        logger.error(f"add_users_in_bulk: {e}")

# Realiza o looping na resposta da API e chama a função "hy_get_messages"
def api_pagination(start_time, end_time):
    #print("Função iniciada: hy_get_messages_from_api_loop")
    all_messages = []
    page = 1
    while True:
        response = api_call(start_time, end_time, page)
        if response is None or 'Clientes' not in response:
            break
        
        messages = response['Clientes']
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
def model_dict(db: Session, results):
    #print("Função iniciada: dict_model_messages")
    
    model = []

    if results:
        for result in results:
            dimensions_ids=create_dimensions(db, result)
            #logging.info(f"Dimensions IDs que chegaram na model_dict: {dimensions_ids}")
            
            # Cadastro dos dados de ENDEREÇO
            if any([
                dimensions_ids.get('IdState'),
                dimensions_ids.get('IdCity'),
                dimensions_ids.get('IdNeighborhood'),
                result.get('Cep'),
                result.get('Logradouro')
            ]):
                
                address_obj = HyDimClientAdress(
                    id=                 result.get('CodCliente'),
                    idState=            dimensions_ids.get('IdState') or None,
                    idCity=             dimensions_ids.get('IdCity') or None,
                    idNeighborhood=     dimensions_ids.get('IdNeighborhood') or None,
                    ZipCode=            result.get('Cep') or None,
                    PublicPlace=        result.get('Logradouro') or None,
                    Number=             result.get('Numero') or None,
                    Complement=         result.get('Complemento') or None,
                    Type=               "R"
                )
            else:
                address_obj = None

            # Cadastro dos dados de RANGE (DE / ATÉ)

            price_from =        clean_value(result.get('ValorDe'))
            price_to =          clean_value(result.get('ValorAte'))
            area_from =         clean_value(result.get('MetragemDe'))
            area_to =           clean_value(result.get('MetragemAte'))
            bedrooms_from =     clean_value(result.get('DormDe'))
            bedrooms_to =       clean_value(result.get('DormAte'))

            if any([price_from, price_to, area_from, area_to, bedrooms_from, bedrooms_to]):
                ranges_obj = HyDimRanges(
                    id=result.get('CodCliente'),
                    PriceFrom=price_from,
                    PriceTo=price_to,
                    AreaFrom=area_from,
                    AreaTo=area_to,
                    BedroomsFrom=bedrooms_from,
                    BedroomsTo=bedrooms_to,
                )
            else:
                ranges_obj = None

            # Cadastro dos dados dos EMAILS

            emails = []
            if result.get('Email'):
                emails.append(HyDimClientEmail(id=result.get('CodCliente'), Email=result.get('Email'), EmailType="Email1"))
            if result.get('Email2'):
                emails.append(HyDimClientEmail(id=result.get('CodCliente'), Email=result.get('Email2'), EmailType="Email2"))
            if result.get('Email3'):
                emails.append(HyDimClientEmail(id=result.get('CodCliente'), Email=result.get('Email3'), EmailType="Email3"))

            # Cadastro dos dados dos TELEFONES
            phones = []


            if result.get('TelResidencial'):
                phones.append(HyDimClientPhone(id=result.get('CodCliente'), Phone=result.get('TelResidencial'), PhoneDDD=filter_ddd(result.get('DddResidencial')), PhoneType="TelResidencial"))
            if result.get('TelCelular'):
                phones.append(HyDimClientPhone(id=result.get('CodCliente'), Phone=result.get('TelCelular'), PhoneDDD=filter_ddd(result.get('DddCelular')), PhoneType="TelCelular"))
            if result.get('TelComercial'):
                phones.append(HyDimClientPhone(id=result.get('CodCliente'), Phone=result.get('TelComercial'), PhoneDDD=filter_ddd(result.get('DddComercial')), PhoneType="TelComercial"))
            if result.get('Celular2'):
                phones.append(HyDimClientPhone(id=result.get('CodCliente'), Phone=result.get('Celular2'), PhoneDDD=filter_ddd(result.get('Celular2DDD')), PhoneType="Celular2"))
            if result.get('TelOutro'):
                phones.append(HyDimClientPhone(id=result.get('CodCliente'), Phone=result.get('TelOutro'), PhoneDDD=filter_ddd(result.get('DddOutro')), PhoneType="TelOutro"))


            # Cadastro da TABELA DESCRIÇÃO

            description_obj = None
            if result.get('Descricao'):
                description_obj = HyClientDescription(
                    id=result.get('CodCliente'),
                    Description=result.get('Descricao')
                )


            # Cadastro dos dados DEMOGRÁFICOS

            id =                    clean_value(result.get('CodCliente'))
            CpfValue =              clean_value(result.get('Cpf'))
            idGender =              clean_value(result.get('IdGender'))
            idMaritalStatus =       clean_value(result.get('IdMaritalStatus'))
            ProductType =           clean_value(result.get('TipoProduto'))
            Phase =                 clean_value(result.get('Fase'))
            Finality =              clean_value(result.get('Finalidade'))
            #Objective =            clean_value(result.get('Objetivo'))
            TimeSearch =            clean_value(result.get('TempoProcura'))
            TimeDecision =          clean_value(result.get('TempoDecisao'))
            LiveInvest =            clean_value(result.get('MorarInvestir'))
            PaymentPlan =           clean_value(result.get('PlanoPagamento'))
            #FirstProperty =         clean_value(result.get('PrimeiroImovel'))
            MoreImportant =         clean_value(result.get('MaisImportante'))
            FGTSValue =             clean_value(result.get('ValorFgts'))
            EntryValue =            clean_value(result.get('ValorEntrada'))
            MonthlyIncome =         clean_value(result.get('RendaMensal'))
            BirthDate =             clean_value(result.get('DataNascimento'))
            SpouseName =            clean_value(result.get('NomeConjuge'))
            QtyDependents =         clean_value(result.get('QtdDependentes'))

            if any([CpfValue, idGender, idMaritalStatus, ProductType, Phase, Finality, 
                    TimeSearch, TimeDecision, LiveInvest, PaymentPlan, MoreImportant, 
                    FGTSValue, EntryValue, MonthlyIncome, BirthDate, SpouseName, QtyDependents]):
                
                try:
                    demographic_obj = HyDimClientDemographic(
                        id = id,              
                        CpfValue = CpfValue,             
                        idGender = idGender,         
                        idMaritalStatus = idMaritalStatus,

                        ProductType = ProductType,     
                        Phase = Phase,
                        Finality = Finality,         
                        #Objective = Objective,            
                        TimeSearch = TimeSearch,      
                        TimeDecision = TimeDecision,    
                        LiveInvest =  LiveInvest,     
                        PaymentPlan = PaymentPlan,     
                        #FirstProperty =  FirstProperty,  
                        MoreImportant =  MoreImportant,  
                        FGTSValue =  FGTSValue,      
                        EntryValue =  EntryValue,     
                        MonthlyIncome = MonthlyIncome,   
                        BirthDate = BirthDate,        
                        SpouseName = SpouseName,      
                        QtyDependents = QtyDependents   
                    )
                except Exception as e:
                    print(f"Error creating demographic_obj: {e}")
                    demographic_obj = None
            else:
                demographic_obj = None

            # Cadastro dos dados dos EMAILS


            # Cadastro da TABELA PRINCIPAL DE CLIENTES (FATO)

            dict_obj = HyClientV2(

                id=                     result.get('CodCliente'),
                Name=                   result.get('Nome') or None,
                InternalCode=           result.get('CodInterno') or None,
                DateRegister=           result.get('DataCadastro') or None,
                DateLastInteraction=    result.get('DataUltimaInteracao') or None,
                Denylist=               str_to_bool(result.get('Denylist')),
                Consent=                str_to_bool(result.get('Consentimento')),
                
                IdObjective=            dimensions_ids.get('IdObjective') or None,
                IdMoment=               dimensions_ids.get('IdMoment') or None,
                IdSubMoment=            dimensions_ids.get('IdSubMoment') or None,
                IdTemperature=          dimensions_ids.get('IdTemperature') or None,
                IdInactiveState=        dimensions_ids.get('IdInactiveState') or None,
                IdProductOrigin=        dimensions_ids.get('IdProductOrigin') or None,
                IdProductInterest=      dimensions_ids.get('IdProductInterest') or None,
                IdFirstProperty=        dimensions_ids.get('IdFirstProperty') or None,
                IdStatus=               dimensions_ids.get('IdStatus') or None,

                IdSourceChannel=        dimensions_ids.get('IdSourceChannel') or None,
                IdSourceMedia=          dimensions_ids.get('IdSourceMedia') or None,
                IdCurrentMedia=         dimensions_ids.get('IdCurrentMedia') or None,
                IdMediaOriginGroup=     dimensions_ids.get('IdMediaOriginGroup') or None,
                IdCurrentMediaGroup=    dimensions_ids.get('IdCurrentMediaGroup') or None,

                IdBroker=               dimensions_ids.get('IdBroker') or None,
                IdBrokerOrigin=         dimensions_ids.get('IdBrokerOrigin') or None,
                IdManager=              dimensions_ids.get('IdManager') or None,
                IdGeneralManager=       dimensions_ids.get('IdGeneralManager') or None,
                EmailManagerOrigin=     dimensions_ids.get('EmailManagerOrigin') or None,
                IdBrokerShared=         dimensions_ids.get('IdBrokerShared') or None,
                IdCoordinator=          dimensions_ids.get('IdCoordinator') or None,

                address=address_obj  # Adicionando o objeto de endereço
            )

            # APPEND das informações extras para o objeto principal
            try:
                dict_obj.emails.extend(emails)
                dict_obj.phones.extend(phones)
                model.append(dict_obj)

                if description_obj:
                    dict_obj.description = description_obj

                if ranges_obj:
                    dict_obj.ranges = ranges_obj

                if demographic_obj:
                    dict_obj.demographic = demographic_obj
            except Exception as e:
                print(f"Error appending objects to dict_obj: {e}")
    
    else:
        print("Nenhum resultado encontrado.")

    return model

# Consultar o banco de dados e descobrir última data de atualização captada
def find_last_record(db: Session):
    #print("Função iniciada: get_latest_interaction_date")
    latest_date = db.query(HyClientV2).order_by(HyClientV2.DateLastInteraction.desc()).first()
    print(f'latest_date: {latest_date}')
    if latest_date:
        return latest_date.DateLastInteraction
    return None