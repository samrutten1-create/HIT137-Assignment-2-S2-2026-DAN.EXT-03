"""Create a Python script named evaluator.py that reads math expressions line-by-line from an input file, evaluates them, and writes structured results to output.txt"""
sampleInput = 'sample_input.txt'
inputText = 'input.txt'
outputText = 'output.txt'
try:
    with open(inputText, "r") as file:
        content = file.read()
        print("Input file Exists and read successfully.")
except FileNotFoundError:
    with open(sampleInput, "r") as file:
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
with open(outputText, "w") as file:
    for r in results:
        file.write(f"Input: {r['input']}\nTree: {r['tree']}\nTokens: {r['tokens']}\nResult: {r['result']}\n\n")