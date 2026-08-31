# HIT137-Assignment-2-S2-2026
Python solutions for HIT137 Group Assignment 2 featuring a custom file encryption tool `cipher.py` and a functional recursive descent math expression evaluator `evaluator.py`.
### Group Members:
- Craig Brooks - S407148
- Harrison Breen - S397322
- Richard Tran - S384625
- Sam Rutten - S332039


## Cipher Development History

Development of `cipher.py` followed several trial approaches. The first version used `ord()`, `chr()` and `% 26` to shift letters within the alphabet. This successfully encrypted the text, but decryption initially produced a large number of errors.

Several decryption methods were tested. One approach directly reversed the encryption shift, while a later approach calculated two possible original characters and checked which alphabet half each result belonged to. Testing reduced the number of verification errors, with commits recording improvements from around **1300 errors to 326**, and another trial reaching **241 errors**.

Input handling was then improved by adding a function that only accepts non-negative integers for `shift1` and `shift2`. UTF-8 encoding was also added when reading and writing files.

During testing, `encrypted_text.txt` and `decrypted_text.txt` were removed from Git tracking because they are generated automatically whenever the program runs.

A decryption map and collision detector were then introduced. This revealed that wrapping characters across the entire alphabet allowed characters from different alphabet groups to encrypt to the same value resulting in no notable improvement from the trial that reached **241 errors**.

After reviewing lecturer feedback and the Week 3 `EncryptDecrypt.py` example, the approach was changed so each character wraps within their 'range' : `a-n`, `o-z`, `A-M`, and `N-Z`. This prevented the groups from overlapping and allows the encryption to be reversed directly without a decryption map (then removed).

## Evaluator Development History

Development of `evaluator.py` is as follows. The first working approach added file handling to read `input.txt`, with `sample_input.txt` used as a fallback. Expressions are separated line-by-line and stored for processing. Python's `eval()` was used as a temporary method to test expression evaluation and error handling. Results are stored as dictionaries and written to `output.txt` using the required Input, Tree, Tokens and Result format.

The evaluator was then rebuilt using the **recursive-descent parser**. A tokenizer was added to identify numbers, operators and parentheses. Separate functions were introduced for each level: addition/subtraction, multiplication/division/modulo, unary negation, exponentiation and primary expressions.

Development then added nested parentheses, unary negatives such as `-5` and `--5`, right-associative exponentiation, and implicit multiplication such as `2(3+4)` and `(3+4)2`.

The current version also includes parse-tree formatting, recursive evaluation of the generated tree, handling for invalid expressions and division by zero, the four-line `Input`, `Tree`, `Tokens`, `Result` output, and a returned list of dictionaries.