import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'IDENTIFICADOR', 'NUMBER', 'STRING',
    'EQUALS', 'GT', 'LT', 'GE', 'LE', 'NE',
    'COMMA', 'LP', 'RP'
)

literals = ['*']

reserved = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'insert': 'INSERT',
    'into': 'INTO',
    'values': 'VALUES',
    'delete': 'DELETE',
    'update': 'UPDATE',
    'set': 'SET',
    'join': 'JOIN',
    'on': 'ON',
    'and': 'AND',      # >>> AND / OR <<<
    'or': 'OR'         # >>> AND / OR <<<
}

tokens = tokens + tuple(reserved.values())

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
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

db = {
    "clientes": [
        {"id": 1, "nome": "Ana Souza", "idade": 28},
        {"id": 2, "nome": "João Pereira", "idade": 34},
        {"id": 3, "nome": "Maria Oliveira", "idade": 22},
        {"id": 4, "nome": "Carlos Silva", "idade": 30},
        {"id": 5, "nome": "Paula Costa", "idade": 40}
    ],
    "pedidos": [
        {"id": 1, "cliente_id": 1, "valor": 500},
        {"id": 2, "cliente_id": 2, "valor": 900}
    ]
}

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
)

def p_statement(p):
    '''statement : select_stmt
                 | insert_stmt
                 | delete_stmt
                 | update_stmt'''
    p[0] = p[1]


def p_select_stmt(p):
    "select_stmt : SELECT select_list FROM IDENTIFICADOR join_opt where_opt"

    table = db.get(p[4], [])

    # >>> JOIN <<<
    if p[5]:
        join_table, left_key, right_key = p[5]
        join_rows = db.get(join_table, [])

        new_table = []
        for r1 in table:
            for r2 in join_rows:
                if r1[left_key] == r2[right_key]:
                    new_table.append({**r1, **r2})

        table = new_table

    if p[6]:
        table = [r for r in table if eval_condition(p[6], r)]

    if p[2] == '*':
        result = table
    else:
        result = [{c: r[c] for c in p[2]} for r in table]

    print(result)
    p[0] = result

def p_select_list_all(p):
    "select_list : '*'"
    p[0] = "*"

def p_select_list_columns(p):
    "select_list : column_list"
    p[0] = p[1]

def p_column_list_single(p):
    "column_list : IDENTIFICADOR"
    p[0] = [p[1]]

def p_column_list_multiple(p):
    "column_list : column_list COMMA IDENTIFICADOR"
    p[0] = p[1] + [p[3]]


def p_where_opt_empty(p):
    "where_opt : "
    p[0] = None

def p_where_opt_clause(p):
    "where_opt : WHERE condition"
    p[0] = p[2]


def p_condition_simple(p):
    '''condition : IDENTIFICADOR EQUALS value
                 | IDENTIFICADOR GT value
                 | IDENTIFICADOR LT value
                 | IDENTIFICADOR GE value
                 | IDENTIFICADOR LE value
                 | IDENTIFICADOR NE value'''
    p[0] = ('CMP', p[2], p[1], p[3])

def p_condition_and(p):
    "condition : condition AND condition"
    p[0] = ('AND', p[1], p[3])

def p_condition_or(p):
    "condition : condition OR condition"
    p[0] = ('OR', p[1], p[3])

def p_condition_group(p):
    "condition : LP condition RP"
    p[0] = p[2]

def p_value(p):
    '''value : NUMBER
             | STRING'''
    p[0] = p[1]


def p_delete_stmt(p):
    "delete_stmt : DELETE FROM IDENTIFICADOR where_opt"
    table = db.get(p[3], [])
    if p[4]:
        db[p[3]] = [r for r in table if not eval_condition(p[4], r)]
    else:
        db[p[3]] = []
    print("DELETE OK")


def p_update_stmt(p):
    "update_stmt : UPDATE IDENTIFICADOR SET IDENTIFICADOR EQUALS value where_opt"
    table = db.get(p[2], [])
    for row in table:
        if not p[6] or eval_condition(p[6], row):
            row[p[4]] = p[6]
    print("UPDATE OK")

def p_insert_stmt(p):
    "insert_stmt : INSERT INTO IDENTIFICADOR LP IDENTIFICADOR RP VALUES LP value RP"
    db.setdefault(p[3], []).append({p[5]: p[9]})
    print("INSERT OK")

def eval_condition(cond, row):
    kind = cond[0]

    if kind == 'CMP':
        _, op, field, val = cond
        if op == '=':   return row[field] == val
        if op == '>':   return row[field] > val
        if op == '<':   return row[field] < val
        if op == '>=':  return row[field] >= val
        if op == '<=':  return row[field] <= val
        if op == '<>':  return row[field] != val

    if kind == 'AND':
        return eval_condition(cond[1], row) and eval_condition(cond[2], row)

    if kind == 'OR':
        return eval_condition(cond[1], row) or eval_condition(cond[2], row)


def p_join_opt_empty(p):
    "join_opt : "
    p[0] = None

def p_join_opt_clause(p):
    "join_opt : JOIN IDENTIFICADOR ON IDENTIFICADOR EQUALS IDENTIFICADOR"
    p[0] = (p[2], p[4], p[6])

def p_error(p):
    print("Syntax error")

parser = yacc.yacc()

while True:
    try:
        s = input("sql> ")
    except EOFError:
        break
    if not s:
        continue
    parser.parse(s)
