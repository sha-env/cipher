# Caesar Cipher - Dekripsi

def caesar_decrypt(ciphertext, shift):
    result = ""
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result


if __name__ == "__main__":
    print("=== Caesar Cipher - Dekripsi ===")
    ciphertext = input("Masukkan teks yang akan didekripsi: ")
    shift = int(input("Masukkan shift (angka 1–25): "))

    decrypted = caesar_decrypt(ciphertext, shift)
    print("Hasil dekripsi:", decrypted)
