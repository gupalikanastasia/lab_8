from telegram import Update
from telegram.ext import ContextTypes
from states.user_states import HabitTrackerStates
from keyboards.reply import main_menu_keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Привіт! 👋 Я допоможу тобі формувати корисні звички.",
        reply_markup=main_menu_keyboard()
    )
    return HabitTrackerStates.MAIN_MENU

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "💡 Довідка:\n1. Додай звичку\n2. Відмічай виконання\n3. Слідкуй за прогресом"
    await update.message.reply_text(text)

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Скасовано.", reply_markup=main_menu_keyboard())
    return HabitTrackerStates.MAIN_MENU