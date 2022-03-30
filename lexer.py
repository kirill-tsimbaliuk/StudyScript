from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # подключение библиотек
        self.lexer.add('INCLUDE', r'include')
        # go to
        self.lexer.add("FORWARD", r'forward')
        self.lexer.add("BACK", r'back')
        self.lexer.add("RIGHT", r'right')
        self.lexer.add("LEFT", r'left')
        # input
        self.lexer.add("INPUT", r'input')
        # объявление переменых
        self.lexer.add('VAR', r'var')
        # Print
        self.lexer.add('PRINT', r'print')
        # Условия
        self.lexer.add('IF', r'if')
        # Скобки
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('OPEN_PAREN_FIGURED', r'\{')
        self.lexer.add('CLOSE_PAREN_FIGURED', r'\}')
        # Точка с запятой
        self.lexer.add('SEMI_COLON', r'\;')
        # Операторы
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MULTIPLY', r'\*')
        self.lexer.add('DIV', r'\/')
        # Числа
        self.lexer.add('INTEGER', r'\d+')
        # Строки
        self.lexer.add('QUOTE', r'\"')
        self.lexer.add('QUOTE', r'\'')
        # Команды для системы
        self.lexer.add('COMMAND', r'command')
        # Выход
        self.lexer.add('EXIT', r'exit')
        # Логические операторы
        self.lexer.add('MORE', r'\>')
        self.lexer.add('LESS', r'\<')
        self.lexer.add('EQUALS', r'\=')
        self.lexer.add("NOT", r'\!')
        # типы данных
        self.lexer.add("INT", r'int')
        # while
        self.lexer.add("WHILE", r'while')
        # Строки
        for i in range(97, 123):
            self.lexer.add('TEXT', chr(i))
        self.lexer.add('TEXT', r'_')
        for i in range(65, 91):
            self.lexer.add('TEXT', chr(i))
        # Игнорируем пробелы
        self.lexer.ignore(r'\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
