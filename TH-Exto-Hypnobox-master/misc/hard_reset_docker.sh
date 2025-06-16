#!/bin/bash

# Definição de variáveis para os nomes dos containers e volumes
CONTAINER_PYTHON="th-exto-hypnobox-python-1"
CONTAINER_DB="th-exto-hypnobox-db-1"
VOLUME_DB="th-exto-hypnobox_data"
VOLUME_LOG="th-exto-hypnobox_log-volume"

pwd
echo "Executing a hard reset ..."

# Destruição de toda a rede docker
echo "Listing running containers:"
docker ps &&

echo "Stopping running Docker containers..."
docker stop $CONTAINER_PYTHON $CONTAINER_DB &&
echo "Containers stopped successfully." &&

echo "Deleting containers..."
docker rm $CONTAINER_PYTHON $CONTAINER_DB &&
echo "Containers deleted successfully."

echo "Continue to delete the volumes? (y/n)"
read resposta
if [[ "$resposta" == "y" ]]; then

    echo "Listing volume to be deleted:"
    docker volume inspect $VOLUME_DB &&
    echo "Deleting volume..."
    docker volume rm $VOLUME_DB && $VOLUME_LOG
    echo "Volume deleted successfully."

else
    echo "Process terminated by user."
fi

echo "Current Docker status:" &&

echo "Active containers:"
docker ps &&

echo "Active volumes:"
docker volume list &&

echo "All tasks completed. Would you like to rebuild the Docker network for this project? (y/n)"
read resposta

if [[ "$resposta" == "y" ]]; then
    echo "Rebuilding the Docker network..."
    # Recriação da rede docker
    docker-compose build && 
    docker-compose up -d &&
    echo "Docker network rebuilt successfully. Listing active containers and volumes:"
    docker ps &&
    docker volume list &&
    docker volume inspect $VOLUME_DB
else
    echo "Rebuild canceled by user."
fi

echo "All tasks completed. Would you like RUN MIGRATIONS? (y/n)"
read resposta

if [[ "$resposta" == "y" ]]; then

# Rodar as migração inicial
echo "Running migrations..."
alembic upgrade head


else
    echo "Rebuild canceled by user."
fi

# Os comandos para acessar logs estão comentados, mas disponíveis se necessário
# Acessar logs do container Python
#docker logs -f $CONTAINER_PYTHON

# Acessar logs do container DB
#docker logs -f $CONTAINER_DB
