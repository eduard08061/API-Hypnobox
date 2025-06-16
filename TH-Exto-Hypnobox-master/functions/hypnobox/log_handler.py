from datetime import datetime
from sqlalchemy.orm import Session
from models.log import JobLog
from functions.db_config import SessionLocal

def log_job_start(job_name, data_inicio, data_atualizacao_inicio, data_atualizacao_final, endpoint):
    db: Session = SessionLocal()
    job_log = JobLog(
        job_name=job_name,
        data_inicio=data_inicio,
        data_atualizacao_inicio=data_atualizacao_inicio,
        data_atualizacao_final=data_atualizacao_final,
        endpoint=endpoint
    )
    db.add(job_log)
    db.commit()
    db.refresh(job_log)
    db.close()
    return job_log.id

def log_job_end(job_id, num_records, unique_emails, unique_phones, status, error_message=None):
    db: Session = SessionLocal()
    job_log = db.query(JobLog).get(job_id)
    job_log.end_time = datetime.now()
    job_log.duration = (job_log.end_time - job_log.start_time).total_seconds() / 60 # Converte para minutos
    job_log.num_records = num_records
    job_log.unique_emails = unique_emails
    job_log.unique_phones = unique_phones
    job_log.status = status
    job_log.error_message = error_message
    db.commit()
    db.close()
