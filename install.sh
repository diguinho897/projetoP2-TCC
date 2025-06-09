#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Instalando DSL para Automação de Ambiente de Desenvolvimento...${NC}"

# Verifica se o Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 não encontrado. Instalando...${NC}"
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

# Verifica se o pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 não encontrado. Instalando...${NC}"
    sudo apt install -y python3-pip
fi

# Cria ambiente virtual
echo -e "${YELLOW}Criando ambiente virtual...${NC}"
python3 -m venv venv

# Ativa o ambiente virtual
echo -e "${YELLOW}Ativando ambiente virtual...${NC}"
source venv/bin/activate

# Instala dependências
echo -e "${YELLOW}Instalando dependências...${NC}"
pip install -r requirements.txt

# Cria diretório de logs
echo -e "${YELLOW}Criando diretório de logs...${NC}"
mkdir -p logs

# Cria link simbólico para o executável
echo -e "${YELLOW}Criando link simbólico...${NC}"
sudo ln -sf "$(pwd)/src/run_dsl.py" /usr/local/bin/dsl

# Dá permissão de execução
chmod +x src/run_dsl.py

echo -e "${GREEN}Instalação concluída!${NC}"
echo -e "Para usar o DSL, execute: ${YELLOW}dsl seu_script.dsl${NC}" 