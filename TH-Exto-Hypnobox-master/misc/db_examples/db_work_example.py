from sqlalchemy.orm import Session
from functions.db_config import SessionLocal, engine
from models.models import Base, UserModel
from misc.db_examples.db_crud import create_user, get_user, get_all_users
from datetime import datetime

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Função principal
def main():
    # Inicia uma sessão
    db: Session = SessionLocal()

    # Adiciona um novo usuário
    new_user = create_user(db, "Susanna", "Bresciani", datetime(1990, 1, 1))
    print(f"Usuário criado: {new_user.first_name} {new_user.last_name}")

    # Consulta um usuário pelo ID
    user = get_user(db, new_user.id)
    if user:
        print(f"Usuário consultado: {user.first_name} {user.last_name}")

    # Consulta todos os usuários
    users = get_all_users(db)
    print("Todos os usuários:")
    for user in users:
        print(f"{user.first_name} {user.last_name}")

    # Fecha a sessão
    db.close()

if __name__ == "__main__":
    main()
