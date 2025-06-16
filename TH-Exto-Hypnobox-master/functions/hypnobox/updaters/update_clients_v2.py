from functions.hypnobox.clients_v2 import update

# Configurações que definem para coleta dos dados
# Formato: YYYY-MM-DD HH:MM:SS


data_atualizacao_inicio =   "2018-01-07 00:00:00"
data_atualizacao_final =    "2018-01-08 00:00:00"
delta = 30


# Chama a função de atualização
update(data_atualizacao_inicio, data_atualizacao_final, delta)