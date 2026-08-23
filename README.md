# HIT137-Assignment-2-S2-2026
Python solutions for HIT137 Group Assignment 2 featuring a custom file encryption tool `cipher.py` and a functional recursive descent math expression evaluator `evaluator.py`.

## Development History

Development of `cipher.py` followed several trial approaches. The first version used `ord()`, `chr()` and `% 26` to shift letters within the alphabet. This successfully encrypted the text, but decryption initially produced a large number of errors.

Several decryption methods were tested. One approach directly reversed the encryption shift, while a later approach calculated two possible original characters and checked which alphabet half each result belonged to. Testing reduced the number of verification errors, with commits recording improvements from around **1300 errors to 326**, and another trial reaching **241 errors**.

Input handling was then improved by adding a function that only accepts non-negative integers for `shift1` and `shift2`. UTF-8 encoding was also added when reading and writing files.

During testing, `encrypted_text.txt` and `decrypted_text.txt` were removed from Git tracking because they are generated automatically whenever the program runs.

The latest approach introduced a **decryption map**. The program generates a dictionary mapping encrypted characters back to their original characters. This made the decryption code simpler and also revealed an important problem: some shift values can cause two different original letters to encrypt to the same character. Collision detection was therefore added to identify these cases.

