from functions.hypnobox.messages import update_messages

# Configurações que definem para coleta dos dados

# Data para amostragem de dados
start_time =    "2018-01-05 00:00:00"  # Formato: YYYY-MM-DD HH:MM:SS
end_time =      "2018-03-07 00:00:00"    # Formato: YYYY-MM-DD HH:MM:SS

# Datas originais
#start_time = "2018-03-05 00:00:00"
#end_time = "2018-03-06 00:00:00"
delta = 10

# Chama a função de atualização
update_messages(start_time, end_time, delta)
