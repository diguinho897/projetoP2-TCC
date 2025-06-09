from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum
from lark import Tree, Token

class CommandType(Enum):
    CONFIGURAR_BANCO = "configurarBanco"
    INICIAR_SERVIDOR = "iniciarServidor"
    EXECUTAR_TESTE = "executarTeste"
    DEPLOY_AMBIENTE = "deployEmAmbiente"

@dataclass
class Command:
    type: CommandType
    args: Dict[str, Any]

class SemanticAnalyzer:
    def __init__(self):
        self.commands: List[Command] = []
        self.server_started = False
        self.tests_executed = False
    
    def analyze(self, ast) -> List[Command]:
        """
        Analisa a árvore sintática e valida as regras semânticas.
        
        Args:
            ast: Árvore sintática gerada pelo parser
            
        Returns:
            Lista de comandos validados
            
        Raises:
            SemanticError: Se alguma regra semântica for violada
        """
        for node in ast.children:
            command = self._process_node(node)
            self._validate_command(command)
            self.commands.append(command)
        
        return self.commands
    
    def _process_node(self, node: Tree) -> Command:
        """Processa um nó da árvore sintática e retorna um comando."""
        if not isinstance(node, Tree):
            raise SemanticError(f"Nó inválido: {node}")
            
        if node.data == 'comando':
            # O primeiro filho contém o comando real
            return self._process_node(node.children[0])
            
        if node.data == 'configurar_banco':
            return Command(
                CommandType.CONFIGURAR_BANCO,
                {
                    'host': node.children[0].value.strip('"'),
                    'banco': node.children[1].value.strip('"')
                }
            )
        elif node.data == 'iniciar_servidor':
            args = {'host': node.children[0].value.strip('"')}
            if len(node.children) > 1 and hasattr(node.children[1], 'children'):
                args['porta'] = int(node.children[1].children[0].value)
            return Command(CommandType.INICIAR_SERVIDOR, args)
        elif node.data == 'executar_teste':
            return Command(
                CommandType.EXECUTAR_TESTE,
                {'path': node.children[0].value.strip('"')}
            )
        elif node.data == 'deploy_ambiente':
            return Command(
                CommandType.DEPLOY_AMBIENTE,
                {'ambiente': node.children[0].value.strip('"')}
            )
        
        raise SemanticError(f"Comando inválido: {node.data}")
    
    def _validate_command(self, command: Command):
        """Valida as regras semânticas para um comando."""
        if command.type == CommandType.INICIAR_SERVIDOR:
            self.server_started = True
        elif command.type == CommandType.EXECUTAR_TESTE:
            if not self.server_started:
                raise SemanticError("Servidor deve ser iniciado antes de executar testes")
            self.tests_executed = True
        elif command.type == CommandType.DEPLOY_AMBIENTE:
            if not self.tests_executed:
                raise SemanticError("Testes devem ser executados antes do deploy")

class SemanticError(Exception):
    """Exceção lançada quando uma regra semântica é violada."""
    pass 