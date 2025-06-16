from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from . import Base

class HyProduct(Base):
    __tablename__ = 'hy_products'

    # Identificação do registro
    CodProduto = Column(Integer, primary_key=True, nullable=False, autoincrement=False)

    # Informações básicas do produto - gerais
    CodInterno = Column(String(50), nullable=True)
    DataAtualizacao = Column(DateTime, nullable=True)
    CodRegional = Column(Integer, nullable=True)
    Produto = Column(String(255), nullable=False)
    Regional = Column(String(50), nullable=True)
    Finalidade = Column(String(50), nullable=True)
    IdTipoProduto = Column(Integer, nullable=True)
    TipoProduto = Column(String(50), nullable=True)
    FaseProduto = Column(String(50), nullable=True)
    Descricao = Column(Text, nullable=True)
    AnoEntrega = Column(Integer, nullable=True)
    ValorDe = Column(Float, nullable=True)
    ValorAte = Column(Float, nullable=True)
    AreaUtilDe = Column(Float, nullable=True)
    AreaUtilAte = Column(Float, nullable=True)
    DormitoriosDe = Column(Integer, nullable=True)
    DormitoriosAte = Column(Integer, nullable=True)
    SuitesDe = Column(Integer, nullable=True)
    SuitesAte = Column(Integer, nullable=True)
    BanheiroDe = Column(Integer, nullable=True)
    BanheiroAte = Column(Integer, nullable=True)
    VagasDe = Column(Integer, nullable=True)
    VagasAte = Column(Integer, nullable=True)
    Caracteristicas = Column(Text, nullable=True)
    UrlChat = Column(String(255), nullable=True)

    # Informações básicas do produto - "UnidadesDeAte"
    TotalBanheiroDe = Column(Integer, nullable=True)
    TotalBanheiroAte = Column(Integer, nullable=True)
    TotalVagaDe = Column(Integer, nullable=True)
    TotalVagaAte = Column(Integer, nullable=True)
    TotalDormitorioDe = Column(Integer, nullable=True)
    TotalDormitorioAte = Column(Integer, nullable=True)
    TotalAreaUtilDe = Column(Float, nullable=True)
    TotalAreaUtilAte = Column(Float, nullable=True)

    addresses = relationship("HyProductAddress", back_populates="product")
    units = relationship("HyProductUnit", back_populates="product")


class HyProductAddress(Base):
    __tablename__ = 'hy_product_addresses'
    
    # Identificação do registro e chaves-estrangeiras
    id = Column(Integer, primary_key=True)
    CodProduto = Column(Integer, ForeignKey('hy_products.CodProduto'))

    # Principais campos da tabela
    Cep = Column(String(255), nullable=True)
    Logradouro = Column(String(255), nullable=True)
    Numero = Column(String(255), nullable=True)
    Complemento = Column(String(255), nullable=True)
    Estado = Column(String(255), nullable=True)
    Cidade = Column(String(255), nullable=True)
    Bairro = Column(String(255), nullable=True)

    # Criando relação com a tabela de "HyProduct" 
    product = relationship("HyProduct", back_populates="addresses")

class HyProductUnit(Base):
    __tablename__ = 'hy_product_units'

    # Identificação do registro e chaves-estrangeiras
    id = Column(Integer, primary_key=True)
    CodProduto = Column(Integer, ForeignKey('hy_products.CodProduto'))

    # Principais campos da tabela
    idUnidade = Column(Integer, nullable=False)
    TipoUnidade = Column(String(255), nullable=True)
    Finalidade = Column(String(255), nullable=True)
    Transacao = Column(String(255), nullable=True)
    Valor = Column(Float, nullable=True)
    TotalComodos = Column(Integer, nullable=True)
    TotalDormitorio = Column(Integer, nullable=True)
    TotalAreaUtil = Column(Float, nullable=True)
    TotalAreaTotal = Column(Float, nullable=True)
    TotalSuite = Column(Integer, nullable=True)
    TotalBanheiro = Column(Integer, nullable=True)
    TotalVaga = Column(Integer, nullable=True)
    TotalPeDireito = Column(Float, nullable=True)

    # Criando relação com a tabela de "HyProduct" 
    product = relationship("HyProduct", back_populates="units")
