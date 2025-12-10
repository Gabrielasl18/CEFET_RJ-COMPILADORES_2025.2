import ply.lex as lex
import ply.yacc as yacc

# Lexer
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
    'on': 'ON'
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

# Banco de dados mock 
db = {
    "clientes": [
        {"id": 1, "nome": "Ana Souza", "idade": 28, "cpf": "123.456.789-00", "email": "ana.souza@example.com"},
        {"id": 2, "nome": "João Pereira", "idade": 34, "cpf": "987.654.321-00", "email": "joao.pereira@example.com"},
        {"id": 3, "nome": "Maria Oliveira", "idade": 22, "cpf": "456.789.123-00", "email": "maria.oliveira@example.com"},
        {"id": 4, "nome": "Carlos Silva", "idade": 30, "cpf": "111.222.333-44", "email": "carlos@example.com"},
        {"id": 5, "nome": "Paula Costa", "idade": 40, "cpf": "222.333.444-55", "email": "paula@example.com"}
    ],
    "pedidos": [
        {"id": 1, "cliente_id": 1, "valor": 500},
        {"id": 2, "cliente_id": 2, "valor": 900},
        {"id": 3, "cliente_id": 1, "valor": 250},
        {"id": 4, "cliente_id": 3, "valor": 1200}
    ]
}

# Parser 
precedence = ()

def p_statement(p):
    '''statement : select_stmt SEMICOLON_OPT
                 | insert_stmt SEMICOLON_OPT
                 | delete_stmt SEMICOLON_OPT
                 | update_stmt SEMICOLON_OPT'''
    p[0] = p[1]

def p_SEMICOLON_OPT(p):
    '''SEMICOLON_OPT : ';'
                     | '''
    pass

# SELECT + JOIN 
def p_select_stmt(p):
    "select_stmt : SELECT select_list FROM IDENTIFICADOR join_opt where_opt"
    table = db.get(p[4], [])

    # JOIN 
    if p[5]:
        join_table_name, left_key, right_key = p[5]
        join_table = db.get(join_table_name, [])
        new_rows = []
        for row in table:
            for jrow in join_table:
                if row[left_key] == jrow[right_key]:
                    new_rows.append({**row, **jrow})
        table = new_rows

    columns = p[2]

    # WHERE
    if p[6]:
        op, field, val = p[6]
        if op == '=':   table = [r for r in table if r[field] == val]
        if op == '>':   table = [r for r in table if r[field] > val]
        if op == '<':   table = [r for r in table if r[field] < val]
        if op == '>=':  table = [r for r in table if r[field] >= val]
        if op == '<=':  table = [r for r in table if r[field] <= val]
        if op == '<>':  table = [r for r in table if r[field] != val]

    # Column selection
    if columns == '*':
        p[0] = table
    else:
        p[0] = [{col: row[col] for col in columns} for row in table]

    print_table(p[0])

def p_join_opt_empty(p):
    "join_opt : "
    p[0] = None

def p_join_opt_clause(p):
    "join_opt : JOIN IDENTIFICADOR ON IDENTIFICADOR EQUALS IDENTIFICADOR"
    p[0] = (p[2], p[4], p[6])

def p_select_list_all(p):
    "select_list : '*'"
    p[0] = "*"

def p_select_list_columns(p):
    "select_list : column_list"
    p[0] = p[1]

# UPDATE
def p_update_stmt(p):
    "update_stmt : UPDATE IDENTIFICADOR SET update_list where_opt"
    table = db.get(p[2], [])
    updates = p[4]
    count = 0
    for row in table:
        apply = True
        if p[5]:
            op, field, val = p[5]
            if op == '=':   apply = (row[field] == val)
            if op == '>':   apply = (row[field] > val)
            if op == '<':   apply = (row[field] < val)
            if op == '>=':  apply = (row[field] >= val)
            if op == '<=':  apply = (row[field] <= val)
            if op == '<>':  apply = (row[field] != val)
        if apply:
            row.update(updates)
            count += 1
    print(f"{count} row(s) updated in {p[2]}.")
    p[0] = count

def p_update_list_single(p):
    "update_list : IDENTIFICADOR EQUALS value"
    p[0] = {p[1]: p[3]}

def p_update_list_multiple(p):
    "update_list : update_list COMMA IDENTIFICADOR EQUALS value"
    p[0] = {**p[1], p[3]: p[5]}

# COMMON RULES
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

def p_condition(p):
    '''condition : IDENTIFICADOR EQUALS value
                 | IDENTIFICADOR GT value
                 | IDENTIFICADOR LT value
                 | IDENTIFICADOR GE value
                 | IDENTIFICADOR LE value
                 | IDENTIFICADOR NE value'''
    p[0] = (p[2], p[1], p[3])

def p_value(p):
    '''value : NUMBER
             | STRING'''
    p[0] = p[1]

# INSERT
def p_insert_stmt(p):
    "insert_stmt : INSERT INTO IDENTIFICADOR LP column_list RP VALUES LP value_list RP"
    table = db.setdefault(p[3], [])
    row = dict(zip(p[5], p[9]))
    table.append(row)
    print(f"1 row inserted into {p[3]}.")
    p[0] = row

def p_value_list_single(p):
    "value_list : value"
    p[0] = [p[1]]

def p_value_list_multiple(p):
    "value_list : value_list COMMA value"
    p[0] = p[1] + [p[3]]

# DELETE
def p_delete_stmt(p):
    "delete_stmt : DELETE FROM IDENTIFICADOR where_opt"
    table = db.get(p[3], [])
    if p[4]:
        op, field, val = p[4]
        original_len = len(table)
        if op == '=':   db[p[3]] = [r for r in table if r[field] != val]
        if op == '>':   db[p[3]] = [r for r in table if r[field] <= val]
        if op == '<':   db[p[3]] = [r for r in table if r[field] >= val]
        if op == '>=':  db[p[3]] = [r for r in table if r[field] < val]
        if op == '<=':  db[p[3]] = [r for r in table if r[field] > val]
        if op == '<>':  db[p[3]] = [r for r in table if r[field] == val]
        deleted = original_len - len(db[p[3]])
        print(f"{deleted} row(s) deleted from {p[3]}.")
    else:
        deleted = len(table)
        db[p[3]] = []
        print(f"{deleted} row(s) deleted from {p[3]}.")
    p[0] = deleted

# Error
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# Helper
def print_table(rows):
    if not rows:
        print("(empty set)")
        return
    headers = rows[0].keys()
    col_widths = [max(len(str(r[h])) for r in rows + [dict(zip(headers, headers))]) for h in headers]
    line = "+".join('-'*(w+2) for w in col_widths)
    print("+" + line + "+")
    print("| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |")
    print("+" + line + "+")
    for r in rows:
        print("| " + " | ".join(str(r[h]).ljust(w) for h, w in zip(headers, col_widths)) + " |")
    print("+" + line + "+")

# REPL
if __name__ == "__main__":
    while True:
        try:
            s = input('sql > ')
        except EOFError:
            break
        if not s:
            continue
        parser.parse(s)