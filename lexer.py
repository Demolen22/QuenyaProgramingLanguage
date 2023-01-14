import ply.lex as lex
import ply.yacc as yacc
import sys
from ply.lex import TOKEN


class Lexer:

    def __init__(self):
        print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)
        self.reserved = {
            'lav': 'IF',
            'san': 'THEN',
            'eldarissa': 'ELSE',
            'yare': 'LOOP',
            'an': 'ITERABLE_LOOP',
            'ahya': 'VARIABLE',
            'iluve': 'INT',
            'tema': 'STRING',
            'tulca': 'FUNCTION',
            'lusta': 'NULL',
            'entulesse': 'RETURN',
            'esse': 'BEGIN',
            'lanca': 'END',
            'tec': 'PRINT',
            'hyalin': 'LIST'
        }

    tokens = [
        'COMMENT',
        'STRING_EXPR',
        'ID',
        'NUMBER',
        'LESSER_EQ',
        'GREATER_EQ',
        'DIV',
        'MULT',
        'PLUS',
        'MINUS',
        'MOD'
        'OPEN_BRACKET',
        'CLOSE_BRACKET',
        'OPEN_CURL_BRACKET',
        'CLOSE_CURL_BRACKET',
        'OPEN_SQ_BRACKET',
        'CLOSE_SQ_BRACKET',
        'EQUAL',
        'ASSIGN',
        'LESSER',
        'GREATER',
        'AND',
        'OR',
        'XOR',
        'NOT'
        'ENDLINE',
        'error'

    ]

    def __del__(self):
        print('Lexer destructor called.')

    def t_COMMENT(self, t):
        r'\@.*\;' # czy z takiego czegos zrobic produkcje
        print("COMMENT:", t.value)

    def t_STRING_EXPR(self, t):
        # r'\{[a-zA-Z0-9_\+\-\*\/\%\(\)\{\}\[\]\=\:\<\>\&\|\!\~\;\@\s]*\}'
        r'\{.*\}'
        print("STRING_EXPR:", t.value[1:-1])

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ID')
        if t.value in self.reserved.keys():
            print("RESERVED:", t.type)
        else:
            print("ID:", t.value)

    # def t_INV_NUM_ERROR(self, t): #czy mozna tak robic czy trzeba tak definiowac zeby byl jeden error na koncu jak nie pasuje do niczego
    #     r'[0].*'
    #     print("INVALID_NUMBER_ERROR:", t.value)

    def t_NUMBER(self, t): # czy to definiowac na etapie tokenow (to z 0) czy parsingu
        r'[0]|([1-9][0-9]*)' # w jaki sposob mozna sie odwolywac do innych tokenow w definicji? np do t_OPEN_BRACKET
        print("NUMBER:", t.value)

    def t_LESSER_EQ(self, t):
        r'\<='
        print("LESSER_EQ")

    def t_GREATER_EQ(self, t):
        r'\>='
        print("GREATER_EQ")

    def t_PLUS(self, t):
        r'\+'
        print("PLUS")

    def t_MINUS(self, t):
        r'\-'
        print("MINUS")

    def t_MULT(self, t):
        r'\*'
        print("MULT")

    def t_DIV(self, t):
        r'\/'
        print("DIV")

    def t_MOD(self, t):
        r'\%'
        print("MOD")

    def t_AND(self, t):
        r'\&'
        print("AND")

    def t_OR(self, t):
        r'\|'
        print("AND")

    def t_XOR(self, t):
        r'\!'
        print("XOR")

    def t_NOT(self, t):
        r'\~'
        print("NOT")

    def t_OPEN_BRACKET(self, t):
        r'\('
        print("OPEN_BRACKET")

    def t_CLOSE_BRACKET(self, t):
        r'\)'
        print("CLOSE_BRACKET")

    def t_OPEN_CURL_BRACKET(self, t):
        r'\)'
        print("CLOSE_CURL_BRACKET")

    def t_CLOSE_CURL_BRACKET(self, t):
        r'\)'
        print("CLOSE_CURL_BRACKET")

    def t_OPEN_SQ_BRACKET(self, t):
        r'\['
        print("OPEN_SQ_BRACKET")

    def t_CLOSE_SQ_BRACKET(self, t):
        r'\]'
        print("CLOSE_SQ_BRACKET")

    def t_ASSIGN(self, t):
        r'\:'
        print("ASSIGN")

    def t_EQUAL(self, t):
        r'\='
        print("EQUAL")

    def t_LESSER(self, t):
        r'\<'
        print("LESSER")

    def t_GREATER(self, t):
        r'\>'
        print("GREATER")

    def t_ENDLINE(self, t):
        r'\;'
        print("ENDLINE")

    def t_nl(self, t):
        r'(\n|\r|\r\n)|\s|\t'
        # print("NL")

    def t_error(self, t):
        r'.'
        print("ERROR:", t.value)
        t.lexer.skip(1)