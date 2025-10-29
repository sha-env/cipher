import tkinter as tk
from tkinter import ttk, messagebox
import string
from math import gcd

# -------------------------
# Hill cipher core (3x3)
# -------------------------
ALPH = string.ascii_uppercase

# ... (Fungsi-fungsi yang sudah ada seperti sanitize_key_text, key_text_to_matrix, 
# matrix_mod26, mat_mul_vec, determinant_3x3, modinv, cofactor_matrix_3x3, 
# adjugate_3x3, inverse_matrix_mod26, preprocess_plaintext, pad_text, 
# split_blocks, encrypt_text_with_key, decrypt_text_with_key) ...

# Salin dan tempel fungsi-fungsi yang sudah ada di sini, 
# atau asumsikan sudah ada di file yang sama.

def sanitize_key_text(k):
    # Ambil hanya huruf, uppercase
    letters = [c for c in k.upper() if c.isalpha()]
    return ''.join(letters)

def key_text_to_matrix(key_text):
    """
    Terima string huruf (panjang >=9), kembalikan matriks 3x3 (list of lists) modulo 26.
    Jika kurang dari 9 huruf, raise ValueError.
    """
    s = sanitize_key_text(key_text)
    if len(s) < 9:
        raise ValueError("Key harus berisi minimal 9 huruf (3x3).")
    vals = [ALPH.index(c) for c in s[:9]]
    # buat matriks 3x3 row-major
    mat = [vals[0:3], vals[3:6], vals[6:9]]
    return mat

def matrix_mod26(mat):
    return [[x % 26 for x in row] for row in mat]

def mat_mul_vec(mat, vec):
    """mat 3x3, vec len3 -> hasil len3 modulo 26"""
    res = [0,0,0]
    for i in range(3):
        s = 0
        for j in range(3):
            s += mat[i][j] * vec[j]
        res[i] = s % 26
    return res

def determinant_3x3(mat):
    a,b,c = mat[0]
    d,e,f = mat[1]
    g,h,i = mat[2]
    det = a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)
    return det

def modinv(a, m):
    """modular inverse of a modulo m using extended gcd. Return None jika tidak ada."""
    a = a % m
    if gcd(a, m) != 1:
        return None
    # extended euclid
    def egcd(a,b):
        if b==0:
            return (1,0,a)
        x,y,g = egcd(b, a % b)
        return (y, x - (a // b) * y, g)
    x, y, g = egcd(a, m)
    return x % m

def cofactor_matrix_3x3(mat):
    # compute matrix of cofactors (not transposed)
    a,b,c = mat[0]
    d,e,f = mat[1]
    g,h,i = mat[2]
    C = [
        [ (e*i - f*h), -(d*i - f*g),  (d*h - e*g)],
        [-(b*i - c*h),  (a*i - c*g), -(a*h - b*g)],
        [ (b*f - c*e), -(a*f - c*d),  (a*e - b*d)]
    ]
    return C

def adjugate_3x3(mat):
    # adjugate = transpose of cofactor matrix
    C = cofactor_matrix_3x3(mat)
    # transpose
    return [[C[j][i] for j in range(3)] for i in range(3)]

def inverse_matrix_mod26(mat):
    det = determinant_3x3(mat)
    det_mod = det % 26
    inv_det = modinv(det_mod, 26)
    if inv_det is None:
        return None, det, det_mod, None  # tidak invertible
    adj = adjugate_3x3(mat)
    inv = [[ (inv_det * adj[i][j]) % 26 for j in range(3)] for i in range(3)]
    return inv, det, det_mod, inv_det

# -------------------------
# Text -> blocks 3
# -------------------------
def preprocess_plaintext(pt):
    # Ambil hanya huruf, uppercase
    letters = [c for c in pt.upper() if c.isalpha()]
    return ''.join(letters)

def pad_text(s):
    # pad dengan 'X' agar panjang kelipatan 3
    rem = len(s) % 3
    if rem != 0:
        s += 'X' * (3 - rem)
    return s

def split_blocks(s):
    return [s[i:i+3] for i in range(0, len(s), 3)]

def encrypt_text_with_key(plaintext, key_mat):
    s = preprocess_plaintext(plaintext)
    if not s:
        return ""
    s = pad_text(s)
    blocks = split_blocks(s)
    cipher_blocks = []
    for blk in blocks:
        vec = [ALPH.index(ch) for ch in blk]
        res = mat_mul_vec(key_mat, vec)
        cipher_blocks.append(''.join(ALPH[v] for v in res))
    # Kita tampilkan ciphertext tanpa spasi
    return ''.join(cipher_blocks)

def decrypt_text_with_key(ciphertext, key_mat):
    # diharapkan ciphertext huruf A-Z panjang kelipatan 3
    s = sanitize_key_text(ciphertext)
    if not s:
        return ""
    blocks = split_blocks(s)
    inv_mat_det = inverse_matrix_mod26(key_mat)
    inv_mat, det, det_mod, inv_det = inv_mat_det
    if inv_mat is None:
        raise ValueError("Key matrix tidak invertible (determinant tidak coprime dengan 26).")
    plain_blocks = []
    for blk in blocks:
        vec = [ALPH.index(ch) for ch in blk]
        res = mat_mul_vec(inv_mat, vec)
        plain_blocks.append(''.join(ALPH[v] for v in res))
    return ''.join(plain_blocks)

# -------------------------
# KPA Functionality
# -------------------------

def mat_mul_3x3(mat_a, mat_b):
    """mat_a 3x3, mat_b 3x3 -> hasil 3x3 modulo 26"""
    res = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            s = 0
            for k in range(3):
                s += mat_a[i][k] * mat_b[k][j]
            res[i][j] = s % 26
    return res

def key_from_kpa(plaintext_blocks, ciphertext_blocks):
    """
    Hitung matriks kunci (K) dari 3 blok plaintext (P) dan 3 blok ciphertext (C).
    Hubungan: C = K * P (mod 26)
    Maka: K = C * P^-1 (mod 26)
    
    plaintext_blocks/ciphertext_blocks: list of 3-char strings
    """
    if len(plaintext_blocks) < 3 or len(ciphertext_blocks) < 3:
        raise ValueError("Dibutuhkan minimal 3 blok (9 huruf) untuk Plaintext dan Ciphertext.")

    # Matrix P: Kolom adalah vektor plaintext
    P_cols = [[ALPH.index(c) for c in block] for block in plaintext_blocks[:3]]
    P = [[P_cols[j][i] for j in range(3)] for i in range(3)]
    
    # Matrix C: Kolom adalah vektor ciphertext
    C_cols = [[ALPH.index(c) for c in block] for block in ciphertext_blocks[:3]]
    C = [[C_cols[j][i] for j in range(3)] for i in range(3)]

    # 1. Cari P^-1 (Inverse dari matriks Plaintext)
    P_inv_det = inverse_matrix_mod26(P)
    P_inv, det_P, det_P_mod, inv_det_P = P_inv_det

    if P_inv is None:
        raise ValueError(f"Matriks Plaintext (P) tidak invertible (det P mod 26 = {det_P_mod}). Pilih blok plaintext yang berbeda.")

    # 2. Hitung K = C * P^-1 (mod 26)
    K = mat_mul_3x3(C, P_inv)
    return K, det_P, det_P_mod, inv_det_P

# -------------------------
# GUI
# -------------------------
class HillCipherGUI(tk.Tk):
    # ... (Bagian __init__, _create_style, _build_ui, _build_encrypt_tab, 
    # on_encrypt, _build_decrypt_tab, on_decrypt, _copy_text_widget) ...
    # Salin dan tempel fungsi-fungsi yang sudah ada di sini

    def __init__(self):
        super().__init__()
        self.title("Hill Cipher 3x3 — Encrypt / Decrypt / Drawback")
        self.geometry("820x640") # Ditingkatkan tingginya untuk KPA
        self.configure(bg="#101216")
        self._create_style()
        self._build_ui()

    def _create_style(self):
        style = ttk.Style(self)
        # use default theme and tweak some colors for dark feel
        style.theme_use('clam')
        style.configure('TNotebook', background='#101216')
        style.configure('TNotebook.Tab', background='#22262b', foreground='white')
        style.map('TNotebook.Tab', background=[('selected', '#2f3640')])
        style.configure('TFrame', background='#101216')
        style.configure('TLabel', background='#101216', foreground='white', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TEntry', fieldbackground='#23272b', foreground='white')
        style.configure('TText', background='#23272b', foreground='white')
        # colors for normal tk widgets
        self.bg = "#101216"
        self.fg = "white"
        self.box_bg = "#23272b"
        self.btn_bg = "#3b82f6"
        self.btn_fg = "#ffffff"

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=12, pady=12)

        # Tabs
        encrypt_tab = ttk.Frame(notebook)
        decrypt_tab = ttk.Frame(notebook)
        drawback_tab = ttk.Frame(notebook)

        notebook.add(encrypt_tab, text="Encrypt")
        notebook.add(decrypt_tab, text="Decrypt")
        notebook.add(drawback_tab, text="Drawback (Kelemahan)")

        self._build_encrypt_tab(encrypt_tab)
        self._build_decrypt_tab(decrypt_tab)
        self._build_drawback_tab(drawback_tab)

        # Footer
        footer = tk.Label(self, text="Hill Cipher 3×3 — Key input manual (9 huruf). Padding otomatis pakai 'X'.", 
                             bg=self.bg, fg=self.fg, anchor='w')
        footer.pack(fill='x', padx=12, pady=(0,8))

    # -------------------------
    # Encrypt Tab (Sudah ada)
    # -------------------------
    def _build_encrypt_tab(self, parent):
        frm = tk.Frame(parent, bg=self.bg)
        frm.pack(fill='both', expand=True, padx=12, pady=12)

        # Key input
        tk.Label(frm, text="Key (9 huruf, cont: GYBNQKURP)", bg=self.bg, fg=self.fg).grid(row=0, column=0, sticky='w')
        self.encrypt_key_entry = ttk.Entry(frm, width=28)
        self.encrypt_key_entry.grid(row=0, column=1, sticky='w', padx=(8,0))
        self.encrypt_key_entry.insert(0, "GYBNQKURP")

        # Plaintext input
        tk.Label(frm, text="Plaintext:", bg=self.bg, fg=self.fg).grid(row=1, column=0, sticky='nw', pady=(10,0))
        self.encrypt_plaintext = tk.Text(frm, width=70, height=8, bg=self.box_bg, fg=self.fg)
        self.encrypt_plaintext.grid(row=1, column=1, columnspan=2, pady=(10,0))

        # Buttons
        btn_encrypt = tk.Button(frm, text="Encrypt", command=self.on_encrypt, bg=self.btn_bg, fg=self.btn_fg)
        btn_encrypt.grid(row=2, column=1, sticky='w', pady=10)

        btn_copy = tk.Button(frm, text="Copy Ciphertext", command=lambda: self._copy_text_widget(self.encrypt_result_text), bg="#2a2f33", fg='white')
        btn_copy.grid(row=2, column=1, sticky='e', padx=(0,120), pady=10)

        # Result
        tk.Label(frm, text="Ciphertext:", bg=self.bg, fg=self.fg).grid(row=3, column=0, sticky='nw')
        self.encrypt_result_text = tk.Text(frm, width=70, height=6, bg=self.box_bg, fg=self.fg)
        self.encrypt_result_text.grid(row=3, column=1, columnspan=2, pady=(6,0))

    def on_encrypt(self):
        key_text = self.encrypt_key_entry.get()
        try:
            key_mat = key_text_to_matrix(key_text)
            key_mat = matrix_mod26(key_mat)
        except ValueError as e:
            messagebox.showerror("Key error", str(e))
            return
        pt = self.encrypt_plaintext.get("1.0", tk.END).strip()
        if not pt.strip():
            messagebox.showwarning("Input missing", "Masukkan plaintext terlebih dahulu.")
            return
        cipher = encrypt_text_with_key(pt, key_mat)
        self.encrypt_result_text.delete("1.0", tk.END)
        self.encrypt_result_text.insert(tk.END, cipher)

    # -------------------------
    # Decrypt Tab (Sudah ada)
    # -------------------------
    def _build_decrypt_tab(self, parent):
        frm = tk.Frame(parent, bg=self.bg)
        frm.pack(fill='both', expand=True, padx=12, pady=12)

        tk.Label(frm, text="Key (9 huruf):", bg=self.bg, fg=self.fg).grid(row=0, column=0, sticky='w')
        self.decrypt_key_entry = ttk.Entry(frm, width=28)
        self.decrypt_key_entry.grid(row=0, column=1, sticky='w', padx=(8,0))
        self.decrypt_key_entry.insert(0, "GYBNQKURP")

        tk.Label(frm, text="Ciphertext (A-Z):", bg=self.bg, fg=self.fg).grid(row=1, column=0, sticky='nw', pady=(10,0))
        self.decrypt_ciphertext = tk.Text(frm, width=70, height=8, bg=self.box_bg, fg=self.fg)
        self.decrypt_ciphertext.grid(row=1, column=1, columnspan=2, pady=(10,0))

        btn_decrypt = tk.Button(frm, text="Decrypt", command=self.on_decrypt, bg=self.btn_bg, fg=self.btn_fg)
        btn_decrypt.grid(row=2, column=1, sticky='w', pady=10)

        btn_copy = tk.Button(frm, text="Copy Plaintext", command=lambda: self._copy_text_widget(self.decrypt_result_text), bg="#2a2f33", fg='white')
        btn_copy.grid(row=2, column=1, sticky='e', padx=(0,120), pady=10)

        tk.Label(frm, text="Plaintext (result):", bg=self.bg, fg=self.fg).grid(row=3, column=0, sticky='nw')
        self.decrypt_result_text = tk.Text(frm, width=70, height=6, bg=self.box_bg, fg=self.fg)
        self.decrypt_result_text.grid(row=3, column=1, columnspan=2, pady=(6,0))

    def on_decrypt(self):
        key_text = self.decrypt_key_entry.get()
        try:
            key_mat = key_text_to_matrix(key_text)
            key_mat = matrix_mod26(key_mat)
        except ValueError as e:
            messagebox.showerror("Key error", str(e))
            return

        ciphertext = self.decrypt_ciphertext.get("1.0", tk.END).strip()
        s = sanitize_key_text(ciphertext)
        if not s:
            messagebox.showwarning("Input missing", "Masukkan ciphertext (huruf A-Z) terlebih dahulu.")
            return
        if len(s) % 3 != 0:
            messagebox.showwarning("Length warning", "Ciphertext length bukan kelipatan 3 — tambahkan padding atau periksa input.")
            # kita tetap coba dekode dengan menambah padding X agar kelipatan 3
            s = pad_text(s)
        # compute inverse matrix
        inv_mat, det, det_mod, inv_det = inverse_matrix_mod26(key_mat)
        if inv_mat is None:
            messagebox.showerror("Key non-invertible", f"Key matrix tidak invertible.\nDeterminant = {det} -> det mod26 = {det_mod} (tidak memiliki inverse mod26).")
            return
        # decrypt
        try:
            plain = decrypt_text_with_key(s, key_mat)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self.decrypt_result_text.delete("1.0", tk.END)
        self.decrypt_result_text.insert(tk.END, plain)

    # -------------------------
    # Drawback Tab (Modified to include KPA)
    # -------------------------
    def _build_drawback_tab(self, parent):
        frm = tk.Frame(parent, bg=self.bg)
        frm.pack(fill='both', expand=True, padx=12, pady=12)

        # Frame 1: Key Details
        key_frame = tk.LabelFrame(frm, text=" Key Matrix Details ", bg=self.bg, fg=self.fg, bd=2, relief=tk.GROOVE)
        key_frame.pack(fill='x', pady=5, padx=5)

        tk.Label(key_frame, text="Key (9 huruf):", bg=self.bg, fg=self.fg).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.draw_key_entry = ttk.Entry(key_frame, width=28)
        self.draw_key_entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.draw_key_entry.insert(0, "GYBNQKURP")

        btn_show = tk.Button(key_frame, text="Tampilkan Langkah Key", command=self.on_drawback_key, bg=self.btn_bg, fg=self.btn_fg)
        btn_show.grid(row=0, column=2, sticky='w', padx=12, pady=5)

        # Frame 2: KPA Section
        kpa_frame = tk.LabelFrame(frm, text=" Known Plaintext Attack (KPA) ", bg=self.bg, fg=self.fg, bd=2, relief=tk.GROOVE)
        kpa_frame.pack(fill='x', pady=10, padx=5)

        # KPA Input
        tk.Label(kpa_frame, text="3 Plaintext (9 huruf, cth: ACTGOGAME):", bg=self.bg, fg=self.fg).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.kpa_plain_entry = ttk.Entry(kpa_frame, width=30)
        self.kpa_plain_entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.kpa_plain_entry.insert(0, "ACTGOGAME")

        tk.Label(kpa_frame, text="3 Ciphertext (9 huruf, cth: YKLBQLKAS):", bg=self.bg, fg=self.fg).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.kpa_cipher_entry = ttk.Entry(kpa_frame, width=30)
        self.kpa_cipher_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.kpa_cipher_entry.insert(0, "QGEGEYKAS") # Ini hasil ACTGOGAME dengan key GYBNQKURP

        btn_kpa = tk.Button(kpa_frame, text="Jalankan KPA", command=self.on_drawback_kpa, bg="darkred", fg='white')
        btn_kpa.grid(row=0, column=2, rowspan=2, sticky='w', padx=12)


        # Detail area
        detail_frame = tk.Frame(frm, bg=self.bg)
        detail_frame.pack(fill='both', expand=True)

        self.draw_detail_text = tk.Text(detail_frame, width=95, height=18, bg=self.box_bg, fg=self.fg)
        self.draw_detail_text.pack(pady=10, fill='both', expand=True)

        btn_copy = tk.Button(frm, text="Copy Details", command=lambda: self._copy_text_widget(self.draw_detail_text), bg="#2a2f33", fg='white')
        btn_copy.pack(pady=(0, 5))


    def on_drawback_key(self):
        # ... (Logika yang sudah ada untuk menampilkan detail Key dan Inverse) ...
        key_text = self.draw_key_entry.get()
        try:
            key_mat = key_text_to_matrix(key_text)
            key_mat = matrix_mod26(key_mat)
        except ValueError as e:
            messagebox.showerror("Key error", str(e))
            return

        inv_mat, det, det_mod, inv_det = inverse_matrix_mod26(key_mat)

        # Build details
        lines = []
        lines.append("== Hill Cipher 3x3 — Key Matrix Details ==")
        lines.append("")
        lines.append("Key text (letters): " + sanitize_key_text(key_text)[:9])
        lines.append("Key matrix (3x3) — values 0..25 (row-major):")
        for r in key_mat:
            lines.append("  " + '  '.join(f"{v:2d}" for v in r))
        lines.append("")
        lines.append(f"Determinant (integer): {det}")
        lines.append(f"Determinant mod 26: {det_mod}")
        if inv_det is None:
            lines.append("Inverse determinant mod26: TIDAK ADA (determinant tidak coprime dengan 26).")
            lines.append("")
            lines.append("Karena tidak ada inverse determinant, matriks kunci tidak invertible dan dekripsi tidak mungkin.")
        else:
            lines.append(f"Inverse determinant mod26: {inv_det}  (karena {det_mod} * {inv_det} ≡ 1 (mod 26))")
            lines.append("")
            lines.append("Adjugate (transpose of cofactor matrix):")
            adj = adjugate_3x3(key_mat)
            for r in adj:
                lines.append("  " + '  '.join(f"{v:4d}" for v in r))
            lines.append("")
            lines.append("Inverse matrix modulo 26 (inv_det * adjugate mod 26):")
            for r in inv_mat:
                lines.append("  " + '  '.join(f"{v:2d}" for v in r))
            lines.append("")
            lines.append("Contoh proses enkripsi satu block (ambil block 3 huruf):")
            # contoh blok: "ACT"
            example_plain = "ACT"
            vec = [ALPH.index(c) for c in example_plain]
            enc_vec = mat_mul_vec(key_mat, vec)
            enc_text = ''.join(ALPH[v] for v in enc_vec)
            lines.append(f"  Plain block: {example_plain} -> vector {vec}")
            lines.append(f"  Multiply by key matrix -> {enc_vec} -> Cipher block: {enc_text}")
            lines.append("")
            # contoh dekripsi
            dec_vec = mat_mul_vec(inv_mat, enc_vec)
            dec_text = ''.join(ALPH[v] for v in dec_vec)
            lines.append(f"  Untuk dekripsi: multiply oleh inverse matrix -> {dec_vec} -> Plain: {dec_text}")
            lines.append("")
            lines.append("Catatan: untuk teks asli non-huruf, Hill cipher tradisional mengabaikannya. Padding 'X' digunakan jika block kurang dari 3.")
        # tampilkan
        self.draw_detail_text.delete("1.0", tk.END)
        self.draw_detail_text.insert(tk.END, '\n'.join(lines))

    def on_drawback_kpa(self):
        # Logika KPA
        plain_text = sanitize_key_text(self.kpa_plain_entry.get())
        cipher_text = sanitize_key_text(self.kpa_cipher_entry.get())

        if len(plain_text) < 9 or len(cipher_text) < 9:
            messagebox.showerror("KPA Error", "Plaintext dan Ciphertext harus minimal 9 huruf (3 blok) dan hanya huruf A-Z.")
            return
        
        # Ambil 3 blok pertama
        P_blocks = [plain_text[i:i+3] for i in range(0, 9, 3)]
        C_blocks = [cipher_text[i:i+3] for i in range(0, 9, 3)]

        lines = []
        lines.append("== Hill Cipher 3x3 — Known Plaintext Attack (KPA) ==")
        lines.append("")
        lines.append(f"Known Plaintext (3 Blocks): {P_blocks}")
        lines.append(f"Known Ciphertext (3 Blocks): {C_blocks}")
        lines.append("")
        
        try:
            # Hitung K = C * P^-1 (mod 26)
            K_kpa, det_P, det_P_mod, inv_det_P = key_from_kpa(P_blocks, C_blocks)

            lines.append(f"Matriks Plaintext (P) (kolom adalah vektor P{P_blocks[0]}, P{P_blocks[1]}, P{P_blocks[2]}):")
            # Matriks P dalam format yang mudah dibaca
            P_cols = [[ALPH.index(c) for c in block] for block in P_blocks]
            P = [[P_cols[j][i] for j in range(3)] for i in range(3)]
            for r in P:
                lines.append("  " + '  '.join(f"{v:2d}" for v in r))

            lines.append(f"Matriks Ciphertext (C) (kolom adalah vektor C{C_blocks[0]}, C{C_blocks[1]}, C{C_blocks[2]}):")
            C_cols = [[ALPH.index(c) for c in block] for block in C_blocks]
            C = [[C_cols[j][i] for j in range(3)] for i in range(3)]
            for r in C:
                lines.append("  " + '  '.join(f"{v:2d}" for v in r))

            lines.append(f"Determinant P mod 26: {det_P_mod}")
            lines.append(f"Inverse Determinant P mod 26: {inv_det_P}")

            lines.append("")
            lines.append("Hasil Matriks Kunci (K = C * P^-1 mod 26):")
            for r in K_kpa:
                lines.append("  " + '  '.join(f"{v:2d}" for v in r))
            
            # Konversi Key Matrix ke Key Text (9 huruf)
            K_text = "".join(ALPH[val] for row in K_kpa for val in row)
            lines.append(f"Key Text yang Ditemukan: {K_text} (row-major)")

            # Bandingkan dengan Key yang diinput di tab ini
            manual_key_text = sanitize_key_text(self.draw_key_entry.get())[:9]
            if K_text == manual_key_text:
                 lines.append("\n✅ **Key yang ditemukan COCOK** dengan Key yang diinput!")
            else:
                 lines.append("\n❌ **Key yang ditemukan TIDAK COCOK** dengan Key yang diinput (periksa input KPA Anda).")
            
            lines.append("\nKESIMPULAN: Hill Cipher rentan terhadap Known Plaintext Attack (KPA) jika penyerang mengetahui 3 pasang blok Plaintext/Ciphertext.")

        except ValueError as e:
            lines.append(f"❌ KPA GAGAL: {str(e)}")
            lines.append("\nKESIMPULAN: KPA Gagal. Matriks Plaintext (P) harus invertible (det P harus coprime dengan 26).")
        
        self.draw_detail_text.delete("1.0", tk.END)
        self.draw_detail_text.insert(tk.END, '\n'.join(lines))


    # -------------------------
    # Utilities (Sudah ada)
    # -------------------------
    def _copy_text_widget(self, text_widget):
        txt = text_widget.get("1.0", tk.END).strip()
        if not txt:
            messagebox.showwarning("Peringatan", "Tidak ada teks untuk disalin.")
            return
        self.clipboard_clear()
        self.clipboard_append(txt)
        messagebox.showinfo("Copied", "Teks berhasil disalin ke clipboard.")

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app = HillCipherGUI()
    app.mainloop()