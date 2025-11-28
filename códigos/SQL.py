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

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_EQUALS = r'='
t_GT     = r'>'
t_LT     = r'<'
t_GE     = r'>='
t_LE     = r'<='
t_NE     = r'<>'
t_COMMA  = r','
t_LP     = r'\('
t_RP     = r'\)'


# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}

def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]


def p_statement_expr(p):
    'statement : expression'
    print(p[1])


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