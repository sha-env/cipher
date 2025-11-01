import tkinter as tk
from tkinter import ttk
import math
from typing import Optional, Tuple

# --- Core Cipher Logic ---

def scytale_encrypt(plaintext: str, key_cols: int) -> str:
    """
    Encrypts text using the Scytale Transposition Cipher.

    The plaintext is written across the scytale (a cylinder) and read off 
    down the length, column by column. The key is the number of columns.
    """
    # 1. Calculate grid dimensions
    text_len = len(plaintext)
    # Determine the number of rows needed
    key_rows = math.ceil(text_len / key_cols) 
    
    # 2. Create the grid (row-major order)
    grid = [['' for _ in range(key_cols)] for _ in range(key_rows)]
    
    # Fill the grid row by row
    for i, char in enumerate(plaintext):
        row = i // key_cols
        col = i % key_cols
        grid[row][col] = char

    # 3. Read the ciphertext column by column
    ciphertext = []
    for col in range(key_cols):
        for row in range(key_rows):
            char = grid[row][col]
            if char != '':
                ciphertext.append(char)
                
    return ''.join(ciphertext)

def scytale_decrypt(ciphertext: str, key_cols: int) -> str:
    """
    Decrypts text encrypted with the Scytale Transposition Cipher.

    To decrypt, the ciphertext is written column by column onto a new grid 
    based on the original key, and then read off row by row.
    """
    cipher_len = len(ciphertext)
    
    # Calculate the number of rows from the original encryption
    key_rows = math.ceil(cipher_len / key_cols) 
    
    # Decryption grid dimensions: 
    # Rows = Original Key (Columns); Columns = Original Rows
    decrypt_rows = key_cols
    decrypt_cols = key_rows
    
    # 1. Create the decryption grid
    grid = [['' for _ in range(decrypt_cols)] for _ in range(decrypt_rows)]

    # 2. Fill the grid column by column with the ciphertext
    for i, char in enumerate(ciphertext):
        row = i % decrypt_rows 
        col = i // decrypt_rows
        grid[row][col] = char

    # 3. Read the plaintext row by row
    plaintext = []
    for row in range(decrypt_rows):
        for col in range(decrypt_cols):
            char = grid[row][col]
            if char != '':
                plaintext.append(char)
                
    return ''.join(plaintext)

# --- GUI Application Class ---

class ScytaleCipherApp:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Scytale Transposition Cipher Tool")
        master.resizable(False, False)

        # --- Dark Style Configuration ---
        self.BACKGROUND_COLOR = '#1e1e1e'
        self.FOREGROUND_COLOR = '#f0f0f0'
        self.ENTRY_BG_COLOR = '#333333'
        self.BUTTON_BG_COLOR = '#4a4a4a'
        self.BUTTON_FG_COLOR = '#ffffff'

        master.configure(bg=self.BACKGROUND_COLOR)
        style = ttk.Style()
        style.theme_use('clam') # Use 'clam' for better customization on dark mode
        
        style.configure('TFrame', background=self.BACKGROUND_COLOR)
        style.configure('TLabel', background=self.BACKGROUND_COLOR, foreground=self.FOREGROUND_COLOR, 
                        font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('TButton', background=self.BUTTON_BG_COLOR, foreground=self.BUTTON_FG_COLOR, 
                        font=('Arial', 10, 'bold'), borderwidth=1, focuscolor=self.BUTTON_BG_COLOR)
        style.map('TButton', background=[('active', self.BACKGROUND_COLOR)])

        # --- Main Frame ---
        self.main_frame = ttk.Frame(master, padding="20 20 20 20")
        self.main_frame.pack(fill='both', expand=True)

        # --- Widget Layout ---
        
        # 0. Title
        self.title_label = ttk.Label(self.main_frame, text="SCYTALE TRANSPOSITION CIPHER", 
                                     style='Title.TLabel', anchor='center')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 1. Key Input
        ttk.Label(self.main_frame, text="Key (Number of Columns, Min 2):").grid(row=1, column=0, sticky='w', pady=5)
        self.key_entry = tk.Entry(self.main_frame, width=10, bg=self.ENTRY_BG_COLOR, fg=self.FOREGROUND_COLOR, insertbackground=self.FOREGROUND_COLOR, relief=tk.FLAT)
        self.key_entry.insert(0, '3') # Default key
        self.key_entry.grid(row=1, column=1, sticky='ew', pady=5)
        
        # 2. Text Input
        ttk.Label(self.main_frame, text="Input Text (Plaintext or Ciphertext):").grid(row=2, column=0, sticky='nw', pady=(10, 5), columnspan=2)
        self.input_text = tk.Text(self.main_frame, height=5, width=45, wrap=tk.WORD, 
                                  bg=self.ENTRY_BG_COLOR, fg=self.FOREGROUND_COLOR, insertbackground=self.FOREGROUND_COLOR, relief=tk.FLAT, padx=5, pady=5)
        self.input_text.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        # 3. Action Buttons
        self.encrypt_button = ttk.Button(self.main_frame, text="Encrypt", command=self.run_encryption)
        self.encrypt_button.grid(row=4, column=0, padx=(0, 5), pady=10, sticky='ew')
        
        self.decrypt_button = ttk.Button(self.main_frame, text="Decrypt", command=self.run_decryption)
        self.decrypt_button.grid(row=4, column=1, padx=(5, 0), pady=10, sticky='ew')

        # 4. Result Output
        ttk.Label(self.main_frame, text="Result:").grid(row=5, column=0, sticky='nw', pady=(10, 5), columnspan=2)
        self.output_text = tk.Text(self.main_frame, height=5, width=45, state=tk.DISABLED, wrap=tk.WORD, 
                                   bg=self.ENTRY_BG_COLOR, fg='#90ee90', relief=tk.FLAT, padx=5, pady=5)
        self.output_text.grid(row=6, column=0, columnspan=2, pady=(0, 15))

        # 5. Drawback Explanation (Interactive Feature)
        ttk.Label(self.main_frame, text="Cipher Drawback:").grid(row=7, column=0, sticky='nw', pady=(10, 5), columnspan=2)
        
        # Button to run brute force test
        self.drawback_test_button = ttk.Button(self.main_frame, text="Test Brute-Force on Ciphertext", 
                                               command=self.run_drawback_test)
        self.drawback_test_button.grid(row=8, column=0, columnspan=2, pady=(0, 10), sticky='ew')
        
        # Frame for Text and Scrollbar (making it interactive/scrollable)
        self.drawback_frame = ttk.Frame(self.main_frame)
        self.drawback_frame.grid(row=9, column=0, columnspan=2, pady=(0, 5), sticky='ew')
        
        self.drawback_scrollbar = ttk.Scrollbar(self.drawback_frame)
        self.drawback_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Drawback text area: Height increased for showing brute-force results
        self.drawback_text = tk.Text(self.drawback_frame, height=8, width=45, wrap=tk.WORD, state=tk.DISABLED,
                                     bg=self.ENTRY_BG_COLOR, fg=self.FOREGROUND_COLOR, relief=tk.FLAT, padx=5, pady=5,
                                     yscrollcommand=self.drawback_scrollbar.set)
        self.drawback_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Connect scrollbar to the text area
        self.drawback_scrollbar.config(command=self.drawback_text.yview)
        
        # Initial drawback message
        self.update_drawback(
            "The Scytale cipher is a simple transposition cipher. Its security relies entirely on the secrecy of the key (the number of columns)."
        )


    # --- Utility Methods ---

    def display_output(self, result: str, is_error: bool = False):
        """Displays the result in the output area."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        
        # Set color based on whether it's an error
        fg_color = '#ff6347' if is_error else '#90ee90' # Tomato for error, light green for success
        self.output_text.config(fg=fg_color)
        
        self.output_text.insert(tk.END, result)
        self.output_text.config(state=tk.DISABLED)

    def update_drawback(self, message: str):
        """Updates the drawback explanation area."""
        self.drawback_text.config(state=tk.NORMAL)
        self.drawback_text.delete(1.0, tk.END)
        self.drawback_text.insert(tk.END, message)
        self.drawback_text.config(state=tk.DISABLED)

    def get_and_validate_input(self) -> Tuple[Optional[str], Optional[int], Optional[str]]:
        """Retrieves and validates the text and key input."""
        raw_text = self.input_text.get(1.0, tk.END).strip()
        
        # Process text: remove spaces and convert to uppercase for standard cipher operation
        processed_text = "".join(raw_text.split()).upper()

        if not processed_text:
            return None, None, "Error: Input text cannot be empty."

        try:
            key = int(self.key_entry.get())
            if key < 2:
                return None, None, "Error: Key (columns) must be at least 2."
        except ValueError:
            return None, None, "Error: Key must be an integer."
            
        return processed_text, key, None

    # --- Action Handlers ---

    def run_encryption(self):
        """Handles the Encryption process."""
        processed_text, key, error_message = self.get_and_validate_input()
        
        if error_message:
            self.display_output(error_message, is_error=True)
            self.update_drawback("Please fix the input errors above to continue.")
            return
            
        try:
            ciphertext = scytale_encrypt(processed_text, key)
            self.display_output(f"ENCRYPTION SUCCESSFUL (Key: {key}):\n{ciphertext}")
            self.update_drawback(
                "Drawback: This cipher is vulnerable to brute-force attacks. After encryption, try the 'Test Brute-Force' button below to see how easily the cipher can be broken."
            )
        except Exception as e:
            self.display_output(f"Encryption Error: {e}", is_error=True)
            self.update_drawback("An unexpected error occurred during encryption.")

    def run_decryption(self):
        """Handles the Decryption process."""
        processed_cipher, key, error_message = self.get_and_validate_input()
        
        if error_message:
            self.display_output(error_message, is_error=True)
            self.update_drawback("Please fix the input errors above to continue.")
            return

        try:
            decrypted_text = scytale_decrypt(processed_cipher, key)
            self.display_output(f"DECRYPTION SUCCESSFUL (Key: {key}):\n{decrypted_text}")
            self.update_drawback(
                "Drawback: Decryption requires the correct key. Even if you succeeded in decryption, try the 'Test Brute-Force' button to see how easily an attacker can find your key."
            )
        except Exception as e:
            self.display_output(f"Decryption Error: Ensure the Key is Correct. Details: {e}", is_error=True)
            self.update_drawback("An unexpected error occurred during decryption. Check your ciphertext and key.")
            
    def run_drawback_test(self):
        """Demonstrates the brute-force weakness of Scytale by trying all possible keys."""
        
        raw_text = self.input_text.get(1.0, tk.END).strip()
        ciphertext = "".join(raw_text.split()).upper()
        cipher_len = len(ciphertext)

        if not ciphertext:
            self.update_drawback("Test Failed: Enter the ciphertext (encrypted text) to be tested into the 'Input Text' box first.")
            self.display_output("Brute-Force Test Failed: Input Text box is empty.", is_error=True)
            return

        # Test limit: only trying keys from 2 up to 15 or the text length (whichever is smaller)
        # Scytale's key space is small, closely related to the text length.
        MAX_KEY_TEST = min(cipher_len, 15)
        
        results = [f"\n--- Brute-Force Test Results (Keys 2 to {MAX_KEY_TEST}) ---"]
        
        # Brute-Force Attack: try every possible column size (key)
        for key in range(2, MAX_KEY_TEST + 1):
            try:
                decrypted = scytale_decrypt(ciphertext, key)
                # Display only the first 30 characters for readability
                display_text = decrypted[:30] + ('...' if len(decrypted) > 30 else '')
                results.append(f"Key {key:2}: {display_text}")
            except Exception:
                results.append(f"Key {key:2}: [Decryption Failed / Invalid Key Length]")

        results.append("\nDrawback Analysis:\nOnly one key will produce a meaningful message. Because the number of keys to try is very small, an attacker can quickly identify the correct key manually.")
        
        self.display_output(f"Brute-force test started on ciphertext of length {cipher_len}. Results are displayed in the Cipher Drawback panel.")
        self.update_drawback('\n'.join(results))


# --- Main Execution ---

def main():
    root = tk.Tk()
    # Apply a temporary fix for high DPI scaling if needed
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass 

    app = ScytaleCipherApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
