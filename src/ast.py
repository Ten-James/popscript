class AstNode:
    def __init__(self):
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return self.__class__.__name__ + ' ' + str(self.children)

    def __repr__(self):
        return self.__str__()


class AstNumber(AstNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f'{self.__class__.__name__} {self.value}'


class AstVariable(AstNode):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f'{self.__class__.__name__} {self.name}'


class AstBinaryOp(AstNode):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.add_child(left)
        self.add_child(right)

    def __str__(self):
        return f'{self.__class__.__name__} {self.op} \n {self.children[0]} \n {self.children[1]}'


class AstFunctionCall(AstNode):
    def __init__(self, name, params):
        super().__init__()
        self.name = name
        self.params = params

    def __str__(self):
        return f'{self.__class__.__name__} {self.name} {self.params}'


class AstIf(AstNode):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def __str__(self):
        return f'{self.__class__.__name__} {self.condition} {self.body}'


class AstWhile(AstNode):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def __str__(self):
        return f'{self.__class__.__name__} {self.condition} {self.body}'


class AstDoWhile(AstNode):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def __str__(self):
        return f'{self.__class__.__name__} {self.condition} {self.body}'


class AstBlock(AstNode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.__class__.__name__} {self.children}'


class AstAssignment(AstNode):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    def __str__(self):
        return f'{self.__class__.__name__} {self.name} = {self.value}'


class AstProgram(AstNode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'{self.__class__.__name__} {self.children}'
