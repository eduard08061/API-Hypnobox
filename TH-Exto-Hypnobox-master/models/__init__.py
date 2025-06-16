from sqlalchemy.orm import declarative_base
Base = declarative_base()

# Importa todas as models para que Alembic possa detectá-las
#from .hy_client import *
from .hy_products import *
from .hy_messages import *
from .hy_chat import *
from .hy_users import *
from .log import JobLog
from .hy_client_v2 import *
from .hy_dimensions import *