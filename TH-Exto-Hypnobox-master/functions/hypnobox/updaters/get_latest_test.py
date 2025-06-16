
from functions.db_config import SessionLocal
from functions.hypnobox.auth import hy_url, hy_token
from sqlalchemy.orm import Session
from functions.hypnobox.log_handler import log_job_start, log_job_end
from functions.general import str_to_datetime, logging_config, timestamp_now_ddmmaa
import json, requests
from models.hy_messages import *

db: Session = SessionLocal()

def get_latest_interaction_date(db: Session):
    latest_date = db.query(HyMessage).order_by(HyMessage.Datamensagem.desc()).first()
    if latest_date:
        return latest_date.Datamensagem
    return None

call = get_latest_interaction_date(db)
print(call)