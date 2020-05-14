# Jamy, 2/19/2020

import ply.lex as lex
import re
import sys

tokens = (
    'T_IntConstant',
    'T_DoubleConstant',
    'T_STRINGCONSTANT',
    'T_IDENTIFIER',
    'SINGLE_COMMENT',
    'COMMENT',
    'T_Or',
    'T_LessEqual',
    'T_GreaterEqual',
    'T_Equal',
    'T_Void',
    'T_Int',
    'T_Double',
    'T_String',
    'T_While',
    'T_For',
    'T_Print',
    'T_If',
    'T_Else',
    'T_Return',
    'T_Break',
    'T_BoolConstant',
    'T_logicaland',
    'T_NotEqual'
)


literals = ['+','-','*','/','<','>','=',';',',','!','{','}','(',')','.','%']

t_ignore = ' \t'


def t_COMMENT(t):
    r'((\/\*(\s)*\/\*)|(\/\*(\s|\/)*)|(\/\*(\S|\/)*))([^\*\/]*)\*\/'
    t.lexer.lineno += len(re.findall(r'\n+', t.value))
    pass

def t_SINGLE_COMMENT(t):
    r'\/\/[^\n]*'
    t.lexer.lineno += len(re.findall(r'\n+', t.value))
    pass

def check_key_xist(val):
    kewords = ['void','int','string','double','while','if','else','break','return','true','false']
    for key in kewords:
        if key == val.lower():
            return True
    return False

def t_T_logicaland(t):
    r'&&'
    return t

def t_T_Void(t):
    r'(?<![\w\d])void(?![\w\d])'
    return t

def t_T_Int(t):
    r'(int)'
    return t

def t_T_String(t):
    r'(string)'
    return t

def t_T_Double(t):
    r'(double)'
    return t

def t_T_While(t):
    r'(while)'
    return t

def t_T_For(t):
    r'(for)'
    return t

def t_T_Print(t):
    r'(Print)'
    return t

def t_T_If(t):
    r'(if)'
    return t
def t_T_Else(t):
    r'(else)'
    return t
def t_T_Return(t):
    r'(return)'
    return t
def t_T_Break(t):
    r'(break)'
    return t
def t_T_BoolConstant(t):
    r'(true|false)'
    return t

def t_T_Or(t):
    r'\|\|'
    return t

def t_T_LessEqual(t):
    r'<='
    return t

def t_T_GreaterEqual(t):
    r'>='
    return t


def t_T_NotEqual(t):
    r'!='
    return t


def t_T_Equal(t):
    r'=='
    return t

def t_percent(t):
    r'%'
    t.type = '%'
    return t

def t_coma(t):
    r','
    t.type = ','
    return t

def t_semicolon(t):
    r';'
    t.type = ';'
    return t
def t_greater(t):
    r'<'
    t.type = '<'
    return t

def t_less(t):
    r'>'
    t.type = '>'
    return t

def t_exclamatory(t):
    r'\!'
    t.type = '!'
    return t

def t_equal(t):
    r'\='
    t.type = '='
    return t

def t_divide(t):
    r'/'
    t.type = '/'
    return t

def t_times(t):
    r'\*'
    t.type = '*'
    return t

def t_minus(t):
    r'-'
    t.type = '-'
    return t

def t_plus(t):
    r'\+'
    t.type = '+'
    return t

def t_lbrace(t):
    r'\{'
    t.type = '{'
    return t

def t_rbrace(t):
    r'\}'
    t.type = '}'
    return t


def t_T_STRINGCONSTANT(t):
    r'"[^\n|"]*(")?'
    if not re.match('"[^\n]*"', t.value):
        print("*** Error in line: " + str(t.lineno))
        print("*** Unterminated string constant: " + t.value)
        t.lexer.lineno += 1
        t.lexer.skip(1)
        return
    return t


def t_T_DoubleConstant(t):
    #r'([0-9]+)(\.)((E|e)\+)?([0-9])*((E|e)\+)?([0-9]+)'
    r'([0-9]+)(\.)(((E|e)\+)?([0-9])*(\.)?|((E|e)\+)?([0-9]+)(\.)?)'
    return t

def t_T_IntConstant(t):
    r'(0(x|X)[\d|A-Fa-f]+)|([\d]+)'
    #t.value = t.value
    return t

def t_T_IDENTIFIER(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    if len(t.value)>31:
        print("*** Error in line: " + str(t.lineno))
        print("*** Identifier too long: " + t.value)
        t.lexer.skip(1)
    return t


def t_dot(t):
    r'(\.)'
    t.type = '.'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



def t_error(t):
    print("*** Error in line: " + str(t.lineno))
    print("*** Unrecognized character: " + t.value[0])
    t.lexer.skip(1)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    colNumber = (token.lexpos - line_start) + 1
    return str(colNumber) + " - " + str(colNumber - 1 + len(str(token.value).strip()))

def find_column_start(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def find_type(tok):
    if tok.type in literals:
        return '\''+ tok.type + '\''
    else:
        return tok.type

def find_value(tok):
    if tok.type == 'T_IntConstant':
        if 'x' in str(tok.value) or 'X' in str(tok.value):
            return "(value= " + str(int(tok.value,16)) + ")"
        else:
            return "(value= " + str(int(tok.value)) + ")"
    elif tok.type == "T_STRINGCONSTANT" or tok.type == "T_BoolConstant":
        return "(value= " + str(tok.value) + ")"
    elif tok.type == 'T_IDENTIFIER' and len(tok.value) > 31:
        return "(truncated to " + str(tok.value)[0:31] + ")"
    elif tok.type == 'T_DoubleConstant':
        result = re.sub(r'((E|e)\+[0-9]*)', '0', str(tok.value))
        serach = re.search(r'((E|e)\+[0-9]*)', str(tok.value), re.M | re.I)
        if serach:
            power = serach.group()[2:]
            result = float(result)*pow(10,int(power))
            return "(value= " + str(result) + ")"
        else:
            return "(value= " + str(tok.value) + ")"
    else:
        return ""


def gettoken(data):
    ls = []
    lexer.input(data)
    while True:
        tk = lexer.token()
        if not tk:
            break
        ls.append(tk)
    return ls

lexer = lex.lex()

if __name__ == "__main__":
    #fileName = sys.argv[1]
    fileName = "Input/1.frag"
    f = open(fileName, "r")
    data = f.read()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok.value, '    line', tok.lineno, 'Cols ', find_column(data,tok),' is ', find_type(tok), find_value(tok))