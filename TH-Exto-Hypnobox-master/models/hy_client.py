from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime

class HyClient(Base):
    __tablename__ = 'hy_clients'

    CodCliente = Column(Integer, primary_key=True)
    Nome = Column(String(255))
    Cpf = Column(String(20), nullable=True)
    DataUltimaInteracao = Column(DateTime, nullable=True)
    DataCadastro = Column(DateTime, nullable=True)
    Momento = Column(String(50), nullable=True)
    Submomento = Column(String(50), nullable=True)
    Temperatura = Column(String(20), nullable=True)
    Status = Column(String(50), nullable=True)
    InactiveState = Column(String(50), nullable=True)
    InactiveStateId = Column(Integer, nullable=True)
    Objetivo = Column(String(50), nullable=True)

    # Relationships
    emails = relationship("HyClientEmail", back_populates="client", cascade="all, delete-orphan")
    phones = relationship("HyClientPhone", back_populates="client", cascade="all, delete-orphan")
    demographics = relationship("HyClientDemographic", back_populates="client", uselist=False, cascade="all, delete-orphan")
    trackings = relationship("HyClientTracking", back_populates="client", cascade="all, delete-orphan")
    teams = relationship("HyClientTeam", back_populates="client", cascade="all, delete-orphan")
    address = relationship("HyClientAddress", back_populates="client", uselist=False, cascade="all, delete-orphan")
    product_interests = relationship("HyClientProductInterest", back_populates="client", cascade="all, delete-orphan")
    genders = relationship("HyClientGender", back_populates="client", cascade="all, delete-orphan")

class HyClientEmail(Base):
    __tablename__ = 'hy_client_emails'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('hy_clients.CodCliente'))
    email = Column(String(255))

    client = relationship("HyClient", back_populates="emails")

class HyClientPhone(Base):
    __tablename__ = 'hy_client_phones'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('hy_clients.CodCliente'))
    telefone = Column(String(20))
    tipo = Column(String(50))
    ddd = Column(String(3))

    client = relationship("HyClient", back_populates="phones")

class HyClientDemographic(Base):
    __tablename__ = 'hy_client_demographics'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('hy_clients.CodCliente'))
    estadocivil = Column(String(50), nullable=True)
    NomeConjuge = Column(String(255), nullable=True)
    QtdDependentes = Column(Integer, nullable=True)
    ValorFgts = Column(Float, nullable=True)
    ValorEntrada = Column(Float, nullable=True)
    ValorRendaMensal = Column(Float, nullable=True)
    DataNascimento = Column(DateTime, nullable=True)

    client = relationship("HyClient", back_populates="demographics")

class HyClientGender(Base):
    __tablename__ = 'hy_client_genders'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('hy_clients.CodCliente'))
    Sexo = Column(String(10), nullable=True)
 
    client = relationship("HyClient", back_populates="genders")

class HyClientTracking(Base):
    __tablename__ = 'hy_client_trackings'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('hy_clients.CodCliente'))
    CanalOrigem = Column(String(50), nullable=True)
    MidiaOrigem = Column(String(255), nullable=True)
    MidiaAtual = Column(String(255), nullable=True)

    client = relationship("HyClient", back_populates="trackings")

class HyClientTeam(Base):
    __tablename__ = 'hy_client_teams'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('hy_clients.CodCliente'))

    NomeCorretor = Column(String(255), nullable=True)
    EmailCorretor = Column(String(255), nullable=True)
    CpfCorretor = Column(String(255), nullable=True)
    NomeGerenteGeral = Column(String(255), nullable=True)
    EmailGerenteGeral = Column(String(255), nullable=True)
    NomeGerente = Column(String(255), nullable=True)
    EmailGerente = Column(String(255), nullable=True)
    NomeCoordenador = Column(String(255), nullable=True)
    EmailCoordenador = Column(String(255), nullable=True)
    NomeCorretorCompartilhado = Column(String(255), nullable=True)
    EmailCorretorCompartilhado = Column(String(255), nullable=True)
    RegionalCorretor = Column(String(50), nullable=True)

    client = relationship("HyClient", back_populates="teams")

class HyClientAddress(Base):
    __tablename__ = 'hy_client_addresses'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('hy_clients.CodCliente'))

    tipo = Column(String(50))  # 'Residencial' ou 'Comercial'
    cep = Column(String(20), nullable=True)
    logradouro = Column(String(255), nullable=True)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(255), nullable=True)
    estado = Column(String(50), nullable=True)
    cidade = Column(String(50), nullable=True)
    bairro = Column(String(50), nullable=True)

    client = relationship("HyClient", back_populates="address")

class HyClientProductInterest(Base):
    __tablename__ = 'hy_client_product_interests'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('hy_clients.CodCliente'))

    CodProduto = Column(String(50))
    CodInterno = Column(String(50), nullable=True)
    produto = Column(String(255))
    data_oferta = Column(DateTime)

    client = relationship("HyClient", back_populates="product_interests")