# -*- encoding: utf-8 -*-
import re

def tokenizer(input):
	current = 0;
	tokens = []

	while current < len(input):
		char = input[current]

		NUMBER = r'[0-9]|\.'
		LETTER = r'[a-z]|[A-Z]'

		if char == '"':
			value = ''

			if current == (len(input) - 1):
				break

			current += 1
			char = input[current]

			while char != '"':
				value += char
				current += 1
				char = input[current]

			tokens.append({'type': 'quoted-string', 'value': value})

			continue

		if char == '\'':
			value = ''

			if current == (len(input) - 1):
				break

			current += 1
			char = input[current]

			while char != '\'':
				value += char
				current += 1
				char = input[current]

			tokens.append({'type': 'single-quote-string', 'value': value})

			continue

		if re.search(NUMBER, char):
			value = ''
			type = 'int'

			while re.search(NUMBER, char):
				value += char

				if current == (len(input) - 1):
					break

				current += 1
				char = input[current]

			if value.find('.') > -1:
				type = 'float'

			tokens.append({'type': type, 'value': value})

			if current == (len(input) - 1):
				break

			continue

		if re.search(LETTER, char):
			value = ''

			if current == (len(input) - 1):
				break

			while re.search(LETTER, char):
				value += char

				if current == (len(input) - 1):
					break

				current += 1
				char = input[current]

			if value == 'true' or value == 'false':
				tokens.append({'type': 'boolean', 'value': value})

			continue

		if char == ' ' or char == '\n':
			if current == (len(input) - 1):
				break

			current += 1

			continue

		if char == '+':
			if current == (len(input) - 1):
				break

			current += 1

			tokens.append({ 'type': 'operation', 'value': char })

			continue

		raise TypeError('Unknown char: "%s"' % (char))

	return tokens

def parser(tokens):
	current = 0

	def base_ast(token):
		if token['type'] == 'quoted-string':
			return {
				'type': 'QuotedStringLiteral',
				'value': token['value']
			}
		elif token['type'] == 'single-quote-string':
			return {
				'type': 'SingleQuoteStringLiteral',
				'value': token['value']
			}
		elif token['type'] == 'int':
			return {
				'type': 'IntLiteral',
				'value': token['value']
			}
		elif token['type'] == 'float':
			return {
				'type': 'FloatLiteral',
				'value': token['value']
			}
		elif token['type'] == 'boolean':
			return {
				'type': 'BooleanLiteral',
				'value': token['value']
			}

		raise TypeError(token['type'])

	def walk():
		token = tokens[current]

		if token['type'] == 'quoted-string':
			return base_ast(token)
		elif token['type'] == 'single-quote-string':
			return base_ast(token)
		elif token['type'] == 'int':
			return base_ast(token)
		elif token['type'] == 'float':
			return base_ast(token)
		elif token['type'] == 'boolean':
			return base_ast(token)
		elif token['type'] == 'operation' and token['value'] == '+':
			node = {
				'type': 'OperationExpression',
				'value': token['value'],
			}

			node['left'] = base_ast(tokens[current - 1])
			node['right'] = base_ast(tokens[current + 1])

			return node

		raise TypeError(token['type'])

	ast = {
		'type': 'Program',
		'body': []
	}

	while current < len(tokens):
		ast['body'].append(walk())
		has_operation = len([x for x in filter(lambda n: n['type'] == 'OperationExpression', ast['body'])]) > 0
		if has_operation:
			ast['body'] = [x for x in filter(lambda n: n['type'] != 'IntLiteral', ast['body'])]
		current += 1

	return ast

def traverse(ast, visitor):
	def traverseArray(array, parent):
		if array:
			for child in array:
				traverseNode(child, parent)

	def traverseNode(node, parent):
		if node['type'] in visitor.keys():
			methods = visitor[node['type']]

		if not node['type'] in visitor.keys():
			methods = None

		if methods and methods['enter']:
			methods['enter'](node, parent)

		if node['type'] == 'Program':
			traverseArray(node['body'], node)
		elif node['type'] == 'QuotedStringLiteral':
			pass
		elif node['type'] == 'SingleQuoteStringLiteral':
			pass
		elif node['type'] == 'IntLiteral':
			pass
		elif node['type'] == 'FloatLiteral':
			pass
		elif node['type'] == 'BooleanLiteral':
			pass
		elif node['type'] == 'OperationExpression':
			pass
		else:
			raise TypeError(node['type'])

		if methods and methods['exit']:
			methods['exit'](node, parent)

	traverseNode(ast, None)

def transformer(ast):
	newAst = {
		'type': 'Program',
		'body': []
	}

	ast['_context'] = newAst['body']

	def enterQuotedStringLiteral(node, parent):
		parent['_context'].append({
			'type': 'QuotedStringLiteral',
			'value': node['value']
		})

	def exitQuotedStringLiteral(node, parent):
		pass

	def enterSingleQuoteStringLiteral(node, parent):
		parent['_context'].append({
			'type': 'SingleQuoteStringLiteral',
			'value': node['value']
		})

	def exitSingleQuoteStringLiteral(node, parent):
		pass

	def enterIntLiteral(node, parent):
		parent['_context'].append({
			'type': 'IntLiteral',
			'value': node['value']
		})

	def exitIntLiteral(node, parent):
		pass

	def enterFloatLiteral(node, parent):
		parent['_context'].append({
			'type': 'FloatLiteral',
			'value': node['value']
		})

	def exitFloatLiteral(node, parent):
		pass

	def enterBooleanLiteral(node, parent):
		parent['_context'].append({
			'type': 'BooleanLiteral',
			'value': node['value']
		})

	def exitBooleanLiteral(node, parent):
		pass

	def enterOperationStatement(node, parent):
		parent['_context'].append({
			'type': 'OperationStatement',
			'expression': {
				'type': 'OperationExpression',
				'value': node['value'],
				'left': node['left'],
				'right': node['right']
			}
		})

	def exitOperationStatement(node, parent):
		pass

	traverse(ast, {
		'QuotedStringLiteral': {
			'enter': enterQuotedStringLiteral,
			'exit': exitQuotedStringLiteral
		},

		'SingleQuoteStringLiteral': {
			'enter': enterSingleQuoteStringLiteral,
			'exit': exitSingleQuoteStringLiteral
		},

		'IntLiteral': {
			'enter': enterIntLiteral,
			'exit': exitIntLiteral
		},

		'FloatLiteral': {
			'enter': enterFloatLiteral,
			'exit': exitFloatLiteral
		},

		'BooleanLiteral': {
			'enter': enterBooleanLiteral,
			'exit': exitBooleanLiteral
		},

		'OperationExpression': {
			'enter': enterOperationStatement,
			'exit': exitOperationStatement
		}
	})

	return newAst

def code_generator(node):
	if node['type'] == 'Program':
		return '\n'.join(map(code_generator, node['body']))
	elif node['type'] == 'QuotedStringLiteral':
		return '"%s"' % (node['value'])
	elif node['type'] == 'SingleQuoteStringLiteral':
		return '\'%s\'' % (node['value'])
	elif node['type'] == 'IntLiteral':
		return '%s' % (node['value'])
	elif node['type'] == 'FloatLiteral':
		return '%s' % (node['value'])
	elif node['type'] == 'BooleanLiteral':
		return '%s' % (node['value'])
	elif node['type'] == 'OperationStatement':
		return '%s %s %s' % (node['expression']['left']['value'], node['expression']['value'], node['expression']['right']['value'])
	else:
		raise TypeError(node['type'])

def compiler(input):
	tokens = tokenizer(input)
	ast = parser(tokens)
	newAst = transformer(ast)
	out = code_generator(newAst)
	return out
