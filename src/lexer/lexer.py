from ply import lex

# Lista de tokens
tokens = (
    'STRING',
    'NUMBER',
    'CONFIGURAR_BANCO',
    'INICIAR_SERVIDOR',
    'EXECUTAR_TESTE',
    'DEPLOY_AMBIENTE',
    'PORTA',
)

# Regras para tokens simples
t_STRING = r'"[^"]*"'
t_NUMBER = r'\d+'
t_PORTA = r'porta='

# Regras para comandos
def t_CONFIGURAR_BANCO(t):
    r'configurarBanco'
    return t

def t_INICIAR_SERVIDOR(t):
    r'iniciarServidor'
    return t

def t_EXECUTAR_TESTE(t):
    r'executarTeste'
    return t

def t_DEPLOY_AMBIENTE(t):
    r'deployEmAmbiente'
    return t

# Caracteres ignorados (espaços e tabs)
t_ignore = ' \t'

# Nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

class DSLexer:
    def __init__(self):
        self.lexer = lex.lex()
    
    def tokenize(self, data):
        """
        Tokeniza o input e retorna a lista de tokens.
        
        Args:
            data (str): O texto a ser tokenizado
            
        Returns:
            list: Lista de tokens
        """
        self.lexer.input(data)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens 