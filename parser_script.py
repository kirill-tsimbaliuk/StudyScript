import turtle
from rply import ParserGenerator
from tree import *


def flatten(temp_list):
    new_list = []
    for ele in temp_list:
        if type(ele) == list:
            r = flatten(ele)
            for i in r:
                new_list.append(i)
        else:
            new_list.append(ele)
    return new_list


included = []
value = {}


class Value(Abstract):
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def call(self):
        global value
        value[self.name.call()] = self.val


class Parser:

    def __init__(self):
        self.pg = ParserGenerator(
            ['INTEGER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN', 'MULTIPLY', 'DIV', 'MORE', 'EQUALS', 'LESS', 'NOT',
             'SEMI_COLON', 'SUM', 'SUB', 'COMMAND', 'QUOTE', 'VAR', 'IF', 'OPEN_PAREN_FIGURED', 'CLOSE_PAREN_FIGURED',
             'EXIT', 'INCLUDE', 'FORWARD', 'RIGHT', 'LEFT', 'BACK', 'INPUT', 'INT', 'WHILE',
             'TEXT', ]
        )

    def parse(self):
        global value

        @self.pg.production('program : INCLUDE text SEMI_COLON')
        def include(p):
            global included
            name = p[1].call()
            included.append(name)
            if name == 'turtle':
                screen = turtle.Screen()
                screen.title("StudyScript")
            return NoAnswer()

        @self.pg.production('string : INPUT OPEN_PAREN CLOSE_PAREN')
        def inp(p):
            try:
                return String(input())
            except KeyboardInterrupt:
                return NoAnswer()

        @self.pg.production('program : INPUT OPEN_PAREN CLOSE_PAREN SEMI_COLON')
        def inp_2(p):
            try:
                return String(input())
            except KeyboardInterrupt:
                return NoAnswer()

        @self.pg.production('expression : INT OPEN_PAREN string CLOSE_PAREN')
        def to_int(p):
            return Integer(int(p[2].call()))

        @self.pg.production('program : FORWARD OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        @self.pg.production('program : BACK OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        @self.pg.production('program : RIGHT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        @self.pg.production('program : LEFT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def com(p):
            for name in included:
                if name == "turtle":
                    if p[0].gettokentype() == "FORWARD":
                        turtle.forward(p[2].call())
                    elif p[0].gettokentype() == "BACK":
                        turtle.backward(p[2].call())
                    elif p[0].gettokentype() == "RIGHT":
                        turtle.right(p[2].call())
                    elif p[0].gettokentype() == "LEFT":
                        turtle.left(p[2].call())
            return NoAnswer()

        @self.pg.production('program : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        @self.pg.production('program : PRINT OPEN_PAREN string CLOSE_PAREN SEMI_COLON')
        @self.pg.production('program : PRINT OPEN_PAREN logic CLOSE_PAREN SEMI_COLON')
        @self.pg.production('program : PRINT OPEN_PAREN type CLOSE_PAREN SEMI_COLON')
        def program(p):
            if p[2] is None:
                print("Error in the method 'print'")
            return Print(p[2])

        @self.pg.production('program : COMMAND OPEN_PAREN string CLOSE_PAREN SEMI_COLON')
        @self.pg.production('program : COMMAND OPEN_PAREN type CLOSE_PAREN SEMI_COLON')
        def command(p):
            if p[2] is None:
                print("Error in the method 'command'")
            return Command(p[2])

        @self.pg.production('type : text')
        def type_check(p):
            global value
            s = ""
            for i in p:
                s = s + i.value
            if s == "true":
                return Boolean(True)
            elif s == "false":
                return Boolean(False)
            for key in list(value):
                if key == s:
                    return value[key]

        @self.pg.production('program : program program')
        def combination(p):
            return p

        @self.pg.production('program : IF OPEN_PAREN logic CLOSE_PAREN OPEN_PAREN_FIGURED program CLOSE_PAREN_FIGURED')
        def IF(p):
            if p[2].call():
                if isinstance(p[5], list):
                    p[5] = list(flatten(p[5]))
                    for c in p[5]:
                        c.call()
                else:
                    p[5].call()
            else:
                return NoAnswer()

        @self.pg.production('program : WHILE OPEN_PAREN logic CLOSE_PAREN OPEN_PAREN_FIGURED program '
                            'CLOSE_PAREN_FIGURED')
        def wh(p):
            if p[2].call():
                if isinstance(p[5], list):
                    p[5] = list(flatten(p[5]))
                    for c in p[5]:
                        c.call()
                else:
                    p[5].call()
            else:
                return NoAnswer()

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MULTIPLY expression')
        @self.pg.production('expression : expression DIV expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            try:
                if operator.gettokentype() == 'SUM':
                    return Sum(left, right)
                elif operator.gettokentype() == 'SUB':
                    return Sub(left, right)
                elif operator.gettokentype() == 'MULTIPLY':
                    return Multiply(left, right)
                elif operator.gettokentype() == 'DIV':
                    return Div(left, right)
            except TypeError:
                print("Incompatible data type")


        @self.pg.production('expression : INTEGER')
        def number(p):
            return Integer(p[0].value)

        @self.pg.production('expression : type')
        @self.pg.production('expression : string')
        def get_expression(p):
            if isinstance(p[0], Boolean):
                print("Incompatible data type")
            return p[0]

        @self.pg.production('string : QUOTE text QUOTE')
        def string(p):
            res = p[1].value
            res = res.replace("_", ' ')
            return String(res)

        @self.pg.production('text : text TEXT')
        @self.pg.production('text : text DIV')
        def text(p):
            s = ""
            for i in p:
                s = s + i.value
            return String(s)

        @self.pg.production('text : TEXT')
        @self.pg.production('text : DIV')
        @self.pg.production('text : INTEGER')
        def text(p):
            return String(str(p[0].value))

        @self.pg.production('logic : logic MORE logic')
        @self.pg.production('logic : logic LESS logic')
        @self.pg.production('logic : logic EQUALS EQUALS logic')
        @self.pg.production('logic : logic MORE EQUALS logic')
        @self.pg.production('logic : logic LESS EQUALS logic')
        @self.pg.production('logic : logic NOT EQUALS logic')
        def logistic(p):
            left = p[0]
            right = p[-1]
            operator = p[1:-1]
            if len(operator) == 1:
                operator = operator[0]
                if operator.gettokentype() == 'MORE':
                    return More(left, right)
                elif operator.gettokentype() == 'LESS':
                    return Less(left, right)
            elif len(operator) == 2:
                if operator[0].gettokentype() == 'MORE' and operator[1].gettokentype() == "EQUALS":
                    return Boolean(True) if left.call() >= right.call() else Boolean(False)

                if operator[0].gettokentype() == 'LESS' and operator[1].gettokentype() == "EQUALS":
                    return Boolean(True) if left.call() <= right.call() else Boolean(False)

                if operator[0].gettokentype() == 'EQUALS' and operator[1].gettokentype() == "EQUALS":
                    return Equals(left, right)

                if operator[0].gettokentype() == 'NOT' and operator[1].gettokentype() == "EQUALS":
                    return Boolean(True) if left.call() != right.call() else Boolean(False)

        @self.pg.production('logic : expression')
        @self.pg.production('logic : type')
        def logic(p):
            return p[0]

        @self.pg.production('program : VAR text EQUALS expression SEMI_COLON')
        @self.pg.production('program : VAR text EQUALS string SEMI_COLON')
        @self.pg.production('program : VAR text EQUALS logic SEMI_COLON')
        @self.pg.production('program : VAR text EQUALS type SEMI_COLON')
        def var(p):
            return Value(p[1], p[3])

        @self.pg.production('program : text EQUALS type SEMI_COLON')
        @self.pg.production('program : text EQUALS expression SEMI_COLON')
        @self.pg.production('program : text EQUALS string SEMI_COLON')
        @self.pg.production('program : text EQUALS logic SEMI_COLON')
        def var_change(p):
            global value
            s = ""
            for i in p:
                if i.value == "=":
                    break
                s = s + i.value
            for key in list(value):
                if key == s:
                    value[key] = p[2]
                    return NoAnswer()
            else:
                print("Incorrect variable declaration")

        @self.pg.production('program : EXIT OPEN_PAREN CLOSE_PAREN SEMI_COLON')
        def finish(p):
            return Exit(None)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
