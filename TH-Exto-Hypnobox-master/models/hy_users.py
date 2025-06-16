from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from . import Base

#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class HyUser(Base): 
    __tablename__ = 'hy_users'
    
    id =                    Column(Integer,     primary_key=True,   nullable=False, autoincrement=False)
    Email =                 Column(String(255), nullable=False)
    Creci =                 Column(String(255), nullable=True)
    CreciType =             Column(String(255), nullable=True)
    CreciValidity =         Column(String(255), nullable=True)
    CPF =                   Column(String(255), nullable=True)
    
    IdProfile =             Column(Integer,   nullable=True)
    IdManager =             Column(Integer,   nullable=True)
    IdManager1 =            Column(Integer,   nullable=True)
    IdManager2 =            Column(Integer,   nullable=True)
    IdManager3 =            Column(Integer,   nullable=True)
    IdManager4 =            Column(Integer,   nullable=True)
    IdManager5 =            Column(Integer,   nullable=True)
    IdManager6 =            Column(Integer,   nullable=True)
    
    Name =                  Column(String(255), nullable=True)
    NickName =              Column(String(255), nullable=True)
    Phone =                 Column(String(255), nullable=True)
    Photo =                 Column(String(255), nullable=True)

    
    Active =                Column(Boolean,     nullable=True)
    LegacyUserId =          Column(Integer,     nullable=True)
    DescriptionStatus =     Column(String(255), nullable=True)
    
    DateRegister =          Column(DateTime,    nullable=True)
    DateUpdate =            Column(DateTime,    nullable=True)
    DateBirth =             Column(DateTime,    nullable=True)
    DateAdmission =         Column(DateTime,    nullable=True)
    DateLastEvaluation =    Column(DateTime,    nullable=True)

    Gender =                Column(String(255), nullable=True)
    AverageRating =         Column(String(255), nullable=True)