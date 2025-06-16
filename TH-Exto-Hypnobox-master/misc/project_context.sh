#!/bin/bash

# Define o diretório de trabalho (um nível acima de 'for_gpt')
cd ..

# Define o arquivo de saída dentro da pasta 'for_gpt'
output_file="misc/gpt_context.txt"

# Limpa ou cria o arquivo de saída
echo "" > $output_file

# Função para adicionar arquivos ao arquivo de saída
function add_file() {
    echo "----- $(realpath --relative-to=. $1) -----" >> $output_file
    cat $1 >> $output_file
    echo "" >> $output_file
}

# Exporta a função para que esteja disponível para o 'find'
export -f add_file

# Exporta o nome do arquivo de saída para que esteja disponível para o 'find'
export output_file

# Encontra arquivos de várias extensões especificadas, exceto nas pastas 'for_gpt' e 'docs'
find . -type f \( -name "*.py" -o -name "*.env" -o -name "Dockerfile" -o -name "*.yml" -o -name "*.ini" -o -name "*.txt" -o -name "*.mako" \) ! -path "./misc/*" ! -path "./docs/*" ! -path "./.github/*" -exec bash -c 'add_file "$0"' {} \;
#find . -type f \( -name "*.py" -o -name "*.env" -o -name "Dockerfile" -o -name "*.yml" -o -name "*.ini" -o -name "*.txt" -o -name "*.mako" -o -name "*.json" \) -exec bash -c 'add_file "$0"' {} \;

# Adiciona a saída do comando 'tree' ao final do arquivo de saída, excluindo 'for_gpt'
echo "----- ESTRUTURA DE DIRETÓRIOS -----" >> $output_file
tree --noreport --charset=ascii | grep -v "for_gpt" >> $output_file

echo "Arquivo combinado criado com sucesso: $output_file"
