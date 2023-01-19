import ply.lex as lex
import ply.yacc as yacc
import sys
from lexer import Lexer
from parser import Parser

lexer_ = Lexer().lexer
parser_ = Parser(lexer_).parser

file = open(sys.argv[1])
result = parser_.parse(file.read())
print("result", result)
# with file as fp:
#     for line in fp:
#         try:
#             lexer_.input(line)
#             for token in lexer_:
#                 pass
#         except EOFError:
#             break