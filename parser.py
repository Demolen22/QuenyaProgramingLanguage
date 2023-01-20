from lexer import Lexer
import ply.yacc as yacc
import sys


class Parser:
    def __init__(self, lexer):
        print("Parser constructor called")
        self.parser = yacc.yacc(module=self)
        self.lexer = lexer
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

    def __del__(self):
        print('Parser destructor called.')


    tokens = Lexer.tokens

    # GRAMMAR
    def p_program_decl(self, p):
        '''
        program_decl : PROGRAM block
        '''
        print("program", end="\n\n")

    def p_comment(self, p):
        '''
        comment : COMMENT
        '''

    def p_block(self, p):
        '''
        block : BEGIN block_body END
        '''
        p[0] = dict()
        if type(p[2]) == list:
            self._fill_event_list(p[2], p[0])
        print(f"block {p[0]}", end="\n\n")

    def _fill_event_list(self, event_list, scope_dict):
        for event in event_list:
            if event is not None:
                if type(event) == list:
                    self._fill_event_list(event, scope_dict)
                elif event["operation"] == "add_new_var":
                    scope_dict[event["id"]] = {"type":event["type"], "value":event["value"]}
                elif event["operation"] == "update":
                    scope_dict[event["id"]]["value"] = event["value"]

    def p_block_body(self, p):
        '''
        block_body : lines
                     | loop
                     | func_decl
        '''
        p[0] = p[1]
        print(f'block_body {p[0]}', end="\n\n")

    def p_lines(self, p):
        '''
        lines : lines line
                | line
        '''
        print(p[0])
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1]+[p[2]]
        print(f'p_lines {p[0]}', end="\n\n")

    # def p_line(self, p):
    #     '''
    #     line : line_body
    #     '''
    #     p[0] = p[1]
    #     print(p[0])
    #     print('p_line', end="\n\n")

    def p_line(self, p):
        '''
        line : var_decl
                | var_assign
                | if_stat
                | comment
                | print
        '''
        p[0] = p[1]
        print(f'line {p[0]}', end="\n\n")

    def p_loop(self, p):
        '''
        loop : LOOP OPEN_BRACKET expr CLOSE_BRACKET BEGIN block_body END
        '''

        print('loop', end="\n\n")

    def p_print(self, p):
        '''
        print : PRINT OPEN_BRACKET expr CLOSE_BRACKET ENDLINE
        '''
        print("OUTPUT:",p[3])
        p[0] = {"operation":None}

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
        var_decl : type ID ASSIGN factor_n ENDLINE
        '''
        p[0] = {"type":self.reserved[p[1]], "id":p[2], "value":p[4], "operation":"add_new_var"}
        print(f'var_decl {p[0]}', end="\n\n")

    def p_var_assign(self, p):
        '''
        var_assign : ID ASSIGN factor_n ENDLINE
        '''
        p[0] = {"operation":"update", "id":p[1], "value":p[3]}
        print(f'var_assign {p[0]}', end="\n\n")

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
        func_call : ID OPEN_BRACKET factors_n CLOSE_BRACKET
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
        if p[3] > 0:
            p[0] = p[6]
        elif p[7] is not None:
            p[0] = p[7]
        print(f'if_stat {p[0]}', end="\n\n")

    def p_end_if(self, p):
        '''
        end_if : END
                 | else_stat
        '''
        p[0] = p[1]
        print('end_if', end="\n\n")

    def p_else_stat(self, p):
        '''
        else_stat : ELSE THEN block_body END
        '''
        p[0] = p[3]
        print(f'else_stat {p[0]}', end="\n\n")

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
                    | N_EQUAL
        '''
        p[0] = p[1]
        print('oper_mult', end="\n\n")

    def p_factor(self, p):
        '''
        factor : ID
                 | NUMBER
                 | brac_expr
                 | func_call
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
            p[0] = int(not p[2])
        print(p[0])
        print('p_factor_n', end="\n\n")

    def p_factors_n(self, p):
        '''
        factors_n : factor_n
                | factors_n factor_n
        '''

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
        elif p[2] == '%':
            if p[3] == 0:
                print('Cannot divide by 0')
                raise ZeroDivisionError
            else:
                p[0] = p[1] % p[3]
        elif p[2] == '<=':
            p[0] = int(p[1] <= p[3])
        elif p[2] == '>=':
            p[0] = int(p[1] >= p[3])
        elif p[2] == '<':
            p[0] = int(p[1] < p[3])
        elif p[2] == '>':
            p[0] = int(p[1] > p[3])
        elif p[2] == '=':
            p[0] = int(p[1] == p[3])
        elif p[2] == '~=':
            p[0] = int(p[1] != p[3])
        elif p[2] == '&':
            p[0] = int(p[1] and p[3])
        elif p[2] == '|':
            p[0] = int(p[1] or p[3])
        elif p[2] == '!':
            p[0] = int((p[1] and (not p[3])) or ((not p[1]) and p[3]))
        print('comp')

    def p_error(self, p):
        '''
        '''
        print("ERROR", p)