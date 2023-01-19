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
        block : BEGIN block_body END
        '''
        print("block")

    def p_block_body(self, p):
        '''
        block_body : lines
                     | loop
                     | if_stat
                     | func_decl
        '''
        print('block_body')

    def p_lines(self, p):
        '''
        lines : lines line
                | line
        '''
        print('p_lines')

    def p_line(self, p):
        '''
        line : line_body ENDLINE
        '''
        print('p_line')

    def p_line_body(self, p):
        '''
        line_body : var_decl
                    | func_call
                    | var_assign
        '''
        print('line_body')

    def p_loop(self, p):
        '''
        loop : LOOP OPEN_BRACKET bool CLOSE_BRACKET block
        '''
        print('loop')

    def p_func_decl(self, p):
        '''
        func_decl : FUNCTION ID OPEN_BRACKET args CLOSE_BRACKET BEGIN block_body RETURN return_val
        '''
        print('func_decl')
    def p_return_val(self, p):
        '''
        return_val : ID
                     | bool
                     | func_call
        '''
        print('return_val')

    def p_var_decl(self, p):
        '''
        var_decl : type ID ASSIGN value
        '''
        print('var_decl')

    def p_var_assign(self, p):
        '''
        var_assign : ID ASSIGN value
        '''
        print('var_assign')

    def p_value(self, p):
        '''
        value : NUMBER
                | STRING_EXPR
                | func_call
                | expr
        '''
        print('value')

    def p_values(self, p):
        '''
        values : values value
                 | value
        '''
        print('value')

    def p_type(self, p):
        '''
        type : INT
               | STRING
        '''
        print('type')

    def p_func_call(self, p):
        '''
        func_call : ID OPEN_BRACKET values CLOSE_BRACKET
        '''
        print('func_call')

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
        print('args')

    def p_if_stat(self, p):
        '''
        if_stat : IF OPEN_BRACKET bool CLOSE_BRACKET THEN block_body end_if
        '''
        print('if_stat')

    def p_end_if(self, p):
        '''
        end_if : END
                 | else_stat
        '''
        print('end_if')

    def p_else_stat(self, p):
        '''
        else_stat : ELSE THEN block_body END
        '''
        print('else_stat')

    def p_expr(self, p):
        '''
        expr : expr oper_add comp
               | comp
        '''
        print('expr')

    def p_brac_expr(self, p):
        '''
        brac_expr : OPEN_BRACKET expr CLOSE_BRACKET
        '''
        print('brac_expr')

    def p_oper_add(self, p):
        '''
        oper_add : PLUS
                   | MINUS
        '''
        print('oper_add')

    def p_oper_mult(self, p):
        '''
        oper_mult : MULT
                    | DIV
        '''
        print('oper_mult')

    def p_factor(self, p):
        '''
        factor : ID
                 | NUMBER
                 | brac_expr
        '''
        print('factor')

    def p_comp(self, p):
        '''
        comp : comp oper_mult factor
               | factor
        '''
        print('comp')

    def p_bool(self, p):
        '''
        bool : bool bool_oper bool_fact_n
               | bool_fact_n
        '''
        print('bool')

    def p_bool_oper(self, p):
        '''
        bool_oper : AND
                    | OR
                    | XOR
                    | LESSER
                    | GREATER
                    | EQUAL
                    | LESSER_EQ
                    | GREATER_EQ
        '''
        print('bool_oper')

    def p_bool_br(self, p):
        '''
        bool_br : OPEN_BRACKET bool CLOSE_BRACKET
        '''
        print('bool_br')

    def p_bool_fact(self, p):
        '''
        bool_fact : bool_br
                    | ID
                    | NUMBER
        '''
        print('bool_fact')

    def p_bool_fact_n(self, p):
        '''
        bool_fact_n : bool_fact
                      | NOT bool_fact
        '''
        print('bool_fact_n')

    def p_error(self, p):
        '''
        '''
        print("ERROR")