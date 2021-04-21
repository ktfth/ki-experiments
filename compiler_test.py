# -*- encoding: utf-8 -*-
import unittest

from compiler import tokenizer
from compiler import parser
from compiler import transformer
from compiler import code_generator
from compiler import compiler

class TestQuotedStringLiteralCompilation(unittest.TestCase):

	def setUp(self):
		self.input = '"hello world"'
		self.output = '"hello world"'

		self.tokens = [
			{ 'type': 'quoted-string', 'value': 'hello world' }
		]

		self.ast = {
			'type': 'Program',
			'body': [{
				'type': 'QuotedStringLiteral',
				'value': 'hello world',
			}]
		}

		self.newAst = {
			'type': 'Program',
			'body': [{
				'type': 'QuotedStringLiteral',
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

class TestSingleQuoteStringLiteralCompilation(unittest.TestCase):

	def setUp(self):
		self.input = '\'hello world\''
		self.output = '\'hello world\''

		self.tokens = [
			{ 'type': 'single-quote-string', 'value': 'hello world' }
		]

		self.ast = {
			'type': 'Program',
			'body': [{
				'type': 'SingleQuoteStringLiteral',
				'value': 'hello world',
			}]
		}

		self.newAst = {
			'type': 'Program',
			'body': [{
				'type': 'SingleQuoteStringLiteral',
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

class TestIntLiteralCompilation(unittest.TestCase):

	def setUp(self):
		self.input = '10'
		self.output = '10'

		self.tokens = [{'type': 'int', 'value': '10'}]

		self.ast = {
			'type': 'Program',
			'body': [{
				'type': 'IntLiteral',
				'value': '10'
			}]
		}

		self.newAst = {
			'type': 'Program',
			'body': [{
				'type': 'IntLiteral',
				'value': '10'
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

class TestFloatLiteralCompilation(unittest.TestCase):

	def setUp(self):
		self.input = '1.5'
		self.output = '1.5'

		self.tokens = [{'type': 'float', 'value': '1.5'}]

		self.ast = {
			'type': 'Program',
			'body': [{
				'type': 'FloatLiteral',
				'value': '1.5'
			}]
		}

		self.newAst = {
			'type': 'Program',
			'body': [{
				'type': 'FloatLiteral',
				'value': '1.5'
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

class TestTrueBooleanLiteralCompilation(unittest.TestCase):

	def setUp(self):
		self.input = 'true'
		self.output = 'true'

		self.tokens = [{'type': 'boolean', 'value': 'true'}]

		self.ast = {
			'type': 'Program',
			'body': [{
				'type': 'BooleanLiteral',
				'value': 'true'
			}]
		}

		self.newAst = {
			'type': 'Program',
			'body': [{
				'type': 'BooleanLiteral',
				'value': 'true'
			}]
		}

	def test_tokenization(self):
		self.assertEqual(tokenizer(self.input), self.tokens)

	def test_parsing(self):
		self.assertEqual(parser(self.tokens), self.ast)

	def test_transformation(self):
		self.assertEqual(transformer(self.ast), self.newAst)

if __name__ == '__main__':
	unittest.main()
