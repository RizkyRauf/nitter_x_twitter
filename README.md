# TwitterXScraper

**TwitterXScraper** adalah alat Python yang dirancang untuk mengotomatisasi proses pengambilan data dari Nitter, sebuah antarmuka Twitter tanpa JavaScript. Alat ini menggunakan Selenium untuk web scraping dan menyediakan cara yang nyaman untuk mengekstrak tweet berdasarkan kriteria pencarian.

## Prasyarat

- Python 3.x
- Browser Chrome terinstal
- ChromeDriver

## Instalasi

1. **Klon repositori**:

    ```bash
    git clone https://github.com/nama-pengguna-anda/TwitterXScraper.git
    ```

2. **Pasang dependensi yang diperlukan** :

    ```bash
    pip install -r requirements.txt
    ```

## Penggunaan

**Argumen Melalui Command-line**

- `--key`: Kata kunci pencarian untuk Nitter (contoh: 'Python').
- `--start`: Tanggal mulai dalam format YYYY-MM-DD.
- `--end`: Tanggal akhir dalam format YYYY-MM-DD.
- `--lang`: Bahasa pencarian. Default adalah 'all'.

### Contoh

```bash
python main.py --key "Python" --start "2022-01-01" --end "2022-12-31" --lang "indonesia"
```
Contoh ini akan mengambil tweet terkait "Python" yang diposting antara 1 Januari 2022 hingga 31 Desember 2022 dalam bahasa Indonesia.

## Berkas

- [``content.py``](./lib/content.py): Berisi kelas `TwitterContent`, yang mewakili struktur sebuah tweet dan menyediakan metode untuk mengekstrak berbagai informasi.

- [``run.py``](./lib/run.py): Mengimplementasikan kelas `TwitterXScraper`, yang mengonfigurasi proses web scraping dan menjalankan scraping berdasarkan parameter yang diberikan.

- [``util.py``](./lib/util.py): Termasuk fungsi utilitas seperti menghasilkan agen pengguna acak, menangani aksi "load more," dan menggulir halaman.

- [``main.py``](main.py): Skrip utama untuk menjalankan TwitterXScraper, menguraikan argumen baris perintah, dan memulai proses scraping.
