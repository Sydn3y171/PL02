#
# Autores: [a20446-a23033-a23290]
# Data: 
#

#--------------------------------------------------------------------------------------------------------------------------

import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = (
    'FUNCAO', 'ID', 'NUMBER', 'COLON', 'COMMA', 'SEMICOLON', 'ASSIGN', 'LPAREN', 'RPAREN', 'PLUS', 'TIMES'
)

# Definições de tokens
t_COLON = r':'
t_COMMA = r','
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_TIMES = r'\*'

def t_FUNCAO(t):
    r'FUNCAO'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Caracter inválido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Definições de precedência e associatividade dos operadores
precedence = (
    ('left', 'PLUS'),
    ('left', 'TIMES')
)

# Tabela de funções
functions = {}

# Tabela de símbolos (variáveis)
symbols = {}

# Definição da gramática
def p_program(p):
    '''program : statements'''
    pass

def p_statements_multiple(p):
    '''statements : statements statement'''
    pass

def p_statements_single(p):
    '''statements : statement'''
    pass

def p_statement_assign(p):
    '''statement : ID ASSIGN expression SEMICOLON'''
    symbols[p[1]] = p[3]

def p_statement_function_declaration(p):
    '''statement : function_declaration'''
    pass

def p_function_declaration_inline(p):
    '''function_declaration : FUNCAO ID LPAREN parameters RPAREN COMMA COLON expression SEMICOLON'''
    functions[(p[2], len(p[4]))] = (p[4], p[8])

def p_function_declaration_block(p):
    '''function_declaration : FUNCAO ID LPAREN parameters RPAREN COLON statements FIM'''
    functions[(p[2], len(p[4]))] = (p[4], p[7])

def p_parameters_multiple(p):
    '''parameters : parameters COMMA ID'''
    p[0] = p[1] + [p[3]]

def p_parameters_single(p):
    '''parameters : ID'''
    p[0] = [p[1]]

def p_parameters_empty(p):
    '''parameters : '''
    p[0] = []

def p_statements_block(p):
    '''statements : statements statement_block'''
    p[0] = p[1] + [p[2]]

def p_statements_block_single(p):
    '''statements : statement_block'''
    p[0] = [p[1]]

def p_statement_block(p):
    '''statement_block : ID ASSIGN expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

def p_statement_block_expression(p):
    '''statement_block : expression SEMICOLON'''
    p[0] = ('expr', p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression TIMES expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

def p_expression_id(p):
    '''expression : ID'''
    try:
        p[0] = symbols[p[1]]
    except LookupError:
        print(f"Erro: Variável '{p[1]}' não definida")
        p[0] = 0

def p_expression_function_call(p):
    '''expression : ID LPAREN arguments RPAREN'''
    func_name = p[1]
    arg_count = len(p[3])
    func_key = (func_name, arg_count)

    if func_key in functions:
        params, body = functions[func_key]
        local_symbols = dict(zip(params, p[3]))
        
        if isinstance(body, list):
            for stmt in body:
                if stmt[0] == 'assign':
                    local_symbols[stmt[1]] = evaluate_expression(stmt[2], local_symbols)
                elif stmt[0] == 'expr':
                    result = evaluate_expression(stmt[1], local_symbols)
            p[0] = result
        else:
            p[0] = evaluate_expression(body, local_symbols)
    else:
        print(f"Erro: Função '{func_name}' com {arg_count} argumentos não definida")
        p[0] = 0

def p_arguments_multiple(p):
    '''arguments : arguments COMMA expression'''
    p[0] = p[1] + [p[3]]

def p_arguments_single(p):
    '''arguments : expression'''
    p[0] = [p[1]]

def p_arguments_empty(p):
    '''arguments : '''
    p[0] = []

def p_error(p):
    print(f"Erro de sintaxe em '{p.value}'" if p else "Erro de sintaxe no final do arquivo")

def evaluate_expression(expr, local_symbols):
    if isinstance(expr, int):
        return expr
    elif isinstance(expr, str):
        return local_symbols.get(expr, symbols.get(expr, 0))
    elif isinstance(expr, tuple):
        if expr[0] == '+':
            return evaluate_expression(expr[1], local_symbols) + evaluate_expression(expr[2], local_symbols)
        elif expr[0] == '*':
            return evaluate_expression(expr[1], local_symbols) * evaluate_expression(expr[2], local_symbols)
    return 0

parser = yacc.yacc()

# Programa de exemplo para testar
programa = '''
FUNCAO soma(a, b),: a + b ;
FUNCAO soma2(c) :
c = c + 1 ;
c + 1 ;
FIM
seis = soma(4, 2);
oito = soma2(seis);

FUNCAO area_retangulo(a, b):
a * b;
FIM

FUNCAO area_quadrado(a):
area_retangulo(a, a);
FIM

a = area_retangulo(10, 20);
b = area_quadrado(30);

FUNCAO area(a, b),: a * b ;
FUNCAO area(c),: area(c, c);
d = area(10, 20);
e = area(30);

FUNCAO fib(0),: 0 ;
FUNCAO fib(1),: 1 ;
FUNCAO fib(n):
a = fib(n - 1);
b = fib(n - 2);
a + b;
FIM

fib5 = fib(5);
'''

parser.parse(programa)

print(f"Variável 'seis': {symbols['seis']}")
print(f"Variável 'oito': {symbols['oito']}")
print(f"Variável 'a': {symbols['a']}")
print(f"Variável 'b': {symbols['b']}")
print(f"Variável 'd': {symbols['d']}")
print(f"Variável 'e': {symbols['e']}")
print(f"Variável 'fib5': {symbols['fib5']}")
