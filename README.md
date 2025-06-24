# DSL para Automação de Ambiente de Desenvolvimento

Uma linguagem de domínio específico (DSL) para automação de ambientes de desenvolvimento, implementada em Python usando PLY.

## Requisitos

- Python 3.8+
- pip
- Pop!_OS (ou outra distribuição Linux baseada em Ubuntu)

## Instalação

### Instalação Manual

1. Clone o repositório:
```bash
git clone https://github.com/diguinho897/projetoP2-TCC.git
cd dsl-automacao
```

2. Execute o script de instalação:
```bash
chmod +x install.sh
./install.sh
```

### Instalação como Serviço

1. Clone o repositório:
```bash
git clone https://github.com/diguinho897/projetoP2-TCC.git
cd projetoP2-TCC
```

2. Execute o script de instalação do serviço:
```bash
chmod +x install_service.sh
sudo ./install_service.sh
```

## Uso

### Executando Scripts DSL

```bash
python src/run_dsl.py examples/test.dsl
```

### Comandos Disponíveis

1. Configurar Banco de Dados:
```
configurarBanco "host" "nome_do_banco" "senha"
```

2. Iniciar Servidor:
```
iniciar_servidor "tipo" "arquivo" "porta"
```

3. Executar Testes:
```
executar_teste "framework" "diretorio"
```

4. Deploy em Ambiente:
```
deploy_ambiente "ambiente" "branch" "repositorio"
```

### Logs

Os logs de execução são armazenados em `logs/dsl_execution.log`.

### Serviço Systemd

Se instalado como serviço, você pode:

- Verificar status:
```bash
systemctl status dsl@$USER
```

- Ver logs:
```bash
journalctl -u dsl@$USER
```

## Desenvolvimento

### Estrutura do Projeto

```
.
├── src/
│   ├── lexer/
│   │   └── lexer.py
│   ├── parser/
│   │   └── parser.py
│   ├── vm/
│   │   └── interpreter.py
│   └── run_dsl.py
├── examples/
│   └── test.dsl
├── tests/
│   └── test_*.py
├── requirements.txt
├── install.sh
├── install_service.sh
└── dsl.service
```

### Executando Testes

```bash
pytest
```

## Licença

MIT 
