from functions.hypnobox.clients import update_clients

# Configurações que definem para coleta dos dados
# Formato: YYYY-MM-DD HH:MM:SS

data_inicio = "2017-01-01 00:00:00"
data_atualizacao_inicio = "2017-01-15 00:00:00"
data_atualizacao_final = "2017-01-31 00:00:00"
delta = 1

# Chama a função de atualização
update_clients(data_inicio, data_atualizacao_inicio, data_atualizacao_final, delta)
