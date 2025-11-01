import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import string
import sys

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
    
    Transposition (0123 <-> 2301):
    C0 = P2, C1 = P3, C2 = P0, C3 = P1
    """
    if len(block) != BLOCK_SIZE:
        # This shouldn't happen if padding is correct
        raise ValueError(f"Block size error: expected {BLOCK_SIZE}, got {len(block)}.")

    # The transposition and its inverse are the same for this simple 2301 scheme
    return block[2] + block[3] + block[0] + block[1]

# --- Core Cipher Logic ---

def stbc_process_text(text, mode='encrypt'):
    """
    Encrypts or decrypts text using the STBC by processing it in blocks of 4.
    """
    
    if mode == 'encrypt':
        # 1. Normalize (remove non-letters, uppercase)
        normalized_text = ''.join(c.upper() for c in text if c.isalpha())
        # 2. Pad
        processed_text = pad_text(normalized_text)
    else: # Decrypt
        # 1. Validation for decryption
        if len(text) % BLOCK_SIZE != 0:
            raise ValueError(f"Ciphertext length ({len(text)}) must be a multiple of the block size ({BLOCK_SIZE}).")
        processed_text = text
        
    result_blocks = []
    
    # 2. Process in Blocks
    for i in range(0, len(processed_text), BLOCK_SIZE):
        block = processed_text[i:i + BLOCK_SIZE]
        result_blocks.append(process_block(block, mode))
        
    result = ''.join(result_blocks)
    
    if mode == 'decrypt':
        # 3. Remove Padding
        return result.rstrip(PADDING_CHAR)
        
    return result

# --- 🖥️ TKINTER GUI APPLICATION (DARK MODE) ---

class BlockCipherApp(tk.Tk):
    
    # Dark Mode Color Constants
    BG_DARK = '#2e2e2e'
    FG_LIGHT = '#ffffff'
    ACCENT_COLOR = '#8a2be2' # Blue-Violet accent for Block Cipher
    TEXT_AREA_BG = '#3a3a3a'
    TEXT_AREA_FG = '#e0e0e0'
    BUTTON_BG = '#4f4f4f'
    
    def __init__(self):
        super().__init__()
        self.title("Simple Block Cipher Tool - Encrypt and Decrypt")
        self.geometry("750x550")
        
        # Setup visual styling
        self._setup_style()
        
        # Main container for the single tab
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Initialize tabs
        self._create_encrypt_decrypt_tab()
        self._create_note_tab()

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
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_rowconfigure(3, weight=1)

        # 1. Cipher Info
        ttk.Label(tab, text=f"**Cipher Type:** Simple Transposition Block Cipher (STBC)", 
                  font=('Inter', 10, 'bold'), foreground=self.ACCENT_COLOR).grid(row=0, column=0, columnspan=2, padx=5, pady=(0, 5), sticky="w")
        ttk.Label(tab, text=f"**Fixed Block Size:** {BLOCK_SIZE} characters | **Padding Char:** '{PADDING_CHAR}'", 
                  font=('Inter', 9, 'italic')).grid(row=0, column=0, columnspan=2, padx=5, pady=(25, 10), sticky="w")

        # 2. Input Text Area
        ttk.Label(tab, text="Input Text (Plaintext/Ciphertext):").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.input_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('Inter', 10), 
                                                         bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.input_text_area.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # 3. Action Buttons
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="ENCRYPT >>", command=lambda: self._handle_process('encrypt')).pack(side=tk.LEFT, padx=20)
        ttk.Button(button_frame, text="<< DECRYPT", command=lambda: self._handle_process('decrypt')).pack(side=tk.LEFT, padx=20)

        # 4. Output Text Area
        ttk.Label(tab, text="Output Result:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.output_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('monospace', 9), state='disabled',
                                                          bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.output_text_area.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        # 5. Status/Error Message
        self.status_label = ttk.Label(tab, text="", foreground='red', font=('Inter', 10, 'bold'))
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

    def _create_note_tab(self):
        """Creates a tab explaining modern block cipher principles."""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="Block Cipher Principles")
        
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1) 

        title_label = ttk.Label(tab, text="Modern Block Cipher Concepts (e.g., AES) 🛡️", 
                                font=('Inter', 12, 'bold'), foreground=self.ACCENT_COLOR)
        title_label.grid(row=0, column=0, pady=10, sticky="w")

        info_text = (
            "This GUI uses a **Simple Transposition Block Cipher (STBC)** to demonstrate the concept of "
            "processing data in fixed-size blocks.\n\n"
            "**Modern Block Ciphers (like AES)** are far more complex and secure. They operate on "
            "fixed blocks of **bits** (e.g., 128 bits) and achieve security through many **rounds** involving:\n"
            "\n**1. Substitution (Confusion):** Using S-boxes to obscure the relationship between the key and the ciphertext."
            "\n**2. Permutation (Diffusion):** Spreading the influence of single plaintext bits over multiple ciphertext bits (Avalanche Effect)."
            "\n\nThey do **not** use simple alphabetic substitution or fixed transpositions as implemented here. "
            "Cracking modern block ciphers is infeasible without the correct key, unlike simple historical ciphers."
        )

        note_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=15, font=('Inter', 10), state='disabled',
                                              bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG)
        note_area.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        note_area.config(state='normal')
        note_area.insert(tk.END, info_text)
        note_area.config(state='disabled')


    # --- 🛠️ HANDLER METHODS ---

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
        text = self.input_text_area.get('1.0', tk.END).strip()
        
        if not text:
            self._update_output(self.output_text_area, f"Please enter text to {mode}.", is_error=True)
            return

        try:
            # Process the text using STBC logic
            result_text = stbc_process_text(text, mode)

            # Display Result
            if mode == 'encrypt':
                # Show the padded input for context
                normalized_text = ''.join(c.upper() for c in text if c.isalpha())
                padded_input = pad_text(normalized_text)
                
                output = (
                    f"Padded Input (Block Size {BLOCK_SIZE}): {padded_input}\n"
                    "----------------------------------------------------\n"
                    f"CIPHERTEXT: {result_text}"
                )
            else:
                output = (
                    f"Input Length: {len(text)}\n"
                    f"Padding Removed: {PADDING_CHAR} characters removed from the end.\n"
                    "----------------------------------------------------\n"
                    f"DECRYPTED TEXT: {result_text}"
                )
            
            self._update_output(self.output_text_area, output, is_error=False)

        except ValueError as e:
            self._update_output(self.output_text_area, str(e), is_error=True)
        except Exception as e:
            self._update_output(self.output_text_area, f"An unexpected error occurred: {e}", is_error=True)


if __name__ == "__main__":
    # Initialize and run the GUI application
    try:
        app = BlockCipherApp()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred while running the application: {e}", file=sys.stderr)