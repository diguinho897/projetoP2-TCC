#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Instalando serviço DSL...${NC}"

# Verifica se está rodando como root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Por favor, execute como root${NC}"
    exit 1
fi

# Cria diretório de instalação
mkdir -p /opt/dsl

# Copia arquivos
cp -r src /opt/dsl/
cp requirements.txt /opt/dsl/
cp install.sh /opt/dsl/

# Instala dependências
cd /opt/dsl
./install.sh

# Instala serviço
cp dsl.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable dsl@$SUDO_USER
systemctl start dsl@$SUDO_USER

echo -e "${GREEN}Serviço DSL instalado com sucesso!${NC}"
echo "Para verificar o status: systemctl status dsl@$SUDO_USER"
echo "Para ver os logs: journalctl -u dsl@$SUDO_USER" 