import ply.lex as lex

from numpy import *

tokens = [
	'INT',
	'DOUBLE',
	'CHAR',
	'STRING',
	'BOOL',
	'PLUS',
	'MINUS',
	'DIVIDE',
	'MULTIPLY',
	'EQUALS',
	'MOD',
	'POWER',
	'INCREMENT',
	'DECREMENT',
	'EQUALEQUAL',
	'ANDAND',       # &&
	'COMMA',        # ,
	'DIVIDE',       # /
	'ELSE',         # else
	'EQUAL',        # =
	'EQUALEQUAL',   # ==
	'FALSE',        # false
	'IDENTIFIER',     # function
	'GE',           # >=
	'GT',           # >
	'IDENTIFIER',   # factorial
	'IF',           # if
	'LBRACE',       # {
	'LE',           # <=
	'LPAREN',       # (
	'LT',           # <
	'NOT',          # !
	'RBRACE',       # }
	'RETURN',       # return
	'RPAREN',       # )
	'SEMICOLON',   # ;	
	'TYPE',
	'VAR',
	'OROR',
	'NOTEQUAL',
	'TRUE',
	'IF',
	'ELSEIF',
	'ELSE',
	'RBRACE',
	'LBRACE',
	'LIST',
	'DOT',
	'slice',
	'push',
	'pop',
	'index',
	'LBRACKET',
	'RBRACKET'

]


t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
t_MOD = r'\%'
t_POWER = r'\@'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\-\-'
t_GE = r'\>\='
t_GT = r'\>'
t_LE = r'\<\='
t_LT = r'\<'
t_EQUALEQUAL = r'\=\='
t_NOTEQUAL = r'\!\='
t_NOT = r'\!'
t_OROR = r'\|\|'
t_ANDAND = r'\&\&'
t_LPAREN = r'\(+'
t_RPAREN = r'\)+'
t_COMMA = r'\,'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_ignore=r' \n'



def t_TYPE(t):
	r'\bINT\b | \bSTRING\b | \bDOUBLE\b | \bCHAR\b | \bBOOL\b | \bLIST\b'
	return t


def t_LIST(t):
	r'\[[0-9]*(,[0-9]+)*\]'
	# t.value = t.value[1:-1]
	return t


def t_IF(t):
	r'IF'
	# print(t.value)
	return t
	
def t_ELSE(t):
	r'ELSE'
	# print(t.value)
	return t

def t_IFELSEIF(t):
    r'ELSEIF'
    # print(t.value)
    return t

def t_slice(t):
	r'slice'
	return t

def t_push(t):
	r'push'
	return t

def t_pop(t):
	r'pop'
	return t

def t_index(t):
	r'index'
	return t

def t_DOUBLE(t):
	r'\d+\.\d+'
	t.value = double(t.value)
	return t

def t_INT(t):
	r'[-]?\d+'
	t.value = int(t.value)
	return t

def t_STRING(t):
	r'\"[^+\n]*\"'
	t.value = t.value[1:-1]
	t.type = 'STRING'
	# print('here',t)
	return t

def t_BOOL(t):
	r'\bFALSE\b | \bTRUE\b'
	t.type = 'BOOL'
	return t

def t_VAR(t):
	r'[a-z_][a-zA-Z_0-9]*'
	t.type = 'VAR'
	return t

def t_IDENTIFIER(token):
		r'[A-Z][A-Za-z_]*'
		token.type = 'IDENTIFIER'
		return token

def t_CHAR(t):
	r'\'[a-zA-Z]\''
	t.type = 'CHAR'
	return t


def t_error(t):
	print('')
	t.lexer.skip(1)


lexer = lex.lex()