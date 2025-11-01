import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import string
import sys

# --- 📚 VIGENÈRE CIPHER LOGIC AND CONSTANTS ---

ALPHABET_SIZE = 26

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

def vigenere_shift_char(char, key_char, mode='encrypt'):
    """Shifts a single alphabetic character based on the Vigenère rule."""
    
    char_index = get_char_index(char)
    if char_index is None:
        return char # Return non-alphabetic characters unchanged

    # Determine the shift value from the key character (0-25)
    key_shift = get_char_index(key_char.upper())
    
    # Set the direction of the shift
    shift = key_shift if mode == 'encrypt' else -key_shift

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
    
    keyword = ''.join(c.upper() for c in keyword if c.isalpha())
    keyword_len = len(keyword)
    
    if not keyword_len:
        raise ValueError("Keyword must contain at least one alphabetic character.")
    
    processed_text = []
    keyword_index = 0 # Tracks position within the keyword
    
    for char in text:
        if char.isalpha():
            # Get the current key character (repeating the keyword)
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

# --- 🖥️ TKINTER GUI APPLICATION (DARK MODE) ---

class VigenereCipherApp(tk.Tk):
    
    # Dark Mode Color Constants
    BG_DARK = '#2e2e2e'
    FG_LIGHT = '#ffffff'
    ACCENT_COLOR = '#ff8c00' # Orange accent color for Vigenère
    TEXT_AREA_BG = '#3a3a3a'
    TEXT_AREA_FG = '#e0e0e0'
    BUTTON_BG = '#4f4f4f'
    
    def __init__(self):
        super().__init__()
        self.title("Vigenère Cipher Tool - Encrypt and Decrypt")
        self.geometry("750x550")
        
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
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_rowconfigure(3, weight=1)

        # 1. Keyword Input
        key_frame = ttk.Frame(tab)
        key_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        key_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(key_frame, text="Keyword (Alphabetic):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.keyword_entry = ttk.Entry(key_frame, width=30)
        self.keyword_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w") 
        self.keyword_entry.insert(0, "SECRET") # Default Vigenère key
        
        ttk.Label(key_frame, text="*Only alphabetic characters are used for the keyword.", 
                  font=('Inter', 9, 'italic')).grid(row=1, column=0, columnspan=2, padx=5, sticky="w")


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
        self.output_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('Inter', 10), state='disabled',
                                                          bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.output_text_area.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        # 5. Status/Error Message
        self.status_label = ttk.Label(tab, text="", foreground='red', font=('Inter', 10, 'bold'))
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")


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
        keyword = self.keyword_entry.get().strip()
        text = self.input_text_area.get('1.0', tk.END).strip()
        
        # Basic validation
        if not text:
            self._update_output(self.output_text_area, f"Please enter text to {mode}.", is_error=True)
            return

        clean_keyword = ''.join(c for c in keyword if c.isalpha())
        if not clean_keyword:
            self._update_output(self.output_text_area, "Keyword error: Please enter an alphabetic keyword.", is_error=True)
            return

        try:
            # Process the text using Vigenère logic
            result_text = vigenere_process_text(text, clean_keyword, mode)

            # Display Result
            self._update_output(self.output_text_area, result_text, is_error=False)

        except ValueError as e:
            self._update_output(self.output_text_area, str(e), is_error=True)
        except Exception as e:
            self._update_output(self.output_text_area, f"An unexpected error occurred: {e}", is_error=True)


if __name__ == "__main__":
    # Initialize and run the GUI application
    try:
        app = VigenereCipherApp()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred while running the application: {e}", file=sys.stderr)