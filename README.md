Register: https://form.zootools.co/go/Qkr0xCL2rXK0nY39DAO2?ref=J26dwc9nXnMNJhIj7wgq
# Pison Referral Bot

Bot otomatis untuk program referral Pison dengan fitur:
- Auto submit referral dengan email random
- Captcha solver menggunakan 2captcha
- Random user agent untuk menghindari deteksi
- Sistem retry dengan exponential backoff
- Rate limit handling yang optimal
- Session management otomatis
- Statistik realtime dan summary
- Output berwarna untuk monitoring

## Persyaratan

- Python 3.7+
- 2captcha API key (https://2captcha.com)
- Kode referral Pison yang valid
- Koneksi internet yang stabil

## Instalasi

### Windows

1. Install Python:
   - Download Python 3.7+ dari [python.org](https://www.python.org/downloads/)
   - **PENTING**: Centang "Add Python to PATH" saat instalasi

2. Install Git:
   - Download Git dari [git-scm.com](https://git-scm.com/download/win)
   - Install dengan opsi default

3. Clone repository:
   ```bash
   git clone https://github.com/cuansegar/pison-autoreff && cd pison-autoreff
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Linux (Ubuntu/Debian)

1. Install dependencies sistem:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip git
   ```

2. Clone repository:
   ```bash
   git clone https://github.com/cuansegar/pison-autoreff && cd pison-autoreff
   ```

3. Install dependencies Python:
   ```bash
   pip3 install -r requirements.txt
   ```

## Penggunaan

1. Jalankan bot:
   ```bash
   # Windows
   python reff.py
   ```
   ```bash
   # Linux
   python3 reff.py
   ```

2. Masukkan informasi yang diminta:
   - API Key 2captcha
   - Kode referral Pison
   - Jumlah referral yang diinginkan

3. Bot akan mulai bekerja secara otomatis dengan:
   - Verifikasi koneksi setiap 30 detik
   - Reset session setiap 5 menit
   - Delay dinamis 5-15 detik antara submit
   - Retry otomatis jika terkena rate limit

## Fitur Detail

1. **Email Generator**
   - Generate email random dengan domain populer
   - Format: [random10char]@[domain]
   - Domain: gmail.com, yahoo.com, outlook.com, hotmail.com

2. **Session Management**
   - Auto reset setiap 5 menit
   - Keep-alive connection
   - Connection pooling
   - Random user agent

3. **Rate Limit Handler**
   - Exponential backoff
   - Delay dinamis berdasarkan jumlah kegagalan
   - Auto retry dengan verifikasi ulang

4. **Statistik Realtime**
   - Success/failed counter
   - Rate referral per detik
   - Total waktu berjalan
   - Progress (X/Total)

## Menjalankan di Background

### Linux Screen
```bash
screen -S pison
python3 reff.py
# Detach: Ctrl+A kemudian D
# Reattach: screen -r pison
```

### Windows Task Scheduler
1. Buka Task Scheduler
2. Create Basic Task
3. Action: Start a Program
4. Program: python
5. Arguments: reff.py
6. Start in: C:\path\to\pison-bot

## Troubleshooting

1. **SSL Error**
   ```
   [!] SSL Error, mencoba tanpa verifikasi SSL...
   ```
   - Bot akan retry otomatis tanpa SSL
   - Jika masih error, update Python dan OpenSSL

2. **Rate Limit**
   ```
   [!] Rate limit terdeteksi, tunggu...
   ```
   - Bot akan menunggu dengan delay yang meningkat
   - Verifikasi ulang otomatis

3. **Captcha Error**
   ```
   [-] Error solving captcha...
   ```
   - Cek saldo 2captcha
   - Verifikasi API key
   - Bot akan skip ke referral berikutnya

## Tips Optimal

1. **Kecepatan**
   - Mulai dengan jumlah kecil (5-10)
   - Tingkatkan bertahap jika stabil
   - Monitor success rate

2. **Rate Limit**
   - Gunakan VPN jika terlalu sering limit
   - Biarkan bot mengatur delay otomatis
   - Jangan ubah delay default

3. **Biaya**
   - Monitor saldo 2captcha
   - Harga per captcha ±$0.002
   - Isi saldo sesuai target referral


## Disclaimer

Bot ini dibuat untuk tujuan edukasi. Gunakan dengan bijak dan sesuai Terms of Service platform target.

## License

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan.
