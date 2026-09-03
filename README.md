# HIT137-Assignment-2-S2-2026
Python solutions for HIT137 Group Assignment 2 featuring a custom file encryption tool `cipher.py` and a functional recursive descent math expression evaluator `evaluator.py`.

## Cipher Development History

Development of `cipher.py` followed several trial approaches. The first version used `ord()`, `chr()` and `% 26` to shift letters within the alphabet. This successfully encrypted the text, but decryption initially produced a large number of errors.

Several decryption methods were tested. One approach directly reversed the encryption shift, while a later approach calculated two possible original characters and checked which alphabet half each result belonged to. Testing reduced the number of verification errors, with commits recording improvements from around **1300 errors to 326**, and another trial reaching **241 errors**.

Input handling was then improved by adding a function that only accepts non-negative integers for `shift1` and `shift2`. UTF-8 encoding was also added when reading and writing files.

During testing, `encrypted_text.txt` and `decrypted_text.txt` were removed from Git tracking because they are generated automatically whenever the program runs.

The latest approach introduced a **decryption map**. The program generates a dictionary mapping encrypted characters back to their original characters. This made the decryption code simpler and also revealed an important problem: some shift values can cause two different original letters to encrypt to the same character. Collision detection was therefore added to identify these cases.

## Evaluator Development History

`evaluator.py` was initially created as a blank scaffold for Question 2. The first working approach added file handling to read `input.txt`, with `sample_input.txt` used as a fallback. Expressions are separated line-by-line and stored for processing. Python's `eval()` is currently used as a temporary method to test expression evaluation and error handling. Results are stored as dictionaries and written to `output.txt` using the required Input, Tree, Tokens and Result format. Tree and token generation are still under development, with the next stage being replacement of `eval()` with the required recursive-descent parser.

## Test input file (`raw_text.txt`)

Chosen to exercise every character category the cipher needs to handle:

- A full sentence with mixed-case words and punctuation
- Every lowercase letter a–z (both halves: a–n and o–z)
- Every uppercase letter A–Z (both halves: A–M and N–Z)
- Every digit 0–9
- Punctuation and symbols (`@#$%^&*()_+-={}[]|\:;"'<>,.?/`)
- Tabs and multiple spaces
- A blank line
- Specific boundary letters (`a n o z A M N Z`) and boundary digits (`0 9`)
- Mixed-case words with embedded numbers

## Test cases

| # | shift_1 | shift_2 | Purpose | Result |
|---|---------|---------|---------|--------|
| 1 | 0 | 0 | Edge case: no shift at all should still round-trip (identity case) | ✅ Match confirmed |
| 2 | 5 | 3 | Typical small values | ✅ Match confirmed |
| 3 | 100 | 50 | Large shift values (well beyond alphabet length) | ✅ Match confirmed |
| 4 | 1 | 13 | shift_2 much larger than shift_1 | ✅ Match confirmed |
| 5 | 20 | 1 | shift_1 much larger than shift_2 | ✅ Match confirmed |
| 6 | -5, "abc", then 7, 2 | — | Invalid input handling: negative number, then non-numeric input, before a valid value | ✅ Correctly re-prompted twice, then succeeded |

**Result: 6/6 test cases passed.** `verify_files()` reported `"Match confirmed: Decrypted text matches the original."` in every case, and no test triggered the `"files are not identical"` branch.

## Evidence: sample output (shift_1=5, shift_2=3)

**Original (`raw_text.txt`):**
```
The Quick Brown Fox Jumps Over The Lazy Dog.
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
0123456789
```

**Encrypted (`encrypted_text.txt`):**
```
Pif Zyjdl Jvsoa Asp Eyntw Xzfv Pif Gbrq Lsh.
bcdefghijklmnastuvwxyzopqr
IJKLMABCDEFGHWXYZNOPQRSTUV
2345678901
```

**Decrypted (`decrypted_text.txt`):**
```
The Quick Brown Fox Jumps Over The Lazy Dog.
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
0123456789
```

A `diff` between `raw_text.txt` and `decrypted_text.txt` confirmed the files are
**byte-for-byte identical** — every character, space, tab, and newline round-tripped
correctly, not just the visible text.

## Test 6 console output (invalid input handling)

```
Enter the first shift value: That was not a non-negative integer! Please enter a number 0 or greater
Enter the first shift value: That was not a non-negative integer! Please enter a number 0 or greater
Enter the first shift value: Enter the second shift value: Match confirmed: Decrypted text matches the original.
```

Confirms `get_shift_input()` correctly rejects both a negative number (`-5`) and
non-numeric text (`"abc"`) and keeps re-prompting until a valid value is entered,
without crashing.

## Conclusion

Across zero, small, large, and asymmetric shift values, plus invalid-input
handling, the cipher consistently encrypts and decrypts back to an exact match
of the original file. No mismatches were found in any test.
