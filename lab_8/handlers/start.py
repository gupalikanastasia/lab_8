from telegram import Update
from telegram.ext import ContextTypes
from states.user_states import HabitTrackerStates
from keyboards.reply import main_menu_reply_keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user    # Дізнаємося, хто нам написав (ім'я, ID)
    await update.message.reply_text(
        f"Привіт, {user.first_name}! 👋\nЯ допоможу тобі формувати корисні звички.\n\nТисни на кнопки знизу 👇",
        reply_markup=main_menu_reply_keyboard()
    )
    return HabitTrackerStates.MAIN_MENU

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "💡 Використовуй меню внизу екрану."
    await update.message.reply_text(text)

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Скасовано.", reply_markup=main_menu_reply_keyboard())
    return HabitTrackerStates.MAIN_MENU