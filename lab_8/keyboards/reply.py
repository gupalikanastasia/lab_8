from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_menu_reply_keyboard():
    keyboard = [
        [KeyboardButton("➕ Додати звичку"), KeyboardButton("📋 Мої звички")],
        [KeyboardButton("📊 Статистика")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)