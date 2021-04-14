# -*- encoding: utf-8 -*-
def tokenizer(input):
	current = 0;
	tokens = []

	while current < len(input):
		char = input[current]
		stringEnding = False

		if char == '"':
			value = ''

			try:
				current += 1
				char = input[current]
			except Exception:
				stringEnding = True

			while char != '"':
				value += char
				current += 1
				char = input[current]

			if not stringEnding:
				tokens.append({'type': 'string', 'value': value})

			continue

		raise TypeError('Unknown char: "%s"' % (char))

	return tokens

def parser(tokens):
	current = 0

	def walk():
		token = tokens[current]

		if token['type'] == 'string':
			return {
				'type': 'StringLiteral',
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
		elif node['type'] == 'StringLiteral':
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

	def enterStringLiteral(node, parent):
		parent['_context'].append({
			'type': 'StringLiteral',
			'value': node['value']
		})

	def exitStringLiteral(node, parent):
		pass

	traverse(ast, {
		'StringLiteral': {
			'enter': enterStringLiteral,
			'exit': exitStringLiteral
		}
	})

	return newAst

def code_generator(node):
	if node['type'] == 'Program':
		return '\n'.join(map(code_generator, node['body']))
	elif node['type'] == 'StringLiteral':
		return '"%s"' % (node['value'])
	else:
		raise TypeError(node['type'])

def compiler(input):
	tokens = tokenizer(input)
	ast = parser(tokens)
	newAst = transformer(ast)
	out = code_generator(newAst)
	return out
