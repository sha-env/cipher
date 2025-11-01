import sys
import string # Used for convenience

# --- 📚 VIGENERE CIPHER LOGIC AND CONSTANTS ---

ALPHABET_SIZE = 26

def get_char_index(char):
    """Converts an alphabetic character (A-Z or a-z) to its 0-25 index."""
    char = char.upper()
    if 'A' <= char <= 'Z':
        return ord(char) - ord('A')
    return None # Return None for non-alphabetic characters

def get_index_char(index, is_upper):
    """Converts a 0-25 index back to a character, preserving original case."""
    start = ord('A') if is_upper else ord('a')
    return chr(index % ALPHABET_SIZE + start)

def vigenere_shift_char(char, key_char, mode='encrypt'):
    """Shifts a single alphabetic character based on the Vigenère rule."""
    
    # Check if the character is alphabetic
    char_index = get_char_index(char)
    if char_index is None:
        return char # Return non-alphabetic characters unchanged

    # Determine the shift value from the key character (0-25)
    key_shift = get_char_index(key_char)
    
    # Set the direction of the shift
    if mode == 'encrypt':
        shift = key_shift
    else: # Decrypt
        shift = -key_shift # Decrypt is simply encrypting with the negative shift

    # Apply the shift
    new_index = (char_index + shift) % ALPHABET_SIZE
    
    # Restore the original case
    is_upper = char.isupper()
    return get_index_char(new_index, is_upper)

# --- Core Cipher Logic ---

def vigenere_process_text(text, keyword, mode='encrypt'):
    """
    Encrypts or decrypts text using the Vigenère Cipher.
    The keyword is repeated to match the length of the plaintext.
    """
    
    keyword = keyword.upper()
    keyword_len = len(keyword)
    
    processed_text = []
    keyword_index = 0 # Tracks position within the keyword
    
    for char in text:
        if char.isalpha():
            # Get the current key character to use for shifting
            key_char = keyword[keyword_index % keyword_len]
            
            # Apply the Vigenère shift
            shifted_char = vigenere_shift_char(char, key_char, mode)
            processed_text.append(shifted_char)
            
            # Move to the next character in the keyword only for alphabetic characters
            keyword_index += 1
        else:
            # Append non-alphabetic characters unchanged
            processed_text.append(char)
            
    return ''.join(processed_text)

def vigenere_encrypt(plaintext, keyword):
    """Encrypts plaintext using the Vigenère Cipher."""
    return vigenere_process_text(plaintext, keyword, mode='encrypt')

def vigenere_decrypt(ciphertext, keyword):
    """Decrypts ciphertext using the Vigenère Cipher."""
    return vigenere_process_text(ciphertext, keyword, mode='decrypt')


# --- Helper Functions (Input Validation) ---

def get_valid_keyword():
    """Prompts the user for a valid alphabetic keyword."""
    while True:
        key_input = input("  Enter Keyword (Alphabetic, e.g., SECRET): ")
        key_input = key_input.strip()
        
        if key_input.isalpha() and key_input:
            return key_input
        else:
            print("  Error: Key must be alphabetic and non-empty.")

# --- Menu Functions ---

def run_encryption_mode():
    """Handles the user interaction for Vigenère encryption."""
    print("\n--- ENCRYPTION MODE ---")
    plaintext = input("  Enter Plaintext (message to hide): ")
    keyword = get_valid_keyword()
    
    ciphertext = vigenere_encrypt(plaintext, keyword)
    
    print("\n--- RESULT ---")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Keyword:    {keyword.upper()}")
    print(f"  Ciphertext: {ciphertext}\n")

def run_decryption_mode():
    """Handles the user interaction for Vigenère decryption."""
    print("\n--- DECRYPTION MODE ---")
    ciphertext = input("  Enter Ciphertext (message to reveal): ")
    keyword = get_valid_keyword()
    
    decrypted_text = vigenere_decrypt(ciphertext, keyword)
    
    print("\n--- RESULT ---")
    print(f"  Ciphertext: {ciphertext}")
    print(f"  Keyword:    {keyword.upper()}")
    print(f"  Decrypted:  {decrypted_text}\n")

def run_cryptanalysis_note():
    """Provides a note on Vigenère cryptanalysis (Kasiski/Frequency Analysis)."""
    print("\n--- CRYPTANALYSIS NOTE ---")
    print("  **Vulnerability**: The Vigenère Cipher is vulnerable to **Frequency Analysis** combined with methods like the **Kasiski Examination**.")
    print("\n  1. **Kasiski Test**: Finds repeated ciphertext groups to determine the length of the keyword.")
    print("  2. **Frequency Analysis**: Once the keyword length ($N$) is known, the ciphertext is broken into $N$ separate Caesar Ciphers. Each can then be easily solved using standard frequency analysis (e.g., finding the shift that makes 'E' the most frequent letter).")
    print("\n  This makes Vigenère much stronger than Caesar but still breakable with enough ciphertext.\n")

# --- Main Program Loop ---

def main_menu():
    """The main entry point for the application, displaying the menu loop."""
    while True:
        print("=" * 60)
        print("  VIGENÈRE CIPHER TOOL (The Polyalphabetic Substitution Cipher) 🔐")
        print("=" * 60)
        print("  1. Encrypt Message")
        print("  2. Decrypt Message (Requires Keyword)")
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