import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import string
from collections import Counter
import sys

# --- 📚 CAESAR CIPHER LOGIC AND CONSTANTS ---

# Alphabet Constants
ALPH_LO = string.ascii_lowercase
ALPH_UP = string.ascii_uppercase
ALPH_LEN = 26

# Standard English letter frequencies (for frequency analysis)
EN_FREQ = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074
}

def caesar_shift_char(char, shift):
    """Shifts a single alphabetic character according to the Caesar Cipher rules."""
    if char.islower():
        # Calculate new position (0-25) and convert back to char
        return chr((ord(char) - ord('a') + shift) % ALPH_LEN + ord('a'))
    if char.isupper():
        return chr((ord(char) - ord('A') + shift) % ALPH_LEN + ord('A'))
    # Return non-alphabetic characters unchanged
    return char

def caesar_process_text(text, shift):
    """
    General function for encryption (positive shift) or decryption (negative shift).
    """
    return ''.join(caesar_shift_char(c, shift) for c in text)

def brute_force_crack(ciphertext):
    """Attempts all 26 possible decryption shifts (0 through 25)."""
    # Decrypting with shift 's' is equivalent to encrypting with shift '-s'
    return [(s, caesar_process_text(ciphertext, -s)) for s in range(ALPH_LEN)]

def score_text_by_frequency(text, freq_table=EN_FREQ):
    """
    Scores a text based on how closely its letter frequency matches the target
    frequency table (e.g., English). It uses a normalized Chi-squared test.
    Lower score indicates a higher probability of being standard English text.
    """
    text_lower = [c for c in text.lower() if c.isalpha()]
    if not text_lower:
        return float('inf') # Worst score for empty or non-alphabetic text
    
    counts = Counter(text_lower)
    total_letters = len(text_lower)
    score = 0.0
    
    # Calculate Chi-squared score
    for ch in string.ascii_lowercase:
        observed_count = counts.get(ch, 0)
        expected_percentage = freq_table.get(ch, 0)
        expected_count = expected_percentage * total_letters / 100.0
        
        # Chi-squared: (Observed - Expected)^2 / Expected
        if expected_count > 0:
            score += (observed_count - expected_count) ** 2 / expected_count
            
    # Normalize score by text length
    return score / total_letters


def frequency_analysis_crack(ciphertext):
    """
    Performs frequency analysis by trying all 26 shifts and scoring the resulting
    plaintexts. Returns candidates sorted by score (best first).
    """
    candidates = []
    for s in range(ALPH_LEN):
        # Decrypt with shift 's'
        candidate_text = caesar_process_text(ciphertext, -s)
        score = score_text_by_frequency(candidate_text)
        candidates.append((s, candidate_text, score))
        
    # Sort by score: smallest score (best fit) first
    candidates.sort(key=lambda x: x[2])
    return candidates

# --- 🖥️ TKINTER GUI APPLICATION (DARK MODE) ---

class CaesarCipherApp(tk.Tk):
    
    # Dark Mode Color Constants
    BG_DARK = '#2e2e2e'
    FG_LIGHT = '#ffffff'
    ACCENT_COLOR = '#00aaff' 
    TEXT_AREA_BG = '#3a3a3a'
    TEXT_AREA_FG = '#e0e0e0'
    BUTTON_BG = '#4f4f4f'
    
    def __init__(self):
        super().__init__()
        self.title("Caesar Cipher Tool - Encrypt, Decrypt, and Crack")
        self.geometry("850x650")
        
        # Setup visual styling
        self._setup_style()
        
        # Main container for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Initialize tabs
        self._create_encrypt_decrypt_tab()
        self._create_brute_force_tab()
        self._create_frequency_analysis_tab()
        
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

        # 1. Shift Input
        shift_frame = ttk.Frame(tab)
        shift_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        shift_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(shift_frame, text="Shift (Key 0-25):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.shift_entry = ttk.Entry(shift_frame, width=10)
        self.shift_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w") 
        self.shift_entry.insert(0, "3") # Default

        # 2. Input Text Area
        ttk.Label(tab, text="Input Text (Plaintext/Ciphertext):").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.input_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('Inter', 10), 
                                                         bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.input_text_area.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # 3. Action Buttons
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="ENCRYPT >>", command=self._handle_encrypt).pack(side=tk.LEFT, padx=20)
        ttk.Button(button_frame, text="<< DECRYPT", command=self._handle_decrypt).pack(side=tk.LEFT, padx=20)

        # 4. Output Text Area
        ttk.Label(tab, text="Output Result:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.output_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('Inter', 10), state='disabled',
                                                          bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.output_text_area.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")


    def _create_brute_force_tab(self):
        """Creates the Brute Force Cracking tab."""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="Brute Force Crack")
        
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(4, weight=1) 

        # 1. Input Ciphertext
        ttk.Label(tab, text="Enter Ciphertext for Brute Force:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.brute_force_input = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=5, font=('Inter', 10),
                                                           bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.brute_force_input.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # 2. Action Button
        ttk.Button(tab, text="RUN BRUTE FORCE (26 Possibilities)", command=self._handle_brute_force).grid(row=2, column=0, pady=10)

        # 3. Output Area
        ttk.Label(tab, text="All 26 Plaintext Candidates (Shift 0-25):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.brute_force_output = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=15, font=('monospace', 9), state='disabled',
                                                            bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.brute_force_output.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

    def _create_frequency_analysis_tab(self):
        """Creates the Frequency Analysis Cracking tab."""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="Frequency Analysis")
        
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(4, weight=1) 

        # 1. Input Ciphertext
        ttk.Label(tab, text="Enter Ciphertext for Frequency Analysis:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.freq_analysis_input = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=5, font=('Inter', 10),
                                                             bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.freq_analysis_input.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # 2. Action Button
        ttk.Button(tab, text="RUN FREQUENCY ANALYSIS (Predict Key)", command=self._handle_frequency_analysis).grid(row=2, column=0, pady=10)

        # 3. Output Area
        ttk.Label(tab, text="5 Most Likely Plaintext Candidates:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.freq_analysis_output = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=15, font=('monospace', 9), state='disabled',
                                                              bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.freq_analysis_output.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        
        # 4. Note
        ttk.Label(tab, text="*Uses English letter frequencies. Lower Chi-Squared score = Better fit.", 
                  font=('Inter', 9, 'italic')).grid(row=5, column=0, sticky="w", pady=(5, 0))


    # --- 🛠️ HANDLER METHODS ---

    def _get_shift(self):
        """Retrieves and validates the shift value from the entry field."""
        try:
            # Get modulo 26 to handle shifts > 25
            shift = int(self.shift_entry.get())
            return shift % ALPH_LEN
        except ValueError:
            messagebox.showerror("Input Error", "The **Shift** value must be an integer (0-25).")
            return None

    def _update_output(self, widget, text, font=('Inter', 10)):
        """Helper function to update a ScrolledText widget."""
        widget.config(state='normal', font=font)
        widget.delete('1.0', tk.END)
        widget.insert(tk.END, text)
        widget.config(state='disabled')
        # Scroll to top
        widget.yview_moveto(0)

    def _handle_encrypt(self):
        """Handler for the Encrypt button."""
        shift = self._get_shift()
        if shift is not None:
            text = self.input_text_area.get('1.0', tk.END).strip()
            # Encryption uses a positive shift
            encrypted_text = caesar_process_text(text, shift)
            self._update_output(self.output_text_area, encrypted_text)

    def _handle_decrypt(self):
        """Handler for the Decrypt button."""
        shift = self._get_shift()
        if shift is not None:
            text = self.input_text_area.get('1.0', tk.END).strip()
            # Decryption uses a negative shift
            decrypted_text = caesar_process_text(text, -shift)
            self._update_output(self.output_text_area, decrypted_text)
            
    def _handle_brute_force(self):
        """Handler for the Brute Force Crack button."""
        ciphertext = self.brute_force_input.get('1.0', tk.END).strip()
        if not ciphertext:
            self._update_output(self.brute_force_output, "Please enter **ciphertext** in the input field above.", font=('Inter', 10))
            return

        candidates = brute_force_crack(ciphertext)
        
        # Format output table
        output = " Shift | Plaintext (First 70 Characters)\n"
        output += "=" * 75 + "\n"
        
        for s, cand in candidates:
            # Clean up newlines and limit/pad the text for uniform display
            display_cand = cand.replace('\n', ' ') 
            display_cand = display_cand[:70].ljust(70) 
            output += f"  {s:02d}   | {display_cand}\n"
            
        self._update_output(self.brute_force_output, output, font=('monospace', 9))

    def _handle_frequency_analysis(self):
        """Handler for the Frequency Analysis Crack button."""
        ciphertext = self.freq_analysis_input.get('1.0', tk.END).strip()
        if not ciphertext:
            self._update_output(self.freq_analysis_output, "Please enter **ciphertext** in the input field above.", font=('Inter', 10))
            return
            
        candidates = frequency_analysis_crack(ciphertext)
        
        # Format output for the top candidates
        output = "Rank | Shift | Chi-Squared Score | Plaintext (First 55 Characters)\n"
        output += "=" * 85 + "\n"
        
        # Display the top 5 candidates
        for i, (s, cand, sc) in enumerate(candidates[:5]):
            display_cand = cand.replace('\n', ' ')
            display_cand = display_cand[:55].ljust(55) 
            output += f" {i+1:^4} |  {s:02d}   | {sc:^16.6f} | {display_cand}\n"
        
        # Highlight the best candidate
        best_shift, best_text, best_score = candidates[0]
        
        output += "\n" + "=" * 85 + "\n"
        output += "BEST PREDICTION:\n"
        output += f"Decryption Key (Shift): **{best_shift}**\n"
        output += f"Fitness Score (Chi-Squared): {best_score:.6f}\n"
        output += "\n--- Full Plaintext ---\n"
        output += best_text

        self._update_output(self.freq_analysis_output, output, font=('monospace', 9))


if __name__ == "__main__":
    # Initialize and run the GUI application
    try:
        app = CaesarCipherApp()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred while running the application: {e}", file=sys.stderr)