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
        print("program", end="\n\n")

    def p_block(self, p):
        '''
        block : BEGIN block_body END
        '''
        print("block", end="\n\n")

    def p_block_body(self, p):
        '''
        block_body : lines
                     | loop
                     | if_stat
                     | func_decl
        '''
        print('block_body', end="\n\n")

    def p_lines(self, p):
        '''
        lines : lines line
                | line
        '''
        print('p_lines', end="\n\n")

    def p_line(self, p):
        '''
        line : line_body ENDLINE
        '''
        print('p_line', end="\n\n")

    def p_line_body(self, p):
        '''
        line_body : var_decl
                    | func_call
                    | var_assign
        '''
        print('line_body', end="\n\n")

    def p_loop(self, p):
        '''
        loop : LOOP OPEN_BRACKET expr CLOSE_BRACKET block
        '''
        print('loop', end="\n\n")

    def p_func_decl(self, p):
        '''
        func_decl : FUNCTION ID OPEN_BRACKET args CLOSE_BRACKET BEGIN block_body RETURN return_val
        '''
        print('func_decl', end="\n\n")
    def p_return_val(self, p):
        '''
        return_val : ID
                     | expr
                     | func_call
        '''
        print('return_val', end="\n\n")

    def p_var_decl(self, p):
        '''
        var_decl : type ID ASSIGN value
        '''
        print('var_decl', end="\n\n")

    def p_var_assign(self, p):
        '''
        var_assign : ID ASSIGN value
        '''
        print('var_assign', end="\n\n")

    def p_value(self, p):
        '''
        value : NUMBER
                | STRING_EXPR
                | func_call
                | expr
        '''
        print('value', end="\n\n")

    def p_values(self, p):
        '''
        values : values value
                 | value
        '''
        print('value', end="\n\n")

    def p_type(self, p):
        '''
        type : INT
               | STRING
        '''
        p[0] = p[1]
        print(p[0])
        print('type', end="\n\n")

    def p_func_call(self, p):
        '''
        func_call : ID OPEN_BRACKET values CLOSE_BRACKET
        '''
        print('func_call', end="\n\n")

    def p_arg(self, p):
        '''
        arg : type ID
        '''
        print('arg')

    def p_args(self, p):
        '''
        args : args arg
               | arg
        '''
        print('args', end="\n\n")

    def p_if_stat(self, p):
        '''
        if_stat : IF OPEN_BRACKET expr CLOSE_BRACKET THEN block_body end_if
        '''
        print('if_stat', end="\n\n")

    def p_end_if(self, p):
        '''
        end_if : END
                 | else_stat
        '''
        print('end_if', end="\n\n")

    def p_else_stat(self, p):
        '''
        else_stat : ELSE THEN block_body END
        '''
        print('else_stat', end="\n\n")

    def p_expr(self, p):
        '''
        expr : expr oper_add comp
               | comp
        '''
        if len(p) == 2:
            print(p[0], p[1])
            p[0] = p[1]
        else:
            if p[2] == '-':
                p[0] = p[1] - p[3]
            elif p[2] == '+':
                p[0] = p[1] + p[3]
        print(p[0])
        print('expr', end='\n\n')

    def p_brac_expr(self, p):
        '''
        brac_expr : OPEN_BRACKET expr CLOSE_BRACKET
        '''
        p[0] = p[2]
        print('brac_expr', end="\n\n")

    def p_oper_add(self, p):
        '''
        oper_add : PLUS
                   | MINUS
        '''
        p[0] = p[1]
        print('oper_add', end="\n\n")

    def p_oper_mult(self, p):
        '''
        oper_mult : MULT
                    | DIV
                    | MOD
                    | AND
                    | OR
                    | XOR
                    | LESSER
                    | GREATER
                    | EQUAL
                    | LESSER_EQ
                    | GREATER_EQ
        '''
        p[0] = p[1]
        print('oper_mult', end="\n\n")

    def p_factor(self, p):
        '''
        factor : ID
                 | NUMBER
                 | brac_expr
        '''
        p[0] = p[1]
        print(p[0])
        print('p_factor', end="\n\n")

    def p_factor_n(self, p):
        '''
        factor_n : NOT factor
                    | factor
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = not p[2]
        print(p[0])
        print('p_factor_n', end="\n\n")

    def p_comp(self, p):
        '''
        comp : comp oper_mult factor_n
               | factor_n
        '''
        if len(p) == 2:
            p[0] = p[1]
            print(p[0])
        elif p[2] == '*':
            p[0] = p[1] * p[3]
            print(p[0])
        elif p[2] == '/':
            if p[3] == 0:
                print('Cannot divide by 0')
                raise ZeroDivisionError
            else:
                p[0] = p[1] / p[3]
                print(p[0])
        print('comp')

    def p_error(self, p):
        '''
        '''
        print("ERROR")