from enum import Enum, auto

class TokenType(Enum):
    Equal = auto()
    Comma = auto()
    Less = auto()
    Greater = auto()
    Plus = auto()
    Minus = auto()
    Star = auto()
    Slash = auto()
    Number = auto()
    EOF = auto()
    LParen = auto()
    RParen = auto()
    LCurly = auto()
    RCurly = auto()
    Key_If = auto()
    Key_Else = auto()
    Key_While = auto()
    Key_Do = auto()
    SemiColon = auto()
    Identifier = auto()


class Token:
    def __init__(self, type: TokenType, value, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f'[{self.line}:{self.column}]({self.type}, {self.value})'

    def __repr__(self):
        return self.__str__()


SYMBOL_DICT = {
    '=': TokenType.Equal,
    '<': TokenType.Less,
    '>': TokenType.Greater,
    '+': TokenType.Plus,
    '-': TokenType.Minus,
    '*': TokenType.Star,
    '/': TokenType.Slash,
    '(': TokenType.LParen,
    ')': TokenType.RParen,
    '{': TokenType.LCurly,
    '}': TokenType.RCurly,
    ';': TokenType.SemiColon,
    ',': TokenType.Comma
}

KEYWORD_DICT = {
    'if': TokenType.Key_If,
    'else': TokenType.Key_Else,
    'while': TokenType.Key_While,
    'do': TokenType.Key_Do
}


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.column += 1
            if self.current_char == '\n':
                self.line += 1
                self.column = 1

    def number(self):
        result = ''
        while self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.Number, int(result), self.line, self.column)

    def identifier(self):
        result = ''
        while self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return Token(TokenType.Identifier, result, self.line, self.column)

    def check_keyword(self, keyword: TokenType, text: str):
        if self.text[self.pos:self.pos + len(text)] == text:
            return Token(keyword, text, self.line, self.column)
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def get_tokens(self):
        tokens = []
        while True:
            self.skip_whitespace()
            if self.current_char is None:
                tokens.append(Token(TokenType.EOF, None, self.line, self.column))
                return tokens
            if self.current_char == '#':
                self.advance()
                self.skip_comment()
                continue

            found = False
            for keyword, token_type in KEYWORD_DICT.items():
                token = self.check_keyword(token_type, keyword)
                if token is not None:
                    found = True
                    tokens.append(token)
                    for _ in keyword:
                        self.advance()
                    break
            if found:
                continue

            if self.current_char in SYMBOL_DICT:
                tokens.append(Token(SYMBOL_DICT[self.current_char], self.current_char, self.line, self.column))
                self.advance()
                continue

            if self.current_char.isdigit():
                tokens.append(self.number())
                continue

            if self.current_char.isalpha():
                tokens.append(self.identifier())
                continue

