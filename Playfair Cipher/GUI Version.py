import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import string
import sys
from collections import OrderedDict # Essential for unique key characters

# --- 📚 PLAYFAIR CIPHER LOGIC AND CONSTANTS ---

ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZ' # 25-letter alphabet (J is omitted)
J_REPLACEMENT = 'I' # J is replaced by I in standard Playfair

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
    
    # 2. Use OrderedDict to remove duplicate letters while preserving order
    # Fill the 5x5 grid with the unique key characters, followed by the rest of the alphabet
    key_chars = list(OrderedDict.fromkeys(key + ALPHABET))
    
    # Reshape the list of 25 characters into a 5x5 grid (list of lists)
    key_table = [key_chars[i:i + 5] for i in range(0, 25, 5)]
    
    return key_table

def get_char_coords(char, key_table):
    """
    Finds the (row, col) coordinates of a character in the 5x5 table.
    Replaces 'J' with 'I' internally for lookup.
    """
    char = char.upper().replace('J', J_REPLACEMENT)
    
    for r in range(5):
        try:
            c = key_table[r].index(char)
            return r, c
        except ValueError:
            # Character not in this row (or is not 'I'/'J' and is out of alphabet)
            continue
    return None, None 

# --- Core Transformation Logic ---

def prepare_plaintext(plaintext):
    """
    Cleans and prepares plaintext for Playfair:
    1. Removes non-alpha chars, replaces J with I.
    2. Breaks into digrams (pairs).
    3. Inserts filler ('X') for double letters and odd length.
    """
    
    text = ''.join(c for c in plaintext.upper() if c.isalpha())
    text = text.replace('J', J_REPLACEMENT)
    
    processed_text = ""
    i = 0
    while i < len(text):
        c1 = text[i]
        
        if i + 1 == len(text):
            # Odd length: append filler 'X'
            processed_text += c1 + 'X'
            i += 1
        else:
            c2 = text[i+1]
            if c1 == c2:
                # Double letters: append filler 'X', don't advance i (so the second letter can be re-paired)
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
    r1, c1_idx = get_char_coords(c1, key_table)
    r2, c2_idx = get_char_coords(c2, key_table)
    
    if r1 is None or r2 is None:
        # Should not happen if key_table and input are valid
        raise ValueError(f"Character lookup failed for digram: {c1}{c2}")
        
    shift = 1 if mode == 'encrypt' else -1
    
    # Rule 1: Same Row
    if r1 == r2:
        new_c1 = key_table[r1][(c1_idx + shift) % 5]
        new_c2 = key_table[r2][(c2_idx + shift) % 5]
    
    # Rule 2: Same Column
    elif c1_idx == c2_idx:
        new_c1 = key_table[(r1 + shift) % 5][c1_idx]
        new_c2 = key_table[(r2 + shift) % 5][c2_idx]
        
    # Rule 3: Rectangle (Opposite corners)
    else:
        # Swap column coordinates
        new_c1 = key_table[r1][c2_idx]
        new_c2 = key_table[r2][c1_idx]
        
    return new_c1 + new_c2


def playfair_process_text(text, key_table, mode='encrypt'):
    """
    Encrypts or decrypts a prepared Playfair text in digrams.
    """
    output_text = []
    
    # Text must be processed in digrams (pairs of 2)
    for i in range(0, len(text), 2):
        c1, c2 = text[i], text[i+1]
        
        digram_result = apply_playfair_rule(c1, c2, key_table, mode)
        output_text.append(digram_result)
        
    return "".join(output_text)

# --- 🖥️ TKINTER GUI APPLICATION (DARK MODE) ---

class PlayfairCipherApp(tk.Tk):
    
    # Dark Mode Color Constants
    BG_DARK = '#2e2e2e'
    FG_LIGHT = '#ffffff'
    ACCENT_COLOR = '#4CAF50' # Green accent color for Playfair
    TEXT_AREA_BG = '#3a3a3a'
    TEXT_AREA_FG = '#e0e0e0'
    BUTTON_BG = '#4f4f4f'
    
    def __init__(self):
        super().__init__()
        self.title("Playfair Cipher Tool - Encrypt and Decrypt")
        self.geometry("750x700") # Slightly taller for key display
        
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
        tab.grid_rowconfigure(3, weight=1) # Input area
        tab.grid_rowconfigure(6, weight=1) # Output area

        # 1. Key Input
        key_frame = ttk.Frame(tab)
        key_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        key_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(key_frame, text="Keyword:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.key_entry = ttk.Entry(key_frame, width=30)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w") 
        self.key_entry.insert(0, "MONARCHY") # Default key
        
        ttk.Label(key_frame, text="*Note: J is treated as I. Only alphabetic characters are processed.", 
                  font=('Inter', 9, 'italic')).grid(row=1, column=0, columnspan=2, padx=5, sticky="w")

        # 2. Input Text Area
        ttk.Label(tab, text="Input Text (Plaintext/Ciphertext):").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.input_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('Inter', 10), 
                                                         bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.input_text_area.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        # 3. Action Buttons
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="ENCRYPT >>", command=lambda: self._handle_process('encrypt')).pack(side=tk.LEFT, padx=20)
        ttk.Button(button_frame, text="<< DECRYPT", command=lambda: self._handle_process('decrypt')).pack(side=tk.LEFT, padx=20)

        # 4. Output Text Area
        ttk.Label(tab, text="Output Result:").grid(row=5, column=0, padx=5, pady=5, sticky="nw")
        self.output_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('Inter', 10), state='disabled',
                                                          bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.output_text_area.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")

        # 5. Key Square Display
        self.key_square_label = ttk.Label(tab, text="Key Square will appear here.", foreground=self.FG_LIGHT, font=('Courier', 10))
        self.key_square_label.grid(row=7, column=0, columnspan=2, pady=10, sticky="w")

        # 6. Status/Error Message
        self.status_label = ttk.Label(tab, text="", foreground='red', font=('Inter', 10, 'bold'))
        self.status_label.grid(row=8, column=0, columnspan=2, pady=5, sticky="w")

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

    def _display_key_square(self, key_table):
        """Formats and displays the 5x5 key square."""
        display_text = "🔑 KEY SQUARE 5x5:\n"
        for row in key_table:
            display_text += f"    {' | '.join(row)}\n"
        self.key_square_label.config(text=display_text, foreground=self.FG_LIGHT)


    def _handle_process(self, mode):
        """Handler for Encrypt/Decrypt buttons."""
        key_text = self.key_entry.get().strip()
        text = self.input_text_area.get('1.0', tk.END).strip()
        self.status_label.config(text="") # Clear previous status

        if not text:
            self._update_output(self.output_text_area, f"Please enter text to {mode}.", is_error=True)
            return
        
        if not key_text or not key_text.isalpha():
            self._update_output(self.output_text_area, "Please enter a valid alphabetic key.", is_error=True)
            return

        try:
            # 1. Create Key Table
            key_table = create_playfair_key_table(key_text)
            self._display_key_square(key_table)

            if mode == 'encrypt':
                # 2. Prepare Plaintext (Padding/Filling)
                prepared_text = prepare_plaintext(text)
                
                # 3. Encrypt
                result_text = playfair_process_text(prepared_text, key_table, mode='encrypt')
                
                # Optionally show the prepared text alongside the result
                display_output = f"Prepared Text: {prepared_text}\n\nCiphertext: {result_text}"
            
            else: # Decrypt Mode
                # Clean ciphertext (must be even length for Playfair)
                clean_ciphertext = ''.join(c for c in text.upper() if c in ALPHABET or c == 'J')
                
                if len(clean_ciphertext) % 2 != 0:
                    raise ValueError("Ciphertext must have an even number of characters (digrams).")
                
                # 3. Decrypt
                decrypted_with_fillers = playfair_process_text(clean_ciphertext, key_table, mode='decrypt')
                
                display_output = f"Decrypted Text (may contain 'X' fillers):\n{decrypted_with_fillers}"


            # 4. Display Result
            self._update_output(self.output_text_area, display_output, is_error=False)

        except ValueError as e:
            self._update_output(self.output_text_area, str(e), is_error=True)
        except Exception as e:
            self._update_output(self.output_text_area, f"An unexpected error occurred: {e}", is_error=True)


if __name__ == "__main__":
    try:
        app = PlayfairCipherApp()
        app.mainloop()
    except Exception as e:
        # Catch Tkinter or other system-level errors gracefully
        print(f"An error occurred while running the application: {e}", file=sys.stderr)