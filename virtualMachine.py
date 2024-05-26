import argparse
from enum import Enum, auto


class ACTION(Enum):
    PUSH = auto()
    POP = auto()
    SUM = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    SWAP = auto()
    DUP = auto()
    PRINT = auto()
    PRINTALL = auto()


class VirtualMachine:
    def __init__(self):
        self.stack = []

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
        elif action == ACTION.PRINTALL.name:
            print(self.stack)
            self.stack = []
        else:
            raise ValueError(f"Action {action} not recognized")

    def execute_all(self, actions: list) -> None:
        for action in actions:
            self.execute(action)

    def get_stack(self) -> list:
        return self.stack

    def clear_stack(self) -> None:
        self.stack = []


def main():
    parser = argparse.ArgumentParser(description='Virtual Machine')
    parser.add_argument('file', type=str, help='File with actions')
    args = parser.parse_args()
    with open(args.file) as f:
        actions = f.readlines()
    vm = VirtualMachine()
    vm.execute_all(actions)


if __name__ == '__main__':
    main()