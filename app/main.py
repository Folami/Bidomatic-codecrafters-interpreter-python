import sys


def handle_single_char_token(c):
    tokens = {
        '(': 'LEFT_PAREN',
        ')': 'RIGHT_PAREN',
        '{': 'LEFT_BRACE',
        '}': 'RIGHT_BRACE',
        ',': 'COMMA',
        '.': 'DOT',
        '-': 'MINUS',
        '+': 'PLUS',
        ';': 'SEMICOLON',
        '*': 'STAR',
        '/': 'SLASH'  # Add division operator to single char tokens
    }
    if c in tokens:
        print(f"{tokens[c]} {c} null")
        return True
    return False


def handle_two_char_operator(text, index):
    if index + 1 >= len(text):
        return 0
        
    two_char = text[index:index + 2]
    operators = {
        '<=': 'LESS_EQUAL',
        '>=': 'GREATER_EQUAL',
        '==': 'EQUAL_EQUAL',
        '!=': 'BANG_EQUAL'
    }
    
    if two_char in operators:
        print(f"{operators[two_char]} {two_char} null")
        return 2
    return 0


def handle_single_char_operator(c):
    operators = {
        '<': 'LESS',
        '>': 'GREATER',
        '=': 'EQUAL',
        '!': 'BANG'
    }
    
    if c in operators:
        print(f"{operators[c]} {c} null")
        return True
    return False


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    print("Logs from your program will appear here!", file=sys.stderr)
    
    line_number = 1
    index = 0
    has_error = False

    while index < len(file_contents):
        c = file_contents[index]
        
        # Handle newlines
        if c == '\n':
            line_number += 1
            index += 1
            continue
            
        # Handle whitespace
        if c.isspace():
            index += 1
            continue
            
        # Handle comments and division
        if c == '/' and index + 1 < len(file_contents):
            next_char = file_contents[index + 1]
            if next_char == '/':
                # Skip until end of line or EOF
                while index < len(file_contents):
                    if file_contents[index] == '\n':
                        break
                    index += 1
                continue
            else:
                # It's a division operator
                handle_single_char_token(c)
                index += 1
                continue
        # Handle normal division operator case
        elif c == '/':
            handle_single_char_token(c)
            index += 1
            continue
                
        # Handle single-character tokens
        if handle_single_char_token(c):
            index += 1
            continue
            
        # Handle two-character operators
        consumed = handle_two_char_operator(file_contents, index)
        if consumed > 0:
            index += consumed
            continue
            
        # Handle single-character operators
        if handle_single_char_operator(c):
            index += 1
            continue
            
        # Invalid character
        print(f"[line {line_number}] Error: Unexpected character: {c}", file=sys.stderr)
        has_error = True
        index += 1

    print("EOF  null")
    exit(65 if has_error else 0)


if __name__ == "__main__":
    main()



import sys





# ...existing code...

def main():
    # ...existing code...

    
                
        # Rest of the code remains the same...
        # ...existing code...

