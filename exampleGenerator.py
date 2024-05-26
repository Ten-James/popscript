import os

def generate_example():
    """UTIL for generating example files"""
    name = input("Enter the name of example: ")
    os.system(f"mkdir examples/{name}")
    with open("test.pop") as f:
        code = f.read()
    with open(f"examples/{name}/src.pop", "w") as f:
        f.write(code)
    os.system(f"python pop.py examples/{name}/src.pop --output examples/{name}/tape.byte")
    os.system(f"python pop.py examples/{name}/src.pop --optimalization --output examples/{name}/optimized_tape.byte")
    os.system(f"python virtualMachine.py examples/{name}/tape.byte > examples/{name}/output.txt")
    os.system(f"python virtualMachine.py examples/{name}/optimized_tape.byte > examples/{name}/optimized_output.txt")

def regenerate_examples():
    for folder in os.listdir("examples"):
        os.system(f"python pop.py examples/{folder}/src.pop --output examples/{folder}/tape.byte")
        os.system(f"python pop.py examples/{folder}/src.pop --optimalization --output examples/{folder}/optimized_tape.byte")
        os.system(f"python virtualMachine.py examples/{folder}/tape.byte > examples/{folder}/output.txt")
        os.system(f"python virtualMachine.py examples/{folder}/optimized_tape.byte > examples/{folder}/optimized_output.txt")

def run_examples():
    os.system("mkdir dist")
    for folder in os.listdir("examples"):
        os.system(f"mkdir dist/{folder}")
        os.system(f"python pop.py examples/{folder}/src.pop --output dist/{folder}/tape.byte")
        os.system(f"python pop.py examples/{folder}/src.pop --optimalization --output dist/{folder}/o_tape.byte")
        os.system(f"python virtualMachine.py dist/{folder}/tape.byte > dist/{folder}/output.txt")
        os.system(f"python virtualMachine.py dist/{folder}/o_tape.byte > dist/{folder}/o_output.txt")
        os.system(f"diff dist/{folder}/output.txt examples/{folder}/output.txt")
        print(f"Example {folder} passed")
    print("All examples passed")

def test():
    os.system("mkdir dist")
    os.system("python pop.py test.pop --output dist/tape.byte")
    os.system("python virtualMachine.py dist/tape.byte")


def main():
    choice = input("generate or run examples or test? (g/r/t): ")
    if choice == "g":
        generate_example()
    elif choice == "r":
        regenerate_examples()
        run_examples()
    elif choice == "t":
        test()




if __name__ == '__main__':
    main()