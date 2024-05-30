import argparse
from enum import Enum, auto


class ACTION(Enum):
    PUSH = auto()
    POP = auto()
    READ = auto()
    WRITE = auto()
    SUM = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    SWAP = auto()
    DUP = auto()
    PRINT = auto()
    SCAN = auto()
    PRINTALL = auto()
    OVER = auto()
    OP_LESS = auto()
    OP_LESS_EQUAL = auto()
    OP_GREATER = auto()
    OP_GREATER_EQUAL = auto()
    OP_EQUAL = auto()
    OP_NOT_EQUAL = auto()
    NOT = auto()
    # jump instructions pop from stack and jump args steps
    JMP = auto()
    # go to label
    GOTO = auto()
    IF_GOTO = auto()
    LABEL = auto()


class VirtualMachine:
    def __init__(self, debug=False):
        self.scopes = {}
        self.stack = []
        self.pointer = 0
        self.max_pointer = 0
        self.labels = {}
        self.debug = debug

    def execute(self, action: str) -> None:
        # Split the action string into a list of words
        words = action.split()
        # first word is the action rest is the arguments
        action = words[0]
        args = words[1:]
        if action == ACTION.PUSH.name:
            self.stack.append(int(args[0]))
        elif action == ACTION.POP.name:
            self.stack.pop()
        elif action == ACTION.WRITE.name:
            val = self.stack.pop()
            self.scopes[args[0]] = val
        elif action == ACTION.READ.name:
            if args[0] not in self.scopes:
                raise ValueError(f"Variable {args[0]} not defined")
            self.stack.append(self.scopes[args[0]])
        elif action == ACTION.SUM.name:
            self.stack.append(self.stack.pop() + self.stack.pop())
        elif action == ACTION.SUB.name:
            self.stack.append(self.stack.pop() - self.stack.pop())
        elif action == ACTION.MUL.name:
            self.stack.append(self.stack.pop() * self.stack.pop())
        elif action == ACTION.DIV.name:
            self.stack.append(self.stack.pop() / self.stack.pop())
        elif action == ACTION.SWAP.name:
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        elif action == ACTION.DUP.name:
            self.stack.append(self.stack[-1])
        elif action == ACTION.PRINT.name:
            print(self.stack.pop())
        elif action == ACTION.SCAN.name:
            val = int(input())
            self.stack.append(val)
        elif action == ACTION.PRINTALL.name:
            print(self.stack)
            self.stack = []
        elif action == ACTION.OVER.name:
            self.stack.append(self.stack[-2])
        elif action == ACTION.OP_LESS.name:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b < a)
        elif action == ACTION.OP_LESS_EQUAL.name:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b <= a)
        elif action == ACTION.NOT.name:
            self.stack.append(not self.stack.pop())
        elif action == ACTION.OP_GREATER.name:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b > a)
        elif action == ACTION.OP_GREATER_EQUAL.name:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b >= a)
        elif action == ACTION.OP_EQUAL.name:
            self.stack.append(self.stack.pop() == self.stack.pop())
        elif action == ACTION.OP_NOT_EQUAL.name:
            self.stack.append(self.stack.pop() != self.stack.pop())
        elif action == ACTION.JMP.name:
            val = self.stack.pop()
            if val != 0:
                self.pointer += int(args[0])
        elif action == ACTION.GOTO.name:
            self.pointer = self.labels[args[0]]
        elif action == ACTION.IF_GOTO.name:
            val = self.stack.pop()
            if val != 0:
                self.pointer = self.labels[args[0]]
        else:
            raise ValueError(f"Action {action} not recognized")

    def read_labels(self, actions: list) -> None:
        self.labels = {}
        for i, action in enumerate(actions):
            if action.startswith(":"):
                self.labels[action[1:].strip()] = i

    def execute_all(self, actions: list) -> None:
        self.read_labels(actions)
        self.max_pointer = len(actions)
        while self.pointer < self.max_pointer:
            if actions[self.pointer].startswith(":"):
                self.pointer += 1
                continue
            action = actions[self.pointer]
            self.execute(action)
            if self.debug:
                print(f"Pointer: {self.pointer}, Action: {action}")
                print(f"Scopes: {self.scopes}")
                print(f"Stack: {self.stack}")
                input("Press Enter to continue...")
            self.pointer += 1

    def get_stack(self) -> list:
        return self.stack

    def clear_stack(self) -> None:
        self.stack = []


def main():
    parser = argparse.ArgumentParser(description='Virtual Machine')
    parser.add_argument('file', type=str, help='File with actions')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    args = parser.parse_args()
    with open(args.file) as f:
        actions = f.readlines()
    actions = [action.strip() for action in actions]
    vm = VirtualMachine(args.debug)
    vm.execute_all(actions)


if __name__ == '__main__':
    main()
