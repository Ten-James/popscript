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
    os.system(f"python virtualMachine.py examples/{name}/tape.byte > examples/{name}/output.txt")

def run_examples():
    os.system("mkdir dist")
    for folder in os.listdir("examples"):
        os.system(f"mkdir dist/{folder}")
        os.system(f"python pop.py examples/{folder}/src.pop --output dist/{folder}/tape.byte")
        os.system(f"python virtualMachine.py dist/{folder}/tape.byte > dist/{folder}/output.txt")
        os.system(f"diff dist/{folder}/output.txt examples/{folder}/output.txt")
        print(f"Example {folder} passed")
    print("All examples passed")


def main():
    choice = input("generate or run examples? (g/r): ")
    if choice == "g":
        generate_example()
    elif choice == "r":
        run_examples()



if __name__ == '__main__':
    main()