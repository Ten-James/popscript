from src.parser import Parser
from src.codegen import CodeGen
from src.checkers.checker import SemanticChecker
from src.optimalizations.control import process
import argparse

def main():
    parser = argparse.ArgumentParser(description='Pop compiler')
    parser.add_argument('filename', type=str, help='File to compile')
    parser.add_argument('--output', type=str, help='Output file')
    parser.add_argument('--optimalization', action='store_true', help='Should optimalize code')
    args = parser.parse_args()
    with open(args.filename) as f:
        code = f.read()
    parser = Parser(code)
    ast = parser.parse()
    checker = SemanticChecker(ast)
    checker.check()
    codegen = CodeGen(ast)
    code = codegen.generate()
    if args.optimalization:
        code = process(code)

    if args.output:
        with open(args.output, 'w') as f:
            f.write('\n'.join(code))
    else:
        print('\n'.join(code))



if __name__ == '__main__':
    main()