def enkripsi_scytale(pesan, kunci):
    pesan = pesan.replace(" ", "").upper()
    kolom = kunci
    baris = (len(pesan) + kolom - 1) // kolom
    grid = [['' for _ in range(kolom)] for _ in range(baris)]

    # isi grid baris per baris
    index = 0
    for i in range(baris):
        for j in range(kolom):
            if index < len(pesan):
                grid[i][j] = pesan[index]
                index += 1

    # baca kolom per kolom untuk hasil enkripsi
    hasil = ''
    for j in range(kolom):
        for i in range(baris):
            hasil += grid[i][j]
    return hasil


def dekripsi_scytale(teks, kunci):
    kolom = kunci
    baris = (len(teks) + kolom - 1) // kolom
    grid = [['' for _ in range(kolom)] for _ in range(baris)]

    # isi grid kolom per kolom
    index = 0
    for j in range(kolom):
        for i in range(baris):
            if index < len(teks):
                grid[i][j] = teks[index]
                index += 1

    # baca baris per baris untuk hasil dekripsi
    hasil = ''
    for i in range(baris):
        for j in range(kolom):
            hasil += grid[i][j]
    return hasil


# === Program utama ===
print("=== Program Enkripsi & Dekripsi Scytale Cipher ===")

# input dari pengguna
pesan_asli = input("Masukkan pesan asli : ")
kunci = int(input("Masukkan kunci (jumlah kolom) : "))

# proses enkripsi dan dekripsi
terenkripsi = enkripsi_scytale(pesan_asli, kunci)
terdekripsi = dekripsi_scytale(terenkripsi, kunci)

# hasil
print("\nHasil:")
print("Pesan asli     :", pesan_asli)
print("Terenkripsi    :", terenkripsi)
print("Terdekripsi    :", terdekripsi)