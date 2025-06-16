#!/bin/bash

# Caminho do diretório raiz onde a busca deve começar.
# Use o ponto para indicar o diretório atual ou especifique um caminho absoluto.
ROOT_DIR="."

# Encontra todos os diretórios chamados __pycache__ a partir do diretório raiz especificado
# e remove cada um deles recursivamente.
find "$ROOT_DIR" -type d -name "__pycache__" -exec rm -rf {} +

echo "Todos os diretórios __pycache__ foram removidos."
