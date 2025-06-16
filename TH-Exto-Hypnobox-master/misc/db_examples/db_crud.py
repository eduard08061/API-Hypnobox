from sqlalchemy.orm import Session
from functions.db_config import SessionLocal
from models.models import UserModel
from datetime import datetime

# Função para adicionar um único
def create_user(db: Session, first_name: str, last_name: str, birth: datetime):
    new_user = UserModel(first_name=first_name, last_name=last_name, birth=birth)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Função para obter um usuário pelo ID
def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

# Função para obter todos os usuários
def get_all_users(db: Session):
    return db.query(UserModel).all()


# Função para adicionar múltiplos usuários em uma única sessão
def add_users_in_bulk(users_data):
    # Inicia uma sessão
    db: Session = SessionLocal()

    try:
        for user_data in users_data:
            create_user(db, user_data['first_name'], user_data['last_name'], user_data['birth'])
        
        # Commita todas as transações
        db.commit()

    except Exception as e:
        # Faz rollback se ocorrer algum erro
        db.rollback()
        print(f"Erro ao adicionar usuários: {e}")

    finally:
        # Fecha a sessão
        db.close()