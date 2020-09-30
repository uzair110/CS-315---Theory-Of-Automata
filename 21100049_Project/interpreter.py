import ply.yacc as yacc
from numpy import *
import parser_1
import sys
import re

open_list = ["[","{","("] 
close_list = ["]","}",")"] 
lists = {}

var_array = {}
def check(myStr): 
    stack = [] 
    for i in myStr: 
        if i in open_list: 
            stack.append(i) 
        elif i in close_list: 
            pos = close_list.index(i) 
            if ((len(stack) > 0) and
                (open_list[pos] == stack[len(stack)-1])): 
                stack.pop() 
            else: 
                return "Unbalanced"
    if len(stack) == 0: 
        return "Balanced"
    else: 
        return "Unbalanced"

def IF_conditions(p):
	a = evaluate(p[1])
	if a == False:
		printing_function(p[2])

def slicing_list(p):
	integer_list = []
	arg1 = p[2][0]
	arg2 = p[2][1]
	name = p[1]
	for k,v in lists.items():
		if k == name:
			item = v
	for i in range(len(item)):
		if item[i] != ',' and item[i] != '[' and item[i] != ']':
			integer_list.append(int(item[i]))

	new_list = []
	for i in range(arg1,arg2):
		new_list.append(integer_list[i])
	return (new_list)

pushing = []
def pushing_list(p):
	name = p[1]
	string_list = []
	for k,v in lists.items():
		if name == k:
			item = v

	for i in range(len(item)):
		if item[i] != ',' and item[i] != '[' and item[i] != ']':
			pushing.append(str(item[i]))
	pushing.append(p[2][0])
	return (pushing)

indexer = []
def indexing(p):
	name = p[1]
	arg = p[2][0]
	for k,v in lists.items():
		if name == k:
			item = v
	return (pushing[arg])

def popping(p):
	name = p[1]
	arg = p[2][0]
	for k,v in lists.items():
		if name == k:
			item = v
	return (str(pushing[arg]))

def my_indexer(p):
	name = p[1]
	arg = p[2][0]
	for k,v in lists.items():
		if name == k:
			item = v
	if arg > len(pushing):
		print('OutOFBoundError')
		return
	return (str(pushing[arg]))

def IFELSE_conditions(p):
	a = p[0]
	b = p[1]
	return (a,b)

def printing_function(p):
	lister = p[2]
	for items in p[2]:
		print(items, end=" ")

def new_printing(p):
	u = p[2][0][0]
	if u == '+':
		print(evaluate(p[2][0]))
	for i in range(len(p[2])):
		a = p[2][i]
		for k,v in var_array.items():
			if k == a[1]:
				print(v, end=" ")


def for_function(p):
	# 
	if type(p) == tuple:
		if p[0] == 'call':
			if p[1] == 'PRINT':
				for i in range(len(p[2])):
					if type(p[2][i]) == tuple:
						print(evaluate(p[2][i]))
					if type(p[2][i]) == int:
						print((p[2][i]), end=" ")
					elif p[2][i][1] in var_array:
							for k, v in var_array.items():
								if k == p[2][i][1]:
									print(v, end=" ")
								else:
									print('Undeclared variable', p[2][i][1])
									return
					else:
						print((p[2][i]), end=' ')

def evaluate(p):
	global var_array
	if type(p) == tuple:	
		if p[0] == "++":
			if p[1][0] == "var":
				if p[1][1] not in var_array:
					return ('Name {} is not defined').format(p[1][1])
				else:
					var_array[p[1][1]]= var_array[p[1][1]] + 1
					# return var_array[p[1][1]]
			else:
				return evaluate(p[1])+1
		if p[0] == "--":
			if p[1][0] == "var":
				if p[1][1] not in var_array:
					return ('Name {} is not defined').format(p[1][1])
				else:
					var_array[p[1][1]]= var_array[p[1][1]] - 1
					return var_array[p[1][1]]
			else:
				return evaluate(p[1])-1
		if p[0] == "+":
			a = evaluate(p[1])
			if type(p[2]) == tuple:
				b = evaluate(p[2])
			else:
				b = evaluate(p[2])
			if (type(a) == int and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			if type(a) == str and type(b) == str:
				x = a + b
				return x
			return evaluate(p[1]) + evaluate(p[2])
		if p[0] == "-":
			a = evaluate(p[1])
			b = evaluate(p[2])
			if (type(a) == str and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			return evaluate(p[1]) - evaluate(p[2])
		if p[0] == "*":
			a = evaluate(p[1])
			b = evaluate(p[2])
			if (type(a) == str and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			return evaluate(p[1]) * evaluate(p[2])
		if p[0] == "/":
			a = evaluate(p[1])
			b = evaluate(p[2])
			if (type(a) == str and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			if evaluate(p[2]) == 0:
				return 'NaN'
			return double(evaluate(p[1]) / evaluate(p[2]))
		if p[0] == "@":
			a = evaluate(p[1])
			b = evaluate(p[2])
			if (type(a) == str and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			return evaluate(p[1])**evaluate(p[2])
		if p[0] == "%":
			a = evaluate(p[1])
			b = evaluate(p[2])
			if (type(a) == str and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			return (evaluate(p[1]) % evaluate(p[2]))
		if p[0] == "<":
			if evaluate(p[1]) < evaluate(p[2]):
				return True
			return False
		if p[0] == "<=":
			a = evaluate(p[1])
			b = evaluate(p[2])
			if type(a) != type(b):
				return ("Types ghalat hain Janab!")
				return
			if evaluate(p[1]) <= evaluate(p[2]):
				return True
			return False
		if p[0] == ">":
			a = evaluate(p[1])
			b = evaluate(p[2])
			if type(a) != type(b):
				return ("Types ghalat hain Janab!")
				return
			if evaluate(p[1]) > evaluate(p[2]):
				return True
			return False
		if p[0] == ">=":
			a = evaluate(p[1])
			b = evaluate(p[2])
			if type(a) != type(b):
				return ("Types ghalat hain Janab!")
				return
			if evaluate(p[1]) >= evaluate(p[2]):
				return True
			return False
		if p[0] == "==":
			a = evaluate(p[1])
			b = evaluate(p[2])
			if type(a) != type(b):
				return ("Types ghalat hain Janab!")
				return
			if evaluate(p[1]) == evaluate(p[2]):
				return True
			return False
		if p[0] == "!=":
			if evaluate(p[1]) != evaluate(p[2]):
				return True
			return False
		elif p[0] == '=':
			if p[2] in var_array:
				return 'Variable already declared!'
			var_array[p[2]] = evaluate(p[3])
			# print(var_array)
		if p[0] == 'nvar':
			if p[1] not in var_array:
				return ('Name {} is not defined').format(p[1])
			return -1*var_array[p[1]]
				
		elif p[0] == 'var':
			if p[1] not in var_array:
				return ('Name {} is not defined').format(p[1])
			return var_array[p[1]]

	else:
		return p

def evaluate1(p):
	global var_array
	if type(p) == tuple:	
		if p[0] == "++":
			if p[1][0] == "var":
				if p[1][1] not in var_array:
					return ('Name {} is not defined').format(p[1][1])
				else:
					var_array[p[1][1]]= var_array[p[1][1]] + 1
					return var_array[p[1][1]]
			else:
				return evaluate1(p[1])+1
		if p[0] == "--":
			if p[1][0] == "var":
				if p[1][1] not in var_array:
					return ('Name {} is not defined').format(p[1][1])
				else:
					var_array[p[1][1]]= var_array[p[1][1]] - 1
					return var_array[p[1][1]]
			else:
				return evaluate1(p[1])-1
		if p[0] == "+":
			a = evaluate1(p[1])
			if type(p[2]) == tuple:
				b = popping(p[2])
			else:
				b = evaluate1(p[2])
			if (type(a) == int and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			if type(a) == str and type(b) == str:
				x = a + b
				return x
			return evaluate1(p[1]) + evaluate1(p[2])
		if p[0] == "-":
			a = evaluate1(p[1])
			b = evaluate1(p[2])
			if (type(a) == str and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			return evaluate1(p[1]) - evaluate1(p[2])
		if p[0] == "*":
			a = evaluate1(p[1])
			b = evaluate1(p[2])
			if (type(a) == str and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			return evaluate1(p[1]) * evaluate1(p[2])
		if p[0] == "/":
			a = evaluate1(p[1])
			b = evaluate1(p[2])
			if (type(a) == str and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			if evaluate1(p[2]) == 0:
				return 'NaN'
			return double(evaluate1(p[1]) / evaluate1(p[2]))
		if p[0] == "@":
			a = evaluate1(p[1])
			b = evaluate1(p[2])
			if (type(a) == str and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			return evaluate1(p[1])**evaluate1(p[2])
		if p[0] == "%":
			a = evaluate1(p[1])
			b = evaluate1(p[2])
			if (type(a) == str and type(b) == str) or (type(a) == str and type(b) == int):
				return ("Types ghalat hain Janab!")
				return
			return (evaluate1(p[1]) % evaluate1(p[2]))
		if p[0] == "<":
			if evaluate1(p[1]) < evaluate1(p[2]):
				return True
			return False
		if p[0] == "<=":
			a = evaluate1(p[1])
			b = evaluate1(p[2])
			if type(a) != type(b):
				return ("Types ghalat hain Janab!")
				return
			if evaluate1(p[1]) <= evaluate1(p[2]):
				return True
			return False
		if p[0] == ">":
			a = evaluate1(p[1])
			b = evaluate1(p[2])
			if type(a) != type(b):
				return ("Types ghalat hain Janab!")
				return
			if evaluate1(p[1]) > evaluate1(p[2]):
				return True
			return False
		if p[0] == ">=":
			a = evaluate1(p[1])
			b = evaluate1(p[2])
			if type(a) != type(b):
				return ("Types ghalat hain Janab!")
				return
			if evaluate1(p[1]) >= evaluate1(p[2]):
				return True
			return False
		if p[0] == "==":
			a = evaluate1(p[1])
			b = evaluate1(p[2])
			if type(a) != type(b):
				return ("Types ghalat hain Janab!")
				return
			if evaluate1(p[1]) == evaluate1(p[2]):
				return True
			return False
		if p[0] == "!=":
			if evaluate1(p[1]) != evaluate1(p[2]):
				return True
			return False
		elif p[0] == '=':
			if p[2] in var_array:
				return ('Variable already declared!')
			var_array[p[2]] = evaluate1(p[3])
			# print(var_array)
		if p[0] == 'nvar':
			if p[1] not in var_array:
				return ('Name {} is not defined').format(p[1])
			return -1*var_array[p[1]]
				
		elif p[0] == 'var':
			if p[1] not in var_array:
				return ('Name {} is not defined').format(p[1])
			return var_array[p[1]]

	else:
		return p

# file = open(sys.argv[1], encoding='utf-8')
# data = file.readlines()
# for line in data:
# 	my_parser = yacc.yacc(module=parser_1)
# 	print('\n')
# 	print(line)
# 	# s = input('>> ')
# 	a=my_parser.parse(line)
# 	print(a)
# 	if a[0] == 'IF':
# 		IF_conditions(a)
# 	if a[1] == '(' or a[1] == '((':
# 		print(evaluate(a[0]))
# 	if a[1] == 'PRINT':
# 		for_function(a)
# 	else:
# 		print(evaluate(a))


file = open(sys.argv[1], encoding='utf-8')

if sys.argv[1] == 'standard_output.txt':
	print('Welcome to my YALP Interpreter')
	print('Output:')
	data = file.readlines()
	for lines in data:
		my_parser = yacc.yacc(module=parser_1)
		
		# s = input('')
		a=my_parser.parse(lines)
		printing_function(a)

						
if sys.argv[1] == 'variables.txt':
	print('Welcome to my YALP Interpreter')
	print('Output:')
	data = file.readlines()
	for lines in data:
		my_parser = yacc.yacc(module=parser_1)
		# s = input('')
		a=my_parser.parse(lines)
		if a[0] != 'call':
			res = evaluate(a)
			if res != None:
				print(res)
		else:
			new_printing(a)


if sys.argv[1] == 'expressions.txt' or sys.argv[1] == 'if_else.txt':
	print('Welcome to my YALP Interpreter')
	print('Output:')
	data = file.readlines()
	for lines in data:
		my_parser = yacc.yacc(module=parser_1)
		# s = input('')
		a=my_parser.parse(lines)
		if a[0] == 'indexing':
			print(my_indexer(a))
		if a[0] == 'pop':
			print(popping(a))
		if a[0] == 'index':
			print(indexing(a))
		if a[0] == 'push':
			pushing_list(a)
		if a[1] == 'LIST':
			lists[a[2]] = a[3]
		if a[0] == 'slice':
			print(slicing_list(a))
		if a[0] == 'IF':
			IF_conditions(a)
		if a[1] == '(' or a[1] == '((':
			print(evaluate(a[0]))
		if a[1] == 'PRINT':
			b = a[2][0]
			if type(a[2][0]) == str:
				h_index = re.findall('index',b)
				h_slice = re.findall('slice',b)
				h_sindex = re.findall(']',b)
				if 'index' in h_index:
					x = my_parser.parse(b)
					print(indexing(x))
						
				if 'slice' in h_slice:
					x = my_parser.parse(b)
					print(slicing_list(x))
						
				if ']' in h_sindex:
					x = my_parser.parse(b)
					print(my_indexer(x))
			new_printing(a)
		else:
			x = evaluate(a)
			if x != None:
				print(x)

if sys.argv[1] == 'lists.txt':
	print('Welcome to my YALP Interpreter')
	print('Output:')
	data = file.readlines()
	for lines in data:
		my_parser = yacc.yacc(module=parser_1)
		# s = input('')
		a=my_parser.parse(lines)
		if a[0] == 'indexing':
			my_indexer(a)
		if a[0] == 'pop':
			popping(a)
		if a[0] == 'index':
			print(indexing(a))
		if a[0] == 'push':
			pushing_list(a)
		if a[1] == 'LIST':
			lists[a[2]] = a[3]
		if a[0] == 'slice':
			print(slicing_list(a))
		if a[0] == 'IF':
			IF_conditions(a)
		if a[1] == '(' or a[1] == '((':
			print(evaluate1(a[0]))
		if a[1] == 'PRINT':
			b = a[2][0]
			if type(a[2][0]) == str:
				h_index = re.findall('index',b)
				h_slice = re.findall('slice',b)
				h_sindex = re.findall(']',b)
				if 'index' in h_index:
					x = my_parser.parse(b)
					res = indexing(x)
					if res != None:
						print(res)
						
				if 'slice' in h_slice:
					x = my_parser.parse(b)
					res = slicing_list(x)
					if res != None:
						print(res)
						
				if ']' in h_sindex:
					x = my_parser.parse(b)
					res = my_indexer(x)
					if res != None:
						print(res)
			new_printing(a)
		else:
			x = evaluate1(a)
			if x != None:
				print(x)


			
