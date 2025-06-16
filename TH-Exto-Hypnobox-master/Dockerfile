FROM python:3

# Instale o dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN apt-get update && apt-get install -y wget cron nano vim  \
    && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && apt-get clean

WORKDIR /app

# Copiando e instalando as dependências
COPY requirements.txt .
RUN apt-get update
RUN pip install --no-cache-dir -r requirements.txt

# Adicionar e configurar o crontab
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

# Criar o arquivo de log do cron
RUN touch /var/log/cron-TH-Exto-Hypnobox.log

# Comando para rodar o cron e o aplicativo Python
CMD cron && tail -f /var/log/cron-TH-Exto-Hypnobox.log