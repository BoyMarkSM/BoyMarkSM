import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from datetime import datetime, timedelta  
import json
import os
import pytesseract
from PIL import Image
import time 
import imagehash
import requests
import re
import hashlib
import sys

# Create bot with your token
bot_token = '7354148321:AAE3dANbNB0PgZZzaFElMg1DtYrPNmctYpY'
bot = telebot.TeleBot(bot_token)

# File paths
USER_DATA_FILE = 'user_data.json'
PROCESSED_RECEIPTS_FILE = 'processed_receipts.json'

# User data management
def read_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

def write_user_data(user_id, user_data):
    all_data = read_user_data()
    all_data[str(user_id)] = user_data
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(all_data, file)

def read_processed_receipts():
    if os.path.exists(PROCESSED_RECEIPTS_FILE):
        with open(PROCESSED_RECEIPTS_FILE, 'r') as file:
            return json.load(file)
    return {}

def write_processed_receipts(receipt_id, timestamp):
    all_receipts = read_processed_receipts()
    all_receipts[receipt_id] = timestamp
    with open(PROCESSED_RECEIPTS_FILE, 'w') as file:
        json.dump(all_receipts, file)

def initialize_user(user_id):
    user_data = read_user_data()
    if str(user_id) not in user_data:
        user_info = bot.get_chat_member(user_id, user_id)
        username = user_info.user.username or "Unknown"
        name = user_info.user.first_name
        user_data[str(user_id)] = {
            'username': username,
            'name': name,
            'balance': 0.00,
            'transaction_id': None
        }
        write_user_data(user_id, user_data[str(user_id)])

# Send welcome message with keyboard
@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == '🔝 Main Menu 🔝')
@bot.message_handler(func=lambda message: message.text == '🔙 Back 🔙')
@bot.message_handler(func=lambda message: message.text == '🔙 Back')
def send_welcome(message):
    initialize_user(message.from_user.id)  # Initialize user data
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    button1 = types.KeyboardButton('Account 🛡️')
    button2 = types.KeyboardButton('🎰 Slots')
    button3 = types.KeyboardButton('🥇 payment')
    button4 = types.KeyboardButton('🎲 Lucky')
    button5 = types.KeyboardButton('Rewards 🎁')
    back_button = types.KeyboardButton('Withdraw money 💸')  # Add Back buttbutton1
    markup.add(button4, button2)
    markup.add(button1, button3, button5, back_button)  # Add back button to the markup
    welcome_message = 'សូមស្វាគមន៍មកកាន់ Tes sin'
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)



# Handle "🛡️ Account 🛡️" button clicks
@bot.message_handler(func=lambda message: message.text == 'Account 🛡️')
def handle_account(message):
    try:
        user_id = message.from_user.id
        initialize_user(user_id)  # Ensure user data is initialized
        user_data = read_user_data().get(str(user_id), {})
        user_balance = user_data.get('balance', 0)
        user_name = user_data.get('name', 'Unknown')
        user_username = user_data.get('username', 'Unknown')
        current_date = datetime.now().strftime("%Y-%m-%d")

        response_message = (f"<b>⭐------------------------------------------⭐</b>\n"
                            f" 💠<b>Name:</b> {user_name}\n"
                            f" 👤<b>Username:</b> @{user_username}\n"
                            f" 🆔<b>ID:</b> <code>{user_id}</code>\n"
                            f" 💸<b>Balance:</b> {user_balance}\n"
                            f" 📆<b>Date:</b> {current_date}\n"
                            f"<b>⭐------------------------------------------⭐</b>")
        
        bot.send_message(message.chat.id, response_message, parse_mode='HTML')
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")


# Handle "🎲 Lucky" button clicks
@bot.message_handler(func=lambda message: message.text == '🎲 Lucky')
def handle_lucky(message):
    try:
        # Create the keyboard layout
        markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        
        # Define the buttons
        button1 = KeyboardButton('🎮 Start Game 🎮')
        button2 = KeyboardButton('✉️ Resolve Issue ✉️')
        button3 = KeyboardButton('💸 Withdraw Money 💸')
        button4 = KeyboardButton('🕹️ How to Play 🕹️')
        button5 = KeyboardButton('📊 Statistics 📊')
        button6 = KeyboardButton('🔙 Back 🔙')
        button7 = KeyboardButton('🔝 Main Menu 🔝')
        
        # Add buttons to the markup
        markup.add(button4, button5)    # First row
        markup.add(button2, button1, button3) # Second row
        markup.add(button6, button7)    # Third row
        
        # Send the message with the custom keyboard
        bot.send_message(message.chat.id, "Please select an option:", reply_markup=markup)
    
    except Exception as e:
        # Handle any errors by sending an error message to the user
        bot.send_message(message.chat.id, f"Error: {str(e)}")
        # Restart the bot after sending the error message
        os.execl(sys.executable, sys.executable, *sys.argv)
        

# Handle "🎮 Start Game 🎮" button clicks
@bot.message_handler(func=lambda message: message.text == '🎮 Start Game 🎮')
def handle_start_game(message):
    try:
        markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        button1 = KeyboardButton('Boston 0.10$')
        button2 = KeyboardButton('Boston 0.20$')
        button3 = KeyboardButton('Boston 0.40$')
        button4 = KeyboardButton('Boston 0.60$')
        button5 = KeyboardButton('🔙 Back 🔙')
        button6 = KeyboardButton('🔝 Main Menu 🔝')

        markup.add(button1, button2, button3, button4)
        markup.add(button5, button6)
        
        bot.send_message(message.chat.id, "Please choose your bet amount:", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

# Handle betting amounts
@bot.message_handler(func=lambda message: message.text.startswith('Boston'))
def handle_bet_amount(message):
    try:
        amount = message.text.replace('Boston ', '').replace('$', '')
        user_id = message.from_user.id
        initialize_user(user_id)  # Ensure user data is initialized
        user_data = read_user_data()

        if str(user_id) not in user_data:
            bot.send_message(message.chat.id, "Please start the game first.")
            return

        # Store the bet amount correctly
        user_data[str(user_id)]['amount'] = float(amount)
        write_user_data(user_id, user_data[str(user_id)])

        markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        button1 = KeyboardButton('Roll 1')
        button2 = KeyboardButton('Roll 2')
        button3 = KeyboardButton('Roll 3')
        button4 = KeyboardButton('Roll 4')
        button5 = KeyboardButton('Roll 5')
        button6 = KeyboardButton('Roll 6')
        button7 = KeyboardButton('🔙 Back 🔙')
        button8 = KeyboardButton('🔝 Main Menu 🔝')

        markup.add(button1, button2, button3, button4, button5, button6)
        markup.add(button7, button8)
        
        bot.send_message(message.chat.id, f"Your bet amount is {amount}$. Please ce the number of dice to roll:", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {stExceptionce}")


# Function to log wins to a file
def log_win_to_file(user_id, winnings, dice_choice, dice_value):
    try:
        log_entry = (f"User ID: {user_id}, "
                     f"Winnings: {winnings}$, "
                     f"Dice Choice: {dice_choice}, "
                     f"Dice Value: {dice_value}\n")
        with open('win_log.txt', 'a') as f:
            f.write(log_entry)

    except Exception as e:
        print(f"Error logging win to file: {str(e)}")

@bot.message_handler(func=lambda message: message.text.startswith('Roll'))
def handle_dice_choice(message):
    try:
        dice_choice = int(message.text.replace('Roll ', ''))
        user_id = message.from_user.id
        user_data = read_user_data()
        bet_amount = user_data.get(str(user_id), {}).get('amount', 0.0)
        user_balance = user_data.get(str(user_id), {}).get('balance', 0.0)

        if user_balance < bet_amount:
            bot.send_message(message.chat.id, "💰 <b>បាល់នឹងមានតំលៃមិនគ្រប់គ្រាន់សម្រាប់ការភ្នាល់នេះទេ</b>", parse_mode='HTML')
            return

        # Update user balance by deducting the bet amount
        user_data[str(user_id)]['balance'] -= bet_amount
        write_user_data(user_id, user_data[str(user_id)])

        # Send confirmation message
        confirmation_message = (f"📊 <b>ចំនួនទឹកប្រាក់ដែលបានភ្នាល់:</b> <u>{bet_amount}$</u>\n"
                                f"🎲 <b>ជ្រើសរើសលេខលុកឡាក់:</b> <u>{dice_choice}</u>\n"
                                f"💵 <b>សមតុល្យបច្ចុប្បន្ន:</b> <u>{user_data[str(user_id)]['balance']}$</u>")
        bot.send_message(message.chat.id, confirmation_message, parse_mode='HTML')

        # Simulate dice roll
        dice_message = bot.send_dice(message.chat.id, emoji='🎲')
        dice_value = dice_message.dice.value

        # Wait before sending the result
        time.sleep(3.5)

        # Send dice result
        bot.send_message(message.chat.id, f"🎲 <b>លទ្ធផល:</b> <u>{dice_value}</u>", parse_mode='HTML')

        # Check if the result matches the user's choice
        if dice_value == dice_choice:
            winnings = 2 * bet_amount
            bot.send_message(message.chat.id, f"🎉 <b>អបអរសាទរ!</b> 🏆 អ្នកបានឈ្នះ <u>{winnings}$</u>!", parse_mode='HTML')
            user_data[str(user_id)]['balance'] += winnings

            # Log the win to the file
            log_win_to_file(user_id, winnings, dice_choice, dice_value)
            
            # Send win data to the channel with enhanced styling
            win_message = (f"🔔 <b>ជោគជ័យ! អ្នកប្រើប្រាស់ <code>{user_id}</code> បានឈ្នះ <u>{winnings}$</u> 🎉</b>\n"
                           f"🎲 <b>លទ្ធផល:</b> <u>{dice_value}</u> (ជម្រើស: {dice_choice})\n"
                           f"💵 <b>សមតុល្យថ្មី:</b> <u>{user_data[str(user_id)]['balance']}$</u>\n💠 bot @good_luck_kh_robot")
            bot.send_message('@tes_sin', win_message, parse_mode='HTML')

        else:
            bot.send_message(message.chat.id, "😢 <b>សូមទោស អ្នកបានចាញ់</b> បូកប្រាក់ភ្នាល់វិញ!", parse_mode='HTML')

        # Update the user balance in the database
        write_user_data(user_id, user_data[str(user_id)])

    except Exception as e:
        bot.send_message(message.chat.id, f"❗ <b>កំហុស:</b> {str(e)}", parse_mode='HTML')
        
        

# Handle Back button clicks
@bot.message_handler(func=lambda message: message.text == '🔙 Back 🔙')
def handle_back(message):
    send_welcome(message)

# Handle "🔝 Main Menu 🔝" button clicks
@bot.message_handler(func=lambda message: message.text == '🔝 Main Menu 🔝')
def handle_main_menu(message):
    send_welcome(message)

# Handle "/userbalance" command for admin
@bot.message_handler(commands=['userbalance'])
def handle_user_balance(message):
    if message.from_user.id == 6555584010:
        bot.send_message(message.chat.id, "Please provide the user ID and the balance amount to adjust")
        bot.register_next_step_handler(message, process_user_balance_request)
    else:
        bot.send_message(message.chat.id, "You do not have permission to use this command")

def process_user_balance_request(message):
    try:
        user_input = message.text.split()
        user_id = int(user_input[0])
        amount = float(user_input[1])

        user_data = read_user_data()
        if str(user_id) in user_data:
            user = user_data[str(user_id)]
            user_name = user['name']
            user_username = user['username']
            user_balance = user['balance']
            current_date = datetime.now().strftime("%Y-%m-%d")

            response_message = (f"<b>⭐------------------------------------------⭐</b>\n"
                                f" 👉<b>Name:</b> {user_name}\n"
                                f" 👉<b>Username:</b> @{user_username}\n"
                                f" 👉<b>ID:</b> <code>{user_id}</code>\n"
                                f" 👉<b>Balance:</b> {user_balance}\n"
                                f" 👉<b>Date:</b> {current_date}📆\n"
                                f"<b>⭐------------------------------------------⭐</b>")
            
            bot.send_message(message.chat.id, response_message, parse_mode='HTML')
            bot.send_message(message.chat.id, "Would you like to add or subtract the balance? Please reply with + or -.")
            bot.register_next_step_handler(message, lambda msg: confirm_balance_update(msg, user_id, amount))
        else:
            bot.send_message(message.chat.id, "User ID not found")

    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

def confirm_balance_update(message, user_id, amount):
    try:
        user_data = read_user_data()
        if message.text == '+':
            if str(user_id) in user_data:
                user_data[str(user_id)]['balance'] += amount
                write_user_data(user_id, user_data[str(user_id)])
                bot.send_message(message.chat.id, f"Balance increased by {amount}$ for user ID {user_id}!")
                bot.send_message(user_id, f"Your balance has been increased by {amount}$.")
        elif message.text == '-':
            if str(user_id) in user_data:
                user_data[str(user_id)]['balance'] -= amount
                write_user_data(user_id, user_data[str(user_id)])
                bot.send_message(message.chat.id, f"Balance decreased by {amount}$ for user ID {user_id}!")
                bot.send_message(user_id, f"Your balance has been decreased by {amount}$.")
        else:
            bot.send_message(message.chat.id, "Invalid response. Please use the command again and reply with + or -.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

# Handle "/data" command for admin
@bot.message_handler(commands=['data'])
def handle_data(message):
    if message.from_user.id == 6555584010:
        user_data = read_user_data()
        total_users = len(user_data)
        if total_users == 0:
            bot.send_message(message.chat.id, "No user data available.")
            return
        
        # Find the user with the highest balance
        highest_balance_user = max(user_data.items(), key=lambda x: x[1]['balance'])
        highest_balance_user_id = highest_balance_user[0]
        highest_balance_user_info = highest_balance_user[1]
        highest_balance = highest_balance_user_info['balance']

        # Calculate the total balance of all users
        total_balance = sum(user['balance'] for user in user_data.values())

        # Prepare the response message
        response_message = (f"<b>Total Users:</b> {total_users}\n"
                            f"<b>User with Highest Balance:</b> {highest_balance_user_info['name']} "
                            f"(Username: {highest_balance_user_info['username']}, "
                            f"ID: {highest_balance_user_id}, "
                            f"Balance: {highest_balance}$)\n"
                            f"<b>Total Balance of All Users:</b> {total_balance}$")
        
        bot.send_message(message.chat.id, response_message, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "You do not have permission to use this command")

# Handle "/messages" command for admin
@bot.message_handler(commands=['messages'])
def handle_messages(message):
    if message.from_user.id == 6555584010:
        bot.send_message(message.chat.id, "Please provide the message text and emoji (e.g., Hello 😊)")
        bot.register_next_step_handler(message, process_message_request)
    else:
        bot.send_message(message.chat.id, "You do not have permission to use this command")

def process_message_request(message):
    try:
        # Send a confirmation request to send or cancel the message
        user_input = message.text
        admin_id = message.from_user.id

        # Create confirmation keyboard
        markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button1 = KeyboardButton('Send')
        button2 = KeyboardButton('Cancel')
        markup.add(button1, button2)
        
        bot.send_message(admin_id, "Would you like to send this message or cancel?", reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: confirm_message_send(msg, user_input))
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

def confirm_message_send(message, user_input):
    try:
        if message.text == 'Send':
            user_data = read_user_data()
            for user_id in user_data:
                bot.send_message(user_id, user_input)
            bot.send_message(message.chat.id, "Message sent to all users!")
        elif message.text == 'Cancel':
            bot.send_message(message.chat.id, "Message sending canceled.")
        else:
            bot.send_message(message.chat.id, "Invalid response. Please use the command again.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")



# Handle '🥇 payment' button click
@bot.message_handler(func=lambda message: message.text == '🥇 payment')
def handle_payment(message):
    try:
        user_id = message.from_user.id
        initialize_user(user_id)

        bot.send_message(message.chat.id, "សូមស្នើចំនួនទឹកប្រាក់ដែលអ្នកបានបង់:")
        
        bot.register_next_step_handler(message, process_payment_amount)
    except Exception as e:
        bot.send_message(message.chat.id, f"កំហុស: {str(e)}")
        # Restart the bot after sending the error message
        os.execl(sys.executable, sys.executable, *sys.argv)

def process_payment_amount(message):
    try:
        amount = float(message.text)
        user_id = message.from_user.id
        
        user_data = read_user_data()
        user_data[str(user_id)]['payment_amount'] = amount
        write_user_data(user_id, user_data[str(user_id)])
        
        # Send the image URL
        bot.send_photo(message.chat.id, photo='https://telegra.ph/file/062c1606a780c819142e6.jpg')
        bot.send_message(message.chat.id, "សូមផ្ដល់រូបភាពវិក្កយបត្រ។")
        
        bot.register_next_step_handler(message, process_receipt_image)
    except Exception as e:
        bot.send_message(message.chat.id, f"កំហុស: {str(e)}")
        # Restart the bot after sending the error message
        os.execl(sys.executable, sys.executable, *sys.argv)

def process_receipt_image(message):
    try:
        if message.photo:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            file_path = f"{file_id}.jpg"
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            user_id = message.from_user.id
            user_data = read_user_data()
            payment_amount = user_data[str(user_id)].get('payment_amount', 0.0)

            # Sending to admin
            admin_id = 6555584010
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
            correct_button = telebot.types.KeyboardButton("✅ ត្រឹមត្រូវ")
            incorrect_button = telebot.types.KeyboardButton("❌ មិនត្រឹមត្រូវ")
            markup.add(correct_button, incorrect_button)
            bot.send_message(admin_id, "សូមផ្តល់ការបញ្ជាក់៖", reply_markup=markup)

            bot.send_photo(admin_id, photo=open(file_path, 'rb'), caption=f"វិក្កយបត្រ: {file_path}\nចំនួនទឹកប្រាក់: {payment_amount}")

            bot.register_next_step_handler_by_chat_id(admin_id, lambda msg: verify_payment(msg, payment_amount, file_path, user_id))
        else:
            bot.send_message(message.chat.id, "សូមផ្តល់រូបភាពវិក្កយបត្រ។")
    except Exception as e:
        bot.send_message(message.chat.id, f"កំហុស: {str(e)}")
        # Restart the bot after sending the error message
        os.execl(sys.executable, sys.executable, *sys.argv)

def verify_payment(message, payment_amount, file_path, user_id):
    if message.text == "✅ ត្រឹមត្រូវ":
        user_data = read_user_data()
        user_data[str(user_id)]['balance'] += payment_amount
        write_user_data(user_id, user_data[str(user_id)])

        # Sending confirmation to channel
        channel_username = "@tes_sin"
        bot.send_message(channel_username, f"🟢 **ការទូទាត់ត្រូវបានផ្ទៀងផ្ទាត់**\n\n🔹 **អ្នកប្រើ**: {user_id}\n🔹 **ចំនួនទឹកប្រាក់**: {payment_amount}\n🔹 **វិក្កយបត្រ**: {file_path}\n💠bot @good_luck_kh_robot\n", parse_mode='Markdown')
        
        bot.send_message(message.chat.id, "ការទូទាត់ត្រូវបានផ្ទៀងផ្ទាត់ដោយជោគជ័យ! /start")
    elif message.text == "❌ មិនត្រឹមត្រូវ":
        bot.send_message(message.chat.id, "ការទូទាត់មិនត្រឹមត្រូវ។ /start")
        
        

    os.remove(file_path)  # Clean up the image file after processing
    
import json
import time
from datetime import datetime, timedelta

# Initialize rewards data
def initialize_rewards(user_id):
    try:
        with open('user_rewards.json', 'r') as f:
            rewards_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        rewards_data = {}

    if str(user_id) not in rewards_data:
        rewards_data[str(user_id)] = {
            'balance': 0.0,
            'last_redeem_time': '',
            'referral_count': 0
        }

    with open('user_rewards.json', 'w') as f:
        json.dump(rewards_data, f, indent=4)

    return rewards_data

# Update rewards data
def update_rewards(user_id, data):
    with open('user_rewards.json', 'r') as f:
        rewards_data = json.load(f)

    rewards_data[str(user_id)].update(data)

    with open('user_rewards.json', 'w') as f:
        json.dump(rewards_data, f, indent=4)

# Handle "Rewards 🎁" button click
@bot.message_handler(func=lambda message: message.text == 'Rewards 🎁')
def handle_rewards(message):
    try:
        markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        button1 = KeyboardButton('Recommend a Friend 🃏')
        button2 = KeyboardButton('Redeem 🎉')
        button3 = KeyboardButton('🔙 Back')

        markup.add(button1, button2)
        markup.add(button3)
        
        bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)
    
    except Exception as e:
        bot.send_message(message.chat.id, f"❗ Error: {str(e)}")

# Handle "Recommend a Friend 🃏" button click
@bot.message_handler(func=lambda message: message.text == 'Recommend a Friend 🃏')
def handle_recommend_friend(message):
    try:
        user_id = message.from_user.id
        initialize_rewards(user_id)
        
        referral_link = f"https://t.me/good_luck_kh_robot?start={user_id}"
        update_rewards(user_id, {'balance': 0.05})
        
        bot.send_message(message.chat.id, f"Share this referral link with your friends:\n{referral_link}\nYou earned $0.05!")

    except Exception as e:
        bot.send_message(message.chat.id, f"❗ Error: {str(e)}")

# Handle "Redeem 🎉" button click
@bot.message_handler(func=lambda message: message.text == 'Redeem 🎉')
def handle_redeem(message):
    try:
        user_id = message.from_user.id
        rewards_data = initialize_rewards(user_id)
        user_rewards = rewards_data[str(user_id)]

        current_time = datetime.now()
        last_redeem_time_str = user_rewards.get('last_redeem_time')
        last_redeem_time = datetime.strptime(last_redeem_time_str, "%Y-%m-%d %H:%M:%S") if last_redeem_time_str else None
        
        if last_redeem_time and current_time - last_redeem_time < timedelta(hours=24):
            time_remaining = timedelta(hours=24) - (current_time - last_redeem_time)
            bot.send_message(message.chat.id, f"You can redeem again in {time_remaining}.")
        else:
            new_balance = user_rewards['balance'] + 0.025
            update_rewards(user_id, {
                'balance': new_balance,
                'last_redeem_time': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })

            bot.send_message(message.chat.id, f"You have successfully redeemed $0.025! Your new balance is ${new_balance}.")

    except Exception as e:
        bot.send_message(message.chat.id, f"❗ Error: {str(e)}")

# Handle "🔙 Back 🔙" button clicks
@bot.message_handler(func=lambda message: message.text == 'Back ⬅️')
def handle_back(message):
    send_welcome(message)

import telebot
import random
import time
import json
from telebot import types



# Function to read user data from a file
def read_user_data():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to write user data to a file
def write_user_data(user_id, data):
    user_data = read_user_data()
    user_data[str(user_id)] = data
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

# Function to initialize user
def initialize_user(user_id):
    user_data = read_user_data()
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {'balance': 100}  # Initialize with default balance
        write_user_data(user_id, user_data[str(user_id)])

# Command to start the slots game
@bot.message_handler(func=lambda message: message.text == '🎰 Slots')
def select_bet_amount(message):
    user_id = message.from_user.id
    initialize_user(user_id)  # Make sure user is initialized

    # Create a keyboard for bet amounts
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    bet_1_button = types.KeyboardButton('1$')
    bet_2_button = types.KeyboardButton('2$')
    bet_5_button = types.KeyboardButton('5$')
    bet_10_button = types.KeyboardButton('10$')
    back_button = types.KeyboardButton('🔙 Back')

    markup.add(bet_1_button, bet_2_button, bet_5_button, bet_10_button, back_button)

    bot.send_message(message.chat.id, "🎲 *សូមជ្រើសរើសតម្លៃនៃការភ្នាល់*:", parse_mode='Markdown', reply_markup=markup)

    bot.register_next_step_handler(message, process_bet_amount)

def process_bet_amount(message):
    user_id = message.from_user.id
    user_data = read_user_data()

    if message.text in ['1$', '2$', '5$', '10$']:
        bet_amount = float(message.text[:-1])  # Get the numeric value

        if user_data[str(user_id)]['balance'] >= bet_amount:
            # Proceed with the slots game
            play_slots(message, bet_amount)
        else:
            bot.send_message(message.chat.id, "💵 *អ្នកមានប្រាក់មិនគ្រប់គ្រាន់សម្រាប់ការភ្នាល់នេះ។ សូមជ្រើសរើសម្តងទៀត!*", parse_mode='Markdown')
            select_bet_amount(message)  # Re-show the bet amount options
    elif message.text == '🔙 Back':
        # Call the function to handle going back to the main menu
        handle_back(message)  # Go back to the welcome or previous menu
    else:
        bot.send_message(message.chat.id, "⚠️ *សូមជ្រើសរើសតម្លៃនៃការភ្នាល់ដែលបានផ្តល់*.", parse_mode='Markdown')
        select_bet_amount(message)

def play_slots(message, bet_amount):
    user_id = message.from_user.id
    user_data = read_user_data()

    # Update user balance after deducting the bet amount
    user_data[str(user_id)]['balance'] -= bet_amount
    write_user_data(user_id, user_data[str(user_id)])

    # Define slot options
    slot_options = ['🍒', '🍋', '🔔', '⭐', '🍉', '🍇']

    # Get the current balance
    current_balance = user_data[str(user_id)]['balance']

    # Animation for slots with current balance
    bot.send_message(message.chat.id, f"🎰 *កំពុងដំណើរស្លុត...* 🎰\n\n💰 *ចំនួនប្រាក់បច្ចុប្បន្នរបស់អ្នក: {current_balance}$*", parse_mode='Markdown')
    time.sleep(1)

    # Simulate slot machine spin
    slot_result = []
    for i in range(3):
        slot_result.append(random.choice(slot_options))
        bot.send_message(message.chat.id, f"🎰 | {' | '.join(slot_result)} | 🎰", parse_mode='Markdown')
        time.sleep(1)
    
    # Final result
    result_message = f"🎰 | {' | '.join(slot_result)} | 🎰\n\n"
    
    # Check for winning combinations
    if slot_result[0] == slot_result[1] == slot_result[2]:
        prize = bet_amount * 2  # Double the bet amount for the prize
        result_message += f"🏆 *Congratulations! You won {prize}$!*"
        
        # Update user's balance with the prize
        user_data[str(user_id)]['balance'] += prize
        write_user_data(user_id, user_data[str(user_id)])

        # Log win to file
        log_win(user_id, bet_amount, prize)

        # Send notification to the channel
        notify_channel(user_id, bet_amount, prize)
    else:
        result_message += "😢 *Sorry, you lost. Better luck next time!*"

    # Send the final result message to the user
    bot.send_message(message.chat.id, result_message, parse_mode='Markdown')

    # Ask if the user wants to play again
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    play_again_button = types.KeyboardButton('🎰 Play Again')
    back_button = types.KeyboardButton('🔙 Back')

    markup.add(play_again_button, back_button)
    bot.send_message(message.chat.id, "🎮 *Do you want to play again?* 🎮", parse_mode='Markdown', reply_markup=markup)

def log_win(user_id, bet_amount, prize):
    with open('win_log.txt', 'a') as log_file:
        log_file.write(f"User {user_id} bet {bet_amount}$ and won {prize}$\n")

def notify_channel(user_id, bet_amount, prize):
    channel_username = "@tes_sin"  # Replace with your channel username or ID
    message = (
        f"<b>🟢 អ្នកឈ្នះ!</b>\n\n"
        f"<b>🔹 ID អ្នកប្រើ:</b> {user_id}\n"
        f"<b>🔹 ចំនួនភ្នាល់:</b> {bet_amount}$\n"
        f"<b>🔹 ចំនួនឈ្នះ:</b> {prize}$\n"
        f"<b>💠bot @good_luck_kh_robot</b>\n"
    )
    try:
        bot.send_message(channel_username, message, parse_mode='HTML')
    except Exception as e:
        print(f"Error sending message to channel: {e}")
        
        

# Handle "🔙 Back 🔙" button clicks
@bot.message_handler(func=lambda message: message.text == '🔙 Back')
def handle_back(message):
    send_welcome(message)  # Define the send_welcome function

# Handle "🎰 Play Again" button clicks
@bot.message_handler(func=lambda message: message.text == '🎰 Play Again')
def handle_play_again(message):
    select_bet_amount(message)

# Polling to keep the bot running continuously
bot.polling(none_stop=True)
