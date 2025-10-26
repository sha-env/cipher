# caesar_demo_crack.py
# Demonstrasi: enkripsi/dekripsi Caesar cipher + cara membongkarnya
# (interaktif, edukatif)

import string
from collections import Counter

ALPH_LO = string.ascii_lowercase
ALPH_UP = string.ascii_uppercase

# Frekuensi huruf bahasa Inggris (digunakan untuk scoring dalam frequency analysis).
# Untuk bahasa lain (mis. Indonesia) sebaiknya ganti dengan distribusi huruf yang sesuai.
EN_FREQ = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074
}

def caesar_shift_char(c, shift):
    if c.islower():
        return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
    if c.isupper():
        return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
    return c

def caesar_encrypt(text, shift):
    return ''.join(caesar_shift_char(c, shift) for c in text)

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def brute_force_crack(ciphertext):
    """Coba semua kemungkinan shift (1..25) dan kembalikan daftar (shift, candidate)."""
    candidates = []
    for s in range(1, 26):
        cand = caesar_decrypt(ciphertext, s)
        candidates.append((s, cand))
    return candidates

def score_text_by_frequency(text, freq_table=EN_FREQ):
    """
    Beri skor berdasarkan seberapa mirip frekuensi huruf pada text terhadap freq_table.
    Skor lebih kecil = lebih mirip (menggunakan chi-squared like measure).
    """
    # hitung frekuensi huruf a-z pada text (abaikan non-huruf)
    text_lower = [c for c in text.lower() if c.isalpha()]
    if not text_lower:
        return float('inf')
    counts = Counter(text_lower)
    total = sum(counts.values())
    score = 0.0
    for ch in string.ascii_lowercase:
        observed = counts.get(ch, 0)
        expected = freq_table.get(ch, 0) * total / 100.0
        # gunakan (O - E)^2 / E, tapi jaga agar E tidak 0
        if expected > 0:
            score += (observed - expected) ** 2 / expected
    return score

def frequency_analysis_crack(ciphertext):
    """
    Coba semua shift, nilai tiap kandidat menggunakan frequency scoring,
    lalu kembalikan kandidat terbaik (shift, plaintext, score) yang berpotensi jadi pesan asli.
    """
    candidates = []
    for s in range(0, 26):
        cand = caesar_decrypt(ciphertext, s)
        sc = score_text_by_frequency(cand)
        candidates.append((s, cand, sc))
    # urutkan berdasarkan score (kecil lebih baik)
    candidates.sort(key=lambda x: x[2])
    return candidates

def interactive():
    print("=== Caesar Cipher Demo & Crack ===")
    print("Pilihan:")
    print(" 1. Enkripsi")
    print(" 2. Dekripsi")
    print(" 3. Brute-force crack (tampilkan semua 25 kandidat)")
    print(" 4. Frequency-analysis crack (tampilkan kandidat teratas)")
    print(" 5. Contoh demonstrasi (auto-run)")
    choice = input("Pilih (1/2/3/4/5): ").strip()

    if choice == '1':
        txt = input("Masukkan plaintext: ")
        s = int(input("Masukkan shift (1-25): "))
        print("Encrypted:", caesar_encrypt(txt, s))

    elif choice == '2':
        txt = input("Masukkan ciphertext: ")
        s = int(input("Masukkan shift (1-25): "))
        print("Decrypted:", caesar_decrypt(txt, s))

    elif choice == '3':
        txt = input("Masukkan ciphertext: ")
        print("\nHasil brute-force (shift, plaintext):")
        for s, cand in brute_force_crack(txt):
            print(f"{s:2d} -> {cand}")

    elif choice == '4':
        txt = input("Masukkan ciphertext: ")
        candidates = frequency_analysis_crack(txt)
        print("\nTop 5 kandidat menurut frequency analysis:")
        for s, cand, sc in candidates[:5]:
            print(f"shift={s:2d} score={sc:8.3f} -> {cand}")

        print("\n(Perlu diperhatikan: scoring memakai distribusi huruf bahasa Inggris.")
        print(" Untuk teks bahasa Indonesia, ganti tabel frekuensi supaya hasil lebih akurat.)")

    elif choice == '5':
        # demo singkat
        sample = "ini adalah pesan rahasia yang akan diuji"
        shift = 7
        cipher = caesar_encrypt(sample, shift)
        print("Plaintext sample :", sample)
        print("Encrypted sample :", cipher)
        print("\nBrute-force candidates (potongan):")
        for s, cand in brute_force_crack(cipher)[:8]:
            print(f"{s:2d} -> {cand}")
        print("\nFrequency analysis top candidate:")
        best = frequency_analysis_crack(cipher)[0]
        print(f"shift={best[0]} score={best[2]:.3f} -> {best[1]}")

    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    interactive()
