import sys
import math

# --- Core Cipher Logic ---

def encrypt(plaintext, key_cols):
    """
    Encrypts text using the Scytale Cipher.
    The text is written horizontally (row by row) and read vertically (column by column).
    key_cols is the number of columns (the key/diameter of the scytale rod).
    """
    text_len = len(plaintext)
    
    # Calculate the number of rows needed (the 'height' of the grid)
    key_rows = math.ceil(text_len / key_cols)
    
    # Initialize the grid: (rows x columns)
    grid = [['' for _ in range(key_cols)] for _ in range(key_rows)]
    
    # Fill the grid row by row
    for i, char in enumerate(plaintext):
        row = i // key_cols
        col = i % key_cols
        grid[row][col] = char

    # Read the ciphertext column by column
    ciphertext = []
    for col in range(key_cols):
        for row in range(key_rows):
            char = grid[row][col]
            if char:  # Check if char is not an empty string
                ciphertext.append(char)
                
    return ''.join(ciphertext)

def decrypt(ciphertext, key_cols):
    """
    Decrypts text using the Scytale Cipher.
    The ciphertext is conceptually placed vertically, and the plaintext is read horizontally.
    key_cols is the number of columns used during encryption.
    """
    
    cipher_len = len(ciphertext)
    
    # 1. Determine the grid dimensions used during ENCRYPTION
    original_rows = math.ceil(cipher_len / key_cols)
    
    # 2. For DECRYPTION, the grid dimensions are swapped:
    #    Decryption Columns (Width) = Original Rows
    #    Decryption Rows (Height) = Original Columns (key_cols)
    decrypt_cols = original_rows
    decrypt_rows = key_cols
    
    # Initialize the grid: (decrypt_rows x decrypt_cols)
    grid = [['' for _ in range(decrypt_cols)] for _ in range(decrypt_rows)]

    # Fill the grid column by column
    for i, char in enumerate(ciphertext):
        row = i % decrypt_rows  # Vertical filling
        col = i // decrypt_rows
        grid[row][col] = char

    # Read the plaintext row by row
    plaintext = []
    for row in range(decrypt_rows):
        for col in range(decrypt_cols):
            char = grid[row][col]
            if char: # Check if char is not an empty string
                plaintext.append(char)
                
    return ''.join(plaintext)

# --- Helper Functions and I/O ---

def clean_input(text):
    """Removes spaces and converts to uppercase for traditional Scytale neatness."""
    return "".join(text.split()).upper()

def get_valid_key(prompt_text, min_val=2):
    """Prompts the user for a valid integer key."""
    while True:
        try:
            key = int(input(f"  {prompt_text} (Min {min_val}): "))
            if key >= min_val:
                return key
            else:
                print(f"  Error: Key must be an integer and at least {min_val}.")
        except ValueError:
            print("  Error: Invalid input. Please enter an integer.")

# --- Encryption Mode ---

def run_encryption_mode():
    """Handles the user interaction for encryption."""
    print("\n--- SCYTALE CIPHER ENCRYPTION MODE ---")
    plaintext = input("  Enter Plaintext (message to hide): ")
    
    processed_text = clean_input(plaintext)
    
    if not processed_text:
        print("  Message cannot be empty after space removal.")
        return

    print(f"  Cleaned Text Length: {len(processed_text)}")
    
    key = get_valid_key("Enter Key (Number of Columns/Wraps)")
    
    ciphertext = encrypt(processed_text, key)
    
    print("\n--- RESULT ---")
    print(f"  Plaintext (Clean): {processed_text}")
    print(f"  Key (Columns):   {key}")
    print(f"  Ciphertext:      {ciphertext}\n")

# --- Decryption Mode ---

def run_decryption_mode():
    """Handles the user interaction for decryption."""
    print("\n--- SCYTALE CIPHER DECRYPTION MODE ---")
    ciphertext = input("  Enter Ciphertext (message to reveal): ")
    
    processed_cipher = clean_input(ciphertext)

    if not processed_cipher:
        print("  Ciphertext cannot be empty.")
        return
        
    print(f"  Ciphertext Length: {len(processed_cipher)}")
    key = get_valid_key("Enter Key (Number of Columns used for Encryption)")
    
    if key > len(processed_cipher):
        print("  Warning: Key (Columns) is greater than Ciphertext length. The result might be odd.")

    decrypted_text = decrypt(processed_cipher, key)
    
    print("\n--- RESULT ---")
    print(f"  Ciphertext: {processed_cipher}")
    print(f"  Key (Columns): {key}")
    print(f"  Decrypted:  {decrypted_text}\n")

# --- Brute Force Mode ---

def run_brute_force_mode():
    """
    Attempts decryption using all possible column keys 
    (from 2 up to the ciphertext length - 1).
    """
    print("\n--- SCYTALE CIPHER BRUTE FORCE ATTACK MODE ---")
    print("  This mode tries all possible number of columns/wraps.")
    ciphertext = input("  Enter Ciphertext to Crack: ")
    
    processed_cipher = clean_input(ciphertext)

    cipher_len = len(processed_cipher)
    
    if cipher_len < 2:
        print("  Ciphertext is too short for brute force (minimum 2 characters).")
        return
        
    print(f"\n--- POSSIBLE DECRYPTIONS (Keys 2 through {cipher_len - 1}) ---")
    
    # Possible keys are from 2 up to the length of the text - 1.
    for key in range(2, cipher_len):
        decrypted_text = decrypt(processed_cipher, key)
        print(f"  Key {key:2}: {decrypted_text}") 

    print("\n  The correct plaintext is one of the messages above.")
    print(f"  (For a {cipher_len}-char message, only {cipher_len - 2} keys need to be tested.)\n")

# --- Main Program Loop ---

def main():
    """The main entry point for the application, displaying the menu loop."""
    while True:
        print("=" * 45)
        print("        SCYTALE CIPHER TOOL")
        print("=" * 45)
        print("  1. Encrypt Message")
        print("  2. Decrypt Message (Requires Column Key)")
        print("  3. Brute Force Attack (Crack the Cipher)")
        print("  4. Exit")
        print("-" * 45)
        
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
            
        print("=" * 45)

if __name__ == '__main__':
    main()