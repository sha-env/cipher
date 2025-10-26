# ==========================================================
# Program Dekripsi Hill Cipher (3x3)
# Menggunakan key matrix yang sama seperti proses enkripsi
# ==========================================================

import numpy as np

# ----------------------------------------------------------
# Fungsi bantu: huruf <-> angka
# ----------------------------------------------------------
def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text]

def numbers_to_text(numbers):
    return ''.join(chr(num + ord('A')) for num in numbers)

# ----------------------------------------------------------
# Fungsi untuk menghitung invers modulo 26 dari determinan
# ----------------------------------------------------------
def mod_inverse(a, m):
    # Cari invers modular dari a (mod m)
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Tidak ada invers modulo yang valid untuk determinan ini.")

# ----------------------------------------------------------
# Fungsi untuk menghitung invers matriks (mod 26)
# ----------------------------------------------------------
def matrix_mod_inverse(matrix, modulus):
    det = int(round(np.linalg.det(matrix)))  # determinan
    det_mod = det % modulus

    # Cari invers dari determinan di mod 26
    det_inv = mod_inverse(det_mod, modulus)

    # Hitung adjoin (adjugate matrix)
    matrix_mod_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int)
    ) % modulus

    return matrix_mod_inv.astype(int)

# ----------------------------------------------------------
# Fungsi utama dekripsi Hill Cipher
# ----------------------------------------------------------
def hill_decrypt(ciphertext, key_matrix):
    ciphertext = ciphertext.replace(" ", "").upper()
    ciphertext_numbers = text_to_numbers(ciphertext)
    decrypted_numbers = []

    # Hitung invers dari key_matrix (mod 26)
    key_inverse = matrix_mod_inverse(key_matrix, 26)

    # Proses per blok 3 huruf
    for i in range(0, len(ciphertext_numbers), 3):
        block = np.array(ciphertext_numbers[i:i+3])
        decrypted_block = np.dot(key_inverse, block) % 26
        decrypted_numbers.extend(decrypted_block)

    plaintext = numbers_to_text(decrypted_numbers)
    return plaintext

# ----------------------------------------------------------
# Bagian utama program
# ----------------------------------------------------------

key_matrix = np.array([
    [6, 24, 1],
    [13, 16, 10],
    [20, 17, 15]
])

# Ciphertext hasil enkripsi dari program sebelumnya
ciphertext = "TBD"  # Ganti nanti dengan hasil nyata dari program enkripsi

# Jalankan dekripsi
plaintext_decrypted = hill_decrypt(ciphertext, key_matrix)

print("Ciphertext :", ciphertext)
print("Dekripsi   :", plaintext_decrypted)
