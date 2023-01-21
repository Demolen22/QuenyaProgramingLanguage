from lexer import Lexer
import ply.yacc as yacc
from copy import deepcopy
import sys

OPERATION = "operation"
LOOP = "loop"
VALUE = "value"
TYPE = "type"
ARGS = "args"
BODY = "body"
FUNCTION = "function"
RETURN = "return"
ID = "id"
ADD_NEW_VAR = "add_new_var"
UPDATE = "update"
ADD_NEW_FUNC = "add_new_func"
IF_STAT = "if_stat"
COND = "cond"
FIRST = "first"
IF_LINES = "if_lines"
ELSE_LINES = "else_lines"
PRINT = "print"
FUNC_CALL = "func_call"
FUNC_DECL = "func_decl"
TABLE_DECL = "table_decl"
SIZE = "size"


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
        self.operations = {
            '-': lambda x, y: x - y,
            '+': lambda x, y: x + y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '%': lambda x, y: x % y,
            '<=': lambda x, y: int(x <= y),
            '>=': lambda x, y: int(x >= y),
            '<': lambda x, y: int(x < y),
            '>': lambda x, y: int(x > y),
            '=': lambda x, y: int(x == y),
            '~=': lambda x, y: int(x != y),
            '&': lambda x, y: int(x and y),
            '|': lambda x, y: int(x or y),
            '!': lambda x, y: int((x and (not y)) or ((not x) and y))
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
        block : BEGIN lines END
        '''
        p[0] = dict()
        if type(p[2]) == list:
            self._fill_event_list(p[2], p[0])
        print(f"block {p[0]}", end="\n\n")

    def _save_func_declaration(self, function, scope_dict):
        scope_dict[function[ID]] = {
            TYPE: FUNCTION,
            ARGS: function[ARGS],
            BODY: function[VALUE],
            RETURN: function[RETURN]
        }
        print("scope dict", scope_dict)

    def _call_function(self, id, args, scope_dict):
        func_decl = scope_dict[id]
        if len(func_decl[ARGS]) != len(args):
            raise Exception(f'numer of arguments is {len(args)} and should be {len(func_decl[ARGS])}')
        for idx, arg in enumerate(args):
            func_decl[ARGS][idx][VALUE] = arg
        local_scope_dict = deepcopy(scope_dict)
        for variable in scope_dict.values():
            if variable[TYPE] == FUNCTION:
                for func_var in variable[ARGS]:
                    local_scope_dict[func_var[ID]] = func_var
        print(f'local scope dict {local_scope_dict}')
        print(f'func {id} called with args {func_decl[ARGS]} scope dict is {local_scope_dict}')
        self._fill_event_list(func_decl[BODY], local_scope_dict)
        print(f'And got {local_scope_dict[func_decl[RETURN]][VALUE]}')
        return local_scope_dict[func_decl[RETURN]][VALUE]

    def _fill_event_list(self, event_list, scope_dict):
        for event in event_list:
            if event is not None:
                if type(event) == list:
                    self._fill_event_list(event, scope_dict)
                elif event[OPERATION] == ADD_NEW_VAR:
                    scope_dict[event[ID]] = {TYPE: event[TYPE],
                                             VALUE: self._arithmetic_interpreter(event[VALUE], scope_dict)}
                    if event[TYPE] == "INT":
                        scope_dict[event[ID]] = {TYPE:event[TYPE], VALUE:self._arithmetic_interpreter(event[VALUE], scope_dict)}
                    elif event[TYPE] == "STRING":
                        scope_dict[event[ID]] = {TYPE: event[TYPE], VALUE: event[VALUE]}
                elif event[OPERATION] == UPDATE:
                    if scope_dict.get(event[ID]) is None:
                        print(f"VARIABLE {event[ID]} UNDECLARED")
                        raise Exception
                    if scope_dict[event[ID]][TYPE] == "INT":
                        if type(event[VALUE]) == str:
                            print(f"CANNOT ASSIGN STRING '{event['value']}' TO INT {event[ID]}")
                            raise Exception
                        scope_dict[event[ID]][VALUE] = self._arithmetic_interpreter(event[VALUE], scope_dict)
                    elif scope_dict[event[ID]][TYPE] == "STRING":
                        scope_dict[event[ID]][VALUE] = str(event[VALUE])
                elif event[OPERATION] == ADD_NEW_FUNC:
                    self._save_func_declaration(event, scope_dict)
                elif event[OPERATION] == IF_STAT:
                    if self._arithmetic_interpreter(event[COND], scope_dict) != 0:
                        self._fill_event_list(event[IF_LINES], scope_dict)
                    elif event[ELSE_LINES] is not None:
                        self._fill_event_list(event[ELSE_LINES], scope_dict)
                elif event[OPERATION] == LOOP:
                    while self._arithmetic_interpreter(event[COND], scope_dict) != 0:
                        self._fill_event_list(event[BODY], scope_dict)
                elif event[OPERATION] == PRINT:
                    print(f"OUTPUT: {self._arithmetic_interpreter(event[VALUE], scope_dict)}")
                elif event[OPERATION] == TABLE_DECL:
                    scope_dict[event[ID]] = {TYPE: event[TYPE], SIZE: event[SIZE], VALUE: [None]*event[SIZE]}
        print("scope dict ", scope_dict)

    def _arithmetic_interpreter(self, value, scope_dict):
        if type(value) == list:
            result = 0
            for val in value:
                if val[OPERATION] == FIRST:
                    result = self._arithmetic_interpreter(val[VALUE], scope_dict)
                else:
                    component = self._arithmetic_interpreter(val[VALUE], scope_dict)
                    if component == 0 and (val[OPERATION] == '/' or val[OPERATION] == '%'):
                        print("ZERO DIVISION ATTEMPT")
                        raise ZeroDivisionError
                    else:
                        print(f"{result} {val[OPERATION]} {component} = ", end="")
                        result = self.operations[val[OPERATION]](result, component)
                        print(result)
            return result
        elif type(value) == dict:
            if value[OPERATION] == "~":
                return int(not self._arithmetic_interpreter(value[VALUE], scope_dict))
            elif value[OPERATION] == FUNC_CALL:
                print(self._call_function(value[ID], value[ARGS], scope_dict))
                return self._call_function(value[ID], value[ARGS], scope_dict)
            elif value[OPERATION] == LOOP:
                pass
            else:
                return self._arithmetic_interpreter(value[VALUE], scope_dict)
        elif type(value) == str:
            if scope_dict.get(value) is None:
                print(f"VARIABLE {value} UNDECLARED")
                raise Exception
            if scope_dict[value][TYPE] == "STRING":
                print(f"ILLEGAL ARITHMETIC OPERATION ON STRING VARIABLE: {value} {scope_dict[value]['value']}")
                raise Exception
            return scope_dict[value][VALUE]
        else:
            return value

    def p_lines(self, p):
        '''
        lines : lines line
                | line
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
        print(f'p_lines {p[0]}', end="\n\n")

    def p_line(self, p):
        '''
        line : var_decl
                | var_assign
                | if_stat
                | comment
                | print
                | loop
                | func_decl
                | table_decl
        '''
        p[0] = p[1]
        print(f'line {p[0]}', end="\n\n")

    def p_loop(self, p):
        '''
        loop : LOOP OPEN_BRACKET expr CLOSE_BRACKET BEGIN lines END
        '''
        p[0] = dict()
        p[0][OPERATION] = LOOP
        p[0][COND] = p[3]
        p[0][BODY] = p[6]
        print('loop', end="\n\n")

    def p_print(self, p):
        '''
        print : PRINT OPEN_BRACKET expr CLOSE_BRACKET ENDLINE
        '''
        p[0] = {OPERATION:"print", VALUE:p[3]}

    def p_table_decl(self, p):
        '''
        table_decl : LIST type NUMBER ID ENDLINE
        '''
        p[0] = {OPERATION:TABLE_DECL, TYPE:p[1], ID:p[4], SIZE:p[3]}
        print(f"table_decl {p[0]}")

    def p_table_assign(self):
        '''
        table_assign ID
        '''

    def p_func_decl(self, p):
        '''
        func_decl : FUNCTION ID OPEN_BRACKET args CLOSE_BRACKET BEGIN lines RETURN factor_n
        '''
        p[0] = dict()
        p[0][ID] = p[2]
        p[0][ARGS] = p[4]
        p[0][VALUE] = p[7]
        p[0][RETURN] = p[9]
        p[0][OPERATION] = ADD_NEW_FUNC
        p[0][TYPE] = FUNCTION
        print(FUNC_DECL, end="\n\n")

    def p_var_decl(self, p):
        '''
        var_decl : INT ID ASSIGN factor_n ENDLINE
                | STRING ID ASSIGN STRING_EXPR ENDLINE
        '''
        p[0] = {TYPE: self.reserved[p[1]], ID: p[2], VALUE: p[4], OPERATION: ADD_NEW_VAR}
        print(f'var_decl {p[0]}', end="\n\n")

    def p_var_assign(self, p):
        '''
        var_assign : ID ASSIGN factor_n ENDLINE
                    | ID ASSIGN STRING_EXPR ENDLINE
        '''
        p[0] = {OPERATION: UPDATE, ID: p[1], VALUE: p[3]}
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
        p[0] = dict()
        p[0][ID] = p[1]
        p[0][ARGS] = p[3]
        p[0][OPERATION] = FUNC_CALL
        print('func_call', end="\n\n")

    def p_arg(self, p):
        '''
        arg : type ID
        '''
        p[0] = {TYPE: self.reserved[p[1]], ID: p[2], VALUE: None}
        print(p[0])
        print('arg', end='\n\n')

    def p_args(self, p):
        '''
        args : args arg
               | arg
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
        print(p[0])
        print('args', end="\n\n")

    def p_if_stat(self, p):
        '''
        if_stat : IF OPEN_BRACKET expr CLOSE_BRACKET THEN lines end_if
        '''
        p[0] = {OPERATION: IF_STAT, COND: p[3], IF_LINES: p[6], ELSE_LINES: p[7]}
        print(f'if_stat {p[0]}', end="\n\n")

    def p_end_if(self, p):
        '''
        end_if : END
                 | else_stat
        '''
        if type(p[1]) != str:
            p[0] = p[1]
        print('end_if', end="\n\n")

    def p_else_stat(self, p):
        '''
        else_stat : ELSE THEN lines END
        '''
        p[0] = p[3]
        print(f'else_stat {p[0]}', end="\n\n")

    def p_expr(self, p):
        '''
        expr : expr oper_add comp
               | comp
        '''
        if len(p) == 2:
            p[0] = [{OPERATION: FIRST, VALUE: p[1]}]
        else:
            p[0] = p[1] + [{OPERATION: p[2], VALUE: p[3]}]
        print(f'expr {p[0]}', end='\n\n')

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
        print(f'p_factor {p[0]}', end="\n\n")

    def p_factor_n(self, p):
        '''
        factor_n : NOT factor
                    | factor
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = {OPERATION: p[1], VALUE: p[2]}
        print(f'p_factor_n {p[0]}', end="\n\n")

    def p_factors_n(self, p):
        '''
        factors_n : factor_n
                | factors_n factor_n
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
        print(p[0])

    def p_comp(self, p):
        '''
        comp : comp oper_mult factor_n
               | factor_n
        '''
        if len(p) == 2:
            p[0] = [{OPERATION: FIRST, VALUE: p[1]}]
        else:
            p[0] = p[1] + [{OPERATION: p[2], VALUE: p[3]}]
        print(f'comp {p[0]}')

    def p_error(self, p):
        '''
        '''
        print("ERROR", p)
