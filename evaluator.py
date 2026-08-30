"""Create a Python script named evaluator.py that reads math expressions line-by-line from an input file, evaluates them, and writes structured results to output.txt"""
sample_input = 'sample_input.txt'
input_text = 'input.txt'
output_text = 'output.txt'

def welcome_banner():
    """
==========================================================
                   | Evaluation tool |                    
==========================================================
"""
    width = 58
    print("=" * width)
    print("| Evaluation tool |".center(width))
    print("=" * width)

def tokenize(question):
    # breaks the expression into tokens
    tokens = []
    i = 0
    while i < len(question):
        char = question[i]
        # ignore whitespace as spaces do not affect the expression
        if char.isspace():
            i += 1
            continue
        # read consecutive digits as one token
        if char.isdigit():
            num = ""
            while i < len(question) and question[i].isdigit():
                num += question[i]
                i += 1
            tokens.append(("NUM", num))
            continue
        # stores operators
        if char in "+-*/%^":
            tokens.append(("OP", char))
            i += 1
            continue
        # stores '(' and ')' separately
        if char in "(":
            tokens.append(("LPAREN", char))
            i += 1
            continue
        if char in ")":
            tokens.append(("RPAREN", char))
            i += 1
            continue
        # Any Invalid character makes the question invalid
        raise ValueError(f"Invalid character '{char}' in expression.")
    # END marks the point where the question 'should' finish
    tokens.append(("END", ""))
    return tokens

def tokens_to_string(tokens):
    # Convert the tokens into string
    output = []

    for token_type, token_value in tokens:

        if token_type == "END":
            output.append("[END]")
        else:
            output.append(f"[{token_type}:{token_value}]")

    return " ".join(output)

"""
phase relations

parse_eval    -> + and -
parse_term    -> *, / and %
parse_unary   -> unary -
parse_power   -> ^
parse_primary -> nums and ( )

"""
def parse_primary(tokens, pos):
    # numbers and () expressions
    if tokens[pos][0] == "NUM":
        value = int(tokens[pos][1])

        return ("number", value), pos + 1

    if tokens[pos][0] == "LPAREN":
        # recursively checks everything inside the ( )
        pos += 1
        tree, pos = parse_eval(tokens, pos)
        if tokens[pos][0] != "RPAREN":
            raise ValueError("Missing closing parenthesis")
        pos += 1
        return tree, pos
    raise ValueError("Expected number or opening parenthesis")

def parse_power(tokens, pos):
    # Parse exponentiation. Calling parse_unary makes ^ right-associative
    left, pos = parse_primary(tokens, pos)

    if tokens[pos][0] == "OP" and tokens[pos][1] == "^":
        pos += 1
        right, pos = parse_unary(tokens, pos)
        left = ("binary", "^", left, right)

    return left, pos

def parse_unary(tokens, pos):
    # does unary -5, --5 and -(3 + 4)
    if tokens[pos][0] == "OP" and tokens[pos][1] == "-":
        pos += 1
        operand, pos = parse_unary(tokens, pos)
        return ("neg", operand), pos
    return parse_power(tokens, pos)

def parse_term(tokens, pos):
    # does *, / and % before + and -
    left, pos = parse_unary(tokens, pos)
    # Normal *, / and %
    while True:
        if tokens[pos][0] == "OP" and tokens[pos][1] in "*/%":

            op = tokens[pos][1]
            pos += 1

            right, pos = parse_unary(tokens, pos)

            left = ("binary", op, left, right)

            continue
        # Implicit *: 2(3 + 4)
        if tokens[pos][0] == "LPAREN":
            right, pos = parse_unary(tokens, pos)

            left = ("binary", "*", left, right)
            continue
                # Implicit *: (3 + 4)2
        if tokens[pos][0] == "NUM" and tokens[pos - 1][0] == "RPAREN":
            right, pos = parse_unary(tokens, pos)

            left = ("binary", "*", left, right)
            continue
        break
    return left, pos

def parse_eval(tokens, pos):
    # does + and -
    left, pos = parse_term(tokens, pos)

    while tokens[pos][0] == "OP" and tokens[pos][1] in "+-":
        op = tokens[pos][1]
        pos += 1

        right, pos = parse_term(tokens, pos)

        left = ("binary", op, left, right)

    return left, pos

def format_number(val: float) -> str:
    if val % 1 == 0:
        return str(int(val))
    else:
        return str(round(val, 4))
    
def tree_to_string(tree):
 # Convert the tuple tree into string
    if tree[0] == "number":
        return format_number(tree[1])

    if tree[0] == "neg":
        return f"(neg {tree_to_string(tree[1])})"

    if tree[0] == "binary":
        op = tree[1]
        left = tree_to_string(tree[2])
        right = tree_to_string(tree[3])

        return f"({op} {left} {right})"
    
def evaluate(tree):
    # Num
    if tree[0] == "number":
        return tree[1]
    # neg
    if tree[0] == "neg":
        return -evaluate(tree[1])
    #Binary
    if tree[0] == "binary":
        op = tree[1]

        left = evaluate(tree[2])
        right = evaluate(tree[3])

        if op == "+":
            return left + right

        if op == "-":
            return left - right

        if op == "*":
            return left * right

        if op == "/":
            return left / right

        if op == "%":
            return left % right

        if op == "^":
            return left ** right

    raise ValueError("Invalid tree")

def evaluate_file(content):
    # Process each input 
    results = []
    questions = content.splitlines()
    for question in questions:
        try:
            # Tokenise first then build the tree 
            tokens = tokenize(question)
            token_string = tokens_to_string(tokens)
            tree, pos = parse_eval(tokens, 0)
            # A valid question must finish exactly at the END token
            if tokens[pos][0] != "END":
                raise ValueError("Unexpected token")
            try:
                raw_result = evaluate(tree)
                result = format_number(raw_result)
            except (ZeroDivisionError, ValueError) as e:
                result = "ERROR"
            results.append(f"Input: {question}\nTree: {tree_to_string(tree)}\nTokens: {token_string}\nResult: {result}\n")
        except ValueError as e:
            results.append(f"Input: {question}\nTree: ERROR\nTokens: ERROR\nResult: ERROR\n")
    try:
        with open(output_text, "w") as file:
            file.write("\n".join(results))
            return True
    except:
        return False

#main
welcome_banner()
# Trys to open defined input file else reverts to sample input
try:
    with open(input_text, "r") as file:
        content = file.read()
        print(f"Input file {input_text} Exists and read successfully".center(58))
        print("-"*58)
except FileNotFoundError:
    with open(sample_input, "r") as file:
        content = file.read()
        print(f"Input file {input_text} Doesnt Exist".center(58))
        print(f"Sample file {sample_input} read successfully".center(58))
        print("-"*58)
# runs evaluate_file returns boolean base on if the write was sucessfull
if evaluate_file(content):
    print(f"** Results written to {output_text} successfully **".center(58))
    print("-"*58)
else:
    print(f"!!! Results failed to write to {output_text} !!!".center(58))
    print("-"*58)
