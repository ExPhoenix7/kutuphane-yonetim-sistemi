# Kütüphane Yönetim Sistemi

Bu proje Python ve SQLite kullanılarak hazırlanmış basit bir kütüphane yönetim uygulamasıdır. Program terminalde açılan menüler üzerinden kullanılır.

## Dosyalar

- `kutuphane.py`: Programın bütün Python kodları bu dosyadadır.
- `sema.sql`: Veritabanındaki tabloları oluşturur.
- `kutuphane.db`: Program ilk çalıştırıldığında otomatik oluşur ve kayıtları saklar.
- `.gitignore`: Veritabanı dosyasının GitHub'a yüklenmesini engeller.
- `README.md`: Projeyi açıklayan bu dosyadır.

## Özellikler

- Kitap ekleme, listeleme, güncelleme ve silme
- Üye ekleme, listeleme, güncelleme ve silme
- Kitap ödünç verme
- Ödünç kayıtlarını listeleme
- Kitap iade alma ve eski ödünç kaydını silme
- Kitapların adet kontrolü

## Çalıştırma

Bilgisayarda Python 3 kurulu olmalıdır. Ek bir paket yüklemeye gerek yoktur.

```bash
python kutuphane.py
```

Komut çalıştırılınca ana menü açılır:

```text
1- Kitap işlemleri
2- Üye işlemleri
3- Ödünç işlemleri
0- Çıkış
```

## Veritabanı

Projede üç tablo vardır:

- `kitaplar`: Kitabın adı, yazarı, ISBN numarası ve adedini tutar.
- `uyeler`: Üyenin adı ve telefon numarasını tutar.
- `oduncler`: Hangi kitabın hangi üyeye verildiğini ve iade durumunu tutar.

`oduncler` tablosundaki `kitap_id` ve `uye_id` alanları diğer tablolarla bağlantı kurar.