"""Create a Python script named evaluator.py that reads math expressions line-by-line from an input file, evaluates them, and writes structured results to output.txt"""
sample_input = 'sample_input.txt'
input_text = 'input.txt'
output_text = 'output.txt'

def welcome_banner():
    width = 58
    print("=" * width)
    print("Evaluation tool".center(width))
    print("=" * width)

def tokenize(question):
    tokens = []
    i = 0
    while i < len(question):
        char = question[i]
        if char.isspace():
            i += 1
            continue
        if char.isdigit():
            num = ""
            while i < len(question) and question[i].isdigit():
                num += question[i]
                i += 1
            tokens.append(("NUM", num))
            continue
        if char in "+-*/%^":
            tokens.append(("OP", char))
            i += 1
            continue
        if char in "(":
            tokens.append(("LPAREN", char))
            i += 1
            continue
        if char in ")":
            tokens.append(("RPAREN", char))
            i += 1
            continue
        raise ValueError(f"Invalid character '{char}' in expression.")
    tokens.append(("END", ""))
    return tokens

def tokens_to_string(tokens):
    output = []

    for token_type, token_value in tokens:

        if token_type == "END":
            output.append("[END]")
        else:
            output.append(
                f"[{token_type}:{token_value}]"
            )

    return " ".join(output)
def parse_term(tokens, pos):
    if tokens[pos][0] == "NUM":
        value = int(tokens[pos][1])
        return ("number", value), pos + 1

    raise ValueError("Expected number")

def parse_eval(tokens, pos):
    left, pos = parse_term(tokens, pos)

    while (
        tokens[pos][0] == "OP"
        and tokens[pos][1] in "+-"
    ):
        op = tokens[pos][1]
        pos += 1

        right, pos = parse_term(tokens, pos)

        left = ("binary", op, left, right)

    return left, pos

def tree_to_string(tree):

    if tree[0] == "number":
        return tree[1]

    if tree[0] == "neg":
        return f"(neg {tree_to_string(tree[1])})"

    if tree[0] == "binary":
        operator = tree[1]

        left = tree_to_string(tree[2])
        right = tree_to_string(tree[3])

        return f"({operator} {left} {right})"
def evaluate_file(content):
    results = []
    questions = content.splitlines()
    for question in questions:
        try:
            tokens = tokenize(question)
            token_string = tokens_to_string(tokens)
            tree, pos = parse_eval(tokens, 0)
            if tokens[pos][0] != "END":
                raise ValueError("Unexpected token")
            results.append(f"Question: {question}\nTokens: {token_string}\nTree: {tree_to_string(tree)}\n")
        except ValueError as e:
            results.append(f"Question: {question}\nError: {str(e)}\n")

    with open(output_text, "w") as file:
        file.write("\n".join(results))


#main
welcome_banner()

try:
    with open(input_text, "r") as file:
        content = file.read()
        print(f"Input file {input_text} Exists and read successfully".center(58))
except FileNotFoundError:
    with open(sample_input, "r") as file:
        content = file.read()
        print(f"Input file {input_text} Doesnt Exist".center(58))
        print(f"Sample file {sample_input} read successfully".center(58))
evaluate_file(content)

print(f"Results written to {output_text} successfully.".center(58))