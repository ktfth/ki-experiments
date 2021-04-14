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

assert tokenizer('"hello world"') == [{'type': 'string', 'value': 'hello world'}]

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

assert parser([{'type': 'string', 'value': 'hello world'}]) == {
	'type': 'Program',
	'body': [{
		'type': 'StringLiteral',
		'value': 'hello world',
	}]
}
