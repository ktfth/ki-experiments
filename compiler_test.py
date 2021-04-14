# -*- encoding: utf-8 -*-
import unittest

from compiler import tokenizer
from compiler import parser
from compiler import transformer
from compiler import code_generator
from compiler import compiler

class TestStringLiteralCompilation(unittest.TestCase):

	def setUp(self):
		self.input = '"hello world"'
		self.output = '"hello world"'

		self.tokens = [
			{ 'type': 'string', 'value': 'hello world' }
		]

		self.ast = {
			'type': 'Program',
			'body': [{
				'type': 'StringLiteral',
				'value': 'hello world',
			}]
		}

		self.newAst = {
			'type': 'Program',
			'body': [{
				'type': 'StringLiteral',
				'value': 'hello world'
			}]
		}

	def test_tokenization(self):
		self.assertEqual(tokenizer(self.input), self.tokens)

	def test_parsing(self):
		self.assertEqual(parser(self.tokens), self.ast)

	def test_transformation(self):
		self.assertEqual(transformer(self.ast), self.newAst)

	def test_code_generation(self):
		self.assertEqual(code_generator(self.newAst), self.output)

	def test_compilation(self):
		self.assertEqual(compiler(self.input), self.output)

if __name__ == '__main__':
	unittest.main()