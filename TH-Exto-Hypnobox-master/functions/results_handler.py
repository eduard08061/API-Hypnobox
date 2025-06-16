from datetime import datetime

def hy_count_values(response_data):
    
    data = response_data['Clientes']

    num_client = len(data)
    unique_emails = set()
    unique_phones = set()

    for cliente in data:
        if cliente['Email']:
            unique_emails.add(cliente['Email'])
        if cliente.get('Email2'):
            unique_emails.add(cliente['Email2'])
        if cliente.get('Email3'):
            unique_emails.add(cliente['Email3'])

        phone_types = ['TelResidencial', 'TelCelular', 'TelComercial', 'TelOutro']
        ddd_types = ['DddResidencial', 'DddCelular', 'DddComercial', 'DddOutro']

        for phone_type, ddd_type in zip(phone_types, ddd_types):
            if cliente.get(phone_type) and cliente.get(ddd_type):
                phone = f"({cliente[ddd_type]}) {cliente[phone_type]}"
                unique_phones.add(phone)

    return len(unique_emails), len(unique_phones)

def hy_debug_clients(data):
    oldest_lead = None
    newest_lead = None
    oldest_date = datetime.max
    newest_date = datetime.min

    # Iterar sobre cada cliente
    for cliente in data:
        # Converte DataUltimaInteracao em objeto datetime
        interaction_date = datetime.strptime(cliente['DataUltimaInteracao'], '%Y-%m-%d %H:%M:%S')

        # Verifica se a data atual é mais antiga que a mais antiga já encontrada
        if interaction_date < oldest_date:
            oldest_date = interaction_date
            oldest_lead = cliente

        # Verifica se a data atual é mais nova que a mais nova já encontrada
        if interaction_date > newest_date:
            newest_date = interaction_date
            newest_lead = cliente

    if oldest_lead and newest_lead:
        print(f'Lead mais antigo:   CodCliente: {oldest_lead["CodCliente"]}   {oldest_lead["DataUltimaInteracao"]}      {oldest_lead["Nome"]}')
        print(f'Lead mais novo:     CodCliente: {newest_lead["CodCliente"]}   {newest_lead["DataUltimaInteracao"]}      {newest_lead["Nome"]}')
        print(f'\n')
    else:
        print('Não foi possível determinar leads mais antigos ou mais novos.')