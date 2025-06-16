from sqlalchemy.orm import Session
from functions.db_config import SessionLocal, engine
from models.models import Base, UserModel
from misc.db_examples.db_crud import get_all_users, add_users_in_bulk
from datetime import datetime



def main():
    # Dados de exemplo dos usuários
    users_data = [
        {"first_name": "Rafael", "last_name": " Furquim", "birth": datetime(1989, 5, 30)},
        {"first_name": "Gabriel", "last_name": " Nogueira", "birth": datetime(1985, 5, 15)},
    ]

    # Adiciona múltiplos usuários
    add_users_in_bulk(users_data)

    # Inicia uma nova sessão para consultas
    db: Session = SessionLocal()

    # Consulta todos os usuários
    users = get_all_users(db)
    print("Todos os usuários:")
    for user in users:
        print(f"{user.first_name} {user.last_name}")

    # Fecha a sessão
    db.close()

if __name__ == "__main__":
    main()
