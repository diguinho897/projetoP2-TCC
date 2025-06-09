from ply import yacc
from src.lexer.lexer import tokens

class Command:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or {}

class DSParser:
    def __init__(self):
        self.parser = yacc.yacc()
    
    def parse(self, data):
        """
        Analisa o input e retorna a árvore sintática.
        
        Args:
            data (str): O texto a ser analisado
            
        Returns:
            list: Lista de comandos
        """
        return self.parser.parse(data)

# Regras da gramática
def p_script(p):
    '''script : command
              | script command'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_command(p):
    '''command : configurar_banco
               | iniciar_servidor
               | executar_teste
               | deploy_ambiente'''
    p[0] = p[1]

def p_configurar_banco(p):
    'configurar_banco : CONFIGURAR_BANCO STRING STRING'
    p[0] = Command('configurar_banco', {
        'host': p[2],
        'database': p[3]
    })

def p_iniciar_servidor(p):
    'iniciar_servidor : INICIAR_SERVIDOR STRING porta_param'
    p[0] = Command('iniciar_servidor', {
        'host': p[2],
        'porta': p[3]
    })

def p_executar_teste(p):
    'executar_teste : EXECUTAR_TESTE STRING'
    p[0] = Command('executar_teste', {
        'suite': p[2]
    })

def p_deploy_ambiente(p):
    'deploy_ambiente : DEPLOY_AMBIENTE STRING'
    p[0] = Command('deploy_ambiente', {
        'ambiente': p[2]
    })

def p_porta_param(p):
    'porta_param : PORTA NUMBER'
    p[0] = int(p[2])

# Tratamento de erros
def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}'")
    else:
        print("Erro de sintaxe no final do arquivo") 