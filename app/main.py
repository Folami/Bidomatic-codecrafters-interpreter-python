import sys
from py_lox import PyLox

def main():
    lox = PyLox()
    if len(sys.argv) > 2:
        print("Usage: pylox [script]", file=sys.stderr)
        sys.exit(1)
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()

if __name__ == "__main__":
    main()