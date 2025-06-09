from pathlib import Path
from lark import Lark

class DSLexer:
    def __init__(self):
        grammar_path = Path(__file__).parent.parent.parent / "grammar" / "dsl.lark"
        with open(grammar_path, "r", encoding="utf-8") as f:
            grammar = f.read()
        
        self.parser = Lark(grammar, parser="lalr")
    
    def parse(self, script: str):
        """
        Analisa o script e retorna a árvore sintática.
        
        Args:
            script (str): O script a ser analisado
            
        Returns:
            A árvore sintática gerada pelo Lark
        """
        return self.parser.parse(script) 