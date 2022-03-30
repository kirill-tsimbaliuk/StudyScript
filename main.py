from lexer import Lexer
from parser_script import Parser
from sys import argv, exit
import warnings


def get_construction(l, index):
    rez = []
    j = index
    while j < len(l):
        if ("if" in l[j] or "while" in l[j]) and '{' in l[j] and j > index:
            if not ('}' in l[j]):
                a, c = get_construction(l, j)
                j = c
                for el in a:
                    rez.append(el)
        if l[j] == '}':
            rez.append(l[j])
            return rez, j
        else:
            rez.append(l[j])
        j += 1


with warnings.catch_warnings():
    warnings.filterwarnings('ignore')
    lexer = Lexer().get_lexer()
    pg = Parser()
    pg.parse()
    parser = pg.get_parser()

if len(argv) == 1:
    save_cmd = ""
    print("The virtual shell of Study Script 1.0 is running")
    while True:
        try:
            cmd = input(">>>")
            if cmd:
                if "while" in cmd and "{" in cmd and "}" in cmd:
                    save_while = True
                    save_cmd = cmd
                    while True:
                        c = save_cmd
                        tokens = lexer.lex(c)
                        try:
                            parser.parse(tokens).call()
                        except:
                            pass
                else:
                    tokens = lexer.lex(cmd)
                    parser.parse(tokens).call()
        except KeyboardInterrupt:
            pass
        except ValueError:
            print("Syntax error")
        except AttributeError:
            pass
else:
    parameter = argv[1:]

    if not (".stscr" in parameter[0]):
        print("Invalid file type")
        exit()

    save_index = None
    save = ""
    save_while = True
    with open(parameter[0], 'r') as file:
        lines = file.read().split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            if line == '}':
                i += 1
                continue
            if save:
                line = save
                i -= save_index
                save_index = None
                save = ''
            if "if" in line and '{' in line:
                if '}' in line:
                    tokens = lexer.lex(line)
                    r = tokens
                    if parser.parse(r):
                        try:
                            parser.parse(tokens).call()
                        except ValueError:
                            pass
                else:
                    ans, index = get_construction(lines, i)
                    a = ''
                    for k in ans:
                        a = a + k
                    i = index - 1
                    save = a
                    save_index = 1
            elif "while" in line and '{' in line:
                if '}' in line:
                    tokens = lexer.lex(line)
                    r = tokens
                    if parser.parse(r):
                        try:
                            parser.parse(tokens).call()
                        except ValueError:
                            i += 1
                            save_while = False
                    if save_while:
                        save = line
                        save_index = 1
                    else:
                        i -= 1
                else:
                    new_line, index = get_construction(lines, i)
                    save_index = 1
                    for element in new_line:
                        save += element
                    i = index - 1
                    save_index = 1
                    save_while = True
            else:
                if line:
                    tokens = lexer.lex(line)
                    parser.parse(tokens).call()
            i += 1
