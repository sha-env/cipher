import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import string
import sys
import math # Needed for GCD check

# --- 📚 AFFINE CIPHER LOGIC AND CONSTANTS ---

ALPHABET_SIZE = 26

# Multiplicative inverses of 'a' modulo 26.
# a^-1 only exists if gcd(a, 26) == 1.
MOD_INVERSE = {
    1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25
}
VALID_A_KEYS = list(MOD_INVERSE.keys())

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
        
        # Key 'a' must be valid (checked in handler, but lookup here)
        a_inv = MOD_INVERSE.get(a)
        
        # Calculate P = a_inv * (C - b) mod 26
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

# --- 🖥️ TKINTER GUI APPLICATION (DARK MODE) ---

class AffineCipherApp(tk.Tk):
    
    # Dark Mode Color Constants
    BG_DARK = '#2e2e2e'
    FG_LIGHT = '#ffffff'
    ACCENT_COLOR = '#ff4500' # Orange-Red accent for Affine
    TEXT_AREA_BG = '#3a3a3a'
    TEXT_AREA_FG = '#e0e0e0'
    BUTTON_BG = '#4f4f4f'
    
    def __init__(self):
        super().__init__()
        self.title("Affine Cipher Tool - Encrypt and Decrypt")
        self.geometry("750x550")
        
        # Setup visual styling
        self._setup_style()
        
        # Main container for the single tab
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Initialize tab (Only one tab for Affine)
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

        # 1. Key Input (a and b)
        key_frame = ttk.Frame(tab)
        key_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        
        # Key 'a'
        ttk.Label(key_frame, text="Key 'a' (Multiplier):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.key_a_entry = ttk.Entry(key_frame, width=10)
        self.key_a_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w") 
        self.key_a_entry.insert(0, "5") # Default valid key 'a'
        
        # Key 'b'
        ttk.Label(key_frame, text="Key 'b' (Additive Shift):").grid(row=0, column=2, padx=15, pady=5, sticky="w")
        self.key_b_entry = ttk.Entry(key_frame, width=10)
        self.key_b_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w") 
        self.key_b_entry.insert(0, "8") # Default key 'b'
        
        # Key validation note
        ttk.Label(key_frame, text=f"*Key 'a' must be coprime with 26 (gcd(a, 26)=1). Valid values: {', '.join(map(str, VALID_A_KEYS))}", 
                  font=('Inter', 9, 'italic')).grid(row=1, column=0, columnspan=4, padx=5, sticky="w")


        # 2. Input Text Area
        ttk.Label(tab, text="Input Text (Plaintext/Ciphertext):").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
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

    def _get_keys(self):
        """Retrieves and validates the 'a' and 'b' keys."""
        try:
            a = int(self.key_a_entry.get())
            b = int(self.key_b_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Keys 'a' and 'b' must be integers.")
            return None, None
            
        if not (1 <= a <= 25 and 0 <= b <= 25):
            messagebox.showerror("Input Error", "Key 'a' must be 1-25. Key 'b' must be 0-25.")
            return None, None
            
        if a not in MOD_INVERSE:
            messagebox.showerror("Key Error", f"Key 'a' ({a}) is invalid. It must be coprime with 26 (gcd(a, 26)=1).")
            return None, None
            
        return a, b

    def _update_output(self, widget, text, is_error=False):
        """Helper function to update a ScrolledText widget."""
        widget.config(state='normal')
        widget.delete('1.0', tk.END)
        widget.insert(tk.END, text)
        widget.config(state='disabled')
        widget.yview_moveto(0)
        
        # Update status label
        error_text = text if is_error else ""
        self.status_label.config(text=error_text, foreground=('#ff4444' if is_error else self.BG_DARK))

    def _handle_process(self, mode):
        """Handler for Encrypt/Decrypt buttons."""
        a, b = self._get_keys()
        if a is None:
            return # Validation failed
            
        text = self.input_text_area.get('1.0', tk.END).strip()
        
        if not text:
            self._update_output(self.output_text_area, f"Please enter text to {mode}.", is_error=True)
            return

        try:
            # Process the text using Affine logic
            result_text = affine_process_text(text, a, b, mode)

            # Display Result
            self._update_output(self.output_text_area, result_text, is_error=False)

        except ValueError as e:
            self._update_output(self.output_text_area, str(e), is_error=True)
        except Exception as e:
            self._update_output(self.output_text_area, f"An unexpected error occurred: {e}", is_error=True)


if __name__ == "__main__":
    # Initialize and run the GUI application
    try:
        app = AffineCipherApp()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred while running the application: {e}", file=sys.stderr)