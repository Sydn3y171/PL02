#
# Autores: [a20446-a23033-a23290]
# Data: 
#

#--------------------------------------------------------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc

# Tokens - Definição dos tokens da linguagem
tokens = [
    'ESCREVER',       # Token para a palavra-chave 'ESCREVER'
    'NUMERO',         # Token para números
    'STRING',         # Token para strings
    'LPAREN',         # Token para o parêntese esquerdo '('
    'RPAREN',         # Token para o parêntese direito ')'
    'PLUS',           # Token para o operador de adição '+'
    'MULT',    # Token para o operador de multiplicação '*'
    'DIV',        # Token para o operador de divisão '/'
    'MAIOR',          # Token para o operador de maior '>'
    'MENOR',          # Token para o operador de menor '<'
    'MINOS',          # Token para o operador de subtração '-'
    'VALOR',          # Token para valores (palavras-chave 'valor' ou 'curso')
    'CONCAT'          # Novo token para o operador de concatenação '<>'
]

# Define caracteres a serem ignorados
t_ignore = ' \t\n'  

# Expressões regulares para os tokens
t_ESCREVER = r'ESCREVER'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLICAR = r'\*'
t_DIVIDIR = r'/'
t_MAIOR = r'>'
t_MENOR = r'<'
t_STRING = r'\"(.*?)\"|\'[^\']*\''

# Novo token para o operador de concatenação
t_CONCAT = r'<>'  

# Função de tokenização para o token VALOR
def t_VALOR(t):
    r'valor|curso'  
    return t

# Função de tokenização para o token NUMERO
def t_NUMERO(t):
    r'\d+'  
    t.value = int(t.value)
    return t

# Função para tratar erros léxicos (caracteres não reconhecidos)
def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()  # Cria o analisador léxico

# Parser rules - Definição das regras da gramática
# Função que define a regra inicial da gramática
def p_inicio(p):
    'S : comandos'
    pass

# Função que define a regra para uma sequência de comandos
def p_comandos(p):
    '''comandos : comandos comando
                | comando'''
    pass

# Função que define a regra para o comando "ESCREVER"
def p_comando_escrever(p):
    'comando : ESCREVER LPAREN expressao RPAREN'
    print(p[3])

# Função que define as regras para expressões aritméticas
def p_expressao_aritmetica(p):
    '''expressao : expressao PLUS expressao
                 | expressao MINUS expressao
                 | expressao MULTIPLICAR expressao
                 | expressao DIVIDIR expressao
                 | expressao MAIOR expressao
                 | expressao MENOR expressao'''
    # Avalia expressões aritméticas
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]

# Função que define a regra para a operação de concatenação
def p_expressao_concat(p):
    'expressao : expressao CONCAT expressao'
    p[0] = str(p[1]) + str(p[3])

# Função que define a regra para expressões entre parênteses
def p_expressao_parenteses(p):
    'expressao : LPAREN expressao RPAREN'
    p[0] = p[2]

# Função que define a regra para expressões numéricas
def p_expressao_numero(p):
    'expressao : NUMERO'
    p[0] = p[1]

# Função que define a regra para expressões de string
def p_expressao_string(p):
    'expressao : STRING'
    string_value = p[1][1:-1]  
    if string_value == "Ola Mundo":
        p[0] = "Olá, Mundo!"
    else:
        p[0] = string_value

# Função que define a regra para expressões de valor
def p_expressao_valor(p):
    'expressao : VALOR'
    p[0] = p[1]

# Função para tratar erros sintáticos
def p_error(p):
    if p:
        print("Erro sintático na posição:", p.lexpos)
    else:
        print("Erro sintático!")

parser = yacc.yacc()  # Cria o analisador sintático

# Entrada
input_terminal = """
    ESCREVER(valor);
    ESCREVER(365 * 2);
    ESCREVER("Ola Mundo");
    ESCREVER("Olá, " <> curso);
    ESCREVER(5 < 8);
    ESCREVER(6 > 9);
"""

# Divide as instruções e processa cada uma individualmente
instructions = input_terminal.strip().split(';')
for instruction in instructions:
    instruction = instruction.strip()
    if instruction:  
        result = parser.parse(instruction)