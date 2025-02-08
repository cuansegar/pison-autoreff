import requests
import json
import time
import random
import string
from typing import Dict, Tuple
import uuid
from colorama import init, Fore, Style
from fake_useragent import UserAgent
import os

# Initialize colorama for Windows
init()

# Initialize UserAgent
ua = UserAgent()

# ANSI Color codes using colorama
class Colors:
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    RESET = Style.RESET_ALL

class ReferralBot:
    def __init__(self):
        self.base_url = "https://audience-consumer-api.zootools.co/v3"
        self.list_id = "Qkr0xCL2rXK0nY39DAO2"
        self.session = self.create_session()
        self.client_id = str(uuid.uuid4())
        self.max_retries = 5
        self.base_delay = 5   
        self.max_delay = 20   
        self.last_verify_time = 0
        self.verify_interval = 60  
        self.session_lifetime = 180  
        self.last_session_time = time.time()
        self.user_agents = self.load_user_agents()

    def create_session(self):
        """Buat session baru dengan konfigurasi optimal"""
        session = requests.Session()
        
        # Konfigurasi koneksi langsung
        session.headers.update({
            "Connection": "keep-alive",
            "Keep-Alive": "timeout=60, max=1000"
        })
        
        # Konfigurasi retry dan timeout yang lebih agresif
        adapter = requests.adapters.HTTPAdapter(
            max_retries=5,
            pool_connections=50,
            pool_maxsize=50
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def should_reset_session(self):
        """Cek apakah perlu reset session"""
        current_time = time.time()
        if current_time - self.last_session_time >= self.session_lifetime:
            self.last_session_time = current_time
            return True
        return False

    def load_user_agents(self):
        """Load list of user agents untuk rotasi"""
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/121.0.0.0"
        ]

    def update_headers(self):
        """Update headers dengan random user agent dan tambahan headers"""
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://form.zootools.co",
            "referer": "https://form.zootools.co/",
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": random.choice(self.user_agents),
            "x-client-id": self.client_id,
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "DNT": "1"
        }
        self.session.headers.update(self.headers)
        time.sleep(random.uniform(1, 3))  

    def should_verify(self):
        """Cek apakah perlu verifikasi ulang"""
        current_time = time.time()
        if current_time - self.last_verify_time >= self.verify_interval:
            self.last_verify_time = current_time
            return True
        return False

    def verify_bot(self, referral_code: str) -> bool:
        """Verifikasi bot dengan mengakses halaman form terlebih dahulu"""
        max_retries = 3  # Maksimal 3x retry untuk verifikasi
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                print(f"{Colors.BLUE}[*] Melakukan verifikasi bot (Percobaan {retry_count + 1}/{max_retries})...{Colors.RESET}")
                
                # Reset session jika waktunya
                if self.should_reset_session():
                    print(f"{Colors.BLUE}[*] Reset session...{Colors.RESET}")
                    self.session = self.create_session()
                    self.client_id = str(uuid.uuid4())
                
                # Update headers
                self.update_headers()
                
                # Step 1: Verifikasi form
                form_url = f"https://form.zootools.co/go/{self.list_id}?ref={referral_code}"
                try:
                    response = self.session.get(
                        form_url,
                        timeout=20,
                        allow_redirects=True,
                        verify=True
                    )
                except requests.exceptions.SSLError:
                    print(f"{Colors.YELLOW}[!] SSL Error, mencoba tanpa verifikasi SSL...{Colors.RESET}")
                    response = self.session.get(
                        form_url,
                        timeout=20,
                        allow_redirects=True,
                        verify=False
                    )
                except Exception as e:
                    print(f"{Colors.RED}[-] Error koneksi form: {str(e)}{Colors.RESET}")
                    retry_count += 1
                    time.sleep(5)
                    continue
                
                # Handle form response
                if response.status_code == 200:
                    print(f"{Colors.GREEN}[+] Verifikasi form berhasil{Colors.RESET}")
                    self.session.cookies.update(response.cookies)
                elif response.status_code in [403, 429]:
                    print(f"{Colors.YELLOW}[!] Rate limit form, tunggu...{Colors.RESET}")
                    retry_count += 1
                    time.sleep(10)
                    continue
                else:
                    print(f"{Colors.RED}[-] Error form: HTTP {response.status_code}{Colors.RESET}")
                    retry_count += 1
                    time.sleep(5)
                    continue
                
                # Step 2: Verifikasi stats (opsional)
                time.sleep(2)  # Delay antara request
                referral_url = f"{self.base_url}/lists/{self.list_id}/members/referral/{referral_code}/stats"
                
                try:
                    referral_response = self.session.get(
                        referral_url,
                        timeout=20,
                        verify=True
                    )
                    
                    # Status 404 = referral baru (expected)
                    if referral_response.status_code == 404:
                        print(f"{Colors.BLUE}[*] Referral baru terdeteksi{Colors.RESET}")
                        return True
                    
                    # Status 200 = referral existing
                    elif referral_response.status_code == 200:
                        try:
                            ref_data = referral_response.json()
                            total = ref_data.get('totalReferrals', 0)
                            print(f"{Colors.GREEN}[+] Total referral saat ini: {total}{Colors.RESET}")
                        except:
                            print(f"{Colors.YELLOW}[!] Gagal parse stats response{Colors.RESET}")
                        return True
                    
                    # Rate limit = retry
                    elif referral_response.status_code in [403, 429]:
                        print(f"{Colors.YELLOW}[!] Rate limit stats, tunggu...{Colors.RESET}")
                        time.sleep(10)
                        retry_count += 1
                        continue
                    
                    # Error lain = log tapi tetap lanjut
                    else:
                        print(f"{Colors.RED}[-] Error stats: HTTP {referral_response.status_code}{Colors.RESET}")
                        return True
                        
                except Exception as e:
                    print(f"{Colors.RED}[-] Error cek stats: {str(e)}{Colors.RESET}")
                    # Lanjutkan meski gagal cek stats
                    return True
                
            except Exception as e:
                print(f"{Colors.RED}[-] Error tidak terduga: {str(e)}{Colors.RESET}")
                retry_count += 1
                time.sleep(5)
                continue
        
        # Jika sudah retry maksimal
        print(f"{Colors.RED}[-] Gagal verifikasi setelah {max_retries}x percobaan{Colors.RESET}")
        return False

    def get_random_email(self) -> str:
        """Generate random email"""
        domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = random.choice(domains)
        return f"{username}@{domain}"

    def solve_captcha(self, api_key: str, referral_code: str) -> str:
        """Solve captcha using 2captcha"""
        try:
            print(f"{Colors.BLUE}[*] Memulai solve captcha...{Colors.RESET}")
            
            # Submit captcha ke 2captcha
            data = {
                'key': api_key,
                'method': 'turnstile',
                'sitekey': '0x4AAAAAAABCOgX4x6RvmA0a',
                'pageurl': f'https://form.zootools.co/go/{self.list_id}?ref={referral_code}'
            }
            
            response = requests.post('http://2captcha.com/in.php', data=data)
            if not response.text.startswith('OK|'):
                raise Exception(f"Gagal submit captcha: {response.text}")
            
            captcha_id = response.text.split('|')[1]
            print(f"{Colors.GREEN}[+] Captcha submitted, ID: {captcha_id}{Colors.RESET}")
            
            # Polling untuk hasil
            for _ in range(30):  # Max 5 menit (30 x 10 detik)
                time.sleep(10)
                result_response = requests.get(
                    f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}'
                )
                
                if result_response.text.startswith('OK|'):
                    token = result_response.text.split('|')[1]
                    print(f"{Colors.GREEN}[+] Captcha solved!{Colors.RESET}")
                    return token
                    
                if "ERROR" in result_response.text:
                    raise Exception(f"Error dari 2captcha: {result_response.text}")
                    
                print(f"{Colors.BLUE}[*] Menunggu hasil captcha...{Colors.RESET}")
            
            raise Exception("Timeout menunggu hasil captcha")
            
        except Exception as e:
            print(f"{Colors.RED}[-] Error solving captcha: {str(e)}{Colors.RESET}")
            return None

    def handle_rate_limit(self, retry_count: int):
        """Handle rate limit dengan exponential backoff"""
        delay = min(self.base_delay * (2 ** retry_count) + random.uniform(1, 3), self.max_delay)
        print(f"{Colors.YELLOW}[!] Rate limit terdeteksi, tunggu {delay:.1f} detik...{Colors.RESET}")
        time.sleep(delay)

    def submit_referral(self, email: str, referrer_code: str, captcha_token: str = None) -> bool:
        """Submit referral ke Zootools dengan retry mechanism"""
        
        # Verifikasi ulang jika perlu
        if self.should_verify():
            if not self.verify_bot(referrer_code):
                print(f"{Colors.RED}[-] Gagal verifikasi, tunggu sebelum retry...{Colors.RESET}")
                time.sleep(random.uniform(10, 15))  
                return False
            
        payload = {
            "email": email,
            "referral": referrer_code,
            "captchaToken": captcha_token,
            "source": "online_form",
            "fields": {"hasAccess": False},
            "hiddenFields": {}
        }

        for retry in range(self.max_retries):
            try:
                print(f"\n{Colors.BLUE}[*] Mencoba mendaftarkan: {email}{Colors.RESET}")
                print(f"{Colors.BLUE}[*] Percobaan ke-{retry + 1}/{self.max_retries}{Colors.RESET}")
                
                # Update headers
                self.update_headers()
                
                response = self.session.post(
                    f"{self.base_url}/lists/{self.list_id}/members",
                    json=payload,
                    timeout=20,
                    verify=True
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"{Colors.GREEN}[+] Berhasil mendaftarkan {email}{Colors.RESET}")
                    print(f"{Colors.GREEN}[+] Member ID: {data['member']['id']}{Colors.RESET}")
                    print(f"{Colors.GREEN}[+] Ranking: {data['member']['rankingPosition']}{Colors.RESET}")
                    time.sleep(2)
                    return True
                    
                elif response.status_code in [401, 403, 429]:
                    print(f"{Colors.YELLOW}[!] Rate limit/expired, verifikasi ulang...{Colors.RESET}")
                    if self.verify_bot(referrer_code):
                        time.sleep(random.uniform(5, 8))
                        continue
                    else:
                        time.sleep(10)
                        return False
                    
                else:
                    print(f"{Colors.RED}[-] Gagal: {response.text}{Colors.RESET}")
                    if retry < self.max_retries - 1:
                        time.sleep(random.uniform(5, 8))
                        continue
                    
            except Exception as e:
                print(f"{Colors.RED}[-] Error: {str(e)}{Colors.RESET}")
                if retry < self.max_retries - 1:
                    time.sleep(random.uniform(5, 8))
                    continue
        
        return False

def main():
    print(f"""
{Colors.GREEN}==========================================
       Auto Referral Bot Pison v1.0      
   Support: @AirdropFamilyIDN x @ntrcd00    
=========================================={Colors.RESET}
    """)
    
    try:
        # Input API key dan referral code
        print(f"{Colors.BLUE}[*] Masukkan informasi yang diperlukan:{Colors.RESET}")
        api_key = input(f"{Colors.BLUE}[?] API Key 2captcha: {Colors.RESET}")
        referral_code = input(f"{Colors.BLUE}[?] Kode referral: {Colors.RESET}")
        
        if not api_key or not referral_code:
            print(f"{Colors.RED}[-] API key dan kode referral tidak boleh kosong{Colors.RESET}")
            return
            
        print(f"{Colors.GREEN}[+] Konfigurasi diterima{Colors.RESET}")
        print(f"{Colors.BLUE}[*] Kode referral: {referral_code}{Colors.RESET}")
            
        # Input jumlah referral
        jumlah = int(input(f"{Colors.BLUE}[?] Masukkan jumlah referral: {Colors.RESET}"))
        
        # Init bot
        bot = ReferralBot()
        
        # Verifikasi bot sebelum mulai
        print(f"{Colors.BLUE}[*] Memulai verifikasi awal...{Colors.RESET}")
        for _ in range(3):  # 3x percobaan verifikasi awal
            if bot.verify_bot(referral_code):
                break
            print(f"{Colors.YELLOW}[!] Gagal verifikasi, mencoba lagi...{Colors.RESET}")
            time.sleep(5)
        else:
            print(f"{Colors.RED}[-] Gagal verifikasi setelah 3x percobaan{Colors.RESET}")
            return
        
        # Stats
        success = 0
        failed = 0
        start_time = time.time()
        
        # Mulai loop
        for i in range(jumlah):
            current_time = time.time()
            elapsed = current_time - start_time
            rate = (success + failed) / elapsed if elapsed > 0 else 0
            
            print(f"\n{Colors.BLUE}[*] Proses referral ke-{i+1}/{jumlah}{Colors.RESET}")
            print(f"{Colors.BLUE}[*] Rate: {rate:.2f} referral/detik{Colors.RESET}")
            print(f"{Colors.BLUE}[*] Waktu berjalan: {elapsed:.0f} detik{Colors.RESET}")
            
            # Generate random email
            email = bot.get_random_email()
            
            # Solve captcha
            captcha = bot.solve_captcha(api_key, referral_code)
            if not captcha:
                print(f"{Colors.RED}[-] Gagal solve captcha, skip...{Colors.RESET}")
                failed += 1
                continue
                
            # Submit referral dengan delay dinamis
            delay = min(max(8, failed/3), 20)  
            print(f"{Colors.BLUE}[*] Delay {delay:.1f} detik sebelum submit...{Colors.RESET}")
            time.sleep(delay + random.uniform(1, 5))  
            
            if bot.submit_referral(email, referral_code, captcha):
                success += 1
                if failed > 0:  # Kurangi delay jika berhasil
                    failed = max(0, failed-1)
            else:
                failed += 1

        # Print summary
        end_time = time.time()
        total_time = end_time - start_time
        rate = (success + failed) / total_time if total_time > 0 else 0
        
        print(f"\n{Colors.BLUE}=== Summary ==={Colors.RESET}")
        print(f"{Colors.GREEN}[+] Berhasil: {success}{Colors.RESET}")
        print(f"{Colors.RED}[-] Gagal: {failed}{Colors.RESET}")
        print(f"{Colors.BLUE}[*] Total: {jumlah}{Colors.RESET}")
        print(f"{Colors.BLUE}[*] Waktu total: {total_time:.0f} detik{Colors.RESET}")
        print(f"{Colors.BLUE}[*] Rate: {rate:.2f} referral/detik{Colors.RESET}")
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[-] Program dihentikan oleh user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}[-] Error: {str(e)}{Colors.RESET}")

if __name__ == "__main__":
    main()
