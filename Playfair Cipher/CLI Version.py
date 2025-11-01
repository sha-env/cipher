import sys
import string
from collections import OrderedDict # Used to remove duplicate characters from the key

# --- 📚 PLAYFAIR CIPHER LOGIC AND CONSTANTS ---

# Constants
ALPHABET_SIZE = 25 # We use 25 letters (I/J are combined)
ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZ' # Alphabet excluding J (or I)
J_REPLACEMENT = 'I' # Standard practice is to replace J with I

# --- Core Setup Logic ---

def create_playfair_key_table(key):
    """
    Creates the 5x5 key square (matrix) from the given keyword.
    1. Removes duplicates from the key.
    2. Appends remaining alphabet letters (excluding 'J').
    """
    
    # 1. Prepare key: Convert to uppercase, replace J with I, remove non-alpha
    key = key.upper().replace('J', J_REPLACEMENT)
    key = ''.join(c for c in key if c in ALPHABET)
    
    # 2. Use OrderedDict (or similar logic) to remove duplicate letters while preserving order
    # The key square is filled with the key first, then remaining letters of the alphabet
    key_chars = list(OrderedDict.fromkeys(key + ALPHABET))
    
    # Reshape the list of 25 characters into a 5x5 grid (list of lists)
    key_table = [key_chars[i:i + 5] for i in range(0, 25, 5)]
    
    return key_table

def get_char_coords(char, key_table):
    """
    Finds the (row, col) coordinates of a character in the 5x5 table.
    """
    # Replace 'J' with 'I' if not already done
    char = char.upper().replace('J', J_REPLACEMENT)
    
    for r in range(5):
        for c in range(5):
            if key_table[r][c] == char:
                return r, c
    return None, None # Should not happen for valid input

# --- Core Transformation Logic ---

def prepare_plaintext(plaintext):
    """
    Cleans and prepares plaintext for Playfair:
    1. Removes non-alpha chars.
    2. Replaces J with I.
    3. Breaks into digrams (pairs).
    4. Inserts filler ('X') for double letters and odd length.
    """
    
    text = ''.join(c for c in plaintext.upper() if c.isalpha())
    text = text.replace('J', J_REPLACEMENT)
    
    processed_text = ""
    i = 0
    while i < len(text):
        c1 = text[i]
        
        if i + 1 == len(text):
            # Odd length: append filler
            processed_text += c1 + 'X'
            i += 1
        else:
            c2 = text[i+1]
            if c1 == c2:
                # Double letters: append filler, don't advance i
                processed_text += c1 + 'X'
                i += 1
            else:
                # Normal digram
                processed_text += c1 + c2
                i += 2
                
    return processed_text

def apply_playfair_rule(c1, c2, key_table, mode='encrypt'):
    """
    Applies the four Playfair rules to a digram (c1, c2).
    """
    r1, c1 = get_char_coords(c1, key_table)
    r2, c2 = get_char_coords(c2, key_table)
    
    shift = 1 if mode == 'encrypt' else -1
    
    if r1 is None or r2 is None:
        # Should be caught by preprocessing, but as a safeguard:
        return c1 + c2 
        
    # Rule 1: Same Row
    if r1 == r2:
        new_c1 = key_table[r1][(c1 + shift) % 5]
        new_c2 = key_table[r2][(c2 + shift) % 5]
    
    # Rule 2: Same Column
    elif c1 == c2:
        new_c1 = key_table[(r1 + shift) % 5][c1]
        new_c2 = key_table[(r2 + shift) % 5][c2]
        
    # Rule 3: Rectangle (Opposite corners)
    else:
        # Swap column coordinates
        new_c1 = key_table[r1][c2]
        new_c2 = key_table[r2][c1]
        
    return new_c1 + new_c2


def playfair_process_text(text, key_table, mode='encrypt'):
    """
    Encrypts or decrypts a prepared Playfair text.
    """
    processed_text = []
    
    # Process text in digrams (pairs of 2)
    for i in range(0, len(text), 2):
        c1, c2 = text[i], text[i+1]
        
        digram_result = apply_playfair_rule(c1, c2, key_table, mode)
        processed_text.append(digram_result)
        
    return "".join(processed_text)

# --- CLI Menu Functions ---

def get_valid_key():
    """Prompts the user for a Playfair key."""
    while True:
        key_input = input("  Enter Keyword (alphabetic): ")
        if not key_input or not key_input.isalpha():
            print("  Error: Key must be alphabetic and non-empty.")
            continue
        return key_input

def run_encryption_mode():
    """Handles user interaction for encryption."""
    print("\n--- ENCRYPTION MODE ---")
    plaintext = input("  Enter Plaintext: ")
    key = get_valid_key()
    
    try:
        # 1. Create Key Table
        key_table = create_playfair_key_table(key)
        
        # 2. Prepare Plaintext (Padding/Filling)
        prepared_text = prepare_plaintext(plaintext)
        
        # 3. Encrypt
        ciphertext = playfair_process_text(prepared_text, key_table, mode='encrypt')
        
        print("\n--- RESULT ---")
        print(f"  Keyword:     {key.upper()}")
        print(f"  Key Square:")
        for row in key_table:
            print(f"    {row}")
        print(f"  Prepared P:  {prepared_text}")
        print(f"  Ciphertext:  {ciphertext}\n")
    
    except Exception as e:
        print(f"\n  An error occurred: {e}\n")

def run_decryption_mode():
    """Handles user interaction for decryption."""
    print("\n--- DECRYPTION MODE ---")
    ciphertext = input("  Enter Ciphertext: ")
    key = get_valid_key()
    
    # Ciphertext must be an even length and contain only I/J-replaced alphabet
    clean_ciphertext = ''.join(c for c in ciphertext.upper() if c in ALPHABET or c == 'J')
    if len(clean_ciphertext) % 2 != 0:
        print("  Error: Ciphertext must have an even number of letters.")
        return
    
    try:
        # 1. Create Key Table
        key_table = create_playfair_key_table(key)
        
        # 2. Decrypt (uses shift=-1)
        decrypted_text_with_fillers = playfair_process_text(clean_ciphertext, key_table, mode='decrypt')
        
        # 3. Attempt to remove fillers (not perfect, but helpful)
        # Check the result. If the decrypted text has 'X' where the original padding/filler would be
        
        print("\n--- RESULT ---")
        print(f"  Keyword:     {key.upper()}")
        print(f"  Ciphertext:  {clean_ciphertext}")
        print(f"  Decrypted (with fillers): {decrypted_text_with_fillers}")
        print("  *Note: Fillers ('X') may remain. Original odd-length padding and double-letter fillers ('X') should be manually removed.*\n")
    
    except Exception as e:
        print(f"\n  An error occurred: {e}\n")


def run_attack_note():
    """Provides a note on Playfair cryptanalysis."""
    print("\n--- CRYPTANALYSIS NOTE ---")
    print("  The Playfair Cipher is a **digraphic cipher** (encrypts pairs) and is much harder to break")
    print("  than monoalphabetic ciphers like Caesar, as it hides single-letter frequencies.")
    print("\n  **VULNERABILITY**: It is still vulnerable to **frequency analysis** of **digrams**.")
    print("  Common English digrams (TH, HE, AN, ER, etc.) can be matched to common ciphertext digrams.")
    print("  However, this requires a significant amount of ciphertext (usually hundreds of letters) and often **Known-Plaintext** segments to fully recover the key square.")
    print("  Due to the complexity of digram analysis and grid reconstruction, a dedicated attack function is omitted here.")
    print("-" * 60)

# --- Main Program Loop ---

def main_menu():
    """The main entry point for the application, displaying the menu loop."""
    
    while True:
        print("=" * 60)
        print("  PLAYFAIR CIPHER TOOL (CLI) 🔠")
        print("=" * 60)
        print("  1. Encrypt Message")
        print("  2. Decrypt Message (Requires Key)")
        print("  3. Cryptanalysis Note")
        print("  4. Exit")
        print("-" * 60)
        
        choice = input("  Select an option (1-4): ")
        
        if choice == '1':
            run_encryption_mode()
        elif choice == '2':
            run_decryption_mode()
        elif choice == '3':
            run_attack_note()
        elif choice == '4':
            print("\nExiting the program. Goodbye! 👋")
            sys.exit(0)
        else:
            print("\n  Invalid choice. Please select an option between 1 and 4.")
            
        print("=" * 60)

if __name__ == '__main__':
    # Add a check for OrderedDict/Python version if necessary, but it's standard since Python 3.1
    main_menu()