# Drawback Vigenere Cipher (menebak panjang kunci)

from collections import Counter
import re

def kasiski_examination(ciphertext, n=3):
    """
    Cari pola substring berulang (default panjang 3 huruf)
    untuk menebak panjang kunci.
    """
    ciphertext = ciphertext.upper().replace(" ", "")
    seq_positions = {}

    for i in range(len(ciphertext) - n):
        seq = ciphertext[i:i+n]
        if seq in seq_positions:
            seq_positions[seq].append(i)
        else:
            seq_positions[seq] = [i]

    # Hanya ambil pola yang muncul lebih dari sekali
    repeated = {seq: pos for seq, pos in seq_positions.items() if len(pos) > 1}

    return repeated


def get_distances(repeated):
    """Hitung jarak antar kemunculan pola"""
    distances = []
    for seq, positions in repeated.items():
        for i in range(len(positions) - 1):
            distance = positions[i+1] - positions[i]
            distances.append(distance)
    return distances


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def guess_key_length(ciphertext):
    repeated = kasiski_examination(ciphertext)
    if not repeated:
        return None

    distances = get_distances(repeated)
    if not distances:
        return None

    # Cari GCD dari semua jarak
    key_length = distances[0]
    for d in distances[1:]:
        key_length = gcd(key_length, d)
    return key_length


# ===== MAIN PROGRAM =====
ciphertext = input("Masukkan ciphertext: ")
predicted_length = guess_key_length(ciphertext)

if predicted_length:
    print(f"Perkiraan panjang kunci adalah: {predicted_length}")
else:
    print("Tidak ditemukan pola perulangan yang cukup untuk menebak panjang kunci.")
