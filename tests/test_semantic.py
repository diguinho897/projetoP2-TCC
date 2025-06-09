import pytest
from src.lexer.lexer import DSLexer
from src.semantic.analyzer import SemanticAnalyzer, SemanticError, CommandType

def test_valid_command_sequence():
    lexer = DSLexer()
    analyzer = SemanticAnalyzer()
    
    # Sequência válida de comandos
    script = """
    configurarBanco "localhost" "banco_teste"
    iniciarServidor "localhost" porta=8080
    executarTeste "testes_unitarios"
    deployEmAmbiente "producao"
    """
    
    ast = lexer.parse(script)
    commands = analyzer.analyze(ast)
    
    assert len(commands) == 4
    assert commands[0].type == CommandType.CONFIGURAR_BANCO
    assert commands[1].type == CommandType.INICIAR_SERVIDOR
    assert commands[2].type == CommandType.EXECUTAR_TESTE
    assert commands[3].type == CommandType.DEPLOY_AMBIENTE

def test_invalid_command_sequence():
    lexer = DSLexer()
    analyzer = SemanticAnalyzer()
    
    # Sequência inválida: tenta executar testes antes de iniciar o servidor
    script = """
    configurarBanco "localhost" "banco_teste"
    executarTeste "testes_unitarios"
    iniciarServidor "localhost" porta=8080
    deployEmAmbiente "producao"
    """
    
    ast = lexer.parse(script)
    with pytest.raises(SemanticError) as exc_info:
        analyzer.analyze(ast)
    
    assert "Servidor deve ser iniciado antes de executar testes" in str(exc_info.value)

def test_invalid_deploy_sequence():
    lexer = DSLexer()
    analyzer = SemanticAnalyzer()
    
    # Sequência inválida: tenta fazer deploy sem executar testes
    script = """
    configurarBanco "localhost" "banco_teste"
    iniciarServidor "localhost" porta=8080
    deployEmAmbiente "producao"
    """
    
    ast = lexer.parse(script)
    with pytest.raises(SemanticError) as exc_info:
        analyzer.analyze(ast)
    
    assert "Testes devem ser executados antes do deploy" in str(exc_info.value) 