# 🛡️ Tapu Güvenlik 2026 - Etkileşimli Arazi Rehberi

[Tapu Güvenlik 2026](https://cenktekin.github.io/tapu-guvenlik) projesine hoş geldiniz! Bu açık kaynaklı platform, Türkiye'deki gayrimenkul ve arazi satın alma süreçlerinde kullanıcıları olası dolandırıcılıklara, imar problemlerine ve hukuki tuzaklara karşı korumak amacıyla tasarlanmış modern bir rehberdir.

## 🌟 Öne Çıkan Özellikler

- **🗂️ İşlem Adımları:** Arazi alım sürecinde masa başı, saha, resmi teyit ve satış işlemlerinin adım adım analizi.
- **📊 Arazi Yapılaşma Simülatörü:** Seçeceğiniz arazi türüne (Tarla, Zeytinlik vs.) göre 2026 güncel mevzuat kuralları çerçevesinde ne kadarlık bir yapı inşa edebileceğinizi görsel grafiklerle (Chart.js) hesaplayın.
- **🚩 Dolandırıcılık Sinyalleri (Red Flags):** İlanlarda sıkça karşılaşılan yanıltıcı söylemlerin ("İmara Açılıyor", "Çevresi Kapalı", vs.) gerçek anlamlarını tek tıkla öğrenin.
- **✅ Interaktif Kontrol Listesi:** Alım sürecinde "Neredeyim?" ve "Neyi unuttum?" sorularını gidermek için kullanabileceğiniz interaktif liste.
- **📚 Kapsamlı Emlak Sözlüğü:** Resmi "Tapu Terimleri" rehberinden derlenmiş, kolay arama motoru olan ve kelimelerin üzerine gelince açılan (tooltip) detaylı tapu sözlüğü.
- **🌙 Gece Modu Desteği:** Rahat okuma için göz yormayan, cihazlara tam uyumlu (Responsive) "Dark Mode" arayüzü.

## 🚀 Başlangıç & Kurulum

Bu projeyi kendi ortamınızda çalıştırmak veya geliştirmek çok kolay! Herhangi bir derleme (build) işlemine gerek kalmadan doğrudan tarayıcınızda açabilirsiniz.

1. **Repoyu Klonlayın:**
   ```bash
   git clone https://github.com/cenktekin/tapu-guvenlik.git
   cd tapu-guvenlik
   ```

2. **Çalıştırma:**
   Özel bir sunucuya ihtiyaç yoktur. Klasör içindeki `index.html` dosyasını çift tıklatarak tarayıcınızda açabilirsiniz. 
   *(Opsiyonel)* Eğer lokal bir sunucu kullanmak isterseniz:
   ```bash
   python -m http.server 8080
   ```
   Tarayıcınızda `http://localhost:8080` adresine gidebilirsiniz.

## 🛠️ Teknolojiler

- **HTML5 & CSS3**
- **Vanilla JavaScript** (Modern ES6 Standartları)
- **TailwindCSS** (CDN üzerinden, yüksek performanslı arayüz için)
- **Chart.js** (Veri görselleştirme ve simülatörler için)
- **Python 3** (yalnız geliştirme/veri hattı: PDF'ten sözlük çıkarımı ve HTML'e enjeksiyon — sitenin çalışması için gerekmez)

## 📄 Proje Dosyaları
- `index.html` - Ana uygulama dosyası.
- `dictionary.json` - Sözlük verileri (245 terim).
- `infografik.html` - İlgili veri görselleştirme dökümanı.
- `Tapu_Dolandiricilik_Korunma.pptx` - Resmi kurum sunumu.
- `extract.py` · `parse_dict.py` - PDF → metin → `dictionary.json` veri hattı.
- `inject.py` · `inject2.py` · `inject_dark_mode.py` - Sözlük/tooltip ve gece modu enjeksiyon scriptleri (tek seferlik; `index.html`'i yerinde günceller).

## 🔁 Yeniden Üretim (Veri Hattı)

Kaynak PDF (`TAPU_TERIMLERI_SOZLUK.pdf`) telif nedeniyle repoda dağıtılmaz. Elinizde varsa sözlük yeniden üretilebilir:

```bash
pip install PyPDF2
python extract.py     # PDF → output.txt
python parse_dict.py  # output.txt → dictionary.json
```

`inject*.py` scriptleri `index.html`'i yerinde değiştirir; çalıştırmadan önce değişikliği git ile geri alabilirsiniz (`git checkout -- index.html`).

> **Not:** `dictionary.json` üzerinde sonradan elle yapılmış düzeltmeler üretim çıktısında yer almaz. `parse_dict.py` 244 terim üretir; repodaki dosyada 245 terim vardır (elle eklenen `TAPUK` ve boşluk normalizasyonları).

## 🌐 Canlı Demo (GitHub Pages)

Uygulamanın yayındaki en güncel versiyonunu **[Canlı Demo Linki](https://cenktekin.github.io/tapu-guvenlik/)** adresinden inceleyebilirsiniz. 

*- Bu veri seti resmi kaynaklardan derlense de, kesin yasal tavsiye yerine genel rehberlik amacı taşır. Alım/Satım işlemlerinizden önce daima güncel Tapu veya Belediye kurumlarından doğrudan teyit alınız.*
