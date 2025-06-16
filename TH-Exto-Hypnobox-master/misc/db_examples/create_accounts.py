from datetime import datetime
from app import create_app, db
from models import Account
from functions.general import generate_token

app = create_app()

def create_account(company_name, cnpj, domain, uf, city, state, phone, customer_since, segment, company_size):
    """Função para criar uma conta de cliente."""
    with app.app_context():
        access_token = generate_token()
        registration_date = datetime.now()
        
        new_account = Account(
            company_name=company_name,
            cnpj=cnpj,
            access_token=access_token,
            domain=domain,
            uf=uf,
            city=city,
            state=state,
            phone=phone,
            customer_since=datetime.strptime(customer_since, '%d/%m/%Y').date(),
            registration_date=registration_date,
            segment=segment,
            company_size=company_size
        )
        
        db.session.add(new_account)
        try:
            db.session.commit()
            print("Conta criada com sucesso:", new_account)
        except Exception as e:
            db.session.rollback()
            print("Erro ao criar conta:", e)

if __name__ == '__main__':

    create_account(
        company_name="Penso Tecnologia",
        cnpj="11.319.574/0001-43",
        domain="www.penso.com.br",
        uf="SP",
        city="São Paulo",
        state="São Paulo",
        phone="(11) 3515-1818",
        customer_since="02/01/2023",
        segment="Tecnologia",
        company_size="200 - 300 funcionários"
    )
