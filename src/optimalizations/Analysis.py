from virtualMachine import ACTION

ACTION_TO_STACK_CHANGE = {
    ACTION.PUSH: 1,
    ACTION.POP: -1,
    ACTION.WRITE: -1,
    ACTION.READ: 1,
    ACTION.SUM: -2,
    ACTION.SUB: -2,
    ACTION.MUL: -2,
    ACTION.DIV: -2,
    ACTION.SWAP: 0,
    ACTION.DUP: 1,
    ACTION.PRINT: -1,
    ACTION.PRINTALL: 0,
    ACTION.OVER: 1,
    ACTION.OP_LESS: -1,
    ACTION.OP_LESS_EQUAL: -1,
    ACTION.NOT: 0,
    ACTION.OP_GREATER: -1,
    ACTION.OP_GREATER_EQUAL: -1,
    ACTION.OP_EQUAL: -1,
    ACTION.OP_NOT_EQUAL: -1,
    ACTION.JMP: 0,
    ACTION.GOTO: 0,
    ACTION.IF_GOTO: 0,
}


class DetailedAction():
    def __init__(self, line: str):
        if line.startswith(':'):
            self.action = ACTION.LABEL
            self.args = [line[1:]]
            self.stack_change = 0
            return
        splited = line.split()
        self.action = ACTION[splited[0]]
        self.args = splited[1:]
        self.stack_change = ACTION_TO_STACK_CHANGE[ACTION[splited[0]]]

    def __str__(self):
        return f'[{self.stack_change:2}] {self.action.name:10} {self.args}'

    def __repr__(self):
        return self.__str__()

    def to_action(self) -> str:
        if self.action == ACTION.LABEL:
            return f':{self.args[0]}'
        return f'{self.action.name} {" ".join(self.args)}'


def to_detailed_actions(lines: list[str]) -> list[DetailedAction]:
    return [DetailedAction(line) for line in lines]

def to_actions(detailed: list[DetailedAction]) -> list[str]:
    return [action.to_action() for action in detailed]

def matches(action: DetailedAction, action_type: ACTION = None, stack: int = None, args=None) -> bool:
    ret = True
    if action_type is not None:
        ret = ret and action.action == action_type
    if stack is not None:
        ret = ret and action.stack_change == stack
    if args is not None:
        ret = ret and action.args == args
    return ret
