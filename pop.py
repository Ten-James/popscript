from src.parser import Parser
from src.codegen import CodeGen
import argparse

def main():
    parser = argparse.ArgumentParser(description='Pop compiler')
    parser.add_argument('filename', type=str, help='File to compile')
    parser.add_argument('--output', type=str, help='Output file')
    args = parser.parse_args()
    with open(args.filename) as f:
        code = f.read()
    parser = Parser(code)
    ast = parser.parse()
    codegen = CodeGen(ast)
    code = codegen.generate()
    if args.output:
        with open(args.output, 'w') as f:
            f.write('\n'.join(code))
    else:
        print('\n'.join(code))



if __name__ == '__main__':
    main()