def scytale_encrypt(text, diameter):
    # hilangkan spasi biar lebih klasik (opsional)
    text = text.replace(" ", "")
    # panjang pesan
    length = len(text)
    # jumlah baris
    rows = (length + diameter - 1) // diameter  
    
    # isi matriks dengan karakter
    matrix = [['' for _ in range(diameter)] for _ in range(rows)]
    index = 0
    for r in range(rows):
        for c in range(diameter):
            if index < length:
                matrix[r][c] = text[index]
                index += 1
    
    # baca per kolom untuk hasil cipher
    encrypted = ''.join(matrix[r][c] for c in range(diameter) for r in range(rows) if matrix[r][c] != '')
    return encrypted


def scytale_decrypt(ciphertext, diameter):
    length = len(ciphertext)
    rows = (length + diameter - 1) // diameter
    
    # jumlah karakter per kolom
    full_cols = length % diameter
    if full_cols == 0:
        full_cols = diameter
    
    matrix = [['' for _ in range(diameter)] for _ in range(rows)]
    
    index = 0
    for c in range(diameter):
        for r in range(rows):
            if (c < full_cols and r < rows) or (c >= full_cols and r < rows - 1):
                if index < length:
                    matrix[r][c] = ciphertext[index]
                    index += 1
    
    # baca baris demi baris
    decrypted = ''.join(matrix[r][c] for r in range(rows) for c in range(diameter) if matrix[r][c] != '')
    return decrypted


# --- Contoh penggunaan ---
plain_text = input("Masukkan teks: ")
diameter = int(input("Masukkan diameter (jumlah kolom): "))

encrypted = scytale_encrypt(plain_text, diameter)
print("Hasil enkripsi :", encrypted)

decrypted = scytale_decrypt(encrypted, diameter)
print("Hasil dekripsi :", decrypted)
