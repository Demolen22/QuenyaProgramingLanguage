import ply.lex as lex
import ply.yacc as yacc
import sys
from lexer import Lexer
from parser import Parser

lexer_ = Lexer().lexer
parser_ = Parser(lexer_).parser

try:
    file = open(sys.argv[1])
    result = parser_.parse(file.read())
except Exception:
    print("Parser error")