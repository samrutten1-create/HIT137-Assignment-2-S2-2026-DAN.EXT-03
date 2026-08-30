"""Create a Python script named evaluator.py that reads math expressions line-by-line from an input file, evaluates them, and writes structured results to output.txt"""
sample_input = 'sample_input.txt'
input_text = 'input.txt'
output_text = 'output.txt'


def welcome_banner():
    """Displays a welcome banner for the evaluation tool"""
    width = 58
    print("=" * width)
    print("| Evaluation tool |".center(width))
    print("=" * width)


def tokenize(question):
    """Breaks a math expression string down into a list of categorized tokens 
    (NUM, OP, LPAREN, RPAREN, END), supporting integers and decimals.
    """
    tokens = []
    i = 0
    while i < len(question):
        char = question[i]

        # Ignore whitespace as spaces do not affect the expression
        if char.isspace():
            i += 1
            continue

        # Read consecutive digits and decimal point as one token
        if char.isdigit():
            num = ""
            while i < len(question) and question[i].isdigit():
                num += question[i]
                i += 1

            if i < len(question) and question[i] == ".":
                num += "."
                i += 1

                if i >= len(question) or not question[i].isdigit():
                    raise ValueError("Invalid number")

            while i < len(question) and question[i].isdigit():
                num += question[i]
                i += 1
    
            tokens.append(("NUM", num))
            continue

        # Store operators
        if char in "+-*/%^":
            tokens.append(("OP", char))
            i += 1
            continue

        # Store '(' and ')' separately
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
    """Convert the tokens into a readable string"""
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
    """Parse numbers and () expressions"""
    if tokens[pos][0] == "NUM":
        value = float(tokens[pos][1])
        return ("number", value), pos + 1

    if tokens[pos][0] == "LPAREN":
        # Recursively checks everything inside the ( )
        pos += 1
        tree, pos = parse_eval(tokens, pos)
        if tokens[pos][0] != "RPAREN":
            raise ValueError("Missing closing parenthesis")
        pos += 1
        return tree, pos
    raise ValueError("Expected number or opening parenthesis")


def parse_power(tokens, pos):
    """ Parse exponentiation. Calling parse_unary makes ^ right-associative"""
    left, pos = parse_primary(tokens, pos)

    if tokens[pos][0] == "OP" and tokens[pos][1] == "^":
        pos += 1
        right, pos = parse_unary(tokens, pos)
        left = ("binary", "^", left, right)

    return left, pos


def parse_unary(tokens, pos):
    """ Parse unary eg. -5, --5 and -(3 + 4) """
    if tokens[pos][0] == "OP" and tokens[pos][1] == "-":
        pos += 1
        operand, pos = parse_unary(tokens, pos)
        return ("neg", operand), pos
    return parse_power(tokens, pos)


def parse_term(tokens, pos):
    """Parse higher operators eg. *, / and % before + and - """
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
    """ Parse + and - """
    left, pos = parse_term(tokens, pos)

    while tokens[pos][0] == "OP" and tokens[pos][1] in "+-":
        op = tokens[pos][1]
        pos += 1
        right, pos = parse_term(tokens, pos)
        left = ("binary", op, left, right)

    return left, pos


def format_number(val: float) -> str:
    """ Formats numbers to integers if whole, else rounds decimals to 4 places"""
    if val % 1 == 0:
        return str(int(val))
    else:
        return str(round(val, 4))

    
def tree_to_string(tree):
    """ Convert the tuple tree into string"""
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
    """Recursively computes the numerical result of the tree."""
    # Num
    if tree[0] == "number":
        return tree[1]
    
    # Neg
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


def evaluate_file(input_path: str) -> list:
    """Reads math expressions line-by-line from the input file, parses and evaluates 
    them, writes structured text blocks to output.txt, and returns a list of dictionaries.
    """
    # Read the content
    with open(input_path, 'r', encoding="utf-8") as file:
        content = file.read()

    # Two separate lists: one for the text file strings, one for the dictionaries
    text_blocks = []
    dict_results = []
    
    questions = content.splitlines()
    for question in questions:
            
        tree_str = "ERROR"
        token_str = "ERROR"
        result_str = "ERROR"
        dict_val = "ERROR"
        
        try:
            # Tokenise first then build the tree 
            tokens = tokenize(question)
            token_str = tokens_to_string(tokens)
            tree, pos = parse_eval(tokens, 0)
            
            # A valid question must finish exactly at the END token
            if tokens[pos][0] != "END":
                raise ValueError("Unexpected token")

            tree_str = tree_to_string(tree)
                
            try:
                raw_result = evaluate(tree)
                result_str = format_number(raw_result)
                dict_val = float(raw_result) # Dictionary requires a float on success
                
            except (ZeroDivisionError, ValueError):
                pass # Leaves values as "ERROR"
                
        except ValueError:
            pass # Leaves values as "ERROR"

        # Append the dictionary format required
        dict_results.append({
            "input": question,
            "tree": tree_str,
            "tokens": token_str,
            "result": dict_val
        })

        # Format the four-line block for the text file
        text_blocks.append(f"Input: {question}\nTree: {tree_str}\nTokens: {token_str}\nResult: {result_str}\n")

    # Write blocks to the file. 
    # Joining with "\n" ensures there is a blank line separating each block
    with open(output_text, "w") as file:
        file.write("\n".join(text_blocks))
        
    # Return the list of dictionaries
    return dict_results


#Main
welcome_banner()
# Trys to open defined input file else reverts to sample input
try:
    with open(input_text, "r") as file:
        print(f"Input file {input_text} Exists and read successfully".center(58))
        print("-"*58)
        returned_data = evaluate_file(input_text)
except FileNotFoundError:
    try:
        with open(sample_input, "r") as file:
            print(f"Input file {input_text} Doesnt Exist".center(58))
            print(f"Sample file {sample_input} read successfully".center(58))
            print("-"*58)
            returned_data = evaluate_file(sample_input)
    except FileNotFoundError:
        print("No input files found. Please ensure input.txt file has been placed in the same directory as evaluator.py")
        exit()
try:
    # If the script reaches this line without crashing, it succeeded
    print(f"** Results written to {output_text} successfully **".center(58))
    print("-" * 58)
except Exception:
    # Catches unexpected system crashes during the file write process
    print(f"!!! Results failed to write to {output_text} !!!".center(58))
    print("-" * 58)
