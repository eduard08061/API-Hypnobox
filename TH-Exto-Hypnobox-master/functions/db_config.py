from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
load_dotenv()

if os.getenv('RUNNING_IN_DOCKER') == 'true':
    DATABASE_URL = os.getenv('DATABASE_URL')
else:
    DATABASE_URL = os.getenv('DATABASE_URL_LOCAL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)