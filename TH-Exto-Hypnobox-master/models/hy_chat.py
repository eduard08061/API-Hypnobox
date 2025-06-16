from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from . import Base

#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class HyChatdUser(Base):
    __tablename__ = 'hy_ch_dUsers'
    
    id =        Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    idHyCRM =   Column(Integer,     nullable=True) #Externo
    Name =      Column(String(255), nullable=True)
    Email =     Column(String(255), nullable=True)


class HyChatDimRating(Base):  
    __tablename__ = 'hy_ch_dRating'
    
    id =                Column(Integer, primary_key=True,   nullable=True, autoincrement=True)
    Rating =            Column(String(255),                 nullable=True)

    chat_rating = relationship("HyChat", back_populates="chat_rating")

class HyChat(Base): 
    __tablename__ = 'hy_ch_fChat'

    id =                        Column(Integer, primary_key=True, nullable=False, autoincrement=False) #id_chat

    ClientName =                Column(String(255), nullable=True) 
    ClientEmail =               Column(String(255), nullable=True) 
    ClientPhone =               Column(String(255), nullable=True) 
    ClientIP =                  Column(String(50),  nullable=True) 

    ChatType =                  Column(Integer,     nullable=False)  
    ActiveClient =              Column(Boolean,     nullable=True)
    NewClient =                 Column(Boolean,     nullable=True)  

    StartTimeDate =             Column(DateTime,    nullable=True) 
    EndTimeDate =               Column(DateTime,    nullable=True)

    RatingComment =             Column(Text,       nullable=True) 

    IdBroker_responsible =      Column(Integer, ForeignKey('hy_ch_dUsers.id'),  nullable=True) 
    IdBroker_attendant =        Column(Integer, ForeignKey('hy_ch_dUsers.id'),  nullable=True) 
    IdBroker_forwarded =        Column(Integer, ForeignKey('hy_ch_dUsers.id'),  nullable=True) 
    IdManager_responsible =     Column(Integer, ForeignKey('hy_ch_dUsers.id'),  nullable=True) 
    
    # Chave estrangeira removida até que API de clientes seja implementada (erro de "REFERENCES")
    #IdClient =                  Column(Integer, ForeignKey('hy_clients.CodCliente'),            nullable=True)
    IdClient =                  Column(Integer, nullable=True)


    IdRating =                  Column(Integer, ForeignKey('hy_ch_dRating.id'),                nullable=True) 
    #IdRating_comment =         Column(Integer, ForeignKey('hy_chat_rating_comment.id'),        nullable=True) 
    #IdChat_conversation =      Column(Integer, ForeignKey('hy_chat_conversation.id'),          nullable=True) 
    IdProduct =                 Column(Integer, ForeignKey('hy_dProducts.id'),           nullable=True)  
    IdChannel =                 Column(Integer, ForeignKey('hy_dChannels.id'),                  nullable=True) 
    IdSubChannel =              Column(Integer, ForeignKey('hy_dSubChannels.id'),               nullable=True) 
    IdMoment =                  Column(Integer, ForeignKey('hy_dMoments.id'),                   nullable=True) 
    IdSubMoment =               Column(Integer, ForeignKey('hy_dSubMoments.id'),                nullable=True) 
    IdMedium =                  Column(Integer, ForeignKey('hy_dMedias.id'),                  nullable=True) 
    IdMediumGroup =             Column(Integer, ForeignKey('hy_dMediaGroups.id'),            nullable=True) 
    Idtemperature =             Column(Integer, ForeignKey('hy_dTemperatures.id'),            nullable=True) 

    Broker_responsible =      relationship("HyChatdUser",       foreign_keys=[IdBroker_responsible])
    Broker_attendant =        relationship("HyChatdUser",       foreign_keys=[IdBroker_attendant])
    Broker_forwarded =        relationship("HyChatdUser",       foreign_keys=[IdBroker_forwarded])
    Manager_responsible =     relationship("HyChatdUser",       foreign_keys=[IdManager_responsible])

    #chat_broker_responsible =       relationship("HyChatBrokerResponsible",         back_populates="chat_broker_responsible")  
    #chat_broker_attendant =         relationship("HyChatBrokerAttendant",           back_populates="chat_broker_attendant") 
    #chat_broker_forwarded =         relationship("HyChatBrokerForwarded",           back_populates="chat_broker_forwarded") 
    #chat_manager_responsible =      relationship("HyChatManagerResponsible",        back_populates="chat_manager_responsible") 

    chat_rating =                   relationship("HyChatDimRating",                 back_populates="chat_rating") 
    chat_conversation =             relationship("HyChatConversation",              back_populates="chat_conversation") 

    chat_canal =                    relationship("HyDimChannel",                      back_populates="chat_canal") 
    chat_sub_canal =                relationship("HyDimSubChannel",                   back_populates="chat_sub_canal") 
    chat_momento =                  relationship("HyDimMoment",                    back_populates="chat_momento") 
    chat_sub_momento =              relationship("HyDimSubMoment",                 back_populates="chat_sub_momento") 
    chat_temperatura =              relationship("HyDimTemperature",                back_populates="chat_temperatura") 
    chat_midia =                    relationship("HyDimMedia",                      back_populates="chat_midia") 
    chat_grupo_midia =              relationship("HyDimMediaGroup",                 back_populates="chat_grupo_midia") 


class HyChatConversation(Base): 
    __tablename__ = 'hy_ch_dConversation'
    
    id =                    Column(Integer, primary_key=True, nullable=False, autoincrement=True) 
    id_chat =               Column(Integer, ForeignKey('hy_ch_fChat.id'), nullable=False)    

    Sender =                Column(Integer, nullable=True)
    message =               Column(Text, nullable=True)
    UsersOnly =             Column(Text, nullable=True)
    User =                  Column(Text, nullable=True)
    SubmissionDate =        Column(Text, nullable=True)

    chat_conversation = relationship("HyChat", back_populates="chat_conversation")

