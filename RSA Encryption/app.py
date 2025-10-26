# rsa_interactive.py
# Interaktif RSA demo: generate keypair, encrypt, decrypt, save/load PEM
# Requires: pip install cryptography

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
import base64
import sys
import os

def generate_keys(key_size=2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_private_key_pem(private_key, filename, password=None):
    if password:
        encryption = serialization.BestAvailableEncryption(password.encode())
    else:
        encryption = serialization.NoEncryption()
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption
    )
    with open(filename, "wb") as f:
        f.write(pem)

def save_public_key_pem(public_key, filename):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, "wb") as f:
        f.write(pem)

def load_private_key_pem(filename, password=None):
    with open(filename, "rb") as f:
        data = f.read()
    return serialization.load_pem_private_key(data, password=(password.encode() if password else None))

def load_public_key_pem(filename):
    with open(filename, "rb") as f:
        data = f.read()
    return serialization.load_pem_public_key(data)

def rsa_encrypt(public_key, plaintext_bytes):
    # OAEP with MGF1 + SHA256
    ciphertext = public_key.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # return base64 for safe printing/storage
    return base64.b64encode(ciphertext).decode()

def rsa_decrypt(private_key, b64_ciphertext):
    ciphertext = base64.b64decode(b64_ciphertext)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8', errors='replace')

def show_menu():
    print("\n=== RSA Interactive ===")
    print("1) Generate keypair (2048 bits default)")
    print("2) Save keys to PEM files")
    print("3) Load private key from PEM")
    print("4) Load public key from PEM")
    print("5) Show current public key (PEM)")
    print("6) Encrypt plaintext (with loaded/generated public key)")
    print("7) Decrypt ciphertext (base64) (with loaded/generated private key)")
    print("8) Exit")

def main():
    private_key = None
    public_key = None

    while True:
        show_menu()
        choice = input("Pilih (1-8): ").strip()
        if choice == '1':
            try:
                ks = int(input("Key size (bits, rekomendasi 2048 atau 3072): ").strip() or "2048")
            except ValueError:
                ks = 2048
            print("Generating keys... (ini mungkin butuh beberapa detik)")
            private_key, public_key = generate_keys(ks)
            print("Keypair generated. (private & public tersimpan di memori untuk sesi ini)")

        elif choice == '2':
            if not private_key or not public_key:
                print("Belum ada keypair. Generate dulu (pilihan 1) atau load dari PEM.")
                continue
            priv_file = input("Nama file private PEM (default: private_key.pem): ").strip() or "private_key.pem"
            pub_file = input("Nama file public PEM (default: public_key.pem): ").strip() or "public_key.pem"
            pw = input("Password untuk private key (kosong = tidak terenkripsi): ")
            try:
                save_private_key_pem(private_key, priv_file, password=pw if pw else None)
                save_public_key_pem(public_key, pub_file)
                print(f"Saved private -> {priv_file} (encrypted={'yes' if pw else 'no'}), public -> {pub_file}")
            except Exception as e:
                print("Gagal menyimpan key:", e)

        elif choice == '3':
            fname = input("Path file private PEM: ").strip()
            if not os.path.exists(fname):
                print("File tidak ditemukan.")
                continue
            pw = input("Password private key (kosong jika tidak ada): ")
            try:
                private_key = load_private_key_pem(fname, password=pw if pw else None)
                public_key = private_key.public_key()
                print("Private key loaded. Public key juga di-set dari private.")
            except Exception as e:
                print("Gagal load private key:", e)

        elif choice == '4':
            fname = input("Path file public PEM: ").strip()
            if not os.path.exists(fname):
                print("File tidak ditemukan.")
                continue
            try:
                public_key = load_public_key_pem(fname)
                print("Public key loaded.")
            except Exception as e:
                print("Gagal load public key:", e)

        elif choice == '5':
            if not public_key:
                print("Belum ada public key (generate atau load dulu).")
                continue
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            print("\n=== Public Key PEM ===")
            print(pem.decode())

        elif choice == '6':
            if not public_key:
                print("Public key belum tersedia. Generate atau load public key dulu.")
                continue
            text = input("Masukkan plaintext (akan di-UTF8): ")
            # RSA OAEP hanya bisa enkripsi sampai ukuran tertentu tergantung key. Untuk pesan panjang sebaiknya gunakan hybrid encryption.
            # Di sini hanya untuk teks relatif pendek.
            try:
                ciphertext_b64 = rsa_encrypt(public_key, text.encode('utf-8'))
                print("\n=== Ciphertext (base64) ===")
                print(ciphertext_b64)
                print("\n(Simpan ciphertext base64 untuk didekripsi nanti.)")
            except Exception as e:
                print("Gagal enkripsi (mungkin pesan terlalu panjang untuk RSA OAEP). Error:", e)
                print("Saran: untuk pesan panjang, gunakan hybrid encryption (generate AES key, enkripsi data dengan AES, lalu enkripsi AES key dengan RSA).")

        elif choice == '7':
            if not private_key:
                print("Private key belum tersedia. Generate atau load private key dulu.")
                continue
            b64 = input("Masukkan ciphertext (base64): ").strip()
            try:
                plaintext = rsa_decrypt(private_key, b64)
                print("\n=== Decrypted plaintext ===")
                print(plaintext)
            except Exception as e:
                print("Gagal dekripsi. Error:", e)
                print("Pastikan ciphertext cocok dengan public key yang digunakan untuk enkripsi.")

        elif choice == '8':
            print("Keluar. Bye!")
            sys.exit(0)

        else:
            print("Pilihan tidak valid. Coba lagi.")

if __name__ == "__main__":
    main()
