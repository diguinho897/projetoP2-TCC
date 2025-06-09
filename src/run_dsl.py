#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from src.lexer.lexer import DSLexer
from src.parser.parser import DSParser
from src.vm.interpreter import DSLInterpreter

def main():
    parser = argparse.ArgumentParser(description='Executa scripts DSL')
    parser.add_argument('script', type=str, help='Caminho para o script DSL')
    parser.add_argument('--log-dir', type=str, default='logs',
                      help='Diretório para salvar os logs (padrão: logs)')
    
    args = parser.parse_args()
    
    # Verifica se o arquivo existe
    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Erro: Arquivo '{args.script}' não encontrado")
        sys.exit(1)
    
    try:
        # Lê o script
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # Inicializa os componentes
        lexer = DSLexer()
        parser = DSParser()
        interpreter = DSLInterpreter(log_dir=args.log_dir)
        
        # Tokeniza o script
        tokens = lexer.tokenize(script_content)
        
        # Analisa o script
        commands = parser.parse(script_content)
        
        # Executa os comandos
        results = interpreter.execute(commands)
        
        # Exibe os resultados
        print("\nResultados da execução:")
        print("-" * 50)
        for result in results:
            status = "✓" if result['success'] else "✗"
            print(f"{status} {result['command']}")
            if not result['success'] and 'error' in result:
                print(f"  Erro: {result['error']}")
        print("-" * 50)
        
        # Verifica se houve algum erro
        if any(not r['success'] for r in results):
            sys.exit(1)
            
    except Exception as e:
        print(f"Erro ao executar script: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 