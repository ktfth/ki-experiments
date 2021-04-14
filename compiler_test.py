# -*- encoding: utf-8 -*-
import unittest

from compiler import tokenizer

class TestStringLiteralCompilation(unittest.TestCase):

	def setUp(self):
		self.input = '"hello world"'
		self.output = '"hello world"'

		self.tokens = [
			{ 'type': 'string', 'value': 'hello world' }
		]

	def test_tokenization(self):
		self.assertEqual(tokenizer(self.input), self.tokens)

if __name__ == '__main__':
	unittest.main()
