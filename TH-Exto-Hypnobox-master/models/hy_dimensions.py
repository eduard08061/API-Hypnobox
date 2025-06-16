from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from . import Base

#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class HyDimMoment(Base):
    __tablename__ = 'hy_dMoments'

    id =        Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =   Column(Integer, nullable=True) #Externo
    Moment =    Column(String(255), nullable=True)

    message_momento =   relationship("HyMessage",   back_populates="message_momento")
    chat_momento =      relationship("HyChat",      back_populates="chat_momento")


class HyDimSubMoment(Base):
    __tablename__ = 'hy_dSubMoments'

    id =            Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =       Column(Integer, nullable=True) #Externo
    SubMoment =     Column(String(255), nullable=True)

    message_sub_momento =   relationship("HyMessage",   back_populates="message_sub_momento")
    chat_sub_momento =      relationship("HyChat",      back_populates="chat_sub_momento")

class HyDimTemperature(Base):
    __tablename__ = 'hy_dTemperatures'

    id =            Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =       Column(Integer, nullable=True) #Externo
    Temperature =   Column(String(255), nullable=True)

    message_temperatura =   relationship("HyMessage",     back_populates="message_temperatura")
    chat_temperatura =      relationship("HyChat",      back_populates="chat_temperatura")

class HyDimProduct(Base):
    __tablename__ = 'hy_dProducts'

    id =                Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =           Column(Integer, nullable=True) #Externo
    Product =           Column(String(255), nullable=True)

class HyDimChannel(Base):
    __tablename__ = 'hy_dChannels'

    id =                Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =           Column(Integer, nullable=True) #Externo
    Channel =           Column(String(255), nullable=True)

    message_canal = relationship("HyMessage",   back_populates="message_canal")
    chat_canal =    relationship("HyChat",      back_populates="chat_canal")

class HyDimSubChannel(Base):
    __tablename__ = 'hy_dSubChannels'

    id =                Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =           Column(Integer, nullable=True) #Externo
    SubChannel =           Column(String(255), nullable=True)

    message_sub_canal =     relationship("HyMessage",   back_populates="message_sub_canal")
    chat_sub_canal =        relationship("HyChat",      back_populates="chat_sub_canal")

class HyDimMedia(Base):
    __tablename__ = 'hy_dMedias'

    id =        Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =   Column(Integer, nullable=True) #Externo
    Media =     Column(String(255), nullable=True)

    message_midia =     relationship("HyMessage",   back_populates="message_midia")
    chat_midia =        relationship("HyChat",      back_populates="chat_midia")

class HyDimMediaGroup(Base):
    __tablename__ = 'hy_dMediaGroups'

    id =            Column(Integer, primary_key=True, nullable=False, autoincrement=True) # Interno (gerado pelo TH)
    idHyCRM =       Column(Integer, nullable=True) #Externo
    MediaGroup =    Column(String(255), nullable=True)

    message_grupo_midia =   relationship("HyMessage",   back_populates="message_grupo_midia")
    chat_grupo_midia =      relationship("HyChat",      back_populates="chat_grupo_midia")


