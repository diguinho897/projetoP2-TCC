import pytest
from src.lexer.lexer import DSLexer
from src.semantic.analyzer import SemanticAnalyzer, CommandType, Command
from src.vm.virtual_machine import VirtualMachine

def test_vm_execution():
    lexer = DSLexer()
    analyzer = SemanticAnalyzer()
    vm = VirtualMachine()
    
    # Script válido
    script = """
    configurarBanco "localhost" "banco_teste"
    iniciarServidor "localhost" porta=8080
    executarTeste "testes_unitarios"
    deployEmAmbiente "producao"
    """
    
    # Parse e análise semântica
    ast = lexer.parse(script)
    commands = analyzer.analyze(ast)
    
    # Execução na VM
    vm.execute(commands)
    
    # Verifica se o ambiente foi configurado
    assert vm.environment is not None

def test_vm_command_execution():
    vm = VirtualMachine()
    
    # Testa cada comando individualmente
    commands = [
        Command(CommandType.CONFIGURAR_BANCO, {"host": "localhost", "banco": "teste"}),
        Command(CommandType.INICIAR_SERVIDOR, {"host": "localhost", "porta": 8080}),
        Command(CommandType.EXECUTAR_TESTE, {"path": "testes"}),
        Command(CommandType.DEPLOY_AMBIENTE, {"ambiente": "producao"})
    ]
    
    # Executa os comandos
    vm.execute(commands)
    
    # Verifica se o ambiente foi configurado
    assert vm.environment is not None 