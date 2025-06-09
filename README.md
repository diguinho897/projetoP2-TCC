# DSL para Automação de Ambiente de Desenvolvimento

Este projeto implementa uma Linguagem de Domínio Específico (DSL) para automação de ambientes de desenvolvimento.

## Estrutura do Projeto

```
.
├── src/
│   ├── lexer/         # Implementação do analisador léxico
│   ├── parser/        # Implementação do parser
│   ├── semantic/      # Analisador semântico
│   └── vm/           # Máquina virtual para execução
├── tests/            # Testes unitários e de integração
├── examples/         # Exemplos de scripts
└── grammar/         # Definição da gramática
```

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Exemplo de script:
```
configurarBanco "localhost" "banco_teste"
iniciarServidor "localhost" porta=8080
executarTeste "testes_unitarios"
deployEmAmbiente "producao"
```

## Desenvolvimento

- `black` para formatação de código
- `mypy` para verificação de tipos
- `pytest` para testes

## Licença

MIT 