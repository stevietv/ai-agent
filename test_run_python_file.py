from functions.run_python_file import run_python_file

def main():

    print(f"Running main.py")
    print(run_python_file("calculator", "main.py"))

    print(f"Running main.py with args '3+5'")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    print(f"Running tests.py")
    print(run_python_file("calculator", "tests.py"))

    print(f"Running ../main.py")
    print(run_python_file("calculator", "../main.py"))

    print(f"Running nonexistant.py")
    print(run_python_file("calculator", "nonexistent.py"))

    print(f"Running lorem.txt")
    print(run_python_file("calculator", "lorem.txt"))

if __name__ == "__main__":
    main()
