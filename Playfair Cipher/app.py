# ==========================================================
# PLAYFAIR CIPHER ENCRYPTION - International Standard Version
# Key: "TEKNIK INFORMATIKA"
# Author: Yansha
# ==========================================================

import string

# ---------------------------
# 1. Generate Key Matrix 5x5
# ---------------------------
def generate_key_matrix(key):
    # Ubah ke huruf besar dan ganti J dengan I
    key = key.upper().replace("J", "I")

    # Hapus karakter non-huruf dan duplikasi
    filtered_key = ""
    for char in key:
        if char in string.ascii_uppercase and char not in filtered_key:
            filtered_key += char

    # Tambahkan huruf A-Z kecuali J
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # Tanpa J
        if char not in filtered_key:
            filtered_key += char

    # Bentuk matriks 5x5
    matrix = [list(filtered_key[i:i+5]) for i in range(0, 25, 5)]
    return matrix


# ---------------------------
# 2. Menampilkan Matriks Kunci
# ---------------------------
def print_key_matrix(matrix):
    print("\n=== MATRKS KUNCI 5x5 ===")
    for row in matrix:
        print(" ".join(row))
    print("=========================")


# ---------------------------
# 3. Persiapkan Plaintext
# ---------------------------
def prepare_text(text):
    # Ubah ke uppercase, ganti J dengan I, dan hapus non-huruf
    text = text.upper().replace("J", "I")
    text = "".join([c for c in text if c in string.ascii_uppercase])

    # Bentuk pasangan huruf (digraf)
    digraphs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                # Jika dua huruf sama, sisipkan X
                digraphs.append(a + "X")
                i += 1
            else:
                digraphs.append(a + b)
                i += 2
        else:
            # Jika ganjil, tambahkan X di akhir
            digraphs.append(a + "X")
            i += 1
    return digraphs


# ---------------------------
# 4. Cari posisi huruf di matriks
# ---------------------------
def find_position(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None


# ---------------------------
# 5. Enkripsi per pasangan huruf
# ---------------------------
def encrypt_pair(pair, matrix):
    a, b = pair
    row_a, col_a = find_position(matrix, a)
    row_b, col_b = find_position(matrix, b)

    # Aturan Playfair Cipher:
    if row_a == row_b:
        # Jika di baris sama → geser kanan
        return matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
    elif col_a == col_b:
        # Jika di kolom sama → geser bawah
        return matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
    else:
        # Jika berbeda → bentuk persegi dan ambil huruf silang
        return matrix[row_a][col_b] + matrix[row_b][col_a]


# ---------------------------
# 6. Enkripsi seluruh plaintext
# ---------------------------
def encrypt_playfair(plaintext, key):
    matrix = generate_key_matrix(key)
    print_key_matrix(matrix)

    words = plaintext.upper().split()
    ciphertext_words = []

    print("\n=== PROSES ENKRIPSI ===")
    for word in words:
        digraphs = prepare_text(word)
        print(f"\nKata Asli   : {word}")
        print(f"Digraf      : {digraphs}")

        encrypted = [encrypt_pair(pair, matrix) for pair in digraphs]
        encrypted_word = "".join(encrypted)
        print(f"Hasil Enkrip: {encrypted_word}")
        ciphertext_words.append(encrypted_word)

    final_ciphertext = " ".join(ciphertext_words)
    print("\n=== HASIL AKHIR ENKRIPSI ===")
    print(final_ciphertext)
    print("===============================")
    return final_ciphertext


# ==========================================================
# 7. Main Program
# ==========================================================
if __name__ == "__main__":
    key = "TEKNIK INFORMATIKA"
    plaintexts = [
        "GOOD BROOM SWEEP CLEAN",
        "REDWOOD NATIONAL STATE PARK",
        "JUNK FOOD AND HEALTH PROBLEMS"
    ]

    for text in plaintexts:
        print(f"\n\n##### ENKRIPSI: {text} #####")
        encrypt_playfair(text, key)