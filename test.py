import ply.lex as lex
import ply.yacc as yacc
import sys
from lexer import Lexer

lexer_ = Lexer().lexer

file = open(sys.argv[1])

with file as fp:
    for line in fp:
        try:
            lexer_.input(line)
            for token in lexer_:
                pass
        except EOFError:
            break