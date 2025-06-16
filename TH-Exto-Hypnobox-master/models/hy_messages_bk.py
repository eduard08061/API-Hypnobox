from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from . import Base

class HyDimMidia(Base):
    __tablename__ = 'hy_dim_midia'
    
    id =        Column(Integer, primary_key=True)
    midia =     Column(String(255), nullable=False)

    message_midia =     relationship("HyMessage",   back_populates="message_midia")
    chat_midia =        relationship("HyChat",      back_populates="chat_midia")

class HyDimGrupoMidia(Base):
    __tablename__ = 'hy_dim_grupo_midia'
    
    id =                Column(Integer, primary_key=True)
    grupo_midia =       Column(String(255), nullable=False)

    message_grupo_midia =   relationship("HyMessage", back_populates="message_grupo_midia")
    chat_grupo_midia =      relationship("HyChat",      back_populates="chat_grupo_midia")

class HyDimCanal(Base):
    __tablename__ = 'hy_dim_canal'
    
    id =            Column(Integer, primary_key=True,   nullable=False, autoincrement=False)
    NomeCanal =     Column(String(255),                 nullable=False)

    message_canal = relationship("HyMessage",   back_populates="message_canal")
    chat_canal =    relationship("HyChat",      back_populates="chat_canal")

class HyDimSubCanal(Base):
    __tablename__ = 'hy_dim_sub_canal'
    
    id =            Column(Integer, primary_key=True,    nullable=False, autoincrement=False)
    NomeSubCanal =  Column(String(255),                  nullable=False)

    message_sub_canal =     relationship("HyMessage",   back_populates="message_sub_canal")
    chat_sub_canal =        relationship("HyChat",      back_populates="chat_sub_canal")

class HyDimMomento(Base):
    __tablename__ = 'hy_dim_momento'
    
    id =       Column(Integer, primary_key=True,     nullable=False, autoincrement=False)
    NomeMomento =     Column(String(255),                   nullable=False)

    message_momento =   relationship("HyMessage",   back_populates="message_momento")
    chat_momento =      relationship("HyChat",      back_populates="chat_momento")

class HyDimSubMomento(Base):
    __tablename__ = 'hy_dim_sub_momento'
    
    id =                Column(Integer, primary_key=True,  nullable=False, autoincrement=False)
    NomeSubMomento =    Column(String(255),                nullable=False)

    message_sub_momento =   relationship("HyMessage",   back_populates="message_sub_momento")
    chat_sub_momento =      relationship("HyChat",      back_populates="chat_sub_momento")

class HyDimTemperatura(Base):
    __tablename__ = 'hy_dim_temperatura'
    
    id =       Column(Integer, primary_key=True,  nullable=False, autoincrement=False)
    NomeTemperatura =     Column(String(255),                nullable=False)

    message_temperatura =   relationship("HyMessage",     back_populates="message_temperatura")
    chat_temperatura =      relationship("HyChat",      back_populates="chat_temperatura")

class HyMessageBroker(Base):
    __tablename__ = 'hy_message_brooker'
    
    # Identificação/Valores do registro e 
    id =             Column(Integer, primary_key=True,   nullable=False, autoincrement=False)
    NomeCorretorResponsavel =           Column(String(255),                 nullable=False)
    EmailCorretorResponsavel =          Column(String(255),                 nullable=False)

    # Refere-se às mensagens que estão associadas a este corretor.
    messages = relationship("HyMessage", back_populates="message_broker")


class HyMessageManager(Base):
    __tablename__ = 'hy_message_manager'
    
    # Identificação/Valores do registro
    id =             Column(Integer, primary_key=True,    nullable=False, autoincrement=False)
    NomeGerenteCorretorResponsavel =           Column(String(255),                  nullable=False)
    EmailGerenteCorretorResponsavel =          Column(String(255),                  nullable=False)

    # Refere-se às mensagens que estão associadas a este gerente.
    messages = relationship("HyMessage", back_populates="message_manager")

class HyMessageDimStatus(Base):
    __tablename__ = 'hy_message_dim_status'
    
    # Identificação/Valores do registro
    id =                Column(Integer, primary_key=True, autoincrement=True)
    StatusMensagem =    Column(String(255), nullable=False)

    # Refere-se às mensagens que estão associadas a este gerente.
    message_status = relationship("HyMessage", back_populates="message_status")

class HyMessageDimTipo(Base):
    __tablename__ = 'hy_message_dim_tipo'
    
    # Identificação/Valores do registro
    id =                Column(Integer, primary_key=True)
    TipoMensagem =      Column(String(255), nullable=False)

    # Refere-se às mensagens que estão associadas a este gerente.
    message_tipo = relationship("HyMessage", back_populates="message_tipo")

class HyMessage(Base):
    __tablename__ = 'hy_message'

    # Identificação do registro
    id =                    Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    IDCliente =             Column(Integer, nullable=False)

    # Datalhes da mensagem
    ClienteNovo =           Column(Boolean,     nullable=False)
    CNA =                   Column(Boolean,     nullable=False)
    DataAtribuicao =        Column(DateTime,    nullable=True)

    # Mensagem
    Mensagem =              Column(Text, nullable=True)
    Assunto =               Column(Text, nullable=True)
    Datamensagem =          Column(DateTime,    nullable=True)
    #TipoMensagem =          Column(String(255), nullable=True)

    # Campos com chaves estrangeiras
    IDCorretorResponsavel =                 Column(Integer, ForeignKey('hy_message_brooker.id'),            nullable=True)
    IDGerenteCorretorResponsavel =          Column(Integer, ForeignKey('hy_message_manager.id'),            nullable=True)
    IDProduto =                             Column(Integer, ForeignKey('hy_products.CodProduto'),           nullable=True)
    IDCanal =                               Column(Integer, ForeignKey('hy_dim_canal.id'),                  nullable=True)
    IDSubCanal =                            Column(Integer, ForeignKey('hy_dim_sub_canal.id'),              nullable=True)
    IDMomento =                             Column(Integer, ForeignKey('hy_dim_momento.id'),                nullable=True)
    IDSubMomento =                          Column(Integer, ForeignKey('hy_dim_sub_momento.id'),            nullable=True)
    IDMidia =                               Column(Integer, ForeignKey('hy_dim_midia.id'),                  nullable=True)
    IDGrupoMidia =                          Column(Integer, ForeignKey('hy_dim_grupo_midia.id'),            nullable=True)
    IDTemperatura =                         Column(Integer, ForeignKey('hy_dim_temperatura.id'),            nullable=True)
    IDMensageStatus =                       Column(Integer, ForeignKey('hy_message_dim_status.id'),         nullable=True)
    IDTipoMensagem =                        Column(Integer, ForeignKey('hy_message_dim_tipo.id'),           nullable=True)


    # Outros (TO-DO: descobrir com qual campo essa chave se relaciona)
    IDResponsavelCliente =                  Column(Integer,     nullable=True)
    IDResponsavelClienteCompartilhado =     Column(Integer,     nullable=True)

    # Outros campos
    NomeCliente =           Column(String(255), nullable=True)

    # Propriedades da MODEL
    # Propriedades de relacionamento com outras tabelas
    
    # Quando usamos back_populates="messages", estamos dizendo que, na outra ponta do relacionamento (na classe referenciada), há um atributo chamado messages que estabelece a relação inversa.  
    message_broker =                        relationship("HyMessageBroker",                 back_populates="messages") # Refere-se ao gerente do corretor responsável pela mensagem.
    message_manager =                       relationship("HyMessageManager",                back_populates="messages") # Refere-se ao corretor responsável pela mensagem
    message_canal =                         relationship("HyDimCanal",                      back_populates="message_canal")
    message_sub_canal =                     relationship("HyDimSubCanal",                   back_populates="message_sub_canal")
    message_momento =                       relationship("HyDimMomento",                    back_populates="message_momento")
    message_sub_momento =                   relationship("HyDimSubMomento",                 back_populates="message_sub_momento")
    message_temperatura =                   relationship("HyDimTemperatura",                back_populates="message_temperatura")
    message_midia =                         relationship("HyDimMidia",                      back_populates="message_midia")
    message_grupo_midia =                   relationship("HyDimGrupoMidia",                 back_populates="message_grupo_midia")
    message_email =                         relationship("HyMessageEmail",                  back_populates="message_email")
    message_tel =                           relationship("HyMessageTel",                    back_populates="message_tel")
    message_status =                        relationship("HyMessageDimStatus",              back_populates="message_status")
    message_tipo =                          relationship("HyMessageDimTipo",                back_populates="message_tipo")     

class HyMessageTel(Base):
    __tablename__ = 'hy_message_tel'
    
    #id =                        Column(Integer, primary_key=True)
    IDMensagemCliente =         Column(Integer, ForeignKey('hy_message.id'), primary_key=True)
    tel =                       Column(String(50),   nullable=False)
    tel_ddd =                   Column(String(50),   nullable=True)
    tel_type =                  Column(String(20),  nullable=False) # Residencial, Mensagem, Celular

    message_tel = relationship("HyMessage", back_populates="message_tel")

class HyMessageEmail(Base):
    __tablename__ = 'hy_message_email'
    
    #id =                        Column(Integer,         primary_key=True)
    IDMensagemCliente =         Column(Integer, ForeignKey('hy_message.id'), primary_key=True)
    email =                     Column(String(255),     nullable=False)
    email_number =              Column(Integer,         nullable=False) # 1, 2 ou 3

    message_email = relationship("HyMessage", back_populates="message_email")


# Informações úteis para consulta
""" 
cascade="all, delete-orphan": 
Isso significa que todas as operações (save, update, delete, merge, etc.) 
serão propagadas, e quaisquer registros órfãos serão excluídos automaticamente.

 """
