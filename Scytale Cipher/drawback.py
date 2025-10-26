import math
import re
from collections import Counter

def scytale_decrypt(ciphertext, diameter):
    """Dekripsi scytale: kita asumsikan enkripsi menulis row-wise lalu membaca col-wise.
       Untuk dekripsi kita mengisi kolom pertama ke kolom terakhir dengan jumlah baris yang sesuai.
    """
    ciphertext = ciphertext.replace(" ", "")
    L = len(ciphertext)
    # jumlah baris ketika membungkus pada diameter kolom
    rows = math.ceil(L / diameter)
    # hitung berapa kolom penuh (karena tidak selalu terisi rata)
    full_cols = L % diameter
    if full_cols == 0:
        full_cols = diameter

    # siapkan matriks kosong rows x diameter
    matrix = [[''] * diameter for _ in range(rows)]
    idx = 0
    for c in range(diameter):
        col_height = rows if c < full_cols else rows - 1
        for r in range(col_height):
            if idx < L:
                matrix[r][c] = ciphertext[idx]
                idx += 1

    # baca baris demi baris -> plaintext kandidat
    plaintext = ''.join(matrix[r][c] for r in range(rows) for c in range(diameter) if matrix[r][c] != '')
    return plaintext

# List kata umum (gabungan Bahasa Inggris + Bahasa Indonesia singkat)
COMMON_WORDS = [
    "the","and","that","is","in","to","of","a","for","on","with","as","it",
    "this","you","not","be","by","are","from",
    "yang","dan","untuk","di","dengan","ke","adalah","pada","atau","itu","saya","kamu"
]

def score_candidate(text):
    """Heuristik sederhana:
       - jumlah kata umum yang muncul (lebih baik)
       - rasio huruf vokal terhadap total (bahasa alami cenderung punya banyak vokal)
       - penalti kalau banyak karakter non-alfabet
    """
    # normalisasi: lowercase, pisahkan kata (anggap spasi mungkin hilang; coba temukan kata umum sebagai substring)
    t = text.lower()
    # hitung kemunculan kata umum sebagai substring (bukan hanya kata terpisah)
    common_hits = sum(t.count(w) for w in COMMON_WORDS)
    # vowel ratio
    letters = re.findall(r'[a-z]', t)
    if not letters:
        vowel_ratio = 0.0
    else:
        vowels = sum(1 for ch in letters if ch in "aeiou")
        vowel_ratio = vowels / len(letters)
    # penalti karakter non-alfabet
    non_alpha = len(re.findall(r'[^a-z0-9 ]', text.lower()))
    # skor komposit (bobot bisa diatur)
    score = common_hits * 3 + vowel_ratio * 2 - non_alpha * 0.5
    return score

def brute_force_scytale(ciphertext, max_diameter=None, show_all=False):
    ciphertext = ciphertext.strip()
    L = len(ciphertext.replace(" ", ""))
    if max_diameter is None or max_diameter > L:
        max_diameter = L
    results = []
    for d in range(2, max_diameter + 1):
        cand = scytale_decrypt(ciphertext, d)
        s = score_candidate(cand)
        results.append( (s, d, cand) )
    # urutkan berdasarkan skor tertinggi
    results.sort(reverse=True, key=lambda x: x[0])
    if show_all:
        return results
    else:
        # kembalikan top 10 (atau semua kalau sedikit)
        return results[:min(10, len(results))]

# --- Contoh penggunaan ---
if __name__ == "__main__":
    ct = input("Masukkan ciphertext: ").strip()
    top = brute_force_scytale(ct)
    print("\nKandidat teratas (skor, diameter, plaintext):\n")
    for s, d, p in top:
        # tampilkan sedikit pemformatan supaya mudah dibaca
        snippet = p if len(p) <= 200 else p[:200] + "..."
        print(f"[skor={s:.3f}] diameter={d} => {snippet}")
    print("\nJika tidak menemukan yang benar, coba jalankan dengan show_all=True atau naikkan max_diameter.")
