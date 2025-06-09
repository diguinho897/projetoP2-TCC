import pytest
from pathlib import Path
from src.lexer.lexer import DSLexer

def test_lexer_parse():
    lexer = DSLexer()
    
    # Carrega o exemplo
    example_path = Path(__file__).parent.parent / "examples" / "exemplo.dsl"
    with open(example_path, "r", encoding="utf-8") as f:
        script = f.read()
    
    # Tenta fazer o parse
    tree = lexer.parse(script)
    
    # Verifica se a árvore foi gerada
    assert tree is not None
    
    # Verifica se temos 4 comandos (uma linha para cada comando)
    assert len(tree.children) == 4 