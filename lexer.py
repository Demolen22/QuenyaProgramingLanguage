import ply.lex as lex
import ply.yacc as yacc
import sys
from ply.lex import TOKEN


class Lexer:

    def __init__(self):
        print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)
        self.reserved = {
            r'lav': 'IF',
            r'san': 'THEN',
            r'eldarissa': 'ELSE',
            r'yare': 'LOOP',
            r'an': 'ITERABLE_LOOP',
            r'iluve': 'INT',
            r'tema': 'STRING',
            r'tulca': 'FUNCTION',
            r'lusta': 'NULL',
            r'entulesse': 'RETURN',
            r'esse': 'BEGIN',
            r'lanca': 'END',
            r'tec': 'PRINT',
            r'hyalin': 'LIST',
            r'talma': 'PROGRAM'
        }

    tokens = [
        'COMMENT',
        'STRING_EXPR',

        'IF',
        'THEN',
        'ELSE',
        'LOOP',
        'ITERABLE_LOOP',
        'INT',
        'STRING',
        'FUNCTION',
        'NULL',
        'RETURN',
        'BEGIN',
        'END',
        'PRINT',
        'LIST',
        'PROGRAM',

        'ID',
        'NUMBER',
        'LESSER_EQ',
        'GREATER_EQ',
        'DIV',
        'MULT',
        'PLUS',
        'MINUS',
        'MOD',
        'OPEN_BRACKET',
        'CLOSE_BRACKET',
        'OPEN_CURL_BRACKET',
        'CLOSE_CURL_BRACKET',
        'OPEN_SQ_BRACKET',
        'CLOSE_SQ_BRACKET',
        'EQUAL',
        'N_EQUAL',
        'ASSIGN',
        'LESSER',
        'GREATER',
        'AND',
        'OR',
        'XOR',
        'NOT',
        'ENDLINE'
    ]

    def __del__(self):
        print('Lexer destructor called.')

    def t_COMMENT(self, t):
        r'\@.*\;'
        return t

    def t_STRING_EXPR(self, t):
        r'\{.*\}'
        t.value = t.value[1:-1]
        return t

    def t_IF(self, t):
        r'lav'
        return t

    def t_THEN(self, t):
        r'san'
        return t

    def t_ELSE(self, t):
        r'eldarissa'
        return t

    def t_LOOP(self, t):
        r'yare'
        return t

    def t_ITERABLE_LOOP(self, t):
        r'an'
        return t

    def t_INT(self, t):
        r'iluve'
        return t

    def t_STRING(self, t):
        r'tema'
        return t

    def t_FUNCTION(self, t):
        r'tulca'
        return t

    def t_NULL(self, t):
        r'lusta'
        return t

    def t_RETURN(self, t):
        r'entulesse'
        return t

    def t_BEGIN(self, t):
        r'esse'
        return t

    def t_END(self, t):
        r'lanca'
        return t

    def t_PRINT(self, t):
        r'tec'
        return t

    def t_LIST(self, t):
        r'hyalin'
        return t

    def t_PROGRAM(self, t):
        r'talma'
        return t

    def t_NUMBER(self, t):
        r'[0]|([1-9][0-9]*)'
        t.value = int(t.value)
        return t

    def t_LESSER_EQ(self, t):
        r'\<='
        return t

    def t_GREATER_EQ(self, t):
        r'\>='
        return t

    def t_PLUS(self, t):
        r'\+'
        return t

    def t_MINUS(self, t):
        r'\-'
        return t

    def t_MULT(self, t):
        r'\*'
        return t

    def t_DIV(self, t):
        r'\/'
        return t

    def t_MOD(self, t):
        r'\%'
        return t

    def t_AND(self, t):
        r'\&'
        return t

    def t_OR(self, t):
        r'\|'
        return t

    def t_XOR(self, t):
        r'\!'
        return t

    def t_NOT(self, t):
        r'\~'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        # t.type = self.reserved.get(t.value, 'ID')
        # if t.value in self.reserved.keys():
        #     print("RESERVED:", t.type)
        # else:
        #     print("ID:", t.value)
        return t

    def t_OPEN_BRACKET(self, t):
        r'\('
        return t

    def t_CLOSE_BRACKET(self, t):
        r'\)'
        return t

    def t_OPEN_CURL_BRACKET(self, t):
        r'\)'
        return t

    def t_CLOSE_CURL_BRACKET(self, t):
        r'\)'
        return t

    def t_OPEN_SQ_BRACKET(self, t):
        r'\['
        return t

    def t_CLOSE_SQ_BRACKET(self, t):
        r'\]'
        return t

    def t_ASSIGN(self, t):
        r'\:'
        return t

    def t_EQUAL(self, t):
        r'\='
        return t

    def t_N_EQUAL(self, t):
        r'\~='
        return t

    def t_LESSER(self, t):
        r'\<'
        return t

    def t_GREATER(self, t):
        r'\>'
        return t

    def t_ENDLINE(self, t):
        r'\;'
        return t

    def t_nl(self, t):
        r'(\n|\r|\r\n)|\s|\t'

    def t_error(self, t):
        r'.'
        print("ERROR:", t.value)
        t.lexer.skip(1)