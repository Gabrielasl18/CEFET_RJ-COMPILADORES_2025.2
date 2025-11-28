# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

tokens = (
    'IDENT', 'NUMBER', 'STRING',
    'EQUALS', 'GT', 'LT', 'GE', 'LE', 'NE',
    'COMMA', 'LP', 'RP'
)

literals = ['*', ';']

reserved = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'insert': 'INSERT',
    'create':'CREATE',
    'join' :'JOIN',
    'into': 'INTO',
    'values': 'VALUES',
    'delete': 'DELETE'
}

tokens = tokens + tuple(reserved.values())
# Tokens

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'IDENTIFICADOR')
    return t

def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_EQUALS = r'='
t_GT     = r'>'
t_LT     = r'<'
t_GE     = r'>='
t_LE     = r'<='
t_NE     = r'<>'
t_COMMA  = r','
t_LP     = r'\('
t_RP     = r'\)'

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)
def p_statement(p):
    '''statement : select_stmt
                 | insert_stmt
                 | delete_stmt'''
    print("AST =", p[1])


def p_select_statement(p):
    "select_statement : SELECT select_list FROM IDENTIFICADOR where_opt"
    p[0] = ("select", p[2], p[4], p[5])

def p_select_lista_tudo(p):
    "select_list : '*'"
    p[0] = "*"

def p_select_lista_colunas(p):
    "select_list : column_list"
    p[0] = p[1]

def p_column_lista_unica(p):
    "column_list : IDENTIFICADOR"
    p[0] = [p[1]]

def p_column_list_varios(p):
    "column_list : column_list COMMA IDENT"
    p[0] = p[1] + [p[3]]



def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)