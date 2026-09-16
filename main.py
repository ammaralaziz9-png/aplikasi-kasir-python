from data_produk import katalog_produk as katalog_default, database_member as member_default
from storage import (
    ambil_riwayat, 
    simpan_riwayat, 
    muat_katalog, 
    simpan_katalog, 
    muat_member, 
    simpan_member
)
from struk import cetak_struk
from search import tampilkan_hasil_pencarian

def jalankan_kasir():
    katalog_produk = muat_katalog(katalog_default)
    database_member = muat_member(member_default)
    
    keranjang = []

    while True:
        print("\n=== APLIKASI KASIR MODULAR (DAY 31) ===")
        print("1. Lihat Katalog & Stok Produk")
        print("2. Cari Produk (Search)") 
        print("3. Tambah Barang ke Keranjang")
        print("4. Lihat Keranjang Belanja")
        print("5. Checkout & Pembayaran (Diskon, Multi-Metode & Struk)")
        print("6. Lihat Riwayat & Rekap Omset")
        print("7. Restock / Tambah Stok Produk")
        print("8. Tambah Produk Baru ke Katalog")
        print("9. Registrasi Member Baru")
        print("10. Keluar")                          
        
        pilihan_input = input("Pilih menu (1-10): ").strip()
        
        if not pilihan_input.isdigit():
            print("❌ Masukan tidak valid! Mohon masukkan angka 1 sampai 10.")
            continue
            
        pilihan = int(pilihan_input)
            
        if pilihan == 1:
            print("\n--- KATALOG PRODUK, HARGA & STOK ---")
            for kode, info in katalog_produk.items():
                print(f"[{kode}] {info['nama']} - Rp {info['harga']:,} | Stok: {info['stok']}")
                
        elif pilihan == 2:
            
            tampilkan_hasil_pencarian(katalog_produk)
                
        elif pilihan == 3:
            print("\n--- PILIH PRODUK UNTUK KERANJANG ---")
            for kode, info in katalog_produk.items():
                print(f"[{kode}] {info['nama']} (Rp {info['harga']:,}) - Sisa Stok: {info['stok']}")
                
            kode_pilih = input("Masukkan kode barang: ").strip().upper()
            if kode_pilih in katalog_produk:
                qty_input = input("Masukkan jumlah (qty): ").strip()
                if not qty_input.isdigit():
                    print("❌ Jumlah harus berupa angka yang valid!")
                    continue
                qty = int(qty_input)
                
                if qty <= 0:
                    print("❌ Jumlah harus lebih dari 0!")
                    continue
                
                stok_tersedia = katalog_produk[kode_pilih]["stok"]
                if qty > stok_tersedia:
                    print(f"❌ Stok tidak cukup! Sisa stok untuk barang ini tinggal {stok_tersedia}.")
                    continue
                    
                barang = katalog_produk[kode_pilih]
                subtotal = barang["harga"] * qty
                
                sudah_ada = False
                for item in keranjang:
                    if item["nama"] == barang["nama"]:
                        if (item["qty"] + qty) > stok_tersedia:
                            print(f"❌ Total di keranjang melebihi sisa stok ({stok_tersedia})!")
                            sudah_ada = True
                            break
                        item["qty"] += qty
                        item["subtotal"] = item["qty"] * barang["harga"]
                        sudah_ada = True
                        break
                
                if not sudah_ada:
                    keranjang.append({
                        "nama": barang["nama"],
                        "harga_satuan": barang["harga"],
                        "qty": qty,
                        "subtotal": subtotal
                    })
                    
                print(f"✅ {qty} {barang['nama']} berhasil dimasukkan ke keranjang!")
            else:
                print("❌ Kode barang tidak ditemukan dalam katalog.")
                
        elif pilihan == 4:
            print("\n--- DAFTAR KERANJANG BELANJA ---")
            if not keranjang:
                print("🛒 Keranjang belanja masih kosong.")
            else:
                total_sementara = 0
                for idx, item in enumerate(keranjang, start=1):
                    print(f"{idx}. {item['nama']} x{item['qty']} - Rp {item['subtotal']:,}")
                    total_sementara += item["subtotal"]
                print(f"Total Sementara: Rp {total_sementara:,}")
                
        elif pilihan == 5:
            if not keranjang:
                print("⚠️ Keranjang kosong! Tidak bisa melakukan checkout.")
                continue
                
            total_kotor = sum(item["subtotal"] for item in keranjang)
            print(f"\nTotal Belanja: Rp {total_kotor:,}")
            
            punya_member = input("Apakah punya kartu member? (y/n): ").strip().lower()
            diskon = 0
            status_member = "Non-Member"
            
            if punya_member == 'y':
                id_member = input("Masukkan ID Member: ").strip().upper()
                if id_member in database_member:
                    diskon = total_kotor * 0.10
                    status_member = f"Member ({id_member})"
                    print("🎉 Selamat! Anda mendapatkan diskon member sebesar 10%.")
                else:
                    print("❌ ID Member tidak valid. Tidak ada diskon yang diterapkan.")
            
            total_bersih = int(total_kotor - diskon)
            print(f"Total yang harus dibayar: Rp {total_bersih:,}")
            
            print("\n--- PILIH METODE PEMBAYARAN ---")
            print("1. Tunai (Cash)")
            print("2. QRIS (QR Code)")
            print("3. Transfer Bank")
            print("4. Kartu Debit / Kredit")
            
            metode_input = input("Pilih metode pembayaran (1-4): ").strip()
            if not metode_input.isdigit():
                print("❌ Pilihan tidak valid. Transaksi dibatalkan.")
                continue
            metode_pilih = int(metode_input)
                
            metode_str = "Tunai"
            
            if metode_pilih == 1:
                metode_str = "Tunai"
                bayar_input = input("Masukkan uang pembayaran: Rp ").strip()
                if not bayar_input.isdigit():
                    print("❌ Format uang salah. Transaksi dibatalkan.")
                    continue
                bayar = int(bayar_input)
                    
                if bayar < total_bersih:
                    print("❌ Uang pembayaran kurang! Transaksi dibatalkan.")
                    continue
                else:
                    kembalian = bayar - total_bersih
                    print(f"✅ Pembayaran Tunai sukses! Uang kembalian: Rp {int(kembalian):,}")
                    
            elif metode_pilih == 2:
                metode_str = "QRIS"
                print("📲 Silakan scan kode QRIS menggunakan m-Banking atau E-Wallet...")
                input("Tekan [Enter] setelah pelanggan sukses melakukan scan & pembayaran...")
                print("✅ Pembayaran via QRIS berhasil diverifikasi!")
                
            elif metode_pilih == 3:
                bank = input("Masukkan nama Bank (BCA / Mandiri / BNI / BRI): ").strip()
                metode_str = f"Transfer Bank ({bank})"
                print(f"💳 Silakan transfer ke rekening toko. Menunggu konfirmasi...")
                input("Tekan [Enter] jika dana sudah masuk/terkonfirmasi...")
                print(f"✅ Pembayaran via Transfer {bank} berhasil diverifikasi!")
                
            elif metode_pilih == 4:
                metode_str = "Kartu Debit/Kredit"
                print("💳 Masukkan atau gesek kartu pada mesin EDC...")
                input("Tekan [Enter] setelah transaksi EDC disetujui (Approved)...")
                print("✅ Pembayaran Kartu Debit/Kredit berhasil!")
            else:
                print("❌ Metode pembayaran tidak dikenal. Transaksi dibatalkan.")
                continue
            
            for item_beli in keranjang:
                for kode, info in katalog_produk.items():
                    if info["nama"] == item_beli["nama"]:
                        info["stok"] -= item_beli["qty"]
            
            simpan_katalog(katalog_produk)
            
            transaksi_final = {
                "status_member": status_member,
                "metode_pembayaran": metode_str,
                "items": keranjang,
                "total_kotor": total_kotor,
                "diskon": int(diskon),
                "total_bersih": total_bersih
            }
            
            simpan_riwayat(transaksi_final)
            cetak_struk(transaksi_final)
            keranjang = []
            print("📦 Transaksi selesai, stok produk & riwayat berhasil diperbarui!\n")
                
        elif pilihan == 6:
            riwayat_global = ambil_riwayat()
            if not riwayat_global:
                print("⚠️ Belum ada riwayat transaksi tersimpan.")
            else:
                print("\n--- RIWAYAT & REKAP OMSET KASIR ---")
                total_omset_keseluruhan = 0
                for idx, trx in enumerate(riwayat_global, start=1):
                    metode_bayar = trx.get('metode_pembayaran', 'Tunai')
                    print(f"\nTransaksi #{idx} [{trx['status_member']}] - Bayar via: {metode_bayar}")
                    for item in trx['items']:
                        print(f" - {item['nama']} x{item['qty']} (Rp {item['subtotal']:,})")
                    print(f" Subtotal Bersih: Rp {trx['total_bersih']:,}")
                    total_omset_keseluruhan += trx['total_bersih']
                
                print(f"\n" + "="*40)
                print(f"💰 TOTAL OMSET KESELURUHAN: Rp {total_omset_keseluruhan:,}")
                print(f"="*40)

        elif pilihan == 7:
            print("\n--- RESTOCK / TAMBAH STOK PRODUK ---")
            for kode, info in katalog_produk.items():
                print(f"[{kode}] {info['nama']} (Stok Saat Ini: {info['stok']})")
            kode_restock = input("Masukkan kode produk yang ingin ditambah stoknya: ").strip().upper()
            if kode_restock in katalog_produk:
                tambah_qty = input("Masukkan jumlah stok yang ditambahkan: ").strip()
                if not tambah_qty.isdigit():
                    print("❌ Jumlah stok harus berupa angka!")
                    continue
                qty_tambah = int(tambah_qty)
                if qty_tambah <= 0:
                    print("❌ Penambahan stok harus lebih besar dari 0!")
                    continue
                katalog_produk[kode_restock]["stok"] += qty_tambah
                simpan_katalog(katalog_produk)
                print(f"✅ Stok berhasil ditambah & disimpan! Stok baru untuk {katalog_produk[kode_restock]['nama']} adalah {katalog_produk[kode_restock]['stok']}.")
            else:
                print("❌ Kode produk tidak ditemukan dalam katalog.")

        elif pilihan == 8:
            print("\n--- TAMBAH PRODUK BARU KE KATALOG ---")
            kode_baru = input("Masukkan kode produk baru (contoh: P005): ").strip().upper()
            if not kode_baru:
                print("❌ Kode produk tidak boleh kosong!")
                continue
            if kode_baru in katalog_produk:
                print("❌ Kode produk sudah terdaftar di katalog!")
                continue
            
            nama_baru = input("Masukkan nama produk baru: ").strip()
            if not nama_baru:
                print("❌ Nama produk tidak boleh kosong!")
                continue
                
            harga_input = input("Masukkan harga satuan: Rp ").strip()
            if not harga_input.isdigit():
                print("❌ Harga harus berupa angka!")
                continue
                
            stok_input = input("Masukkan jumlah stok awal: ").strip()
            if not stok_input.isdigit():
                print("❌ Stok harus berupa angka!")
                continue
            
            katalog_produk[kode_baru] = {
                "nama": nama_baru,
                "harga": int(harga_input),
                "stok": int(stok_input)
            }
            
            simpan_katalog(katalog_produk)
            print(f"✅ Produk baru '{nama_baru}' dengan kode {kode_baru} berhasil ditambahkan & disimpan ke katalog!")

        elif pilihan == 9:
            print("\n--- REGISTRASI MEMBER BARU ---")
            id_baru = input("Masukkan ID Member baru (contoh: MEMBER03 / VIP02): ").strip().upper()
            if not id_baru:
                print("❌ ID Member tidak boleh kosong!")
                continue
            if id_baru in database_member:
                print("❌ ID Member tersebut sudah terdaftar di sistem!")
            else:
                database_member.append(id_baru)
                simpan_member(database_member)
                print(f"🎉 Berhasil mendaftarkan & menyimpan ID Member baru: {id_baru}!")
                
        elif pilihan == 10:
            print("Terima kasih! Program ditutup.")
            break
        else:
            print("❌ Pilihan menu tidak valid.")

if __name__ == "__main__":
    jalankan_kasir()
