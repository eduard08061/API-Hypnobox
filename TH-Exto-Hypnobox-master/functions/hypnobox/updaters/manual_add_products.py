from functions.db_config import SessionLocal
from functions.hypnobox.auth import hy_url, hy_token
from sqlalchemy.orm import Session
from functions.hypnobox.log_handler import log_job_start, log_job_end
from functions.general import str_to_datetime, logging_config, timestamp_now_ddmmaa
import json, requests
from models.hy_products import *

products_data = [
    {
        "CodProduto": "39", 
        "CodInterno": "",
        "DataAtualizacao": "2024-06-12 14:00:00",
        "CodRegional": "",
        "Produto": "sem informação (excluído)",
        "Regional": "",
        "Finalidade": "",
        "IdTipoProduto": "",
        "TipoProduto": "",
        "FaseProduto": "",
        "Descricao": "produto excluído do banco de dados",
        "AnoEntrega": "",
        "ValorDe": "",
        "ValorAte": "",
        "AreaUtilDe": "",
        "AreaUtilAte": "",
        "DormitoriosDe": "",
        "DormitoriosAte": "",
        "SuitesDe": "",
        "SuitesAte": "",
        "BanheiroDe": "",
        "BanheiroAte": "",
        "VagasDe": "",
        "VagasAte": "",
        "Caracteristicas": "",
        "UrlChat": "",
        "Endereco": {
            "Cep": "",
            "Logradouro": "",
            "Numero": "",
            "Complemento": "",
            "Estado": "",
            "Cidade": "",
            "Bairro": ""
        },
        #"Unidades": [
        #    {
        #        "idUnidade": "",
        #        "TipoUnidade": "",
        #        "Finalidade": "",
        #        "Transacao": "",
        #        "Valor": "",
        #        "TotalComodos": "",
        #        "TotalDormitorio": "",
        #        "TotalAreaUtil": "",
        #        "TotalAreaTotal": "",
        #        "TotalSuite": "",
        #        "TotalBanheiro": "",
        #        "TotalVaga": "",
        #        "TotalPeDireito": ""
        #    }
        #],
        "unidades_de_ate": {
            "TotalBanheiroDe": "",
            "TotalBanheiroAte": "",
            "TotalVagaDe": "",
            "TotalVagaAte": "",
            "TotalDormitorioDe": "",
            "TotalDormitorioAte": "",
            "TotalAreaUtilDe": "",
            "TotalAreaUtilAte": ""
        }},


        {
        "CodProduto": "38", 
        "CodInterno": "",
        "DataAtualizacao": "2024-06-12 14:00:00",
        "CodRegional": "",
        "Produto": "sem informação (excluído)",
        "Regional": "",
        "Finalidade": "",
        "IdTipoProduto": "",
        "TipoProduto": "",
        "FaseProduto": "",
        "Descricao": "produto excluído do banco de dados",
        "AnoEntrega": "",
        "ValorDe": "",
        "ValorAte": "",
        "AreaUtilDe": "",
        "AreaUtilAte": "",
        "DormitoriosDe": "",
        "DormitoriosAte": "",
        "SuitesDe": "",
        "SuitesAte": "",
        "BanheiroDe": "",
        "BanheiroAte": "",
        "VagasDe": "",
        "VagasAte": "",
        "Caracteristicas": "",
        "UrlChat": "",
        "Endereco": {
            "Cep": "",
            "Logradouro": "",
            "Numero": "",
            "Complemento": "",
            "Estado": "",
            "Cidade": "",
            "Bairro": ""
        },
        #"Unidades": [
        #    {
        #        "idUnidade": "",
        #        "TipoUnidade": "",
        #        "Finalidade": "",
        #        "Transacao": "",
        #        "Valor": "",
        #        "TotalComodos": "",
        #        "TotalDormitorio": "",
        #        "TotalAreaUtil": "",
        #        "TotalAreaTotal": "",
        #        "TotalSuite": "",
        #        "TotalBanheiro": "",
        #        "TotalVaga": "",
        #        "TotalPeDireito": ""
        #    }
        #],
        "unidades_de_ate": {
            "TotalBanheiroDe": "",
            "TotalBanheiroAte": "",
            "TotalVagaDe": "",
            "TotalVagaAte": "",
            "TotalDormitorioDe": "",
            "TotalDormitorioAte": "",
            "TotalAreaUtilDe": "",
            "TotalAreaUtilAte": ""
        }},

        {
        "CodProduto": "42", 
        "CodInterno": "",
        "DataAtualizacao": "2024-06-12 14:00:00",
        "CodRegional": "",
        "Produto": "sem informação (excluído)",
        "Regional": "",
        "Finalidade": "",
        "IdTipoProduto": "",
        "TipoProduto": "",
        "FaseProduto": "",
        "Descricao": "produto excluído do banco de dados",
        "AnoEntrega": "",
        "ValorDe": "",
        "ValorAte": "",
        "AreaUtilDe": "",
        "AreaUtilAte": "",
        "DormitoriosDe": "",
        "DormitoriosAte": "",
        "SuitesDe": "",
        "SuitesAte": "",
        "BanheiroDe": "",
        "BanheiroAte": "",
        "VagasDe": "",
        "VagasAte": "",
        "Caracteristicas": "",
        "UrlChat": "",
        "Endereco": {
            "Cep": "",
            "Logradouro": "",
            "Numero": "",
            "Complemento": "",
            "Estado": "",
            "Cidade": "",
            "Bairro": ""
        },
        #"Unidades": [
        #    {
        #        "idUnidade": "",
        #        "TipoUnidade": "",
        #        "Finalidade": "",
        #        "Transacao": "",
        #        "Valor": "",
        #        "TotalComodos": "",
        #        "TotalDormitorio": "",
        #        "TotalAreaUtil": "",
        #        "TotalAreaTotal": "",
        #        "TotalSuite": "",
        #        "TotalBanheiro": "",
        #        "TotalVaga": "",
        #        "TotalPeDireito": ""
        #    }
        #],
        "unidades_de_ate": {
            "TotalBanheiroDe": "",
            "TotalBanheiroAte": "",
            "TotalVagaDe": "",
            "TotalVagaAte": "",
            "TotalDormitorioDe": "",
            "TotalDormitorioAte": "",
            "TotalAreaUtilDe": "",
            "TotalAreaUtilAte": ""
        }},

        {
        "CodProduto": 118, 
        "CodInterno": "",
        "DataAtualizacao": "2024-06-12 14:00:00",
        "CodRegional": "",
        "Produto": "sem informação (excluído)",
        "Regional": "",
        "Finalidade": "",
        "IdTipoProduto": "",
        "TipoProduto": "",
        "FaseProduto": "",
        "Descricao": "produto excluído do banco de dados",
        "AnoEntrega": "",
        "ValorDe": "",
        "ValorAte": "",
        "AreaUtilDe": "",
        "AreaUtilAte": "",
        "DormitoriosDe": "",
        "DormitoriosAte": "",
        "SuitesDe": "",
        "SuitesAte": "",
        "BanheiroDe": "",
        "BanheiroAte": "",
        "VagasDe": "",
        "VagasAte": "",
        "Caracteristicas": "",
        "UrlChat": "",
        "Endereco": {
            "Cep": "",
            "Logradouro": "",
            "Numero": "",
            "Complemento": "",
            "Estado": "",
            "Cidade": "",
            "Bairro": ""
        },
        #"Unidades": [
        #    {
        #        "idUnidade": "",
        #        "TipoUnidade": "",
        #        "Finalidade": "",
        #        "Transacao": "",
        #        "Valor": "",
        #        "TotalComodos": "",
        #        "TotalDormitorio": "",
        #        "TotalAreaUtil": "",
        #        "TotalAreaTotal": "",
        #        "TotalSuite": "",
        #        "TotalBanheiro": "",
        #        "TotalVaga": "",
        #        "TotalPeDireito": ""
        #    }
        #],
        "unidades_de_ate": {
            "TotalBanheiroDe": "",
            "TotalBanheiroAte": "",
            "TotalVagaDe": "",
            "TotalVagaAte": "",
            "TotalDormitorioDe": "",
            "TotalDormitorioAte": "",
            "TotalAreaUtilDe": "",
            "TotalAreaUtilAte": ""
        }},

        {
        "CodProduto": 0, 
        "CodInterno": "",
        "DataAtualizacao": "2024-06-12 14:00:00",
        "CodRegional": "",
        "Produto": "sem informação (excluído)",
        "Regional": "",
        "Finalidade": "",
        "IdTipoProduto": "",
        "TipoProduto": "",
        "FaseProduto": "",
        "Descricao": "produto excluído do banco de dados",
        "AnoEntrega": "",
        "ValorDe": "",
        "ValorAte": "",
        "AreaUtilDe": "",
        "AreaUtilAte": "",
        "DormitoriosDe": "",
        "DormitoriosAte": "",
        "SuitesDe": "",
        "SuitesAte": "",
        "BanheiroDe": "",
        "BanheiroAte": "",
        "VagasDe": "",
        "VagasAte": "",
        "Caracteristicas": "",
        "UrlChat": "",
        "Endereco": {
            "Cep": "",
            "Logradouro": "",
            "Numero": "",
            "Complemento": "",
            "Estado": "",
            "Cidade": "",
            "Bairro": ""
        },
        #"Unidades": [
        #    {
        #        "idUnidade": "",
        #        "TipoUnidade": "",
        #        "Finalidade": "",
        #        "Transacao": "",
        #        "Valor": "",
        #        "TotalComodos": "",
        #        "TotalDormitorio": "",
        #        "TotalAreaUtil": "",
        #        "TotalAreaTotal": "",
        #        "TotalSuite": "",
        #        "TotalBanheiro": "",
        #        "TotalVaga": "",
        #        "TotalPeDireito": ""
        #    }
        #],
        "unidades_de_ate": {
            "TotalBanheiroDe": "",
            "TotalBanheiroAte": "",
            "TotalVagaDe": "",
            "TotalVagaAte": "",
            "TotalDormitorioDe": "",
            "TotalDormitorioAte": "",
            "TotalAreaUtilDe": "",
            "TotalAreaUtilAte": ""
        }}
        ]
    

# Criar instância de log
logger = logging_config()

# Função principal para atualizar produtos
def update_products():
    job_id = log_job_start("manual update products", None, None, None, None)
    db: Session = SessionLocal()

    try:
        date, hour = timestamp_now_ddmmaa()
        # Realizar chamada para API
        # Grava informações no banco de dados
        add_products_in_bulk(db, products_data)
        print("update add_products_db com sucesso")
        log_job_end(job_id, len(products_data), None, None, "success")

    except Exception as e:
        logger.error(f"error in update_products: {e} {date} ({hour})")
        print(f"error in update_products: {e} {date} ({hour})")
        log_job_end(job_id, None, None, e, "error")

    finally:
        db.close()
        logger.info(f"manual update products {date} ({hour})")
        print(f"manual update products {date} ({hour})")

# Função para realizar chamada na API de produtos



# Função que mapeia a resposta da API para a MODEL
def dict_model_products(products_data):
    print("iniciando função: dict_model_products")
    products = []

    for product in products_data:

        product_obj = HyProduct(
            CodProduto=             product.get('CodProduto'),
            CodInterno=             product.get('CodInterno') or None,
            DataAtualizacao=        str_to_datetime(product.get('DataAtualizacao')),
            CodRegional=            product.get('CodRegional') or None,
            Produto=                product.get('Produto') or None,
            Regional=               product.get('Regional') or None,
            Finalidade=             product.get('Finalidade') or None,
            IdTipoProduto=          product.get('IdTipoProduto') or None,
            TipoProduto=            product.get('TipoProduto') or None,
            FaseProduto=            product.get('FaseProduto') or None,
            Descricao=              product.get('Descricao') or None,
            AnoEntrega=             product.get('AnoEntrega') or None,
            ValorDe=                product.get('ValorDe') or None,
            ValorAte=               product.get('ValorAte') or None,
            AreaUtilDe=             product.get('AreaUtilDe') or None,
            AreaUtilAte=            product.get('AreaUtilAte') or None,
            DormitoriosDe=          product.get('DormitoriosDe') or None,
            DormitoriosAte=         product.get('DormitoriosAte') or None,
            SuitesDe=               product.get('SuitesDe') or None,
            SuitesAte=              product.get('SuitesAte') or None,
            BanheiroDe=             product.get('BanheiroDe') or None,
            BanheiroAte=            product.get('BanheiroAte') or None,
            VagasDe=                product.get('VagasDe') or None,
            VagasAte=               product.get('VagasAte') or None,
            Caracteristicas=        product.get('Caracteristicas') or None,
            UrlChat=                product.get('UrlChat') or None,

            TotalBanheiroDe=        product.get('UnidadesDeAte', {}).get('TotalBanheiroDe') or None,
            TotalBanheiroAte=       product.get('UnidadesDeAte', {}).get('TotalBanheiroAte') or None,
            TotalVagaDe=            product.get('UnidadesDeAte', {}).get('TotalVagaDe') or None,
            TotalVagaAte=           product.get('UnidadesDeAte', {}).get('TotalVagaAte') or None,
            TotalDormitorioDe=      product.get('UnidadesDeAte', {}).get('TotalDormitorioDe') or None,
            TotalDormitorioAte=     product.get('UnidadesDeAte', {}).get('TotalDormitorioAte') or None,
            TotalAreaUtilDe=        product.get('UnidadesDeAte', {}).get('TotalAreaUtilDe') or None,
            TotalAreaUtilAte=       product.get('UnidadesDeAte', {}).get('TotalAreaUtilAte') or None
        )

        # Mapear informações sobre endereço do produto
        if any(product['Endereco'].get(field) 
               for field in ['Cep', 'Logradouro', 'Numero', 'Complemento', 'Estado', 'Cidade', 'Bairro']) and len(product['Endereco']) > 0:
            address = HyProductAddress(
                Cep=product['Endereco'].get('Cep') or None,
                Logradouro=product['Endereco'].get('Logradouro') or None,
                Numero=product['Endereco'].get('Numero') or None,
                Complemento=product['Endereco'].get('Complemento') or None,
                Estado=product['Endereco'].get('Estado') or None,
                Cidade=product['Endereco'].get('Cidade') or None,
                Bairro=product['Endereco'].get('Bairro') or None,
                CodProduto=product.get('CodProduto') or None,                
            )
            product_obj.addresses.append(address)

        # Mapear informações sobre unidades do produto
        if product.get('Unidades') and len(product['Unidades']) > 0:
            for unit in product['Unidades']:
                unit_obj = HyProductUnit(
                    idUnidade=unit.get('idUnidade'),
                    TipoUnidade=unit.get('TipoUnidade') or None,
                    Finalidade=unit.get('Finalidade') or None,
                    Transacao=unit.get('Transacao') or None,
                    Valor=unit.get('Valor') or None,
                    TotalComodos=unit.get('TotalComodos') or None,
                    TotalDormitorio=unit.get('TotalDormitorio') or None,
                    TotalAreaUtil=unit.get('TotalAreaUtil') or None,
                    TotalAreaTotal=unit.get('TotalAreaTotal') or None,
                    TotalSuite=unit.get('TotalSuite') or None,
                    TotalBanheiro=unit.get('TotalBanheiro') or None,
                    TotalVaga=unit.get('TotalVaga') or None,
                    TotalPeDireito=unit.get('TotalPeDireito') or None,
                    
                    CodProduto=product.get('CodProduto')
                )
                product_obj.units.append(unit_obj)

        products.append(product_obj)

    return products

# Função que recebe o mapeamento da MODEL e adiciona cada registro ao DB
def add_products_in_bulk(db: Session, products_data):
    print("iniciando função: add_products_in_bulk")
    products = dict_model_products(products_data)

    try:
        for product in products:
            db.merge(product)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"error in add_products_in_bulk: {e}")
        print(f"error in add_products_in_bulk: {e}")
        
    finally:
        print(f"add_products_in_bulk fineshed")

update_products()
