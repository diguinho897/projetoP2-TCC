from pathlib import Path
from lark import Lark, UnexpectedInput

class DSLexer:
    def __init__(self):
        grammar_path = Path(__file__).parent.parent.parent / "grammar" / "dsl.lark"
        with open(grammar_path, "r", encoding="utf-8") as f:
            grammar = f.read()
        
        self.parser = Lark(
            grammar,
            parser="lalr"
        )
    
    def parse(self, script: str):
        """
        Analisa o script e retorna a árvore sintática.
        
        Args:
            script (str): O script a ser analisado
            
        Returns:
            A árvore sintática gerada pelo Lark
            
        Raises:
            Exception: Se o script contiver comandos inválidos
        """
        try:
            return self.parser.parse(script)
        except UnexpectedInput as e:
            raise Exception(f"Erro de sintaxe: {str(e)}") 