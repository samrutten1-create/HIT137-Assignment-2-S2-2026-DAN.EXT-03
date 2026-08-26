"""Create a Python script named evaluator.py that reads math expressions line-by-line from an input file, evaluates them, and writes structured results to output.txt"""
sample_input = 'sample_input.txt'
input_text = 'input.txt'
output_text = 'output.txt'
def welcome_banner():
    width = 58
    print("=" * width)
    print("Evaluation tool".center(width))
    print("=" * width)
welcome_banner()
try:
    with open(input_text, "r") as file:
        content = file.read()
        print("Input file Exists and read successfully.")
except FileNotFoundError:
    with open(sample_input, "r") as file:
        content = file.read()
        print("Input file Doesnt Exist. Sample input file read successfully.")
questions = content.splitlines()
results = []
for question in questions:
    try:
        result = eval(question)
        tree = "not done yet"
        tokens = "not done yet"
        results.append({"input": question,"tree": tree, "tokens": tokens, "result": result})
    except Exception as e:
        tree = "not done yet"
        tokens = "not done yet"  
        results.append({"input": question,"tree": "Error", "tokens": "Error", "result": "Error"})
with open(output_text, "w") as file:
    for r in results:
        file.write(f"Input: {r['input']}\nTree: {r['tree']}\nTokens: {r['tokens']}\nResult: {r['result']}\n\n")

print(f"Results written to {output_text} successfully.")