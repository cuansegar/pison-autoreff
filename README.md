# Pison Auto Referral Bot

Bot otomatis untuk program referral Pison dengan fitur auto-solve captcha menggunakan 2captcha.

## Fitur Utama
- Auto generate random email
- Auto solve captcha via 2captcha
- Auto submit referral ke Pison
- Progress tracking real-time
- Random delay anti-detect
- Summary hasil referral

## Persyaratan
1. Python 3.x
2. Package `requests`
3. Akun 2captcha.com
4. Saldo 2captcha minimal $2-3
5. Kode referral Pison yang valid

## Cara Install

git clone https://github.com/cuansegar/pison-autoreff && cd pison-autoreff

### Windows
1. Download dan install Python 3.x dari [python.org](https://python.org)
2. Buka Command Prompt sebagai Administrator
3. Install requests:
```bash
pip install requests
```

### Linux/macOS
```bash
# Install Python
sudo apt update
sudo apt install python3 python3-pip

# Install requests
pip3 install requests
```

## Cara Menjalankan Bot

1. **Persiapan 2captcha**
   - Daftar di [2captcha.com](https://2captcha.com)
   - Deposit saldo (min. $2-3)
   - Copy API key dari menu API Setup

2. **Download Bot**
   - Download file `bot.py`
   - Simpan di folder yang mudah diakses

3. **Jalankan Bot**
   - Buka Command Prompt/Terminal
   - Masuk ke folder bot:
   ```bash
   cd path/to/bot/folder
   ```
   - Jalankan bot:
   ```bash
   python bot.py
   ```

4. **Input yang Diperlukan**
```
[?] Masukkan API Key 2captcha: <PASTE_API_KEY_DISINI>
[?] Masukkan kode referral: <KODE_REFERRAL_PISON>
[?] Masukkan jumlah referral: <JUMLAH>
```

## Status dan Output

### Keterangan Status
- `[*]` = Informasi/proses
- `[+]` = Berhasil
- `[-]` = Gagal/error
- `[?]` = Input yang diminta

### Contoh Output
```
[*] Memulai solve captcha...
[+] Captcha submitted, ID: 12345678
[*] Menunggu hasil captcha...
[+] Captcha solved!

[*] Mencoba mendaftarkan: abc123@gmail.com
[*] Kode referral: REF123
[+] Berhasil mendaftarkan abc123@gmail.com
[+] Member ID: xxxxx
[+] Ranking: 123

[*] Delay 5.2 detik...
```

## Troubleshooting

### 1. Error Captcha
```
[-] Error solving captcha: ERROR_ZERO_BALANCE
```
➜ **Solusi**: Isi saldo 2captcha

### 2. Error Koneksi
```
[-] Error: Connection timeout
```
➜ **Solusi**: 
- Cek koneksi internet
- Coba ganti DNS
- Gunakan VPN jika perlu

### 3. Error Rate Limit
```
[-] Gagal: {"error":"Too many requests"}
```
➜ **Solusi**:
- Tunggu 5-10 menit
- Tambah delay (edit nilai di kode)
- Ganti IP address

## Tips Penting

1. **Hindari Spam**
   - Jangan set jumlah terlalu banyak
   - Gunakan delay default (3-7 detik)
   - Monitor hasil di dashboard

2. **Optimasi Biaya**
   - 1 solve captcha ≈ $0.002
   - Contoh: 100 referral = $0.2

3. **Keamanan**
   - Jangan share API key
   - Gunakan VPN jika perlu
   - Monitor aktivitas akun

## Cara Menghentikan Bot

1. **Hentikan Manual**
   - Tekan `Ctrl+C`
   - Bot akan menampilkan summary:
   ```
   === Summary ===
   [+] Berhasil: 45
   [-] Gagal: 5
   [*] Total: 50
   ```

2. **Auto Stop**
   - Bot berhenti otomatis setelah jumlah tercapai
   - Atau jika terjadi error fatal

## Support

Butuh bantuan? Hubungi:
- Telegram: @AirdropFamilyIDN
- Join channel untuk update terbaru

