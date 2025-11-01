import sys
import string
import math # Needed for the GCD check in key validation

# --- 📚 AFFINE CIPHER LOGIC AND CONSTANTS ---

ALPHABET_SIZE = 26

# Multiplicative inverses of 'a' modulo 26.
# a^-1 only exists if gcd(a, 26) == 1.
# Keys 'a' must be from this list: {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25}
MOD_INVERSE = {
    1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25
}

def get_char_index(char):
    """Converts an alphabetic character (A-Z or a-z) to its 0-25 index."""
    char = char.upper()
    if 'A' <= char <= 'Z':
        return ord(char) - ord('A')
    return None

def get_index_char(index, is_upper):
    """Converts a 0-25 index back to a character, preserving original case."""
    start = ord('A') if is_upper else ord('a')
    return chr(index % ALPHABET_SIZE + start)

def affine_transform_char(char, a, b, mode='encrypt'):
    """
    Applies the Affine Cipher transformation to a single character.
    Encrypt: C = (aP + b) mod 26
    Decrypt: P = a^-1 * (C - b) mod 26
    """
    
    char_index = get_char_index(char)
    if char_index is None:
        return char # Return non-alphabetic characters unchanged

    is_upper = char.isupper()
    
    if mode == 'encrypt':
        # C = (a * P + b) mod 26
        transformed_index = (a * char_index + b) % ALPHABET_SIZE
    
    elif mode == 'decrypt':
        # P = a^-1 * (C - b) mod 26
        
        # 1. Get the modular inverse of 'a' (a_inv)
        a_inv = MOD_INVERSE.get(a)
        if a_inv is None:
            # This case should be caught by get_valid_keys, but serves as a safeguard
            raise ValueError(f"Key 'a' ({a}) has no modular inverse mod 26. Cannot decrypt.")
            
        # 2. Calculate P = a_inv * (C - b) mod 26
        # Python's % handles negative results from (char_index - b) correctly.
        transformed_index = (a_inv * (char_index - b)) % ALPHABET_SIZE
    
    else:
        raise ValueError("Invalid mode: must be 'encrypt' or 'decrypt'.")
        
    return get_index_char(transformed_index, is_upper)

# --- Core Cipher Logic ---

def affine_process_text(text, a, b, mode='encrypt'):
    """
    Encrypts or decrypts text using the Affine Cipher with keys (a, b).
    """
    
    return ''.join(affine_transform_char(char, a, b, mode) for char in text)

def affine_encrypt(plaintext, a, b):
    """Encrypts plaintext using the Affine Cipher."""
    return affine_process_text(plaintext, a, b, mode='encrypt')

def affine_decrypt(ciphertext, a, b):
    """Decrypts ciphertext using the Affine Cipher."""
    # Decryption requires the inverse check to be valid.
    if a not in MOD_INVERSE:
        raise ValueError(f"Decryption failed: Key 'a' ({a}) is invalid (gcd(a, 26) != 1).")
        
    return affine_process_text(ciphertext, a, b, mode='decrypt')

# --- Helper Functions (Key/Input Validation) ---

def get_valid_keys():
    """Prompts the user for valid keys (a, b) and ensures valid input."""
    while True:
        try:
            print("\n  **Key Requirement**: Key 'a' must be coprime with 26 (gcd(a, 26) = 1).")
            print(f"  Valid 'a' values: {', '.join(map(str, sorted(MOD_INVERSE.keys())))}")
            
            a_input = input("  Enter Key 'a' (Multiplicative, 1-25): ")
            b_input = input("  Enter Key 'b' (Additive Shift, 0-25): ")
            
            a = int(a_input)
            b = int(b_input)
            
            if not (1 <= a <= 25 and 0 <= b <= 25):
                print("  Error: Keys must be in the range 1-25 for 'a' and 0-25 for 'b'.")
                continue
            
            if a not in MOD_INVERSE:
                print(f"  Error: Key 'a' ({a}) is not valid. gcd(a, 26) = {math.gcd(a, 26)}. Must be 1.")
                continue
                
            return a, b
            
        except ValueError:
            print("  Error: Invalid input. Please ensure both keys are integers.")

# --- Menu Functions ---

def run_encryption_mode():
    """Handles the user interaction for Affine encryption."""
    print("\n--- ENCRYPTION MODE ---")
    plaintext = input("  Enter Plaintext (message to hide): ")
    
    try:
        a, b = get_valid_keys()
        ciphertext = affine_encrypt(plaintext, a, b)
        
        print("\n--- RESULT ---")
        print(f"  Plaintext:  {plaintext}")
        print(f"  Key (a, b): ({a}, {b})")
        print(f"  Ciphertext: {ciphertext}\n")
    except ValueError as e:
        print(f"\n  Error: {e}\n")

def run_decryption_mode():
    """Handles the user interaction for Affine decryption."""
    print("\n--- DECRYPTION MODE ---")
    ciphertext = input("  Enter Ciphertext (message to reveal): ")
    
    try:
        a, b = get_valid_keys()
        decrypted_text = affine_decrypt(ciphertext, a, b)
        
        print("\n--- RESULT ---")
        print(f"  Ciphertext: {ciphertext}")
        print(f"  Key (a, b): ({a}, {b})")
        print(f"  Decrypted:  {decrypted_text}\n")
    except ValueError as e:
        print(f"\n  Error: {e}\n")


def run_cryptanalysis_note():
    """Provides a note on Affine cryptanalysis."""
    print("\n--- CRYPTANALYSIS NOTE ---")
    print("  **Total Keys**: The Affine Cipher has 12 valid 'a' keys (coprime to 26) and 26 valid 'b' keys (0-25).")
    print("  Total possible keys: **12 x 26 = 312**.")
    print("\n  **Vulnerability**: Although 312 keys is more than Caesar's 25, it's still small enough for a quick computer brute-force attack.")
    print("  However, the standard attack is a **Known-Plaintext Attack** or **Frequency Analysis**.")
    print("  1. **Known-Plaintext**: If two plaintext/ciphertext pairs are known (P1/C1 and P2/C2), one can set up a system of two linear equations modulo 26 to solve for 'a' and 'b'.")
    print("  2. **Frequency Analysis**: The most frequent letter in the ciphertext is assumed to correspond to 'E' (or 'T'), and the second most frequent is assumed to correspond to 'T' (or 'A'). This provides two pairs to solve the linear equations.")
    print("-" * 60)

# --- Main Program Loop ---

def main_menu():
    """The main entry point for the application, displaying the menu loop."""
    while True:
        print("=" * 60)
        print("  AFFINE CIPHER TOOL (The ax+b mod 26 Cipher) 🔐")
        print("=" * 60)
        print("  1. Encrypt Message")
        print("  2. Decrypt Message (Requires Keys a, b)")
        print("  3. Cryptanalysis Note")
        print("  4. Exit")
        print("-" * 60)
        
        choice = input("  Select an option (1-4): ")
        
        if choice == '1':
            run_encryption_mode()
        elif choice == '2':
            run_decryption_mode()
        elif choice == '3':
            run_cryptanalysis_note()
        elif choice == '4':
            print("\nExiting the program. Goodbye! 👋")
            sys.exit(0)
        else:
            print("\n  Invalid choice. Please select an option between 1 and 4.")
            
        print("=" * 60)

# Standard Python idiom to run the main function
if __name__ == '__main__':
    main_menu()