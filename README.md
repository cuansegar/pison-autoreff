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
1. Git
2. Python 3.x
3. Package `requests`
4. Akun 2captcha.com
5. Saldo 2captcha minimal $2-3
6. Kode referral Pison yang valid

## Cara Install

### Windows
1. Install Git dari [git-scm.com](https://git-scm.com)
2. Install Python 3.x dari [python.org](https://python.org)
3. Clone repository:
```bash
git clone https://github.com/cuansegar/pison-autoreff
cd pison-autoreff
```
4. Install requests:
```bash
pip install requests
```

### Linux/macOS
```bash
# Install Git & Python
sudo apt update
sudo apt install git python3 python3-pip

# Clone repository
git clone https://github.com/cuansegar/pison-autoreff
cd pison-autoreff

# Install requests
pip3 install requests
```

## Cara Menjalankan Bot

1. **Persiapan 2captcha**
   - Daftar di [2captcha.com](https://2captcha.com)
   - Deposit saldo (min. $2-3)
   - Copy API key dari menu API Setup

2. **Jalankan Bot**
   ```bash
   # Windows
   python bot.py
   
   # Linux/macOS
   python3 bot.py
   ```

3. **Input yang Diperlukan**
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

### 1. Error Git Clone
```
fatal: repository not found
```
➜ **Solusi**: 
- Pastikan URL repository benar
- Cek koneksi internet
- Pastikan Git terinstall: `git --version`

### 2. Error Python/PIP
```
'python' is not recognized...
```
➜ **Solusi**: 
- Pastikan Python terinstall: `python --version`
- Tambahkan Python ke PATH
- Coba gunakan `python3` untuk Linux/macOS

### 3. Error Captcha
```
[-] Error solving captcha: ERROR_ZERO_BALANCE
```
➜ **Solusi**: Isi saldo 2captcha

### 4. Error Rate Limit
```
[-] Gagal: {"error":"Too many requests"}
```
➜ **Solusi**:
- Tunggu 5-10 menit
- Tambah delay (edit nilai di kode)
- Ganti IP address

## Tips Penting

1. **Update Bot**
```bash
cd pison-bot
git pull origin main
```

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
- Telegram: @AirdropFamilyIDN x @ntrcd00
- Join channel untuk update terbaru
