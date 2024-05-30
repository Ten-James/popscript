from virtualMachine import ACTION
from src.ast import *

BINARY_OPS = {
    '+': ACTION.SUM,
    '-': ACTION.SUB,
    '*': ACTION.MUL,
    '/': ACTION.DIV,
    '<': ACTION.OP_LESS,
    '>': ACTION.OP_GREATER,
    '<=': ACTION.OP_LESS_EQUAL,
    '>=': ACTION.OP_GREATER_EQUAL,
    '==': ACTION.OP_EQUAL,
    '!=': ACTION.OP_NOT_EQUAL,
}


class CodeGen:
    def __init__(self, program: AstProgram):
        self.code = []
        self.label_index = 0
        self.program = program

    def visit(self, node):
        if isinstance(node, AstProgram):
            for child in node.children:
                self.visit(child)
        elif isinstance(node, AstBlock):
            for child in node.children:
                self.visit(child)
        elif isinstance(node, AstVariable):
            self.code.append(f'{ACTION.READ.name} {node.name}')
        elif isinstance(node, AstAssignment):
            self.visit(node.value)
            self.code.append(f'{ACTION.WRITE.name} {node.name.name}')
        elif isinstance(node, AstNumber):
            self.code.append(f'{ACTION.PUSH.name} {node.value}')
        elif isinstance(node, AstBinaryOp):
            self.visit(node.children[0])
            self.visit(node.children[1])
            self.code.append(BINARY_OPS[node.op].name)
        elif isinstance(node, AstFunctionCall):
            for param in node.params:
                self.visit(param)
            if node.name == 'print':
                self.code.append(ACTION.PRINT.name)
            elif node.name == 'read':
                self.code.append(ACTION.SCAN.name)
            else:
                raise NotImplemented
        elif isinstance(node, AstIf):
            label = f"l{self.label_index}"
            self.visit(node.condition)
            self.code.append(ACTION.JMP.name + ' 1')
            self.code.append(ACTION.GOTO.name + f' {label}')
            self.visit(node.body)
            self.code.append(':' + label)
            self.label_index += 1
        elif isinstance(node, AstWhile):
            label = f"l{self.label_index}"
            label2 = f"l{self.label_index + 1}"
            self.code.append(':' + label)
            self.visit(node.condition)
            self.code.append(ACTION.JMP.name + ' 1')
            self.code.append(ACTION.GOTO.name + f' {label2}')
            self.visit(node.body)
            self.code.append(ACTION.GOTO.name + f' {label}')
            self.code.append(':' + label2)
            self.label_index += 2
        elif isinstance(node, AstDoWhile):
            label = f"l{self.label_index}"
            self.code.append(':' + label)
            self.visit(node.body)
            self.visit(node.condition)
            self.code.append(ACTION.NOT.name)
            self.code.append(ACTION.JMP.name + ' 1')
            self.code.append(ACTION.GOTO.name + f' {label}')
            self.label_index += 1
        else:
            raise ValueError(f'Unknown node {node.__class__.__name__}')

    def generate(self):
        self.visit(self.program)
        return self.code
