import sqlite3
from datetime import date, timedelta


VERITABANI = "kutuphane.db"


def baglanti_ac():
    baglanti = sqlite3.connect(VERITABANI)
    baglanti.execute("PRAGMA foreign_keys = ON")
    return baglanti


def veritabanini_hazirla():
    baglanti = baglanti_ac()
    with open("sema.sql", "r", encoding="utf-8") as dosya:
        baglanti.executescript(dosya.read())
    baglanti.close()


def kitap_ekle():
    kitap_adi = input("Kitap adı: ").strip()
    yazar = input("Yazar: ").strip()
    isbn = input("ISBN: ").strip()

    try:
        adet = int(input("Adet: "))
        if adet < 1:
            print("Adet en az 1 olmalıdır.")
            return
    except ValueError:
        print("Adet sayı olmalıdır.")
        return

    if not kitap_adi or not yazar or not isbn:
        print("Bilgiler boş bırakılamaz.")
        return

    try:
        baglanti = baglanti_ac()
        baglanti.execute(
            "INSERT INTO kitaplar (kitap_adi, yazar, isbn, adet) VALUES (?, ?, ?, ?)",
            (kitap_adi, yazar, isbn, adet),
        )
        baglanti.commit()
        baglanti.close()
        print("Kitap eklendi.")
    except sqlite3.IntegrityError:
        print("Bu ISBN numarası daha önce kullanılmış.")


def kitaplari_listele():
    baglanti = baglanti_ac()
    kitaplar = baglanti.execute(
        "SELECT id, kitap_adi, yazar, isbn, adet FROM kitaplar ORDER BY id"
    ).fetchall()
    baglanti.close()

    if not kitaplar:
        print("Kayıtlı kitap yok.")
        return

    print("\nID | Kitap | Yazar | ISBN | Adet")
    print("-" * 60)
    for kitap in kitaplar:
        print(f"{kitap[0]} | {kitap[1]} | {kitap[2]} | {kitap[3]} | {kitap[4]}")


def kitap_guncelle():
    kitaplari_listele()
    try:
        kitap_id = int(input("Güncellenecek kitap ID: "))
        yeni_adet = int(input("Yeni adet: "))
    except ValueError:
        print("ID ve adet sayı olmalıdır.")
        return

    baglanti = baglanti_ac()
    sonuc = baglanti.execute(
        "UPDATE kitaplar SET adet = ? WHERE id = ?", (yeni_adet, kitap_id)
    )
    baglanti.commit()
    baglanti.close()

    if sonuc.rowcount == 0:
        print("Kitap bulunamadı.")
    else:
        print("Kitap güncellendi.")


def kitap_sil():
    kitaplari_listele()
    try:
        kitap_id = int(input("Silinecek kitap ID: "))
        baglanti = baglanti_ac()
        sonuc = baglanti.execute("DELETE FROM kitaplar WHERE id = ?", (kitap_id,))
        baglanti.commit()
        baglanti.close()
        if sonuc.rowcount == 0:
            print("Kitap bulunamadı.")
        else:
            print("Kitap silindi.")
    except ValueError:
        print("ID sayı olmalıdır.")
    except sqlite3.IntegrityError:
        print("Bu kitaba ait ödünç kaydı olduğu için silinemez.")


def uye_ekle():
    ad_soyad = input("Üyenin adı soyadı: ").strip()
    telefon = input("Telefon: ").strip()

    if not ad_soyad or not telefon:
        print("Bilgiler boş bırakılamaz.")
        return

    baglanti = baglanti_ac()
    baglanti.execute(
        "INSERT INTO uyeler (ad_soyad, telefon) VALUES (?, ?)",
        (ad_soyad, telefon),
    )
    baglanti.commit()
    baglanti.close()
    print("Üye eklendi.")


def uyeleri_listele():
    baglanti = baglanti_ac()
    uyeler = baglanti.execute(
        "SELECT id, ad_soyad, telefon FROM uyeler ORDER BY id"
    ).fetchall()
    baglanti.close()

    if not uyeler:
        print("Kayıtlı üye yok.")
        return

    print("\nID | Ad Soyad | Telefon")
    print("-" * 40)
    for uye in uyeler:
        print(f"{uye[0]} | {uye[1]} | {uye[2]}")


def uye_guncelle():
    uyeleri_listele()
    try:
        uye_id = int(input("Güncellenecek üye ID: "))
    except ValueError:
        print("ID sayı olmalıdır.")
        return

    yeni_telefon = input("Yeni telefon: ").strip()
    baglanti = baglanti_ac()
    sonuc = baglanti.execute(
        "UPDATE uyeler SET telefon = ? WHERE id = ?", (yeni_telefon, uye_id)
    )
    baglanti.commit()
    baglanti.close()

    if sonuc.rowcount == 0:
        print("Üye bulunamadı.")
    else:
        print("Üye güncellendi.")


def uye_sil():
    uyeleri_listele()
    try:
        uye_id = int(input("Silinecek üye ID: "))
        baglanti = baglanti_ac()
        sonuc = baglanti.execute("DELETE FROM uyeler WHERE id = ?", (uye_id,))
        baglanti.commit()
        baglanti.close()
        if sonuc.rowcount == 0:
            print("Üye bulunamadı.")
        else:
            print("Üye silindi.")
    except ValueError:
        print("ID sayı olmalıdır.")
    except sqlite3.IntegrityError:
        print("Bu üyeye ait ödünç kaydı olduğu için silinemez.")


def odunc_ver():
    kitaplari_listele()
    uyeleri_listele()

    try:
        kitap_id = int(input("Kitap ID: "))
        uye_id = int(input("Üye ID: "))
    except ValueError:
        print("ID sayı olmalıdır.")
        return

    baglanti = baglanti_ac()
    kitap = baglanti.execute(
        "SELECT adet FROM kitaplar WHERE id = ?", (kitap_id,)
    ).fetchone()
    uye = baglanti.execute("SELECT id FROM uyeler WHERE id = ?", (uye_id,)).fetchone()

    if kitap is None or uye is None:
        print("Kitap veya üye bulunamadı.")
        baglanti.close()
        return

    oduncteki_adet = baglanti.execute(
        "SELECT COUNT(*) FROM oduncler WHERE kitap_id = ? AND durum = 'Ödünçte'",
        (kitap_id,),
    ).fetchone()[0]

    if oduncteki_adet >= kitap[0]:
        print("Bu kitabın müsait kopyası yok.")
        baglanti.close()
        return

    alis_tarihi = date.today()
    son_tarih = alis_tarihi + timedelta(days=14)
    baglanti.execute(
        """
        INSERT INTO oduncler (kitap_id, uye_id, alis_tarihi, son_tarih, durum)
        VALUES (?, ?, ?, ?, 'Ödünçte')
        """,
        (kitap_id, uye_id, alis_tarihi.isoformat(), son_tarih.isoformat()),
    )
    baglanti.commit()
    baglanti.close()
    print("Kitap ödünç verildi.")


def oduncleri_listele():
    baglanti = baglanti_ac()
    kayitlar = baglanti.execute(
        """
        SELECT oduncler.id, kitaplar.kitap_adi, uyeler.ad_soyad,
               oduncler.alis_tarihi, oduncler.son_tarih, oduncler.durum
        FROM oduncler
        JOIN kitaplar ON kitaplar.id = oduncler.kitap_id
        JOIN uyeler ON uyeler.id = oduncler.uye_id
        ORDER BY oduncler.id
        """
    ).fetchall()
    baglanti.close()

    if not kayitlar:
        print("Ödünç kaydı yok.")
        return

    print("\nID | Kitap | Üye | Alış | Son Tarih | Durum")
    print("-" * 75)
    for kayit in kayitlar:
        print(
            f"{kayit[0]} | {kayit[1]} | {kayit[2]} | "
            f"{kayit[3]} | {kayit[4]} | {kayit[5]}"
        )


def kitap_iade_al():
    oduncleri_listele()
    try:
        kayit_id = int(input("İade edilecek kayıt ID: "))
    except ValueError:
        print("ID sayı olmalıdır.")
        return

    baglanti = baglanti_ac()
    sonuc = baglanti.execute(
        """
        UPDATE oduncler SET durum = 'İade edildi', iade_tarihi = ?
        WHERE id = ? AND durum = 'Ödünçte'
        """,
        (date.today().isoformat(), kayit_id),
    )
    baglanti.commit()
    baglanti.close()

    if sonuc.rowcount == 0:
        print("Aktif ödünç kaydı bulunamadı.")
    else:
        print("Kitap iade alındı.")


def odunc_kaydi_sil():
    oduncleri_listele()
    try:
        kayit_id = int(input("Silinecek kayıt ID: "))
    except ValueError:
        print("ID sayı olmalıdır.")
        return

    baglanti = baglanti_ac()
    sonuc = baglanti.execute(
        "DELETE FROM oduncler WHERE id = ? AND durum = 'İade edildi'", (kayit_id,)
    )
    baglanti.commit()
    baglanti.close()

    if sonuc.rowcount == 0:
        print("Kayıt bulunamadı veya kitap henüz iade edilmedi.")
    else:
        print("Ödünç kaydı silindi.")


def kitap_menusu():
    while True:
        print("\n--- KİTAP İŞLEMLERİ ---")
        print("1- Kitap ekle")
        print("2- Kitapları listele")
        print("3- Kitap güncelle")
        print("4- Kitap sil")
        print("0- Ana menü")
        secim = input("Seçiminiz: ")

        if secim == "1":
            kitap_ekle()
        elif secim == "2":
            kitaplari_listele()
        elif secim == "3":
            kitap_guncelle()
        elif secim == "4":
            kitap_sil()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")


def uye_menusu():
    while True:
        print("\n--- ÜYE İŞLEMLERİ ---")
        print("1- Üye ekle")
        print("2- Üyeleri listele")
        print("3- Üye güncelle")
        print("4- Üye sil")
        print("0- Ana menü")
        secim = input("Seçiminiz: ")

        if secim == "1":
            uye_ekle()
        elif secim == "2":
            uyeleri_listele()
        elif secim == "3":
            uye_guncelle()
        elif secim == "4":
            uye_sil()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")


def odunc_menusu():
    while True:
        print("\n--- ÖDÜNÇ İŞLEMLERİ ---")
        print("1- Kitap ödünç ver")
        print("2- Ödünç kayıtlarını listele")
        print("3- Kitap iade al")
        print("4- Ödünç kaydı sil")
        print("0- Ana menü")
        secim = input("Seçiminiz: ")

        if secim == "1":
            odunc_ver()
        elif secim == "2":
            oduncleri_listele()
        elif secim == "3":
            kitap_iade_al()
        elif secim == "4":
            odunc_kaydi_sil()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")


def ana_menu():
    while True:
        print("\n=== KÜTÜPHANE YÖNETİM SİSTEMİ ===")
        print("1- Kitap işlemleri")
        print("2- Üye işlemleri")
        print("3- Ödünç işlemleri")
        print("0- Çıkış")
        secim = input("Seçiminiz: ")

        if secim == "1":
            kitap_menusu()
        elif secim == "2":
            uye_menusu()
        elif secim == "3":
            odunc_menusu()
        elif secim == "0":
            print("Program kapatıldı.")
            break
        else:
            print("Geçersiz seçim.")


veritabanini_hazirla()
ana_menu()

