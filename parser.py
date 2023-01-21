from lexer import Lexer
import ply.yacc as yacc
from copy import deepcopy
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
        scope_dict[function["id"]] = {
            "type": "function",
            "args": function["args"],
            "body": function["value"],
            "return": function["return"]
        }
        print("scope dict", scope_dict)
    def _call_function(self, id, args, scope_dict):
        func_decl = scope_dict[id]
        if len(func_decl["args"]) != len(args):
            raise Exception(f'numer of arguments is {len(args)} and should be {len(func_decl["args"])}')
        for idx, arg in enumerate(args):
            func_decl["args"][idx]["value"] = arg
        local_scope_dict = deepcopy(scope_dict)
        for variable in scope_dict.values():
            if variable["type"] == "function":
                for func_var in variable["args"]:
                    local_scope_dict[func_var["id"]] = func_var
        print(f'local scope dict {local_scope_dict}')
        print(f'func {id} called with args {func_decl["args"]} scope dict is {local_scope_dict}')
        self._fill_event_list(func_decl["body"], local_scope_dict)
        print(f'And got {local_scope_dict[func_decl["return"]]["value"]}')
        return local_scope_dict[func_decl["return"]]["value"]

    def _fill_event_list(self, event_list, scope_dict):
        for event in event_list:
            if event is not None:
                if type(event) == list:
                    self._fill_event_list(event, scope_dict)
                elif event["operation"] == "add_new_var":
                    if event["type"] == "INT":
                        scope_dict[event["id"]] = {"type":event["type"], "value":self._arithmetic_interpreter(event["value"], scope_dict)}
                    elif event["type"] == "STRING":
                        scope_dict[event["id"]] = {"type": event["type"], "value": event["value"]}
                elif event["operation"] == "update":
                    if scope_dict.get(event["id"]) is None:
                        print(f"VARIABLE {event['id']} UNDECLARED")
                        raise Exception
                    if scope_dict[event["id"]]["type"] == "INT":
                        if type(event["value"]) == str:
                            print(f"CANNOT ASSIGN STRING '{event['value']}' TO INT {event['id']}")
                            raise Exception
                        scope_dict[event["id"]]["value"] = self._arithmetic_interpreter(event["value"], scope_dict)
                    elif scope_dict[event["id"]]["type"] == "STRING":
                        scope_dict[event["id"]]["value"] = event["value"]
                elif event["operation"] == "add_new_func":
                    self._save_func_declaration(event, scope_dict)
                elif event["operation"] == "if_stat":
                    if self._arithmetic_interpreter(event["cond"], scope_dict) != 0:
                        self._fill_event_list(event["if_lines"], scope_dict)
                    elif event["else_lines"] is not None:
                        self._fill_event_list(event["else_lines"], scope_dict)
                elif event["operation"] == "print":
                    print(f"OUTPUT: {self._arithmetic_interpreter(event['value'], scope_dict)}")
        print("scope dict ", scope_dict)


    def _arithmetic_interpreter(self, value, scope_dict):
        if type(value) == list:
            result = 0
            for val in value:
                if val["operation"] == "first":
                    result = self._arithmetic_interpreter(val["value"], scope_dict)
                else:
                    component = self._arithmetic_interpreter(val["value"], scope_dict)
                    if component == 0 and (val["operation"] == '/' or val["operation"] == '%'):
                        print("ZERO DIVISION ATTEMPT")
                        raise ZeroDivisionError
                    else:
                        print(f"{result} {val['operation']} {component} = ", end="")
                        result = self.operations[val["operation"]](result, component)
                        print(result)
            return result
        elif type(value) == dict:
            if value["operation"] == "~":
                return int(not self._arithmetic_interpreter(value["value"], scope_dict))
            elif value["operation"] == "func_call":
                print(self._call_function(value["id"], value["args"], scope_dict))
                return self._call_function(value["id"], value["args"], scope_dict)
            else:
                return self._arithmetic_interpreter(value["value"], scope_dict)
        elif type(value) == str:
            if scope_dict.get(value) is None:
                print(f"VARIABLE {value} UNDECLARED")
                raise Exception
            if scope_dict[value]["type"] == "STRING":
                print(f"ILLEGAL ARITHMETIC OPERATION ON STRING VARIABLE: {value} {scope_dict[value]['value']}")
                raise Exception
            return scope_dict[value]["value"]
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
        '''
        p[0] = p[1]
        print(f'line {p[0]}', end="\n\n")

    def p_loop(self, p):
        '''
        loop : LOOP OPEN_BRACKET expr CLOSE_BRACKET BEGIN lines END
        '''

        print('loop', end="\n\n")

    def p_print(self, p):
        '''
        print : PRINT OPEN_BRACKET expr CLOSE_BRACKET ENDLINE
        '''
        p[0] = {"operation":"print", "value":p[3]}

    def p_func_decl(self, p):
        '''
        func_decl : FUNCTION ID OPEN_BRACKET args CLOSE_BRACKET BEGIN lines RETURN factor_n
        '''
        p[0] = dict()
        p[0]["id"] = p[2]
        p[0]["args"] = p[4]
        p[0]["value"] = p[7]
        p[0]["return"] = p[9]
        p[0]["operation"] = "add_new_func"
        p[0]["type"] = "function"
        print('func_decl', end="\n\n")

    def p_var_decl(self, p):
        '''
        var_decl : INT ID ASSIGN factor_n ENDLINE
                | STRING ID ASSIGN STRING_EXPR ENDLINE
        '''
        p[0] = {"type": self.reserved[p[1]], "id": p[2], "value": p[4], "operation": "add_new_var"}
        print(f'var_decl {p[0]}', end="\n\n")

    def p_var_assign(self, p):
        '''
        var_assign : ID ASSIGN factor_n ENDLINE
                    | ID ASSIGN STRING_EXPR ENDLINE
        '''
        p[0] = {"operation": "update", "id": p[1], "value": p[3]}
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
        p[0]["id"] = p[1]
        p[0]["args"] = p[3]
        p[0]["operation"] = "func_call"
        print('func_call', end="\n\n")

    def p_arg(self, p):
        '''
        arg : type ID
        '''
        p[0] = {"type": self.reserved[p[1]], "id": p[2], "value": None}
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
        p[0] = {"operation":"if_stat", "cond":p[3], "if_lines":p[6], "else_lines":p[7]}
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
            p[0] = [{"operation": "first", "value": p[1]}]
        else:
            p[0] = p[1] + [{"operation": p[2], "value": p[3]}]
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
            p[0] = {"operation": p[1], "value": p[2]}
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
            p[0] = [{"operation": "first", "value": p[1]}]
        else:
            p[0] = p[1] + [{"operation": p[2], "value": p[3]}]

        # if len(p) == 2:
        #     p[0] = p[1]
        #     print(p[0])
        # elif p[2] == '*':
        #     p[0] = p[1] * p[3]
        #     print(p[0])
        # elif p[2] == '/':
        #     if p[3] == 0:
        #         print('Cannot divide by 0')
        #         raise ZeroDivisionError
        #     else:
        #         p[0] = p[1] / p[3]
        #         print(p[0])
        # elif p[2] == '%':
        #     if p[3] == 0:
        #         print('Cannot divide by 0')
        #         raise ZeroDivisionError
        #     else:
        #         p[0] = p[1] % p[3]
        # elif p[2] == '<=':
        #     p[0] = int(p[1] <= p[3])
        # elif p[2] == '>=':
        #     p[0] = int(p[1] >= p[3])
        # elif p[2] == '<':
        #     p[0] = int(p[1] < p[3])
        # elif p[2] == '>':
        #     p[0] = int(p[1] > p[3])
        # elif p[2] == '=':
        #     p[0] = int(p[1] == p[3])
        # elif p[2] == '~=':
        #     p[0] = int(p[1] != p[3])
        # elif p[2] == '&':
        #     p[0] = int(p[1] and p[3])
        # elif p[2] == '|':
        #     p[0] = int(p[1] or p[3])
        # elif p[2] == '!':
        #     p[0] = int((p[1] and (not p[3])) or ((not p[1]) and p[3]))
        print(f'comp {p[0]}')

    def p_error(self, p):
        '''
        '''
        print("ERROR", p)
