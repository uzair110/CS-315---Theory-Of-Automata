import lexer
import ply.yacc as yacc
from numpy import *

tokens = lexer.tokens

precendence = (

	('left', 'OROR'),
	('left', 'ANDAND'),
	('left', 'EQUALEQUAL'),
	('left', 'LT', 'LE', 'GT', 'GE'),
	('left', 'PLUS', 'MINUS'),
	('left', 'POWER'),
	('left', 'MULTIPLY', 'DIVIDE')


	)

def p_function_calls(p):
	'''
	statement : expression
	'''
	p[0] = p[1]
	# evaluate(p[1])

def p_increment_decrement(p):
	'''
	expression : expression INCREMENT
			   | expression DECREMENT
	'''
	p[0] = (p[2], p[1])

def p_list_slice(p):
	'''
	expression : VAR DOT slice LPAREN args RPAREN
	'''
	p[0] = ('slice', p[1], p[5])

def p_push(p):
	'''
	expression : VAR DOT push LPAREN args RPAREN
	'''
	p[0] = ('push', p[1],p[5])

def p_pop(p):
	'''
	expression : VAR DOT pop LPAREN args RPAREN
	'''
	p[0] = ('pop', p[1],p[5])

def p_square_index(p):
	'''
	expression : VAR DOT args RBRACKET
	'''
	p[0] = ('indexing',p[1],p[3])

def p_index(p):
	'''
	expression : VAR DOT index LPAREN args RPAREN
	'''
	p[0] = ('index', p[1], p[5])

def p_expression_call(p):
	''' 
	expression : IDENTIFIER LPAREN args RPAREN
	'''
	p[0] = ('call', p[1], p[3])

def p_args(p):
	'''
	args : expression 
	'''
	p[0] = [p[1]]

def p_multiple_args(p):
	'''
	args : expression COMMA args
	'''
	p[0] = [p[1]] + p[3]

def p_no_args(p):
	'''
	args : 
	'''
	p[0] = []

def p_assignment(p):
	'''
	assignment : TYPE VAR
			   | VAR
	'''

def p_variable(p):
	'''
	statement : TYPE VAR EQUALS expression
	'''
	p[0] = ('=', p[1],p[2], p[4])
	

# def p_string_expression(p):
# 	'''
# 	expression : 
# 	'''

def p_string_addition(p):
	'''
	statement : STRING VAR EQUALS expression
	'''
	p[0] = p[4]


def p_expression_int_float(p):
	'''
	expression : INT
			   | DOUBLE
			   | CHAR
			   | STRING
			   | BOOL
			   | LIST
	'''
	# print('aaa')
	p[0] = p[1]

def p_block(p):
	'''
	block : expression compound
		  | empty
	'''
	p[0] = (p[1], p[2])


def p_IF_CONDITION(p):
	'''
	statement : IF expression compound 
	'''
	p[0] = ('IF',p[2], p[3])
	# print(p[8])

	
def p_compound(p):
	'''
	compound : LBRACE statement RBRACE

	'''
	p[0] = p[2]

def p_expression_variable(p):
	'''
	expression : VAR
	'''
	p[0] = ('var',p[1])

def p_negexpression_variable(p):
	'''
	expression : MINUS VAR
	'''
	p[0] = ('nvar',p[2])
	
def p_LPAREN(p):
	'''
	lPAREN : LPAREN
		   | empty
	'''
	p[0] = p[1]
	
def p_RPAREN(p):
	'''
	rPAREN : RPAREN
		   | empty
	'''
	p[0] = p[1]

def p_expression_brackets(p):
	'''
	expression : LPAREN expression RPAREN
	'''
	p[0]=p[2]
	

def p_expression(p):
	'''
    expression : expression PLUS expression
			   | expression MINUS expression
			   | expression DIVIDE expression
			   | expression MULTIPLY expression
			   | expression POWER expression
			   | expression MOD expression
			   | expression LT expression
			   | expression LE expression
			   | expression GT expression
			   | expression GE expression
			   | expression EQUALEQUAL expression
			   | expression ANDAND expression
			   | empty
	'''
	p[0] = (p[2], p[1], p[3])
	# print(p[0])
 

def p_error(p):
	print('')

def p_empty(p):
	'''
	empty :
	'''
	p[0] = None



