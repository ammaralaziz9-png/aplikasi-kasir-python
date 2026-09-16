import json
import os

FILE_RIWAYAT = "riwayat_transaksi.json"
FILE_KATALOG = "katalog_produk.json"
FILE_MEMBER = "database_member.json"

def ambil_riwayat():
    if not os.path.exists(FILE_RIWAYAT):
        return []
    try:
        with open(FILE_RIWAYAT, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def simpan_riwayat(transaksi_baru):
    riwayat = ambil_riwayat()
    riwayat.append(transaksi_baru)
    try:
        with open(FILE_RIWAYAT, "w", encoding="utf-8") as f:
            json.dump(riwayat, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Gagal menyimpan riwayat: {e}")

def simpan_katalog(katalog):
    """Menyimpan data katalog produk ke file JSON."""
    try:
        with open(FILE_KATALOG, "w", encoding="utf-8") as f:
            json.dump(katalog, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Gagal menyimpan katalog: {e}")

def muat_katalog(katalog_default):
    """Memuat katalog dari JSON, atau pakai default jika belum ada."""
    if not os.path.exists(FILE_KATALOG):
        simpan_katalog(katalog_default)
        return katalog_default
    try:
        with open(FILE_KATALOG, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return katalog_default

def simpan_member(database_member):
    """Menyimpan database member ke file JSON."""
    try:
        with open(FILE_MEMBER, "w", encoding="utf-8") as f:
            json.dump(database_member, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Gagal menyimpan member: {e}")

def muat_member(member_default):
    """Memuat database member dari JSON, atau pakai default jika belum ada."""
    if not os.path.exists(FILE_MEMBER):
        simpan_member(member_default)
        return member_default
    try:
        with open(FILE_MEMBER, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return member_default