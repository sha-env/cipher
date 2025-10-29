# Caesar Cipher - Enkripsi

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result


if __name__ == "__main__":
    print("=== Caesar Cipher - Enkripsi ===")
    text = input("Masukkan teks yang akan dienkripsi: ")
    shift = int(input("Masukkan shift (angka 1–25): "))

    encrypted = caesar_encrypt(text, shift)
    print("Hasil enkripsi:", encrypted)
