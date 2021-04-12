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
