import sys
import numpy as np # Essential for matrix operations in Hill Cipher

# --- Constants and Core Math Logic ---

ALPHABET_SIZE = 26
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def text_to_numbers(text):
    """Converts a string (A-Z) into a list of numbers (0-25)."""
    text = text.upper()
    # Filter out non-alphabetic characters
    return [ALPHABET.index(char) for char in text if char in ALPHABET]

def numbers_to_text(numbers):
    """Converts a list of numbers (0-25) into a string (A-Z)."""
    return ''.join(ALPHABET[num] for num in numbers)

def get_mod_inverse(a, m):
    """
    Computes the multiplicative inverse a^-1 mod m.
    Used to find the inverse of the key matrix determinant.
    """
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_mod_26(matrix):
    """Applies the modulo 26 operation to all matrix elements."""
    return matrix % ALPHABET_SIZE

def is_key_invertible(key_matrix):
    """Checks if the key matrix has a multiplicative inverse modulo 26."""
    det = int(np.round(np.linalg.det(key_matrix)))
    return np.gcd(det, ALPHABET_SIZE) == 1

def get_inverse_key_matrix(key_matrix):
    """Computes the inverse of the key matrix modulo 26 (K^-1 mod 26)."""
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = get_mod_inverse(det, ALPHABET_SIZE)
    
    if det_inv is None:
        raise ValueError("Key matrix is not invertible modulo 26. Check the key.")

    inv_matrix_float = np.linalg.inv(key_matrix)
    adj_matrix = np.round(inv_matrix_float * det).astype(int)
    inv_key_matrix = matrix_mod_26(adj_matrix * det_inv)
    
    return inv_key_matrix

# --- Core Cipher Logic ---

def hill_transform(numbers, key_matrix):
    """Performs the encryption/decryption transformation using the key matrix."""
    n = key_matrix.shape[0]
    
    # Padding: Add 'X' (value 23) if the message length is not divisible by n
    padding_needed = (n - (len(numbers) % n)) % n
    padded_numbers = numbers + [ALPHABET.index('X')] * padding_needed
    
    # Reshape numbers into vectors (blocks) of size n
    vectors = np.array(padded_numbers).reshape(-1, n)
    
    # Transformation: C = P * K mod 26
    transformed_vectors = matrix_mod_26(np.dot(vectors, key_matrix))
    
    return transformed_vectors.flatten().tolist()

def hill_encrypt(plaintext, key_matrix):
    """Encrypts plaintext using the Hill Cipher."""
    numbers = text_to_numbers(plaintext)
    cipher_numbers = hill_transform(numbers, key_matrix)
    return numbers_to_text(cipher_numbers)

def hill_decrypt(ciphertext, key_matrix):
    """Decrypts ciphertext using the Hill Cipher."""
    numbers = text_to_numbers(ciphertext)
    
    # Get the inverse of the key matrix (K^-1 mod 26)
    inv_key_matrix = get_inverse_key_matrix(key_matrix)
    
    decrypted_numbers = hill_transform(numbers, inv_key_matrix)
    
    return numbers_to_text(decrypted_numbers)

# --- Helper Functions (Key/Input Validation) ---

def get_valid_key_matrix():
    """Prompts the user for a key matrix and validates it."""
    while True:
        try:
            print("\n  Key Format: Enter numbers separated by spaces or commas.")
            key_input = input("  Enter Key Numbers: ")
            raw_numbers = key_input.replace(',', ' ').split()
            key_numbers = [int(num) for num in raw_numbers]
            
            n = int(np.sqrt(len(key_numbers)))
            
            if n * n != len(key_numbers) or n < 2:
                print(f"  Error: Number of elements ({len(key_numbers)}) must form a square matrix (e.g., 4, 9, 16, ...) with dimension >= 2x2.")
                continue
                
            key_matrix = np.array(key_numbers).reshape(n, n)
            
            if not is_key_invertible(key_matrix):
                det = int(np.round(np.linalg.det(key_matrix)))
                print(f"  Error: Key matrix is not invertible modulo 26 (det={det}, gcd(det, 26)={np.gcd(det, 26)}).")
                continue
                
            return key_matrix
            
        except ValueError:
            print("  Error: Invalid input. Please ensure all elements are integers.")
        except Exception as e:
            print(f"  An unexpected error occurred: {e}")

# --- Core Drawback / Attack Logic ---

def hill_crack_key_from_known_plaintext(P_text, C_text):
    """
    Attempts to recover the key matrix K using the Known-Plaintext Attack.
    Formula: K = C * P_inv (mod 26)
    P_inv is the inverse of the plaintext matrix P modulo 26.
    """
    
    P_numbers = text_to_numbers(P_text)
    C_numbers = text_to_numbers(C_text)
    n = int(np.sqrt(len(P_numbers)))
    
    if len(P_numbers) != len(C_numbers) or len(P_numbers) != n * n:
        raise ValueError(f"Input length error: Plaintext and Ciphertext must have the same length ({n*n}) for the given dimension ({n}).")
        
    # P and C must be represented as n x n matrices (blocks)
    P_matrix = np.array(P_numbers).reshape(n, n)
    C_matrix = np.array(C_numbers).reshape(n, n)
    
    if not is_key_invertible(P_matrix):
        det = int(np.round(np.linalg.det(P_matrix)))
        raise ValueError(f"Plaintext blocks are not linearly independent (det={det}) modulo 26. Cannot solve for the key.")

    # 1. Find the inverse of the Plaintext Matrix (P_inv) modulo 26
    P_inv = get_inverse_key_matrix(P_matrix)
    
    # 2. Calculate the Key Matrix K = C * P_inv (mod 26)
    # np.dot(C_matrix, P_inv) performs the matrix multiplication C * P_inv
    K_matrix = matrix_mod_26(np.dot(C_matrix, P_inv))
    
    return K_matrix

# --- Menu Functions ---

def run_encryption_mode():
    """Handles user interaction for encryption."""
    print("\n--- ENCRYPTION MODE ---")
    plaintext = input("  Enter Plaintext (A-Z only): ")
    
    try:
        key_matrix = get_valid_key_matrix()
        ciphertext = hill_encrypt(plaintext, key_matrix)
        
        print("\n--- RESULT ---")
        print(f"  Plaintext:  {plaintext.upper()}")
        print(f"  Key Matrix Dimension: {key_matrix.shape[0]}x{key_matrix.shape[1]}")
        print(f"  Key Matrix:\n{key_matrix}")
        print(f"  Ciphertext: {ciphertext}\n")
    except ValueError as e:
        print(f"\n  Error: {e}\n")

def run_decryption_mode():
    """Handles user interaction for decryption (the missing function)."""
    print("\n--- DECRYPTION MODE ---")
    ciphertext = input("  Enter Ciphertext (A-Z only): ")
    
    try:
        key_matrix = get_valid_key_matrix()
        
        decrypted_text = hill_decrypt(ciphertext, key_matrix)
        
        print("\n--- RESULT ---")
        print(f"  Ciphertext: {ciphertext.upper()}")
        print(f"  Key Dimension: {key_matrix.shape[0]}x{key_matrix.shape[1]}")
        print(f"  Key Matrix:\n{key_matrix}")
        print(f"  Decrypted:  {decrypted_text}\n")
    except ValueError as e:
        print(f"\n  Error: {e}\n")


def run_known_plaintext_attack():
    """Demonstrates the Hill Cipher's major weakness."""
    print("\n--- KNOWN-PLAINTEXT ATTACK MODE ---")
    
    print("\n  **DRAWBACK**: The Hill Cipher is a linear cipher, making it vulnerable to this attack.")
    print("  We need **N x N** known character pairs (Plaintext/Ciphertext) to find an **N x N** key.")
    
    while True:
        key_dim_input = input("  Enter assumed Key Dimension (N, e.g., 2 or 3): ")
        try:
            n = int(key_dim_input)
            if n < 2:
                print("  Dimension must be 2 or greater.")
                continue
            required_len = n * n
            break
        except ValueError:
            print("  Invalid input. Please enter an integer.")

    print(f"\n  REQUIRED LENGTH: {required_len} characters of known Plaintext/Ciphertext.")
    
    plaintext = input("  Enter Known Plaintext (P): ").upper()
    ciphertext = input("  Enter Corresponding Ciphertext (C): ").upper()
    
    plaintext = ''.join(c for c in plaintext if c in ALPHABET)
    ciphertext = ''.join(c for c in ciphertext if c in ALPHABET)
    
    if len(plaintext) < required_len or len(ciphertext) < required_len:
        print(f"\n  Error: Both P and C must contain at least {required_len} alphabetic characters.")
        return

    # Truncate to the exact required length
    P_block = plaintext[:required_len]
    C_block = ciphertext[:required_len]
    
    try:
        # The key recovery magic happens here
        cracked_key = hill_crack_key_from_known_plaintext(P_block, C_block)
        
        print("\n--- ATTACK RESULT ---")
        print(f"  Plaintext Block Used: {P_block}")
        print(f"  Ciphertext Block Used: {C_block}")
        print(f"  **SUCCESS! Cracked Key Matrix ({n}x{n}):**")
        print(cracked_key)
        
        # Verify the cracked key by decrypting the full ciphertext (optional)
        full_decrypted = hill_decrypt(ciphertext, cracked_key)
        
        print(f"\n  VERIFICATION (Full Ciphertext Decrypted):")
        print(f"  Decrypted: {full_decrypted}")
        
    except ValueError as e:
        print(f"\n  **ATTACK FAILED**: {e}")
        print("  This failure often means the chosen plaintext block was not 'full rank' (invertible) modulo 26.")
        
    except Exception as e:
        print(f"\n  An unexpected error occurred during cracking: {e}")
        
    print("\n  This vulnerability shows that knowing even a small amount of message (Known-Plaintext) is enough to break the entire cipher.\n")


# --- Main Program Loop ---

def main_menu():
    """The main entry point for the application, displaying the menu loop."""
    if 'numpy' not in sys.modules:
        try:
            global np
            import numpy as np
        except ImportError:
            print("Error: NumPy is required for Hill Cipher. Please install it: pip install numpy")
            sys.exit(1)
        
    while True:
        print("=" * 60)
        print("  HILL CIPHER TOOL & CRYPTANALYSIS DEMO")
        print("=" * 60)
        print("  1. Encrypt Message")
        print("  2. Decrypt Message (Requires Key)")
        print("  3. **DEMO: Known-Plaintext Attack (Hill Cipher Drawback)**")
        print("  4. Exit")
        print("-" * 60)
        
        choice = input("  Select an option (1-4): ")
        
        if choice == '1':
            run_encryption_mode()
        elif choice == '2':
            run_decryption_mode() # <-- This is the function that was missing!
        elif choice == '3':
            run_known_plaintext_attack()
        elif choice == '4':
            print("\nExiting the program. Goodbye!")
            sys.exit(0)
        else:
            print("\n  Invalid choice. Please select an option between 1 and 4.")
            
        print("=" * 60)

if __name__ == '__main__':
    main_menu()