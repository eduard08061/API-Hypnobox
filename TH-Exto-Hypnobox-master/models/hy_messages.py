from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from . import Base


class HyMessageUser(Base):
    __tablename__ = 'hy_msg_dUsers'
    
    id =        Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    idHyCRM =   Column(Integer,     nullable=True) #Externo
    Name =      Column(String(255), nullable=True)
    Email =     Column(String(255), nullable=True)

class HyMessageDimStatus(Base):
    # "StatusMenssagem": "ENVIADA" / "RESPONDIDA" ...
    __tablename__ = 'hy_msg_dStatus'
    
    # Identificação/Valores do registro
    id =                Column(Integer, primary_key=True, autoincrement=True)
    MessageStatus =     Column(String(255), nullable=False)

    # Refere-se às mensagens que estão associadas a este gerente.
    message_status = relationship("HyMessage", back_populates="message_status")

class HyMessageDimTipo(Base):
    # "TipoMensagem": "SAIDA"
    __tablename__ = 'hy_msg_dType'
    
    # Identificação/Valores do registro
    id =                Column(Integer, primary_key=True)
    MessageType =       Column(String(255), nullable=False)

    # Refere-se às mensagens que estão associadas a este gerente.
    message_tipo = relationship("HyMessage", back_populates="message_tipo")

class HyMessage(Base):
    __tablename__ = 'hy_msg_fMessages'

    # Identificação do registro
    id =            Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    ClientName =    Column(String(255), nullable=True)
    IdClient =      Column(Integer, nullable=False)

    # Datalhes da mensagem
    ClientNew =             Column(Boolean,     nullable=False)
    CNA =                   Column(Boolean,     nullable=False)
    AssignmentDate =        Column(DateTime,    nullable=True)

    # Mensagem
    Message =               Column(Text, nullable=True)
    Subject =               Column(Text, nullable=True)
    MessageDate =           Column(DateTime,    nullable=True)
    #TipoMensagem =         Column(String(255), nullable=True)

    # Campos com chaves estrangeiras
    IdBrokerResponsible =           Column(Integer, ForeignKey('hy_msg_dUsers.id'),     nullable=True)
    IdBrokerManager =               Column(Integer, ForeignKey('hy_msg_dUsers.id'),     nullable=True)
    IdProduct =                     Column(Integer, ForeignKey('hy_dProducts.id'),      nullable=True)
    IdChannel =                     Column(Integer, ForeignKey('hy_dChannels.id'),      nullable=True)
    IdSubChannel =                  Column(Integer, ForeignKey('hy_dSubChannels.id'),   nullable=True)
    IdMoment =                      Column(Integer, ForeignKey('hy_dMoments.id'),       nullable=True)
    IdSubMoment =                   Column(Integer, ForeignKey('hy_dSubMoments.id'),    nullable=True)
    IdMedia =                       Column(Integer, ForeignKey('hy_dMedias.id'),        nullable=True)
    IdMediaGroup =                  Column(Integer, ForeignKey('hy_dMediaGroups.id'),   nullable=True)
    IdTemperature =                 Column(Integer, ForeignKey('hy_dTemperatures.id'),  nullable=True)
    IdStatusMessage =               Column(Integer, ForeignKey('hy_msg_dStatus.id'),    nullable=True)
    IdMessageType =                 Column(Integer, ForeignKey('hy_msg_dType.id'),      nullable=True)
    IdResponsibleClient =           Column(Integer,     nullable=True)
    IdResponsibleClientShared =     Column(Integer,     nullable=True)
   

    message_canal =         relationship("HyDimChannel",        back_populates="message_canal")
    message_sub_canal =     relationship("HyDimSubChannel",     back_populates="message_sub_canal")
    message_momento =       relationship("HyDimMoment",         back_populates="message_momento")
    message_sub_momento =   relationship("HyDimSubMoment",      back_populates="message_sub_momento")
    message_temperatura =   relationship("HyDimTemperature",    back_populates="message_temperatura")
    message_midia =         relationship("HyDimMedia",          back_populates="message_midia")
    message_grupo_midia =   relationship("HyDimMediaGroup",     back_populates="message_grupo_midia")
    message_email =         relationship("HyMessageEmail",      back_populates="message_email")
    message_tel =           relationship("HyMessageTel",        back_populates="message_tel")
    message_status =        relationship("HyMessageDimStatus",  back_populates="message_status")
    message_tipo =          relationship("HyMessageDimTipo",    back_populates="message_tipo")

    BrokerResponsible =   relationship("HyMessageUser",       foreign_keys=[IdBrokerResponsible])
    BrokerManager =       relationship("HyMessageUser",       foreign_keys=[IdBrokerManager])     

class HyMessageTel(Base):
    __tablename__ = 'hy_msg_dPhone'
    
    IdClientMessage =   Column(Integer, ForeignKey('hy_msg_fMessages.id'), primary_key=True)
    phone =             Column(String(50),   nullable=False)
    phone_ddd =         Column(String(50),   nullable=True)
    phone_type =        Column(String(20),  nullable=False) # Residencial, Mensagem, Celular

    message_tel = relationship("HyMessage", back_populates="message_tel")

class HyMessageEmail(Base):
    __tablename__ = 'hy_msg_dEmail'
    
    IdClientMessage =       Column(Integer, ForeignKey('hy_msg_fMessages.id'), primary_key=True)
    email =                 Column(String(255),     nullable=False)
    email_type =            Column(Integer,         nullable=False) # 1, 2 ou 3

    message_email = relationship("HyMessage", back_populates="message_email")