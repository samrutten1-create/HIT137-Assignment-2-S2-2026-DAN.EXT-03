"""Write a program in a file named cipher.py that reads the text file raw_text.txt , 
encrypts its contents using the scheme described below, and writes the result to 
encrypted_text.txt . You must then write a function that decrypts that file, and a 
function that verifies the decryption was successful."""
# Function to display the welcome banner
def welcome_banner():
    width = 58
    print("=" * width)
    print("Encryption tool".center(width))
    print("Enter values below to begin encryption".center(width))
    print("=" * width)
# Function to handle non-negative integer input validation
def get_shift_input(prompt_text: str) -> int:
    while True:
        try:
            val = int(input(prompt_text))
            if val >= 0:
                return val  # Exit loop and return valid value
            print("That was not a non-negative integer! Please enter a number 0 or greater")
        except ValueError:
            print("That was not a non-negative integer! Please enter a number 0 or greater")
#Display welcome banner
welcome_banner()
# Get user inputs using the helper function
shift1 = get_shift_input("Enter shift1 value (non-negative integer): ")
shift2 = get_shift_input("Enter shift2 value (non-negative integer): ")
rawText = 'raw_text.txt'
encryptedText = 'encrypted_text.txt'
decryptedText = 'decrypted_text.txt'
def encrypt_file(shift1, shift2, input_path, output_path):
    with open(input_path, 'r', encoding="utf-8") as file:
        text = file.read()   
    encryptedText = ''
    for i, char in enumerate(text):
        if char.isalpha():
            if char.islower():
                if (ord(char) - 97) <= 13:
                    encryptedText += chr((ord(char) + (shift1 * shift2)))
                else:
                    encryptedText += chr((ord(char) - (shift1 + shift2)))
            elif char.isupper():
                if (ord(char) - 65) <= 12:
                    encryptedText += chr((ord(char) - shift1))
                else:
                    encryptedText += chr((ord(char) + (shift2**2)))
            else:
                print(f"ERROR: ALPHABET CHARACTER '{char}' IS NOT UPPER OR LOWER CASE")
        elif char.isdigit():
            encryptedText += str((int(char) + shift1-shift2)%10)
        else:
            encryptedText += char
            continue
    with open(output_path, 'w', encoding="utf-8") as file:
        file.write(encryptedText)
def create_decryption_map(shift1, shift2):
    decrypt_map = {}
    # Lowercase a-z
    for char in "abcdefghijklmnopqrstuvwxyz":
        if char <= 'n':
            encrypted_char = chr(ord(char) + (shift1 * shift2))
        else:
            encrypted_char = chr(ord(char) - (shift1 + shift2))
        if encrypted_char in decrypt_map:
            print("COLLISION:",decrypt_map[encrypted_char],"and",char,"both encrypt to",repr(encrypted_char))
        decrypt_map[encrypted_char] = char
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if char <= 'M':
            encrypted_char = chr(ord(char) - shift1)
        else:
            encrypted_char = chr(ord(char) + (shift2 ** 2)) 
        if encrypted_char in decrypt_map:
            print("COLLISION:",decrypt_map[encrypted_char],"and",char,"both encrypt to",repr(encrypted_char))
        decrypt_map[encrypted_char] = char
    return decrypt_map
def decrypt_file(shift1, shift2, input_path, output_path):
    decrypt_map = create_decryption_map(shift1, shift2)
    with open(input_path, 'r', encoding="utf-8") as file:
        text = file.read()   
    decryptedText = ''
    for char in text:
        if char in decrypt_map:
            decryptedText += decrypt_map[char]
        elif char.isdigit():
            decryptedText += str((int(char) - shift1 + shift2) % 10)
        else:
            decryptedText += char
    with open(output_path, 'w', encoding="utf-8") as file:
        file.write(decryptedText)
def verify_files(file1, file2):
    with open(file1, 'r', encoding="utf-8") as f1, open(file2, 'r', encoding="utf-8") as f2:
        content1 = f1.read()
        content2 = f2.read()
        if content1 == content2:
            print("The files are identical.")
        elif content1 != content2:
            errors = 0
            for i, char in enumerate(content1):
                if i >= len(content2) or char != content2[i]:
                    errors += 1
            print(f"The files are not identical. Number of errors found: {errors}")
encrypt_file(shift1, shift2, rawText, encryptedText)
decrypt_file(shift1, shift2, encryptedText, decryptedText)
verify_files(rawText, decryptedText)