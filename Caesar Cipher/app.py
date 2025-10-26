# Caesar Cipher interaktif

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result


def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)


if __name__ == "__main__":
    print("=== Caesar Cipher ===")
    choice = input("Pilih mode (e = enkripsi, d = dekripsi): ").lower()
    text = input("Masukkan teks: ")
    shift = int(input("Masukkan shift (angka 1–25): "))

    if choice == "e":
        encrypted = caesar_encrypt(text, shift)
        print("Hasil enkripsi: ", encrypted)
    elif choice == "d":
        decrypted = caesar_decrypt(text, shift)
        print("Hasil dekripsi: ", decrypted)
    else:
        print("Pilihan tidak valid.")
