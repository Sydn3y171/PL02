#
# Autores: [a20446-a23033-a23290]
# Data: 
#

#--------------------------------------------------------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc

# Dicionário que armazenará as variáveis e seus valores calculados.
variaveis = {}

# Definição dos tokens
tokens = (
    'VARIAVEL',         # Token para nomes de variáveis
    'IGUAL',            # Token para o sinal de igual '='
    'NUMERO',           # Token para números
    'MAIS',             # Token para o operador de adição '+'
    'MENOS',            # Token para o operador de subtração '-'
    'MULTIPLICACAO',    # Token para o operador de multiplicação '*'
    'DIVISAO',          # Token para o operador de divisão '/'
    'LPAREN',           # Token para o parêntese esquerdo '('
    'RPAREN'            # Token para o parêntese direito ')'
)

# Expressões regulares para tokens simples
t_IGUAL = r'='
t_MAIS = r'\+'
t_MENOS = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Expressão regular para variáveis
def t_VARIAVEL(t):
    r'[a-z_][a-zA-Z0-9_]*[!?]?'  # Nomes de variáveis começam com letra minúscula ou _, seguidos de letras, números ou _, podendo terminar com ! ou ?
    return t

# Expressão regular para números
def t_NUMERO(t):
    r'\d+'  # Números são sequências de dígitos
    t.value = int(t.value)  # Converte o valor do token para inteiro
    return t

# Ignora espaços e tabs
t_ignore = ' \t'

# Tratamento de novas linhas
def t_newline(t):
    r'\n+'  # Define como reconhecer novas linhas
    t.lexer.lineno += len(t.value)  # Atualiza o número da linha

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")  # Imprime o caractere ilegal encontrado
    t.lexer.skip(1)  # Pula o caractere ilegal

# Construção do lexer
lexer = lex.lex()

# Precedências dos operadores
precedence = (
    ('left', 'MAIS', 'MENOS'),            # Define a precedência para + e -
    ('left', 'MULTIPLICACAO', 'DIVISAO'), # Define a precedência para * e /
    ('nonassoc', 'LPAREN', 'RPAREN')      # Define a precedência para parênteses
)

# Definição da gramática
def p_atribuicao(p):
    'atribuicao : VARIAVEL IGUAL expressao'
    variaveis[p[1]] = p[3]  # Atribui o valor da expressão à variável
    p[0] = f"Atribuição válida: {p[1]} = {p[3]}"  # Define o valor de retorno

def p_expressao_binaria(p):
    '''expressao : expressao MAIS expressao
                 | expressao MENOS expressao
                 | expressao MULTIPLICACAO expressao
                 | expressao DIVISAO expressao'''
    if p[2] == '+':      # Adição
        p[0] = p[1] + p[3]
    elif p[2] == '-':    # Subtração
        p[0] = p[1] - p[3]
    elif p[2] == '*':    # Multiplicação
        p[0] = p[1] * p[3]
    elif p[2] == '/':    # Divisão
        p[0] = p[1] / p[3]

def p_expressao_numero(p):
    'expressao : NUMERO'
    p[0] = p[1]  # O valor da expressão é o próprio número

def p_expressao_variavel(p):
    'expressao : VARIAVEL'
    try:
        p[0] = variaveis[p[1]]  # O valor da expressão é o valor da variável
    except KeyError:
        print(f"Erro: Variável não definida '{p[1]}'")  # Variável não definida
        p[0] = 0  # Define valor padrão 0

def p_expressao_paren(p):
    'expressao : LPAREN expressao RPAREN'
    p[0] = p[2]  # O valor da expressão é o valor dentro dos parênteses

def p_error(p):
    print(f"Erro de sintaxe em '{p.value}'")  # Imprime mensagem de erro de sintaxe

# Construção do parser
parser = yacc.yacc()

# Exemplos de atribuições de variáveis com expressões aritméticas.
expressoes = """
tmp_01 = 2 * 3 + 4 ;
a1_ = 12345 - (5191 * 15) ;
idade_valida? = 1 ;
mult_3! = a1_ * 3 ;
"""

# Divide o texto de entrada em instruções individuais, separadas por ponto e vírgula.
instructions = expressoes.split(";")
# Remove a última instrução vazia da lista resultante.
instructions = instructions[:-1]

# Itera sobre cada expressão, processando-a e imprimindo o resultado.
for expressao in instructions:
    resultado = parser.parse(expressao.strip())  # Remove espaços em branco ao redor da expressão.
    print(resultado)
