from src import ast
from src import lexer


class Parser:
    def __init__(self, code):
        self.lexer = lexer.Lexer(code)
        self.tokens = self.lexer.get_tokens()
        self.index = 0

    def error(self, message):
        les = max(0, self.index - 5)
        more = min(len(self.tokens), self.index + 5)
        print('\n'.join([str(token) for token in self.tokens[les:more]]))
        raise Exception('Invalid syntax ' + message + f' at {self.tokens[self.index].line}:{self.tokens[self.index].column}')

    def eat(self, token_type):
        if self.tokens[self.index].type == token_type:
            self.index += 1
        else:
            self.error(f'Expected {token_type} but got {self.tokens[self.index].type}')

    def match(self, token_type):
        return self.tokens[self.index].type == token_type

    def matchOneOf(self, token_types):
        return self.tokens[self.index].type in token_types

    def unary_expr(self):
        if self.match(lexer.TokenType.Number):
            token = self.tokens[self.index]
            self.eat(lexer.TokenType.Number)
            return ast.AstNumber(token.value)
        elif self.match(lexer.TokenType.Identifier):
            token = self.tokens[self.index]
            self.eat(lexer.TokenType.Identifier)
            if self.match(lexer.TokenType.LParen):
                self.eat(lexer.TokenType.LParen)
                params = []
                while not self.match(lexer.TokenType.RParen):
                    params.append(self.expr())
                    if self.match(lexer.TokenType.Comma):
                        self.eat(lexer.TokenType.Comma)
                self.eat(lexer.TokenType.RParen)
                return ast.AstFunctionCall(token.value, params)
            return ast.AstVariable(token.value)
        else:
            self.error('Expected Number or Identifier')

    def factor(self):
        unary = self.unary_expr()
        while self.match(lexer.TokenType.Star) or self.match(lexer.TokenType.Slash):
            token = self.tokens[self.index]
            self.eat(token.type)
            unary = ast.AstBinaryOp(token.value, unary, self.unary_expr())
        return unary

    def term(self):
        factor = self.factor()
        while self.match(lexer.TokenType.Plus) or self.match(lexer.TokenType.Minus):
            token = self.tokens[self.index]
            self.eat(token.type)
            factor = ast.AstBinaryOp(token.value, factor, self.factor())
        return factor

    def comparison(self):
        term = self.term()
        if self.matchOneOf(lexer.COMPARISON_TYPES):
            token = self.tokens[self.index]
            self.eat(token.type)
            term = ast.AstBinaryOp(token.value, term, self.term())
        return term

    def expr(self):
        return self.comparison()

    def var_definition(self):
        self.eat(lexer.TokenType.Identifier)
        self.eat(lexer.TokenType.Equal)
        return ast.AstAssignment(
            ast.AstVariable(self.tokens[self.index - 2].value),
            self.expr()
        )

    def if_statement(self):
        self.eat(lexer.TokenType.Key_If)
        condition = self.comparison()
        body = self.block()
        return ast.AstIf(condition, body)

    def while_statement(self):
        self.eat(lexer.TokenType.Key_While)
        condition = self.comparison()
        body = self.block()
        return ast.AstWhile(condition, body)

    def do_while_statement(self):
        self.eat(lexer.TokenType.Key_Do)
        body = self.block()
        self.eat(lexer.TokenType.Key_While)
        condition = self.comparison()
        self.eat(lexer.TokenType.SemiColon)
        return ast.AstDoWhile(condition, body)

    def statement(self):
        if self.match(lexer.TokenType.Key_If):
            return self.if_statement()
        elif self.match(lexer.TokenType.Key_While):
            return self.while_statement()
        elif self.match(lexer.TokenType.Key_Do):
            return self.do_while_statement()
        if self.match(lexer.TokenType.Identifier) and self.tokens[self.index + 1].type == lexer.TokenType.Equal:
            defi = self.var_definition()
            self.eat(lexer.TokenType.SemiColon)
            return defi
        expr = self.expr()
        self.eat(lexer.TokenType.SemiColon)
        return expr

    def block(self):
        block = ast.AstBlock()
        self.eat(lexer.TokenType.LCurly)
        while not self.match(lexer.TokenType.RCurly):
            block.add_child(self.statement())
        self.eat(lexer.TokenType.RCurly)
        return block

    def parse(self):
        program = ast.AstProgram()
        while self.index < len(self.tokens):
            if self.match(lexer.TokenType.EOF):
                break
            program.add_child(self.statement())
        return program
