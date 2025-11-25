from telegram import Update
from telegram.ext import ContextTypes
from states.user_states import HabitTrackerStates
from database import db
from keyboards.inline import (
    habit_source_keyboard,
    habits_list_keyboard,
    goal_days_keyboard
)
from keyboards.reply import main_menu_reply_keyboard


async def main_menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    # 1. Якщо натиснули "Додати звичку"
    if text == "➕ Додати звичку":
        await update.message.reply_text(
            "Як хочеш додати звичку?",
            reply_markup=habit_source_keyboard()  # Показуємо меню вибору (Inline)
        )
        return HabitTrackerStates.CHOOSING_HABIT

    elif text == "📋 Мої звички":
        user_habits = db.get_habits(user_id)
        if not user_habits:
            await update.message.reply_text("Список порожній 🤷‍♂️ Додай першу звичку!")
            return HabitTrackerStates.MAIN_MENU

        await update.message.reply_text(
            "Твої звички (натисни для дій):",
            reply_markup=habits_list_keyboard(user_habits)
        )
        return HabitTrackerStates.MANAGING_HABITS

    elif text == "📊 Статистика":
        user_habits = db.get_habits(user_id)
        if not user_habits:
            await update.message.reply_text("Даних ще немає. Почни виконувати звички!")
        else:
            stats = "\n".join([f"🔹 {h.name}: {len(h.completed_days)}/{h.goal_days} днів" for h in user_habits])
            await update.message.reply_text(f"📊 **Твоя статистика:**\n\n{stats}", parse_mode='Markdown')
        return HabitTrackerStates.MAIN_MENU

    else:
        await update.message.reply_text(
            "Будь ласка, натискай на кнопки меню 👇",
            reply_markup=main_menu_reply_keyboard()
        )
        return HabitTrackerStates.MAIN_MENU


async def custom_habit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    habit_name = update.message.text
    context.user_data['temp_habit_name'] = habit_name
    await update.message.reply_text(
        f"Звичка '{habit_name}'. Скільки днів виконуємо?",
        reply_markup=goal_days_keyboard()
    )
    return HabitTrackerStates.SETTING_GOAL_DAYS