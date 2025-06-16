from functions.db_config import SessionLocal
from functions.hypnobox.auth import hy_url, hy_token

from sqlalchemy.orm import Session

from functions.general import str_to_datetime, save_client_data_to_json, logging_config
from functions.results_handler import hy_count_values
from functions.hypnobox.log_handler import log_job_start, log_job_end

from datetime import datetime, timedelta
import json, requests
from pprint import pprint

# Modelos db
from models.hy_client import *

# Criar instância de log
logger = logging_config()

# Função principal para orquestrar a atualização da base de dados
def update_clients(data_inicio, data_atualizacao_inicio, data_atualizacao_final, delta):
    db: Session = SessionLocal()
    
    try:
        # Obtém última Data/hora do lead mais recente no DB
        last_interaction_date = get_latest_interaction_date(db)

        # Se não existir uma data no banco, usar valores padrão
        if not last_interaction_date:
            last_interaction_date = datetime.strptime(data_atualizacao_inicio, '%Y-%m-%d %H:%M:%S')

        # Define intervalo de datas para chamada na API do Hypnobox
        start_date = last_interaction_date  + timedelta(seconds=1)
        end_date = start_date + timedelta(days=delta)

        # Iniciar registro do LOG 
        endpoint = f'/clients?data_inicio={data_inicio}&data_atualizacao_inicio={start_date}&data_atualizacao_final={end_date}'
        job_id = log_job_start("update clients", data_inicio, start_date, end_date, endpoint)

        # realiza Chamada na API Hypnobox
        
        client_data = hy_get_clients(data_inicio, start_date, end_date)
        # Acessar a lista de clientes dentro do dicionário e contar os elementos
        if 'Clientes' in client_data and isinstance(client_data['Clientes'], list):
            total_results = len(client_data['Clientes'])
        else:
            total_results = 0
        print(f"total_results={total_results}")
        #pprint(client_data['Clientes'])

        # Gravar resposta da API em arquivo JSON
        #json_file_path = save_client_data_to_json(client_data)

        #hy_debug_clients(client_results)

        # Realiza gravação no banco de dados do TH
        add_users_in_bulk(db, client_data['Clientes'])

        # Compara JSON original com dados gravados no banco
        #verify_data_in_db(db, json_file_path)

        # Gerar contagens e atualizar o log
        unique_emails, unique_phones = hy_count_values(client_data)
        log_job_end(job_id, len(client_data['Clientes']), unique_emails, unique_phones, "success")
        logger.info(f"Update Realizado com sucesso")
        print(f"Update Realizado com sucesso")
        print(f"Intervalo: data_inicio: {data_inicio} / start_date: {start_date} / end_date: {end_date}")

    except Exception as e:
        logger.error(f"update_clients: {e}")

    finally:
        db.close()

# Função que realiza a consulta no Hypnobox e retorna a lista de usuários
def hy_get_clients(data_inicio, data_atualizacao_inicio, data_atualizacao_final):
    
    # Obter URL base
    base_url = hy_url()
    token = hy_token()
    
    # Endpoint de autenticação
    hy_auth_endpoint = "clients"

    # Parâmetros da requisição
    data_inicio = data_inicio
    data_final = ""
    data_atualizacao_inicio = data_atualizacao_inicio
    data_atualizacao_final = data_atualizacao_final
    id_produto_atual = ""
    id_produto_origem = ""
    id_corretor = ""
    returnType = "json"

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
        f'&returnType={returnType}'
    )

    # URL final para requisição no ENDPOINT
    hy_conn = f'{base_url}/{hy_auth_endpoint}/{params}'

    # Realiza a requisição para o Endpoint    
    request = requests.get(hy_conn)

    # Captura valores da resposta e converte para JSON
    response = json.loads(request.text)

    return response

# Consultar o banco de dados e descobrir última data de atualização captada
def get_latest_interaction_date(db: Session):
    latest_date = db.query(HyClient).order_by(HyClient.DataUltimaInteracao.desc()).first()
    if latest_date:
        return latest_date.DataUltimaInteracao
    return None

# Função para inclusão de dados do DB em massa
def add_users_in_bulk(db: Session, client_data):

    clients = map_json_to_models(client_data)

    try:
        for client in clients:
            db.merge(client)
            client_id = client.CodCliente
            client_name = client.Nome
            print(f'Mensagem adicionada com sucesso. CodCliente: {client_id} e client_name: {client_name}')
        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"add_users_in_bulk: {e}")

# Função para mapear os dados do JSON para os modelos SQLAlchemy
def map_json_to_models(client_data):
    clients = []

    for client in client_data:
        cod_cliente = client.get('CodCliente')
        if not cod_cliente:
            continue  # Skip if CodCliente is missing or None

        client_obj = HyClient(
            CodCliente=int(client['CodCliente']),
            Nome=client['Nome'],
            Cpf=client.get('Cpf'),
            DataUltimaInteracao=str_to_datetime(client.get('DataUltimaInteracao')),
            DataCadastro=str_to_datetime(client.get('DataCadastro')),
            Momento=client.get('Momento'),
            Submomento=client.get('Submomento'),
            Temperatura=client.get('Temperatura'),
            Status=client.get('Status'),
            InactiveState=client.get('InactiveState'),
            InactiveStateId=int(client.get('InactiveStateId')) if client.get('InactiveStateId') else None,
            Objetivo=client.get('Objetivo')
        )

        # Mapeando emails
        emails = [
            HyClientEmail(email=client.get('Email'), client_id=client_obj.CodCliente),
            HyClientEmail(email=client.get('Email2'), client_id=client_obj.CodCliente),
            HyClientEmail(email=client.get('Email3'), client_id=client_obj.CodCliente)
        ]
        client_obj.emails.extend([e for e in emails if e.email])

        # Mapeando telefones
        phones = [
            HyClientPhone(telefone=client.get('TelResidencial'), tipo='Residencial', ddd=client.get('DddResidencial'), client_id=client_obj.CodCliente),
            HyClientPhone(telefone=client.get('TelCelular'), tipo='Celular', ddd=client.get('DddCelular'), client_id=client_obj.CodCliente),
            HyClientPhone(telefone=client.get('TelComercial'), tipo='Comercial', ddd=client.get('DddComercial'), client_id=client_obj.CodCliente),
            HyClientPhone(telefone=client.get('TelOutro'), tipo='Outro', ddd=client.get('DddOutro'), client_id=client_obj.CodCliente)
        ]
        client_obj.phones.extend([t for t in phones if t.telefone])

        # Mapeando dados demográficos
        if any(client.get(field) for field in ['estadocivil', 'NomeConjuge', 'QtdDependentes', 'ValorFgts', 'ValorEntrada', 'ValorRendaMensal', 'DataNascimento']):
            demographic = HyClientDemographic(
                estadocivil=client.get('estadocivil'),
                NomeConjuge=client.get('NomeConjuge'),
                QtdDependentes=client.get('QtdDependentes'),
                ValorFgts=client.get('ValorFgts'),
                ValorEntrada=client.get('ValorEntrada'),
                ValorRendaMensal=client.get('ValorRendaMensal'),
                DataNascimento=str_to_datetime(client.get('DataNascimento')),
                client_id=client_obj.CodCliente
            )
            client_obj.demographics = demographic

        # Mapeando gênero
        if client.get('Sexo'):
            gender = HyClientGender(
                Sexo=client.get('Sexo'),
                client_id=client_obj.CodCliente
            )
            client_obj.genders.append(gender)

        # Mapeando trackings
        if any(client.get(field) for field in ['CanalOrigem', 'MidiaOrigem', 'MidiaAtual']):
            tracking = HyClientTracking(
                CanalOrigem=client.get('CanalOrigem'),
                MidiaOrigem=client.get('MidiaOrigem'),
                MidiaAtual=client.get('MidiaAtual'),
                client_id=client_obj.CodCliente
            )
            client_obj.trackings.append(tracking)

        # Mapeando equipe
        if any(client.get(field) for field in ['NomeCorretor', 'EmailCorretor', 'CpfCorretor', 'NomeGerenteGeral', 'EmailGerenteGeral', 'NomeGerente', 'EmailGerente', 'NomeCoordenador', 'EmailCoordenador', 'NomeCorretorCompartilhado', 'EmailCorretorCompartilhado', 'RegionalCorretor']):
            team = HyClientTeam(
                NomeCorretor=client.get('NomeCorretor'),
                EmailCorretor=client.get('EmailCorretor'),
                CpfCorretor=client.get('CpfCorretor'),
                NomeGerenteGeral=client.get('NomeGerenteGeral'),
                EmailGerenteGeral=client.get('EmailGerenteGeral'),
                NomeGerente=client.get('NomeGerente'),
                EmailGerente=client.get('EmailGerente'),
                NomeCoordenador=client.get('NomeCoordenador'),
                EmailCoordenador=client.get('EmailCoordenador'),
                NomeCorretorCompartilhado=client.get('NomeCorretorCompartilhado'),
                EmailCorretorCompartilhado=client.get('EmailCorretorCompartilhado'),
                RegionalCorretor=client.get('RegionalCorretor'),
                client_id=client_obj.CodCliente
            )
            client_obj.teams.append(team)

        # Mapeando os endereços
        if client.get('Endereco') and any(any(endereco.get(field) for field in ['cep', 'logradouro', 'numero', 'complemento', 'estado', 'cidade', 'bairro']) for endereco in client['Endereco'].values()):
            enderecos = client.get('Endereco', {})
            for tipo, endereco in enderecos.items():
                if any(endereco.get(field) for field in ['cep', 'logradouro', 'numero', 'complemento', 'estado', 'cidade', 'bairro']):
                    address_obj = HyClientAddress(
                        tipo=tipo,
                        cep=endereco.get('cep'),
                        logradouro=endereco.get('logradouro'),
                        numero=endereco.get('numero'),
                        complemento=endereco.get('complemento'),
                        estado=endereco.get('estado'),
                        cidade=endereco.get('cidade'),
                        bairro=endereco.get('bairro'),
                        client_id=client_obj.CodCliente
                    )
                    client_obj.address = address_obj

        # Mapeando os produtos de interesse
        if client.get('ProdutosInteresse') and any(produto.get('CodProduto') for produto in client['ProdutosInteresse']):
            produtos_interesse = client.get('ProdutosInteresse', [])
            for produto in produtos_interesse:
                if produto.get('CodProduto'):
                    product_interest_obj = HyClientProductInterest(
                        CodProduto=produto['CodProduto'],
                        CodInterno=produto.get('CodInterno'),
                        produto=produto['produto'],
                        data_oferta=str_to_datetime(produto['data_oferta']),
                        client_id=client_obj.CodCliente
                    )
                    client_obj.product_interests.append(product_interest_obj)

        clients.append(client_obj)

    return clients

#Função para verificar se os dados obtidos na API realmente foram gravados no db
def verify_data_in_db(db: Session, json_file_path: str):
    
    with open(json_file_path, 'r') as json_file:
        client_data = json.load(json_file)
    
    for client in client_data['Clientes']:
        db_client = db.query(HyClient).filter(HyClient.CodCliente == client['CodCliente']).first()
        if not db_client:
            logger.error(f"Client with CodCliente {client['CodCliente']} not found in DB.")
        else:
            discrepancies = []
            if db_client.Nome != client['Nome']:
                discrepancies.append(f"Nome mismatch: DB({db_client.Nome}) != API({client['Nome']})")
            # Adicione outras verificações conforme necessário

            if discrepancies:
                logger.warning(f"Discrepancies for CodCliente {client['CodCliente']}:")
                for discrepancy in discrepancies:
                    logger.warning(f" - {discrepancy}")
            else:
                logger.info(f"Client with CodCliente {client['CodCliente']} found successfully with no discrepancies.")
