import requests
import json
import time
import random
import string
from typing import Dict, Tuple

class ReferralBot:
    def __init__(self):
        self.base_url = "https://audience-consumer-api.zootools.co/v3"
        self.list_id = "Qkr0xCL2rXK0nY39DAO2"
        self.headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "origin": "https://form.zootools.co",
            "referer": "https://form.zootools.co/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }

    def get_random_email(self) -> str:
        """Generate random email"""
        domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = random.choice(domains)
        return f"{username}@{domain}"

    def solve_captcha(self, api_key: str, referral_code: str) -> str:
        """Solve captcha using 2captcha"""
        try:
            print("[*] Memulai solve captcha...")
            
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
            print(f"[+] Captcha submitted, ID: {captcha_id}")
            
            # Polling untuk hasil
            for _ in range(30):  # Max 5 menit (30 x 10 detik)
                time.sleep(10)
                result_response = requests.get(
                    f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}'
                )
                
                if result_response.text.startswith('OK|'):
                    token = result_response.text.split('|')[1]
                    print("[+] Captcha solved!")
                    return token
                    
                if "ERROR" in result_response.text:
                    raise Exception(f"Error dari 2captcha: {result_response.text}")
                    
                print("[*] Menunggu hasil captcha...")
            
            raise Exception("Timeout menunggu hasil captcha")
            
        except Exception as e:
            print(f"[-] Error solving captcha: {str(e)}")
            return None

    def submit_referral(self, email: str, referrer_code: str, captcha_token: str = None) -> bool:
        """Submit referral ke Zootools"""
        payload = {
            "email": email,
            "referral": referrer_code,
            "captchaToken": captcha_token,
            "source": "online_form",
            "fields": {"hasAccess": False},
            "hiddenFields": {}
        }

        try:
            print(f"\n[*] Mencoba mendaftarkan: {email}")
            print(f"[*] Kode referral: {referrer_code}")
            
            response = requests.post(
                f"{self.base_url}/lists/{self.list_id}/members",
                json=payload,
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"[+] Berhasil mendaftarkan {email}")
                print(f"[+] Member ID: {data['member']['id']}")
                print(f"[+] Ranking: {data['member']['rankingPosition']}")
                return True
            else:
                print(f"[-] Gagal: {response.text}")
                return False
                
        except Exception as e:
            print(f"[-] Error: {str(e)}")
            return False

def main():
    print("""
==========================================
       Auto Referral Bot Pison v1.0      
   Support: @AirdropFamilyIDN x @ntrcd00    
==========================================
    """)
    
    try:
        # Input dari user
        api_key = input("[?] Masukkan API Key 2captcha: ")
        referral_code = input("[?] Masukkan kode referral: ")
        jumlah = int(input("[?] Masukkan jumlah referral: "))
        
        # Init bot
        bot = ReferralBot()
        
        # Stats
        success = 0
        failed = 0
        
        # Mulai loop
        for i in range(jumlah):
            print(f"\n[*] Proses referral ke-{i+1}/{jumlah}")
            
            # Generate random email
            email = bot.get_random_email()
            
            # Solve captcha
            captcha = bot.solve_captcha(api_key, referral_code)
            if not captcha:
                print("[-] Gagal solve captcha, skip...")
                failed += 1
                continue
                
            # Submit referral
            if bot.submit_referral(email, referral_code, captcha):
                success += 1
            else:
                failed += 1
            
            # Delay random 3-7 detik
            delay = random.uniform(3, 7)
            print(f"[*] Delay {delay:.1f} detik...")
            time.sleep(delay)

        # Print summary
        print("\n=== Summary ===")
        print(f"[+] Berhasil: {success}")
        print(f"[-] Gagal: {failed}")
        print(f"[*] Total: {jumlah}")
        
    except KeyboardInterrupt:
        print("\n\n[-] Program dihentikan oleh user")
    except Exception as e:
        print(f"\n[-] Error: {str(e)}")

if __name__ == "__main__":
    main()