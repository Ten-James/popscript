from src.ast import *


class SemanticChecker:
    def __init__(self, program: AstProgram):
        self.program = program
        self.scope = {}

    def visit(self, node):
        if isinstance(node, AstProgram):
            for child in node.children:
                self.visit(child)
        elif isinstance(node, AstBlock):
            for child in node.children:
                self.visit(child)
        elif isinstance(node, AstVariable):
            if node.name not in self.scope:
                raise ValueError(f"Variable {node.name} not defined")
            pass
        elif isinstance(node, AstAssignment):
            self.visit(node.value)
            if isinstance(node.name, AstVariable):
                self.scope[node.name.name] = True
            pass
        elif isinstance(node, AstNumber):
            pass
        elif isinstance(node, AstBinaryOp):
            for child in node.children:
                self.visit(child)
            pass
        elif isinstance(node, AstFunctionCall):
            for param in node.params:
                self.visit(param)
            if node.name == 'print':
                pass
            elif node.name == 'read':
                pass
            else:
                raise NotImplemented
        elif isinstance(node, AstIf):
            self.visit(node.condition)
            self.visit(node.body)
        elif isinstance(node, AstWhile):
            self.visit(node.condition)
            self.visit(node.body)
        elif isinstance(node, AstDoWhile):
            self.visit(node.body)
            self.visit(node.condition)
        else:
            raise NotImplemented

    def check(self):
        self.visit(self.program)
        return True
