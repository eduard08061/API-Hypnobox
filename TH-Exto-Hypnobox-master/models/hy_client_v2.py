from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from . import Base

#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class HyClientV2(Base):
    __tablename__ = 'hy_c_fClients'

    id =                    Column(Integer,     primary_key=True, autoincrement=False)   # CodCliente
    Name =                  Column(String(255))                     # Nome
    InternalCode =          Column(String(255), nullable=True)      # CodInterno
    DateRegister =          Column(DateTime,    nullable=True)      # DataCadastro
    DateLastInteraction =   Column(DateTime,    nullable=True)      # DataUltimaInteracao
    Denylist =              Column(Boolean,     nullable=True)      # Denylist
    Consent =               Column(Boolean,     nullable=True)      # Consent

    IdObjective =           Column(Integer, ForeignKey('hy_c_dObjectives.id'), nullable=True)
    IdMoment =              Column(Integer, ForeignKey('hy_dMoments.id'), nullable=True)
    IdSubMoment =           Column(Integer, ForeignKey('hy_dSubMoments.id'), nullable=True)
    IdTemperature =         Column(Integer, ForeignKey('hy_dTemperatures.id'), nullable=True)
    IdStatus =              Column(Integer, ForeignKey('hy_c_dStatus.id'), nullable=True)
    IdInactiveState =       Column(Integer, ForeignKey('hy_c_dInactiveStates.id'), nullable=True)
    IdProductOrigin =       Column(Integer, ForeignKey('hy_dProducts.id'), nullable=True) 
    IdProductInterest =     Column(Integer, ForeignKey('hy_dProducts.id'), nullable=True)
    IdFirstProperty =       Column(Integer, ForeignKey('hy_c_dFirstProperty.id'), nullable=True)

    IdSourceChannel =       Column(Integer, ForeignKey('hy_dChannels.id'), nullable=True)
    IdSourceMedia =         Column(Integer, ForeignKey('hy_dMedias.id'), nullable=True)
    IdCurrentMedia =        Column(Integer, ForeignKey('hy_dMedias.id'), nullable=True)
    IdMediaOriginGroup =    Column(Integer, ForeignKey('hy_dMediaGroups.id'), nullable=True)
    IdCurrentMediaGroup =   Column(Integer, ForeignKey('hy_dMediaGroups.id'), nullable=True)

    IdBroker =              Column(Integer, ForeignKey('hy_c_dUsers.id'), nullable=True)
    IdBrokerOrigin =        Column(Integer, ForeignKey('hy_c_dUsers.id'), nullable=True)
    IdManager =             Column(Integer, ForeignKey('hy_c_dUsers.id'), nullable=True)
    IdGeneralManager =      Column(Integer, ForeignKey('hy_c_dUsers.id'), nullable=True)
    EmailManagerOrigin =    Column(Integer, ForeignKey('hy_c_dUsers.id'), nullable=True)
    IdBrokerShared =        Column(Integer, ForeignKey('hy_c_dUsers.id'), nullable=True)
    IdCoordinator =         Column(Integer, ForeignKey('hy_c_dUsers.id'), nullable=True)

    # Atributos para armazenar os objetos adicionais
    address =       relationship("HyDimClientAdress",   back_populates="client", uselist=False, cascade="all, delete-orphan")
    emails =        relationship("HyDimClientEmail",    back_populates="client", cascade="all, delete-orphan")
    phones =        relationship("HyDimClientPhone",    back_populates="client", cascade="all, delete-orphan")
    demographic =   relationship("HyDimClientDemographic", back_populates="client", uselist=False, cascade="all, delete-orphan")
    description =   relationship("HyClientDescription", back_populates="client", uselist=False, cascade="all, delete-orphan")
    ranges =        relationship("HyDimRanges", back_populates="client", uselist=False, cascade="all, delete-orphan")

    # Relacionamentos com as tabelas de dimensões
    objective =             relationship("HyDimObjective")
    moment =                relationship("HyDimMoment")
    sub_moment =            relationship("HyDimSubMoment")
    temperature =           relationship("HyDimTemperature")
    status =                relationship("HyDimStatus")
    inactive_state =        relationship("HyDimInactiveState")
    product_origin =        relationship("HyDimProduct",    foreign_keys=[IdProductOrigin])
    product_interest =      relationship("HyDimProduct",    foreign_keys=[IdProductInterest])
    source_channel =        relationship("HyDimChannel")
    source_media =          relationship("HyDimMedia",      foreign_keys=[IdSourceMedia])
    current_media =         relationship("HyDimMedia",      foreign_keys=[IdCurrentMedia])
    media_origin_group =    relationship("HyDimMediaGroup", foreign_keys=[IdMediaOriginGroup])
    current_media_group =   relationship("HyDimMediaGroup", foreign_keys=[IdCurrentMediaGroup])
    broker =                relationship("HyDimUser",       foreign_keys=[IdBroker])
    broker_origin =         relationship("HyDimUser",       foreign_keys=[IdBrokerOrigin])
    manager =               relationship("HyDimUser",       foreign_keys=[IdManager])
    general_manager =       relationship("HyDimUser",       foreign_keys=[IdGeneralManager])
    email_manager_origin =  relationship("HyDimUser",       foreign_keys=[EmailManagerOrigin])
    broker_shared =         relationship("HyDimUser",       foreign_keys=[IdBrokerShared])
    coordinator =           relationship("HyDimUser",       foreign_keys=[IdCoordinator])

class HyClientDescription(Base):
    __tablename__ = 'hy_c_dDescriptions'

    id =            Column(Integer, ForeignKey('hy_c_fClients.id'), primary_key=True, nullable=False, autoincrement=False)
    Description =   Column(Text, nullable=True)

    client = relationship("HyClientV2", back_populates="description")

class HyDimClientDemographic(Base):
    __tablename__ = 'hy_c_dDemographic'

    id =                Column(Integer, ForeignKey('hy_c_fClients.id'), primary_key=True, nullable=False, autoincrement=False)
    CpfValue =          Column(String(255), nullable=True, autoincrement=False)
    idGender =          Column(Integer, nullable=True, autoincrement=False)
    idMaritalStatus =   Column(Integer, nullable=True, autoincrement=False)

    ProductType =   Column(String(255), nullable=True, autoincrement=False)
    Phase =         Column(String(255), nullable=True, autoincrement=False)
    Finality =      Column(String(255), nullable=True, autoincrement=False)
    #Objective =     Column(String(255), nullable=True, autoincrement=False)
    TimeSearch =    Column(String(255), nullable=True, autoincrement=False)
    TimeDecision =  Column(String(255), nullable=True, autoincrement=False)
    LiveInvest =    Column(String(255), nullable=True, autoincrement=False)
    PaymentPlan =   Column(String(255), nullable=True, autoincrement=False)
    #FirstProperty = Column(String(255), nullable=True, autoincrement=False)
    MoreImportant = Column(String(255), nullable=True, autoincrement=False)
    FGTSValue =     Column(String(255), nullable=True, autoincrement=False)
    EntryValue =    Column(String(255), nullable=True, autoincrement=False)
    MonthlyIncome = Column(String(255), nullable=True, autoincrement=False)
    BirthDate =     Column(String(255), nullable=True, autoincrement=False)
    SpouseName =    Column(String(255), nullable=True, autoincrement=False)
    QtyDependents = Column(String(255), nullable=True, autoincrement=False)


    client = relationship("HyClientV2", back_populates="demographic")

class HyDimClientAdress(Base):
    __tablename__ = 'hy_c_dClientAdress'

    id =                Column(Integer, ForeignKey('hy_c_fClients.id'), primary_key=True, nullable=False, autoincrement=False)
    idState =           Column(Integer, ForeignKey('hy_c_dState.id'), nullable=True, autoincrement=False)                   
    idCity =            Column(Integer, ForeignKey('hy_c_dCity.id'), nullable=True, autoincrement=False)                   
    idNeighborhood =    Column(Integer, ForeignKey('hy_c_dNeighborhood.id'), nullable=True, autoincrement=False)                   

    ZipCode =           Column(String(255), nullable=True)
    PublicPlace =       Column(String(255), nullable=True)
    Number =            Column(String(255), nullable=True)
    Complement =        Column(String(255), nullable=True)

    Type =              Column(String(255), nullable=True) # R = Residencial / C = Comercial

    client =        relationship("HyClientV2", back_populates="address")
    state =         relationship("HyDimState", back_populates="addresses")
    city =          relationship("HyDimCity", back_populates="addresses")
    neighborhood =  relationship("HyDimNeighborhood", back_populates="addresses")

class HyDimUser(Base):
    __tablename__ = 'hy_c_dUsers'

    id =        Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    idHyCRM =   Column(Integer,     nullable=True) #Externo
    Name =      Column(String(255), nullable=True)
    Email =     Column(String(255), nullable=True)
    CPF =       Column(String(255), nullable=True)
    Regional =  Column(String(255), nullable=True)

class HyDimMaritalStatus(Base):
    __tablename__ = 'hy_c_dMaritalStatus'

    id =                Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    idHyCRM =           Column(Integer, nullable=True) #Externo
    MaritalStatus =     Column(String(255), nullable=True)

class HyDimGender(Base):
    __tablename__ = 'hy_c_dGender'

    id =        Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    idHyCRM =   Column(Integer, nullable=True) #Externo
    Gender =    Column(String(255), nullable=True)


class HyDimClientEmail(Base):
    __tablename__ = 'hy_c_dClientEmails'

    id =            Column(Integer, ForeignKey('hy_c_fClients.id'), primary_key=True, nullable=False, autoincrement=False)
    Email =         Column(String(255), nullable=True)
    EmailType =     Column(String(255), nullable=True) # Email1, Email2, Email3

    client = relationship("HyClientV2", back_populates="emails")

class HyDimClientPhone(Base):
    __tablename__ = 'hy_c_dClientPhones'

    id =        Column(Integer, ForeignKey('hy_c_fClients.id'), primary_key=True, nullable=False, autoincrement=False)
    Phone =     Column(String(255), nullable=True)
    PhoneDDD =  Column(String(255), nullable=True)
    PhoneType = Column(String(255), nullable=True) # Comercial, Residencial, Celular, Outro

    client = relationship("HyClientV2", back_populates="phones")


class HyDimState(Base):
    __tablename__ = 'hy_c_dState'

    id =                Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    State =             Column(String(255), nullable=True)

    addresses = relationship("HyDimClientAdress", back_populates="state")

class HyDimCity(Base):
    __tablename__ = 'hy_c_dCity'

    id =                Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    City =              Column(String(255), nullable=True)

    addresses = relationship("HyDimClientAdress", back_populates="city")

class HyDimNeighborhood(Base):
    __tablename__ = 'hy_c_dNeighborhood'

    id =                Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Neighborhood =      Column(String(255), nullable=True)

    addresses = relationship("HyDimClientAdress", back_populates="neighborhood")

class HyDimRanges(Base):
    __tablename__ = 'hy_c_dRanges'

    id =                Column(Integer, ForeignKey('hy_c_fClients.id'), primary_key=True, nullable=False, autoincrement=False)
    PriceFrom =         Column(String(255), nullable=True)
    PriceTo =           Column(String(255), nullable=True)
    AreaFrom =          Column(String(255), nullable=True)
    AreaTo =            Column(String(255), nullable=True)
    BedroomsFrom =      Column(String(255), nullable=True)
    BedroomsTo =        Column(String(255), nullable=True)

    client = relationship("HyClientV2", back_populates="ranges")

class HyDimFirstProperty(Base):
    __tablename__ = 'hy_c_dFirstProperty'

    id =                Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    idHyCRM =           Column(Integer, nullable=True)
    FirstProperty =     Column(String(255), nullable=True)

class HyDimInactiveState(Base):
    __tablename__ = 'hy_c_dInactiveStates'

    id =                Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =           Column(Integer, nullable=True) #Externo
    InactiveState =     Column(String(255), nullable=True)

class HyDimStatus(Base):
    __tablename__ = 'hy_c_dStatus'
 
    id =        Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =   Column(Integer, nullable=True) #Externo
    Status =    Column(String(255), nullable=True)

class HyDimObjective(Base):
    __tablename__ = 'hy_c_dObjectives'

    id =            Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =       Column(Integer, nullable=True) #Externo
    Objective =     Column(String(255), nullable=True)