import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import string
import sys
# Import numpy for matrix operations
try:
    import numpy as np
except ImportError:
    messagebox.showerror("Dependency Error", "The Hill Cipher requires the **NumPy** library.\n\nPlease install it using: **pip install numpy**")
    sys.exit(1)

# --- 📚 HILL CIPHER LOGIC AND CONSTANTS ---

# Alphabet Constants
ALPH_LO = string.ascii_lowercase
ALPH_LEN = 26

# Modular inverse array for mod 26
# inv[a] is the multiplicative inverse of 'a' modulo 26, such that (a * inv[a]) % 26 == 1
# Only exists for a in {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25}
MOD_INVERSE = {
    1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25
}

def get_char_index(char):
    """Converts a letter to its 0-25 index."""
    if 'a' <= char.lower() <= 'z':
        return ord(char.lower()) - ord('a')
    return None # Non-alphabetic

def get_index_char(index):
    """Converts a 0-25 index back to a lowercase letter."""
    return chr(index + ord('a'))

def matrix_mod_inverse(matrix):
    """
    Calculates the modular multiplicative inverse of a matrix (mod 26).
    This function only supports 2x2 and 3x3 matrices for simplicity.
    """
    det = int(np.round(np.linalg.det(matrix))) % ALPH_LEN

    # Check if the determinant has a modular inverse
    if det not in MOD_INVERSE:
        return None, det # Inverse does not exist

    det_inv = MOD_INVERSE[det]

    # Calculate the adjoint matrix
    if matrix.shape == (2, 2):
        # [ a b ]^-1 = det_inv * [ d -b ] (mod 26)
        # [ c d ]              [ -c a ]
        adj = np.array([
            [matrix[1, 1], -matrix[0, 1]],
            [-matrix[1, 0], matrix[0, 0]]
        ]) % ALPH_LEN
    elif matrix.shape == (3, 3):
        # Using built-in linalg.inv and a lot of modular arithmetic
        inv = np.linalg.inv(matrix)
        adj = (inv * np.linalg.det(matrix)).round().astype(int) % ALPH_LEN
    else:
        return None, det

    # Inverse matrix = det_inv * adj (mod 26)
    inv_matrix = (det_inv * adj) % ALPH_LEN
    return inv_matrix, det

def prepare_key_matrix(key_text):
    """Converts a key string into a square matrix (2x2 or 3x3)."""
    key_text = ''.join(c.lower() for c in key_text if c.isalpha())
    L = len(key_text)
    
    # Supported matrix sizes (2x2 or 3x3)
    if L == 4:
        N = 2
    elif L == 9:
        N = 3
    else:
        return None, None
    
    # Convert characters to indices and reshape into an NxN matrix
    key_indices = [get_char_index(c) for c in key_text]
    key_matrix = np.array(key_indices).reshape(N, N)
    
    return key_matrix, N

def hill_process_text(text, key_matrix, N, mode='encrypt'):
    """
    Encrypts or decrypts text using the Hill Cipher.
    """
    key_matrix_inv = None
    if mode == 'decrypt':
        # Calculate the inverse key matrix for decryption
        key_matrix_inv, det = matrix_mod_inverse(key_matrix)
        if key_matrix_inv is None:
            raise ValueError(f"Key matrix is not invertible (Determinant: {det}). Choose a different key.")
        matrix = key_matrix_inv
    else:
        matrix = key_matrix

    # Clean text: lowercase and padding
    clean_text = ''.join(c.lower() for c in text if c.isalpha())
    
    # Pad the plaintext with 'x' if its length is not a multiple of N
    padding_len = (N - (len(clean_text) % N)) % N
    clean_text += 'x' * padding_len

    output_text = []
    
    # Process text in blocks of size N
    for i in range(0, len(clean_text), N):
        block = clean_text[i:i+N]
        # Convert block to a column vector of indices
        vector = np.array([get_char_index(c) for c in block])
        
        # Matrix multiplication: C = K * P (mod 26) or P = K_inv * C (mod 26)
        result_vector = (matrix @ vector) % ALPH_LEN
        
        # Convert result vector back to characters
        output_text.extend([get_index_char(j) for j in result_vector])

    return ''.join(output_text)

# --- 🖥️ TKINTER GUI APPLICATION (DARK MODE) ---

class HillCipherApp(tk.Tk):
    
    # Dark Mode Color Constants
    BG_DARK = '#2e2e2e'
    FG_LIGHT = '#ffffff'
    ACCENT_COLOR = '#ff9900' # Changed accent color for Hill Cipher
    TEXT_AREA_BG = '#3a3a3a'
    TEXT_AREA_FG = '#e0e0e0'
    BUTTON_BG = '#4f4f4f'
    
    def __init__(self):
        super().__init__()
        self.title("Hill Cipher Tool - Encrypt and Decrypt")
        self.geometry("750x650")
        
        # Setup visual styling
        self._setup_style()
        
        # Main container for the single tab
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Initialize tab
        self._create_encrypt_decrypt_tab()

    def _setup_style(self):
        """Configures the global style for Dark Mode."""
        self.config(bg=self.BG_DARK)
        
        self.style = ttk.Style(self)
        self.style.theme_use('clam') 
        
        # General configurations
        self.style.configure('.', background=self.BG_DARK, foreground=self.FG_LIGHT, font=('Inter', 10))
        self.style.configure('TFrame', background=self.BG_DARK)
        self.style.configure('TLabel', background=self.BG_DARK, foreground=self.FG_LIGHT)
        
        # Entry/Input field styling
        self.style.configure('TEntry', fieldbackground=self.TEXT_AREA_BG, foreground=self.TEXT_AREA_FG, borderwidth=0)
        
        # Notebook (Tab) styling
        self.style.configure('TNotebook', background=self.BG_DARK, borderwidth=0)
        self.style.configure('TNotebook.Tab', 
                             padding=[10, 5], 
                             font=('Inter', 10, 'bold'),
                             background=self.BUTTON_BG,
                             foreground=self.FG_LIGHT,
                             lightcolor=self.BUTTON_BG,
                             bordercolor=self.BG_DARK)
        self.style.map('TNotebook.Tab', 
                       background=[('selected', self.ACCENT_COLOR)],
                       foreground=[('selected', self.BG_DARK)])
        
        # Button styling
        self.style.configure('TButton', 
                             background=self.ACCENT_COLOR, 
                             foreground=self.BG_DARK, 
                             font=('Inter', 10, 'bold'),
                             borderwidth=0,
                             padding=[10, 6])
        self.style.map('TButton', 
                       background=[('active', self.ACCENT_COLOR), ('pressed', self.ACCENT_COLOR)],
                       foreground=[('active', self.BG_DARK), ('pressed', self.BG_DARK)])

    def _create_encrypt_decrypt_tab(self):
        """Creates the Encryption/Decryption tab."""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="Encrypt / Decrypt")

        # Configure responsive layout
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=3) 
        tab.grid_rowconfigure(2, weight=1)
        tab.grid_rowconfigure(4, weight=1)

        # 1. Key Input
        key_frame = ttk.Frame(tab)
        key_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        key_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(key_frame, text="Key (String):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.key_entry = ttk.Entry(key_frame, width=30)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w") 
        self.key_entry.insert(0, "GYBNQKURP") # Default 3x3 key
        
        ttk.Label(key_frame, text="*Key must be 4 characters (2x2 matrix) or 9 characters (3x3 matrix).", 
                  font=('Inter', 9, 'italic')).grid(row=1, column=0, columnspan=2, padx=5, sticky="w")
        
        # 2. Input Text Area
        ttk.Label(tab, text="Input Text (Plaintext/Ciphertext):").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.input_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('Inter', 10), 
                                                         bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.input_text_area.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        # 3. Action Buttons
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="ENCRYPT >>", command=lambda: self._handle_process('encrypt')).pack(side=tk.LEFT, padx=20)
        ttk.Button(button_frame, text="<< DECRYPT", command=lambda: self._handle_process('decrypt')).pack(side=tk.LEFT, padx=20)

        # 4. Output Text Area
        ttk.Label(tab, text="Output Result:").grid(row=4, column=0, padx=5, pady=5, sticky="nw")
        self.output_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('Inter', 10), state='disabled',
                                                          bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.output_text_area.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

        # 5. Status/Error Message
        self.status_label = ttk.Label(tab, text="", foreground='red', font=('Inter', 10, 'bold'))
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

    # --- 🛠️ HANDLER METHODS ---
    
    def _update_output(self, widget, text, font=('Inter', 10), is_error=False):
        """Helper function to update a ScrolledText widget."""
        widget.config(state='normal', font=font)
        widget.delete('1.0', tk.END)
        widget.insert(tk.END, text)
        widget.config(state='disabled')
        widget.yview_moveto(0)
        
        # Update status label
        self.status_label.config(text=("" if not is_error else f"ERROR: {text.splitlines()[0]}"))
        self.status_label.config(foreground=('#ff4444' if is_error else self.BG_DARK)) # Hide when not error


    def _handle_process(self, mode):
        """Handler for Encrypt/Decrypt buttons."""
        key_text = self.key_entry.get().strip()
        text = self.input_text_area.get('1.0', tk.END).strip()
        self.status_label.config(text="") # Clear previous status

        if not text:
            self._update_output(self.output_text_area, f"Please enter text to {mode}.", is_error=True)
            return

        try:
            # 1. Prepare Key Matrix
            key_matrix, N = prepare_key_matrix(key_text)
            if key_matrix is None:
                raise ValueError("Key must be 4 (2x2) or 9 (3x3) alphabetic characters.")

            # 2. Process Text
            result_text = hill_process_text(text, key_matrix, N, mode)

            # 3. Display Result
            self._update_output(self.output_text_area, result_text, is_error=False)

        except ValueError as e:
            self._update_output(self.output_text_area, str(e), is_error=True)
        except Exception as e:
            # Catch other potential errors, e.g., NumPy issues
            self._update_output(self.output_text_area, f"An unexpected error occurred: {e}", is_error=True)


if __name__ == "__main__":
    # Initialize and run the GUI application
    try:
        app = HillCipherApp()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred while running the application: {e}", file=sys.stderr)