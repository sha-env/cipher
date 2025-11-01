import sys
import string
import math

# --- 📚 STBC CIPHER LOGIC AND CONSTANTS ---

# Block size is fixed at 4 characters for this simple simulation.
BLOCK_SIZE = 4
PADDING_CHAR = 'X'

def pad_text(text):
    """Pads the plaintext to ensure its length is a multiple of BLOCK_SIZE."""
    text_len = len(text)
    if text_len % BLOCK_SIZE != 0:
        padding_needed = BLOCK_SIZE - (text_len % BLOCK_SIZE)
        return text + (PADDING_CHAR * padding_needed)
    return text

def process_block(block, mode='encrypt'):
    """
    Applies a simple fixed transposition to a 4-character block.
    
    Encryption Transposition (0123 -> 2301):
    C0 = P2, C1 = P3, C2 = P0, C3 = P1
    
    Decryption Transposition (2301 -> 0123):
    P0 = C2, P1 = C3, P2 = C0, P3 = C1
    """
    if len(block) != BLOCK_SIZE:
        raise ValueError(f"Block size must be {BLOCK_SIZE}.")

    if mode == 'encrypt':
        # P0 P1 P2 P3  =>  P2 P3 P0 P1
        return block[2] + block[3] + block[0] + block[1]
    
    elif mode == 'decrypt':
        # C0 C1 C2 C3  =>  C2 C3 C0 C1
        return block[2] + block[3] + block[0] + block[1]
        
    return block

# --- Core Cipher Logic ---

def stbc_encrypt(plaintext):
    """Encrypts text by processing it in blocks of 4 using transposition."""
    
    # 1. Normalize and Pad Text
    # We only process alphabetic characters to keep it simple, converting to uppercase.
    normalized_text = ''.join(c.upper() for c in plaintext if c.isalpha())
    padded_text = pad_text(normalized_text)
    
    ciphertext = []
    
    # 2. Process in Blocks
    for i in range(0, len(padded_text), BLOCK_SIZE):
        block = padded_text[i:i + BLOCK_SIZE]
        ciphertext.append(process_block(block, mode='encrypt'))
        
    return ''.join(ciphertext)

def stbc_decrypt(ciphertext):
    """Decrypts text by processing it in blocks of 4 using the inverse transposition."""
    
    # 1. Validation (Ciphertext length must be a multiple of BLOCK_SIZE)
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError(f"Ciphertext length ({len(ciphertext)}) must be a multiple of the block size ({BLOCK_SIZE}).")
        
    decrypted_text = []
    
    # 2. Process in Blocks
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i + BLOCK_SIZE]
        decrypted_text.append(process_block(block, mode='decrypt'))
        
    result = ''.join(decrypted_text)
    
    # 3. Remove Padding
    return result.rstrip(PADDING_CHAR)


# --- Helper Functions ---

def get_block_size_info():
    """Prints a note about the block structure."""
    print(f"\n  --- NOTE ---")
    print(f"  This is a simulated Block Cipher (STBC) using a fixed **Block Size of {BLOCK_SIZE}**.")
    print(f"  The text is normalized (uppercased, non-alphabetic removed) and padded with '{PADDING_CHAR}' before processing.")
    print(f"  No external key is used, as the 'key' is the fixed internal transposition layer.")
    print(f"  ------------")


# --- Menu Functions ---

def run_encryption_mode():
    """Handles the user interaction for encryption."""
    print("\n--- ENCRYPTION MODE ---")
    plaintext = input("  Enter Plaintext (message to hide): ")
    
    try:
        ciphertext = stbc_encrypt(plaintext)
        
        # Display padding and normalization info
        normalized_text = ''.join(c.upper() for c in plaintext if c.isalpha())
        
        print("\n--- RESULT ---")
        print(f"  Original Text:   {plaintext}")
        print(f"  Padded Input:    {pad_text(normalized_text)}")
        print(f"  Block Size:      {BLOCK_SIZE}")
        print(f"  Ciphertext:      {ciphertext}\n")
    except Exception as e:
        print(f"\n  Encryption Error: {e}\n")

def run_decryption_mode():
    """Handles the user interaction for decryption."""
    print("\n--- DECRYPTION MODE ---")
    ciphertext = input("  Enter Ciphertext (message to reveal): ")
    
    try:
        decrypted_text = stbc_decrypt(ciphertext)
        
        print("\n--- RESULT ---")
        print(f"  Ciphertext:      {ciphertext}")
        print(f"  Block Size:      {BLOCK_SIZE}")
        print(f"  Decrypted Text:  {decrypted_text}\n")
    except ValueError as e:
        print(f"\n  Decryption Error: {e}")
        print("  Tip: Ensure the ciphertext length is a multiple of 4 and contains only letters.\n")
    except Exception as e:
        print(f"\n  Decryption Error: {e}\n")


def run_attack_note():
    """Provides a note on Block Cipher principles."""
    print("\n--- BLOCK CIPHER PRINCIPLES ---")
    print("  **Block Ciphers** like AES are not broken by simple brute force or frequency analysis.")
    print("  They achieve security through the **Feistel Structure** or similar designs that apply many rounds of:")
    print("  1. **Substitution (Confusion)**: S-boxes replace patterns of input bits with complex output patterns.")
    print("  2. **Permutation (Diffusion)**: P-boxes shuffle the bit positions across the entire block.")
    print("  These combined layers ensure that a single bit change in the plaintext significantly alters the entire ciphertext (Avalanche Effect).\n")
    print("  This simple CLI simulation only demonstrates the 'block' and 'transposition' concepts, not the full complexity or security of modern block ciphers.")

# --- Main Program Loop ---

def main_menu():
    """The main entry point for the application, displaying the menu loop."""
    while True:
        print("=" * 60)
        print("  SIMPLE TRANSPOSE BLOCK CIPHER (STBC) TOOL 🧱")
        print("=" * 60)
        print("  1. Encrypt Message")
        print("  2. Decrypt Message")
        print("  3. Block Cipher Principles (Read Note)")
        print("  4. Exit")
        print("-" * 60)
        get_block_size_info()
        
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

# Standard Python idiom to run the main function
if __name__ == '__main__':
    main_menu()