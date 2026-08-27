"""Write a program in a file named cipher.py that reads the text file raw_text.txt , 
encrypts its contents using the scheme described below, and writes the result to 
encrypted_text.txt . You must then write a function that decrypts that file, and a 
function that verifies the decryption was successful."""
# Function to display the welcome banner
def welcome_banner():
    width = 58
    print("=" * width)
    print("| Encryption tool |".center(width))
    print("=" * width)
    print("Enter your values (non-negative integer) below".center(width))
    print('-' * width)
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
shift_1 = get_shift_input("Enter the first shift value: ")
shift_2 = get_shift_input("Enter the second shift value: ")
raw_text = 'raw_text.txt'
encrypted_text = 'encrypted_text.txt'
decrypted_text = 'decrypted_text.txt'
def encrypt_file(shift_1: int,shift_2: int,input_path: str,output_path: str) -> None:
    with open(input_path, 'r', encoding="utf-8") as file:
        text = file.read()   
    encrypted_text = ''
    for char in text:
        if 'a' <= char <= 'n':
            position = ord(char) - ord('a')
            encrypted_text += chr(ord('a') + (position + shift_1 * shift_2) % 14)
        elif 'o' <= char <= 'z':
            position = ord(char) - ord('o')
            encrypted_text += chr(ord('o') + (position - (shift_1 + shift_2)) % 12)
        elif 'A' <= char <= 'M':
            position = ord(char) - ord('A')
            encrypted_text += chr(ord('A') + (position - shift_1) % 13)
        elif 'N' <= char <= 'Z':
            position = ord(char) - ord('N')
            encrypted_text += chr(ord('N') + (position + shift_2 ** 2) % 13)
        elif '0' <= char <= '9':
            encrypted_text += str((int(char) + shift_1 - shift_2) % 10)
        else:
            encrypted_text += char
            continue
    with open(output_path, 'w', encoding="utf-8") as file:
        file.write(encrypted_text)
def decrypt_file(    shift_1: int,shift_2: int,input_path: str,output_path: str) -> None:
    with open(input_path, 'r', encoding="utf-8") as file:
        text = file.read()   
    decrypted_text = ''
    for char in text:
        if 'a' <= char <= 'n':
                    position = ord(char) - ord('a')
                    decrypted_text += chr(ord('a') + (position - shift_1 * shift_2) % 14)
        elif 'o' <= char <= 'z':
                    position = ord(char) - ord('o')
                    decrypted_text += chr(ord('o') + (position + (shift_1 + shift_2)) % 12)
        elif 'A' <= char <= 'M':
                    position = ord(char) - ord('A')
                    decrypted_text += chr(
                        ord('A') + (position + shift_1) % 13)
        elif 'N' <= char <= 'Z':
                    position = ord(char) - ord('N')
                    decrypted_text += chr(ord('N') + (position - shift_2 ** 2) % 13)
        elif '0' <= char <= '9':
            decrypted_text += str((int(char) - shift_1 + shift_2) % 10)
        else:
            decrypted_text += char
    with open(output_path, 'w', encoding="utf-8") as file:
        file.write(decrypted_text)
def verify_files(file_1: str, file_2: str) -> bool:
    with open(file_1, 'r', encoding="utf-8") as f1, open(file_2, 'r', encoding="utf-8") as f2:
        content_1 = f1.read()
        content_2 = f2.read()
        if content_1 == content_2:
            print("The files are identical.")
            return True
        elif content_1 != content_2:
            errors = 0
            for i, char in enumerate(content_1):
                if i >= len(content_2) or char != content_2[i]:
                    errors += 1
            print(f"The files are not identical, decryption not possible.\nNumber of errors found: {errors}")
            return False
encrypt_file(shift_1, shift_2, raw_text, encrypted_text)
decrypt_file(shift_1, shift_2, encrypted_text, decrypted_text)
verify_files(raw_text, decrypted_text)