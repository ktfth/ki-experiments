# -*- encoding: utf-8 -*-
import re

def tokenizer(input):
	current = 0;
	tokens = []

	while current < len(input):
		char = input[current]

		NUMBER = r'[0-9]|\.'

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

			if current == (len(input) - 1):
				break

			while re.search(NUMBER, char):
				value += char

				if current == (len(input) - 1):
					break

				current += 1
				char = input[current]

			if value.find('.') > -1:
				type = 'float'

			tokens.append({'type': type, 'value': value})

			continue

		raise TypeError('Unknown char: "%s"' % (char))

	return tokens

def parser(tokens):
	current = 0

	def walk():
		token = tokens[current]

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

		raise TypeError(token['type'])

	ast = {
		'type': 'Program',
		'body': []
	}

	while current < len(tokens):
		ast['body'].append(walk())
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
	else:
		raise TypeError(node['type'])

def compiler(input):
	tokens = tokenizer(input)
	ast = parser(tokens)
	newAst = transformer(ast)
	out = code_generator(newAst)
	return out
