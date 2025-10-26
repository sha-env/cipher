# ==========================================================
# Program Enkripsi Hill Cipher (3x3)
# Mengikuti standar internasional: A=0, B=1, ..., Z=25
# Plaintext: INTERNATIONALCIPHER
# Key Matrix (K):
# [ [6, 24, 1],
#   [13, 16, 10],
#   [20, 17, 15] ]
# ==========================================================

import numpy as np

# ----------------------------------------------------------
# Fungsi untuk mengubah huruf menjadi angka (A=0, ..., Z=25)
# ----------------------------------------------------------
def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text]

# ----------------------------------------------------------
# Fungsi untuk mengubah angka kembali ke huruf (0=A, ..., 25=Z)
# ----------------------------------------------------------
def numbers_to_text(numbers):
    return ''.join(chr(num + ord('A')) for num in numbers)

# ----------------------------------------------------------
# Fungsi utama untuk enkripsi Hill Cipher
# ----------------------------------------------------------
def hill_encrypt(plaintext, key_matrix):
    # Hapus spasi dan ubah ke huruf besar
    plaintext = plaintext.replace(" ", "").upper()
    
    # Pastikan panjang plaintext kelipatan 3 (karena key 3x3)
    while len(plaintext) % 3 != 0:
        plaintext += 'X'  # tambahkan huruf 'X' sebagai padding jika perlu

    # Ubah plaintext ke angka
    plaintext_numbers = text_to_numbers(plaintext)

    ciphertext_numbers = []

    # Enkripsi per blok 3 huruf (3 angka)
    for i in range(0, len(plaintext_numbers), 3):
        block = np.array(plaintext_numbers[i:i+3])
        # Perkalian matriks (mod 26)
        encrypted_block = np.dot(key_matrix, block) % 26
        ciphertext_numbers.extend(encrypted_block)

    # Ubah kembali hasil enkripsi ke huruf
    ciphertext = numbers_to_text(ciphertext_numbers)
    return ciphertext

# ----------------------------------------------------------
# Bagian utama program
# ----------------------------------------------------------

# Definisikan key matrix (sesuai contoh internasional)
key_matrix = np.array([
    [6, 24, 1],
    [13, 16, 10],
    [20, 17, 15]
])

# Plaintext (hardcoded)
plaintext = "INTERNATIONALCIPHER"

# Jalankan enkripsi
ciphertext = hill_encrypt(plaintext, key_matrix)

# Tampilkan hasil
print("Plaintext  :", plaintext)
print("Ciphertext :", ciphertext)
