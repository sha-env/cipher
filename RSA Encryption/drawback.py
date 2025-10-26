# rsa_drawbacks_demo.py
# DEMO EDUKATIF: menunjukan drawback / kelemahan jika RSA diimplementasikan TIDAK BENAR.
# Hanya untuk pembelajaran — menggunakan bilangan sangat kecil sehingga mudah dipecahkan.
# JANGAN digunakan untuk menyerang / memecah kunci nyata.

import math
import random

# -----------------------
# Util dasar
# -----------------------
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_small_prime(bits=16):
    """Buat prime kecil (untuk demo). bits biasanya 16..32 (sangat kecil)."""
    while True:
        p = random.getrandbits(bits) | 1  # gen ganjil
        if is_prime(p):
            return p

def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    x1, y1, g = egcd(b, a % b)
    return (y1, x1 - (a // b) * y1, g)

def modinv(a, m):
    x, y, g = egcd(a, m)
    if g != 1:
        raise ValueError("Tidak ada modular inverse")
    return x % m

# -----------------------
# Simple textbook RSA (tanpa padding) — DEMO
# -----------------------
def generate_rsa_keypair_small(bits=16, e=65537):
    # Hanya untuk demo: prime kecil
    p = generate_small_prime(bits)
    q = generate_small_prime(bits)
    while q == p:
        q = generate_small_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    if math.gcd(e, phi) != 1:
        # pilih e kecil yang cocok
        e = 3
        if math.gcd(e, phi) != 1:
            raise ValueError("Gagal pilih e")
    d = modinv(e, phi)
    return {'p': p, 'q': q, 'n': n, 'e': e, 'd': d}

def rsa_encrypt_no_padding(m_int, pub):
    # ciphertext = m^e mod n
    return pow(m_int, pub['e'], pub['n'])

def rsa_decrypt_no_padding(c_int, priv):
    return pow(c_int, priv['d'], priv['n'])

# -----------------------
# Drawback demo 1: Deterministic
# -----------------------
def demo_deterministic(pub):
    print("\nDemo: deterministic (textbook RSA tanpa padding)")
    m = 42
    c1 = rsa_encrypt_no_padding(m, pub)
    c2 = rsa_encrypt_no_padding(m, pub)
    print("plaintext:", m)
    print("ciphertext 1:", c1)
    print("ciphertext 2:", c2)
    print("=> ciphertext identik tiap enkripsi: deterministik, memudahkan analisis/pola.")

# -----------------------
# Drawback demo 2: Faktor modulus kecil mudah ditemukan (trial division)
# -----------------------
def naive_factor(n):
    """Trial division — hanya layak untuk n kecil (demo)."""
    if n % 2 == 0:
        return 2, n // 2
    r = int(math.isqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return i, n // i
    return None

def demo_factoring(priv):
    n = priv['n']
    print("\nDemo: factoring modulus kecil (trial division) — bukan untuk kunci nyata")
    print("Modulus n:", n)
    fac = naive_factor(n)
    if fac:
        print("Ditemukan faktor:", fac)
        p, q = fac
        phi = (p - 1) * (q - 1)
        # hitung d dari e
        try:
            d_recovered = modinv(priv['e'], phi)
            print("Private exponent (recomputed):", d_recovered)
            if d_recovered == priv['d']:
                print("=> Berhasil recover private key dari faktorisasi (kunci kecil mudah dipecahkan).")
        except Exception as e:
            print("Gagal recompute d:", e)
    else:
        print("Tidak berhasil factor (n mungkin lebih besar dari demo).")

# -----------------------
# Drawback demo 3: Eksponen kecil (e=3) + pesan kecil -> bisa diambil akar integer
# -----------------------
def integer_nth_root(x, n):
    """Akar pangkat-n integer (floor)."""
    lo = 0
    hi = 1 << ((x.bit_length() + n - 1) // n)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** n < x:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo ** n == x else lo - 1

def demo_low_exponent(pub):
    print("\nDemo: low-exponent attack (e kecil, pesan kecil sehingga m^e < n)")
    e = pub['e']
    n = pub['n']
    # pilih m cukup kecil sehingga m^e < n
    # catatan: ini hanya demo; di dunia nyata, padding mencegah kondisi ini
    m = 2
    c = pow(m, e, n)
    # jika m^e < n, matematika: c = m^e (tidak modulus) sehingga kita bisa ambil e-root
    if pow(m, e) < n:
        print("m^e < n terpenuhi. kita bisa ambil akar e dari c tanpa perlu kunci.")
        recovered = integer_nth_root(pow(m, e), e)
        print("plaintext asli:", m, "recovered via integer root:", recovered)
        print("=> menunjukkan risiko eksponen kecil tanpa padding.")
    else:
        print("Kondisi m^e < n tidak terpenuhi dengan m kecil; coba gunakan modulus lebih besar atau e lebih kecil untuk demo.")

# -----------------------
# Interaktif & run demo
# -----------------------
def interactive_demo():
    print("RSA DRAWBACKS DEMO (EDUKASI) — menggunakan kunci SANGAT KECIL")
    print("1) Generate small RSA keypair (default 16-bit primes -> n ~ 32 bits)")
    print("2) Run all 3 demos on generated keypair")
    print("3) Exit")
    choice = input("Pilih (1/2/3): ").strip()
    if choice != '1':
        if choice == '3':
            return
        print("Pilih 1 dulu untuk generate key.")
        return

    bits = int(input("Masukkan bit size tiap prime (contoh 16..20 recommended untuk demo): ").strip() or "16")
    e_input = input("Masukkan e (default 65537): ").strip()
    e = int(e_input) if e_input else 65537
    priv = generate_rsa_keypair_small(bits=bits, e=e)
    pub = {'n': priv['n'], 'e': priv['e']}
    print("\nGenerated small keypair:")
    print("p =", priv['p'])
    print("q =", priv['q'])
    print("n =", priv['n'])
    print("e =", priv['e'])
    print("d =", priv['d'])

    # Run demos
    demo_deterministic(pub)
    demo_factoring(priv)
    demo_low_exponent(pub)
    print("\n=== Catatan Penting ===")
    print("- Demo ini menunjukan kelemahan jika RSA DIPAKAI SEMAU-NYA tanpa padding,\n  atau jika kunci terlalu kecil, atau jika e terlalu kecil dan pesan tidak dipadding.")
    print("- Di praktik aman: selalu gunakan padding OAEP untuk enkripsi, gunakan kunci yg cukup besar (>=2048 bit),\n  gunakan e yang aman (umumnya 65537), dan jangan implementasikan kriptografi sendiri tanpa library teruji.")
    print("- Jangan gunakan skrip ini untuk mencoba memecah kunci nyata. Ini untuk tujuan pembelajaran.")

if __name__ == "__main__":
    interactive_demo()
