# Vigenere Cipher - Enkripsi & Dekripsi

def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper().replace(" ", "")
    key = key.upper()
    ciphertext = ""
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('A')
            encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            ciphertext += encrypted_char
            key_index = (key_index + 1) % len(key)
        else:
            ciphertext += char
    return ciphertext


def vigenere_decrypt(ciphertext, key):
    ciphertext = ciphertext.upper().replace(" ", "")
    key = key.upper()
    plaintext = ""
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('A')
            decrypted_char = chr(((ord(char) - ord('A') - shift + 26) % 26) + ord('A'))
            plaintext += decrypted_char
            key_index = (key_index + 1) % len(key)
        else:
            plaintext += char
    return plaintext


# ===== MAIN PROGRAM =====
print("=== Vigenere Cipher ===")
choice = input("Pilih mode (E untuk Enkripsi / D untuk Dekripsi): ").strip().upper()

text = input("Masukkan teks: ")
key = input("Masukkan kunci: ")

if choice == "E":
    encrypted = vigenere_encrypt(text, key)
    print("Hasil Enkripsi:", encrypted)
elif choice == "D":
    decrypted = vigenere_decrypt(text, key)
    print("Hasil Dekripsi:", decrypted)
else:
    print("Pilihan tidak valid!")