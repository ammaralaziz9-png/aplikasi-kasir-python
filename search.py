
def cari_produk(katalog, kata_kunci):
    """
    Mencari produk berdasarkan kode atau nama barang.
    Mengembalikan dictionary produk yang cocok.
    """
    kata_kunci = kata_kunci.strip().lower()
    hasil = {}

    for kode, info in katalog.items():
        # Cek apakah kata kunci cocok dengan Kode atau Nama Produk
        if kata_kunci in kode.lower() or kata_kunci in info["nama"].lower():
            hasil[kode] = info

    return hasil

def tampilkan_hasil_pencarian(katalog):
    """
    Menampilkan interface pencarian di terminal.
    """
    print("\n--- FITUR PENCARIAN PRODUK ---")
    keyword = input("Masukkan nama atau kode barang yang dicari: ").strip()

    if not keyword:
        print("❌ Kata kunci pencarian tidak boleh kosong!")
        return

    hasil = cari_produk(katalog, keyword)

    if not hasil:
        print(f"🔍 Produk dengan kata kunci '{keyword}' tidak ditemukan.")
    else:
        print(f"\n🔍 Ditemukan {len(hasil)} produk yang cocok:")
        print("-" * 50)
        for kode, info in hasil.items():
            print(f"[{kode}] {info['nama']} - Rp {info['harga']:,} | Stok: {info['stok']}")
        print("-" * 50)