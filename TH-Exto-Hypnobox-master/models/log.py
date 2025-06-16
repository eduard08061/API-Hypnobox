from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from . import Base
from datetime import datetime

class JobLog(Base):
    __tablename__ = 'job_logs'

    id = Column(Integer, primary_key=True)
    job_name = Column(String(255), nullable=False, default="update clients")
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)
    num_records = Column(Integer, nullable=True)
    unique_emails = Column(Integer, nullable=True)
    unique_phones = Column(Integer, nullable=True)
    status = Column(String(50), nullable=True)
    error_message = Column(Text, nullable=True)
    param_data_inicio = Column(String(50), nullable=True)
    param_data_atualizacao_inicio = Column(String(50), nullable=True)
    param_data_atualizacao_final = Column(String(50), nullable=True)
    endpoint = Column(String(255), nullable=True)

    def __init__(self, job_name, data_inicio, data_atualizacao_inicio, data_atualizacao_final, endpoint):
        self.job_name = job_name
        self.param_data_inicio = data_inicio
        self.param_data_atualizacao_inicio = data_atualizacao_inicio
        self.param_data_atualizacao_final = data_atualizacao_final
        self.endpoint = endpoint
