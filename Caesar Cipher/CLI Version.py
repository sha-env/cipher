import sys
import string # Although string is imported, it's not strictly necessary for the current logic using ord() and chr()

# --- Core Cipher Logic ---

def caesar_shift_char(char, shift):
    """Shifts a single alphabetic character based on the Caesar Cipher rules."""
    
    # Handle lowercase letters
    if 'a' <= char <= 'z':
        start = ord('a')
        # Standard modulo arithmetic for wrapping around the alphabet
        return chr((ord(char) - start + shift) % 26 + start)
    
    # Handle uppercase letters
    if 'A' <= char <= 'Z':
        start = ord('A')
        # Standard modulo arithmetic for wrapping around the alphabet
        return chr((ord(char) - start + shift) % 26 + start)
        
    # Return non-alphabetic characters unchanged
    return char

def caesar_encrypt(text, shift):
    """Encrypts text by applying the character shift to every character."""
    # Use a generator expression for better performance and readability
    return ''.join(caesar_shift_char(char, shift) for char in text)

def caesar_decrypt(ciphertext, shift):
    """Decrypts ciphertext by applying the character shift in reverse."""
    # Decryption is performed by encrypting with a negative shift.
    # Python's % operator handles negative numbers correctly for this purpose.
    return caesar_encrypt(ciphertext, -shift)

# --- Helper Functions ---

def get_valid_key():
    """Prompts the user for a valid shift key (1-25) and ensures valid input."""
    while True:
        try:
            key_input = input("  Enter Key (Shift, 1-25): ")
            key = int(key_input)
            if 1 <= key <= 25:
                return key
            else:
                print("  Error: Key must be between 1 and 25.")
        except ValueError:
            print("  Error: Invalid input. Please enter an integer.")

# --- Menu Functions ---

def run_encryption_mode():
    """Handles the user interaction for encryption."""
    print("\n--- ENCRYPTION MODE ---")
    plaintext = input("  Enter Plaintext (message to hide): ")
    key = get_valid_key()
    
    ciphertext = caesar_encrypt(plaintext, key)
    
    print("\n--- RESULT ---")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Key (Shift): {key}")
    print(f"  Ciphertext: {ciphertext}\n")

def run_decryption_mode():
    """Handles the user interaction for decryption."""
    print("\n--- DECRYPTION MODE ---")
    ciphertext = input("  Enter Ciphertext (message to reveal): ")
    key = get_valid_key()
    
    decrypted_text = caesar_decrypt(ciphertext, key)
    
    print("\n--- RESULT ---")
    print(f"  Ciphertext: {ciphertext}")
    print(f"  Key (Shift): {key}")
    print(f"  Decrypted:  {decrypted_text}\n")

def run_brute_force_mode():
    """
    Attempts decryption using every possible key (shift 1-25).
    Demonstrates the fundamental weakness of the Caesar Cipher.
    """
    print("\n--- BRUTE FORCE ATTACK MODE ---")
    print("This mode demonstrates the weakness of the Caesar Cipher by trying all 25 possible keys.")
    ciphertext = input("  Enter Ciphertext to Crack: ")
    
    print("\n--- POSSIBLE DECRYPTIONS (Keys 1-25) ---")
    
    # Iterate through all 25 possible keys (shifts)
    for key in range(1, 26):
        # Decrypt using the current key
        decrypted_text = caesar_decrypt(ciphertext, key)
        
        # Display the result for each key, formatted neatly
        print(f"  Key {key:2}: {decrypted_text}") 

    print("\n  **The correct decryption is one of the messages above.**")
    print("  With only 25 keys, a computer can try every option instantly, rendering the cipher useless for security.\n")

# --- Main Program Loop ---

def main_menu():
    """The main entry point for the application, displaying the menu loop."""
    while True:
        print("=" * 46)
        print("  CAESAR CIPHER TOOL")
        print("=" * 46)
        print("  1. Encrypt Message")
        print("  2. Decrypt Message (Requires Key)")
        print("  3. Brute Force Attack (Break the Cipher)")
        print("  4. Exit")
        print("-" * 46)
        
        choice = input("  Select an option (1-4): ")
        
        if choice == '1':
            run_encryption_mode()
        elif choice == '2':
            run_decryption_mode()
        elif choice == '3':
            run_brute_force_mode()
        elif choice == '4':
            print("\nExiting the program. Goodbye!")
            sys.exit(0)
        else:
            print("\n  Invalid choice. Please select an option between 1 and 4.")
            
        print("=" * 46)

# Standard Python idiom to run the main function
if __name__ == '__main__':
    main_menu()