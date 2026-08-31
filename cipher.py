"""Reads a text file, encrypts its contents using a custom shift cipher based on 
character categories, and provides functions to decrypt and verify the output."""

def welcome_banner():
    """Displays a welcome banner for the encryption tool"""
    width = 58
    print("=" * width)
    print("| Encryption tool |".center(width))
    print("=" * width)
    print("Enter your values (non-negative integer) below".center(width))
    print('-' * width)


def get_shift_input(prompt_text: str) -> int:
    """
    Prompts the user for a shift value and validates the input.
    Continues to prompt until a valid non-negative integer is provided.
    """
    while True:
        try:
            val = int(input(prompt_text))
            if val >= 0:
                return val  # Exit loop and return valid value
            print("That was not a non-negative integer! Please enter a number 0 or greater")
        except ValueError:
            print("That was not a non-negative integer! Please enter a number 0 or greater")


def encrypt_file(shift_1: int, shift_2: int, input_path: str, output_path: str) -> None:
    """
    Reads text from input_path, applies specific shift rules to characters 
    based on their category, and writes the encrypted text to output_path.
    """
    with open(input_path, 'r', encoding="utf-8") as file:
        text = file.read()   
    encrypted_text = ''

    for char in text:
        # First half lowercase: shift forward by shift_1 * shift_2
        if 'a' <= char <= 'n':
            position = ord(char) - ord('a')
            encrypted_text += chr(ord('a') + (position + shift_1 * shift_2) % 14)

        # Second half lowercase: shift backward by shift_1 + shift_2    
        elif 'o' <= char <= 'z':
            position = ord(char) - ord('o')
            encrypted_text += chr(ord('o') + (position - (shift_1 + shift_2)) % 12)

        # First half uppercase: shift backward by shift_1
        elif 'A' <= char <= 'M':
            position = ord(char) - ord('A')
            encrypted_text += chr(ord('A') + (position - shift_1) % 13)

        # Second half uppercase: shift forward by shift_2 squared
        elif 'N' <= char <= 'Z':
            position = ord(char) - ord('N')
            encrypted_text += chr(ord('N') + (position + shift_2 ** 2) % 13)

        # Digits: shift forward by shift_1 - shift_2    
        elif '0' <= char <= '9':
            encrypted_text += str((int(char) + shift_1 - shift_2) % 10)

        # Special characters and whitespace remain unchanged
        else:
            encrypted_text += char
            

    with open(output_path, 'w', encoding="utf-8") as file:
        file.write(encrypted_text)


def decrypt_file(shift_1: int,shift_2: int,input_path: str,output_path: str) -> None:
    """
    Reads encrypted text from input_path, reverses the shift rules to retrieve 
    the original text, and writes the decrypted output to output_path.
    """
    with open(input_path, 'r', encoding="utf-8") as file:
        text = file.read()   
    decrypted_text = ''

    for char in text:
        # Reverse forward shift (subtract shift_1 * shift_2)
        if 'a' <= char <= 'n':
            position = ord(char) - ord('a')
            decrypted_text += chr(ord('a') + (position - shift_1 * shift_2) % 14)

        # Reverse backward shift (add shift_1 + shift_2)
        elif 'o' <= char <= 'z':
            position = ord(char) - ord('o')
            decrypted_text += chr(ord('o') + (position + (shift_1 + shift_2)) % 12)

        # Reverse backward shift (add shift_1)
        elif 'A' <= char <= 'M':
            position = ord(char) - ord('A')
            decrypted_text += chr(
            ord('A') + (position + shift_1) % 13)

        # Reverse forward shift (subtract shift_2 squared)
        elif 'N' <= char <= 'Z':
            position = ord(char) - ord('N')
            decrypted_text += chr(ord('N') + (position - shift_2 ** 2) % 13)

        # Reverse forward shift (subtract shift_1 - shift_2)
        elif '0' <= char <= '9':
            decrypted_text += str((int(char) - shift_1 + shift_2) % 10)

        # Special characters and whitespace remain unchanged
        else:
            decrypted_text += char

    with open(output_path, 'w', encoding="utf-8") as file:
        file.write(decrypted_text)


def verify_files(file_1: str, file_2: str) -> bool:
    """
    Compares the original raw text file with the decrypted text file 
    character by character to verify the cipher's integrity.
    """
    with open(file_1, 'r', encoding="utf-8") as f1, open(file_2, 'r', encoding="utf-8") as f2:
        content_1 = f1.read()
        content_2 = f2.read()
    if content_1 == content_2:
        print("Match confirmed: Decrypted text matches the original.")
        return True
    errors = 0

    for i, char in enumerate(content_1):
        if i >= len(content_2) or char != content_2[i]:
            errors += 1

        # Count any extra characters in the decrypted file
    if len(content_2) > len(content_1):
        errors += len(content_2) - len(content_1)

    print("The files are not identical.\n" f"Number of errors found: {errors}")
    return False


welcome_banner()

# Get user inputs
shift_1 = get_shift_input("Enter the first shift value: ")
shift_2 = get_shift_input("Enter the second shift value: ")

# Define file paths
raw_text = 'raw_text.txt'
encrypted_text = 'encrypted_text.txt'
decrypted_text = 'decrypted_text.txt'

# Run encryption, decryption and verification functions
encrypt_file(shift_1, shift_2, raw_text, encrypted_text)
decrypt_file(shift_1, shift_2, encrypted_text, decrypted_text)
verify_files(raw_text, decrypted_text)
