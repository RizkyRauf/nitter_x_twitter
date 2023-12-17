# Nitter Twitter Scraper

Nitter Twitter Scraper adalah skrip Python untuk otomatisasi pada Nitter dan mengekstrak tweet berdasarkan kriteria pencarian.

## Instalasi

- Clone repository
    ```bash
    git clone https://github.com/RizkyRauf/nitter-twitter-scraper.git
    cd nitter-twitter-scraper
    ```
- Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Penggunaan

Jalankan skrip dengan perintah berikut:
```bash
python main.py --key "Python" --start "2023-01-01" --end "2023-12-31" --lang "indonesia"
```

Gantilah nilai untuk --key, --start, --end, dan --lang sesuai dengan parameter yang diinginkan.

## Fitur
    - Mengambil tweet dari Nitter berdasarkan kriteria pencarian.
    - Mengekstrak berbagai detail dari setiap tweet, termasuk username, tanggal, konten, dan metrik keterlibatan.

## Dependensi
    - Selenium
    - Webdriver Manager