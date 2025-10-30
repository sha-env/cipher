import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import string
from collections import Counter

# --- LOGIKA CAESAR CIPHER (TETAP SAMA) ---

ALPH_LO = string.ascii_lowercase
ALPH_UP = string.ascii_uppercase

# Frekuensi huruf bahasa Inggris (untuk frequency analysis)
EN_FREQ = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074
}

def caesar_shift_char(c, shift):
    """Menggeser satu karakter berdasarkan aturan Caesar Cipher."""
    if c.islower():
        return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
    if c.isupper():
        return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
    return c

def caesar_encrypt(text, shift):
    """Enkripsi teks dengan Caesar Cipher."""
    return ''.join(caesar_shift_char(c, shift) for c in text)

def caesar_decrypt(text, shift):
    """Dekripsi teks dengan Caesar Cipher."""
    return caesar_encrypt(text, -shift)

def brute_force_crack(ciphertext):
    """Mencoba semua kemungkinan shift (0..25) dan mengembalikan hasilnya."""
    candidates = []
    for s in range(0, 26):
        cand = caesar_decrypt(ciphertext, s)
        candidates.append((s, cand))
    return candidates

def score_text_by_frequency(text, freq_table=EN_FREQ):
    """Memberi skor pada teks berdasarkan kesamaan frekuensi hurufnya dengan tabel frekuensi."""
    text_lower = [c for c in text.lower() if c.isalpha()]
    if not text_lower:
        return float('inf')
    
    counts = Counter(text_lower)
    total = sum(counts.values())
    score = 0.0
    for ch in string.ascii_lowercase:
        observed = counts.get(ch, 0)
        expected = freq_table.get(ch, 0) * total / 100.0
        
        # Menggunakan ukuran seperti Chi-squared: (O - E)^2 / E
        if expected > 0:
            score += (observed - expected) ** 2 / expected
            
    return score / len(text_lower) if len(text_lower) > 0 else float('inf')


def frequency_analysis_crack(ciphertext):
    """Menganalisis frekuensi dan mengembalikan kandidat terbaik."""
    candidates = []
    for s in range(0, 26):
        cand = caesar_decrypt(ciphertext, s)
        sc = score_text_by_frequency(cand)
        candidates.append((s, cand, sc))
        
    candidates.sort(key=lambda x: x[2])
    return candidates

# --- APLIKASI GUI TKINTER (MODIFIKASI UNTUK DARK MODE) ---

class CaesarCipherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Caesar Cipher - Enkripsi, Dekripsi, dan Pembongkaran")
        self.geometry("800x600")
        
        # --- DARK MODE COLORS ---
        self.BG_DARK = '#2e2e2e'
        self.FG_LIGHT = '#ffffff'
        self.ACCENT_COLOR = '#00aaff'
        self.TEXT_AREA_BG = '#3a3a3a'
        self.TEXT_AREA_FG = '#e0e0e0'
        self.BUTTON_BG = '#4f4f4f'
        
        # Set background utama
        self.config(bg=self.BG_DARK)
        
        # Konfigurasi style untuk Dark Mode
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Konfigurasi umum untuk Label, Frame, dan Notebook
        self.style.configure('.', background=self.BG_DARK, foreground=self.FG_LIGHT, font=('Inter', 10))
        self.style.configure('TFrame', background=self.BG_DARK)
        self.style.configure('TLabel', background=self.BG_DARK, foreground=self.FG_LIGHT)
        
        # Konfigurasi Notebook (Tabs)
        self.style.configure('TNotebook', background=self.BG_DARK, borderwidth=0)
        self.style.configure('TNotebook.Tab', 
                             padding=[10, 5], 
                             font=('Inter', 10, 'bold'),
                             background=self.BUTTON_BG,
                             foreground=self.FG_LIGHT,
                             lightcolor=self.BUTTON_BG, # Mengatur garis tepi tab
                             bordercolor=self.BG_DARK)
        self.style.map('TNotebook.Tab', 
                       background=[('selected', self.ACCENT_COLOR)],
                       foreground=[('selected', self.BG_DARK)])
        
        # Konfigurasi Tombol
        self.style.configure('TButton', 
                             background=self.ACCENT_COLOR, 
                             foreground=self.BG_DARK, 
                             font=('Inter', 10, 'bold'),
                             borderwidth=0,
                             padding=6)
        self.style.map('TButton', 
                       background=[('active', self.ACCENT_COLOR), ('pressed', self.ACCENT_COLOR)],
                       foreground=[('active', self.BG_DARK), ('pressed', self.BG_DARK)])

        # Konfigurasi Entry
        self.style.configure('TEntry', fieldbackground=self.TEXT_AREA_BG, foreground=self.TEXT_AREA_FG, borderwidth=0)


        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Membuat Frame untuk setiap tab
        self.create_encrypt_decrypt_tab()
        self.create_brute_force_tab()
        self.create_frequency_analysis_tab()

    def create_encrypt_decrypt_tab(self):
        """Membuat tab untuk Enkripsi dan Dekripsi."""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="Enkripsi / Dekripsi")

        # Grid configuration for the tab
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=3)

        # Bagian Input Shift
        shift_frame = ttk.Frame(tab)
        shift_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        shift_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(shift_frame, text="Shift (1-25):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.shift_entry = ttk.Entry(shift_frame, width=10)
        self.shift_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.shift_entry.insert(0, "3") # Default shift

        # Bagian Input Teks (scrolledtext perlu kustomisasi langsung)
        ttk.Label(tab, text="Teks Input (Plaintext/Ciphertext):").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.input_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('Inter', 10), 
                                                         bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.input_text_area.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Tombol Aksi
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="ENKRIPSI >>", command=self.handle_encrypt).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="<< DEKRIPSI", command=self.handle_decrypt).pack(side=tk.LEFT, padx=10)

        # Bagian Output Teks (scrolledtext perlu kustomisasi langsung)
        ttk.Label(tab, text="Hasil Output:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.output_text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=8, font=('Inter', 10), state='disabled',
                                                          bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.output_text_area.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        # Konfigurasi baris untuk ekspansi
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_rowconfigure(3, weight=1)


    def create_brute_force_tab(self):
        """Membuat tab untuk Brute Force Cracking."""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="Brute Force Crack")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(4, weight=1) # Diubah ke baris output
        
        ttk.Label(tab, text="Masukkan Ciphertext untuk Brute Force:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.brute_force_input = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=5, font=('Inter', 10),
                                                           bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.brute_force_input.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(tab, text="JALANKAN BRUTE FORCE", command=self.handle_brute_force).grid(row=2, column=0, pady=10)

        ttk.Label(tab, text="Semua 26 Kandidat Plaintext (Shift 0-25):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.brute_force_output = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=15, font=('monospace', 9), state='disabled',
                                                            bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.brute_force_output.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        
        # tab.grid_rowconfigure(4, weight=1) # Sudah dipindahkan ke awal

    def create_frequency_analysis_tab(self):
        """Membuat tab untuk Frequency Analysis Cracking."""
        tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(tab, text="Frequency Analysis")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(4, weight=1) # Diubah ke baris output

        ttk.Label(tab, text="Masukkan Ciphertext untuk Analisis Frekuensi:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.freq_analysis_input = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=5, font=('Inter', 10),
                                                             bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.freq_analysis_input.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        ttk.Button(tab, text="ANALISIS FREKUENSI", command=self.handle_frequency_analysis).grid(row=2, column=0, pady=10)

        ttk.Label(tab, text="5 Kandidat Plaintext Paling Mungkin (Skor Kecil = Lebih Baik):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.freq_analysis_output = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=15, font=('monospace', 9), state='disabled',
                                                              bg=self.TEXT_AREA_BG, fg=self.TEXT_AREA_FG, insertbackground=self.FG_LIGHT)
        self.freq_analysis_output.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        
        # tab.grid_rowconfigure(4, weight=1) # Sudah dipindahkan ke awal
        
        ttk.Label(tab, text="(Catatan: Menggunakan frekuensi huruf bahasa Inggris, mungkin kurang akurat untuk bahasa lain.)", 
                  font=('Inter', 9, 'italic')).grid(row=5, column=0, sticky="w")

    # --- HANDLER LOGIKA (TETAP SAMA) ---

    def _get_shift(self):
        """Mengambil dan memvalidasi nilai shift."""
        try:
            shift = int(self.shift_entry.get())
            return shift % 26
        except ValueError:
            messagebox.showerror("Error Input", "Nilai shift harus berupa bilangan bulat.")
            return None

    def _update_output(self, text):
        """Memperbarui widget output teks."""
        self.output_text_area.config(state='normal')
        self.output_text_area.delete('1.0', tk.END)
        self.output_text_area.insert(tk.END, text)
        self.output_text_area.config(state='disabled')

    def handle_encrypt(self):
        """Handler untuk tombol Enkripsi."""
        shift = self._get_shift()
        if shift is not None:
            text = self.input_text_area.get('1.0', tk.END).strip()
            encrypted_text = caesar_encrypt(text, shift)
            self._update_output(encrypted_text)

    def handle_decrypt(self):
        """Handler untuk tombol Dekripsi."""
        shift = self._get_shift()
        if shift is not None:
            text = self.input_text_area.get('1.0', tk.END).strip()
            decrypted_text = caesar_decrypt(text, shift)
            self._update_output(decrypted_text)
            
    def _update_crack_output(self, widget, content):
        """Memperbarui widget output cracking."""
        widget.config(state='normal')
        widget.delete('1.0', tk.END)
        widget.insert(tk.END, content)
        widget.config(state='disabled')

    def handle_brute_force(self):
        """Handler untuk tombol Brute Force Crack."""
        ciphertext = self.brute_force_input.get('1.0', tk.END).strip()
        if not ciphertext:
            self._update_crack_output(self.brute_force_output, "Masukkan ciphertext terlebih dahulu.")
            return

        candidates = brute_force_crack(ciphertext)
        output = "Shift | Plaintext\n"
        output += "-" * 50 + "\n"
        for s, cand in candidates:
            # Batasi panjang tampilan plaintext
            display_cand = cand[:70] + "..." if len(cand) > 70 else cand
            output += f"{s:^5} | {display_cand}\n"
            
        self._update_crack_output(self.brute_force_output, output)

    def handle_frequency_analysis(self):
        """Handler untuk tombol Frequency Analysis Crack."""
        ciphertext = self.freq_analysis_input.get('1.0', tk.END).strip()
        if not ciphertext:
            self._update_crack_output(self.freq_analysis_output, "Masukkan ciphertext terlebih dahulu.")
            return
            
        candidates = frequency_analysis_crack(ciphertext)
        
        # Format output
        output = "Rank | Shift | Score (Normalized) | Plaintext\n"
        output += "-" * 70 + "\n"
        
        # Ambil 5 kandidat teratas
        for i, (s, cand, sc) in enumerate(candidates[:5]):
            # Batasi panjang tampilan plaintext
            display_cand = cand[:55] + "..." if len(cand) > 55 else cand
            output += f"{i+1:^4} | {s:^5} | {sc:^18.6f} | {display_cand}\n"
        
        output += "\n"
        output += f"Kandidat TERBAIK:\nShift {candidates[0][0]} dengan Skor {candidates[0][2]:.6f}\n{candidates[0][1]}"

        self._update_crack_output(self.freq_analysis_output, output)

if __name__ == "__main__":
    # Inisialisasi dan jalankan aplikasi GUI
    app = CaesarCipherApp()
    app.mainloop()