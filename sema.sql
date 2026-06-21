CREATE TABLE IF NOT EXISTS kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kitap_adi TEXT NOT NULL,
    yazar TEXT NOT NULL,
    isbn TEXT NOT NULL UNIQUE,
    adet INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS uyeler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad_soyad TEXT NOT NULL,
    telefon TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS oduncler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kitap_id INTEGER NOT NULL,
    uye_id INTEGER NOT NULL,
    alis_tarihi TEXT NOT NULL,
    son_tarih TEXT NOT NULL,
    iade_tarihi TEXT,
    durum TEXT NOT NULL,
    FOREIGN KEY (kitap_id) REFERENCES kitaplar(id),
    FOREIGN KEY (uye_id) REFERENCES uyeler(id)
);

