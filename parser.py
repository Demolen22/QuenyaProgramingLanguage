from lexer import Lexer
import ply.yacc as yacc
import sys


class Parser:
    def __init__(self, lexer):
        print("Parser constructor called")
        self.parser = yacc.yacc(module=self)
        self.lexer = lexer

    def __del__(self):
        print('Parser destructor called.')

    tokens = Lexer.tokens

    # GRAMMAR
    def p_program_decl(self, p):
        '''
        program_decl : PROGRAM block
        '''
        print("program")


    def p_block(self, p):
        '''
        block : BEGIN lines END
        '''
        print("block")

    def p_lines(self, p):
        '''
        lines : lines line
                | line
        '''
        print("lines")

    def p_line(self, p):
        '''
        line : INT ID ASSIGN NUMBER ENDLINE
        '''
        print("line")

    def p_error(self, p):
        '''
        '''
        print("parser error")
