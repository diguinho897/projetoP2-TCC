import pytest
from pathlib import Path
from src.lexer.lexer import DSLexer

def test_parser_valid_commands():
    lexer = DSLexer()
    
    # Testa cada comando individualmente
    valid_commands = [
        'configurarBanco "localhost" "banco_teste"',
        'iniciarServidor "localhost" porta=8080',
        'executarTeste "testes_unitarios"',
        'deployEmAmbiente "producao"'
    ]
    
    for cmd in valid_commands:
        tree = lexer.parse(cmd)
        assert tree is not None
        assert len(tree.children) == 1

def test_parser_invalid_commands():
    lexer = DSLexer()
    
    # Testa comandos inválidos
    invalid_commands = [
        'configurarBanco',  # Falta argumentos
        'iniciarServidor "localhost"',  # Falta porta
        'executarTeste',  # Falta argumento
        'deployEmAmbiente',  # Falta argumento
        'comandoInvalido "arg"',  # Comando não existe
    ]
    
    for cmd in invalid_commands:
        with pytest.raises(Exception):
            lexer.parse(cmd)

def test_parser_multiple_commands():
    lexer = DSLexer()
    
    # Testa múltiplos comandos em sequência
    script = """
    configurarBanco "localhost" "banco_teste"
    iniciarServidor "localhost" porta=8080
    executarTeste "testes_unitarios"
    deployEmAmbiente "producao"
    """
    
    tree = lexer.parse(script)
    assert tree is not None
    assert len(tree.children) == 4 