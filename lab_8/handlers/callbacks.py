from telegram import Update
from telegram.ext import ContextTypes
from database import db
from config import DEFAULT_HABITS
from states.user_states import HabitTrackerStates

from keyboards.inline import (
    habit_source_keyboard, default_habits_keyboard,
    goal_days_keyboard, habits_list_keyboard, single_habit_keyboard,
    reminder_time_keyboard
)
from keyboards.reply import main_menu_reply_keyboard


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id

    await query.answer()  # Прибираємо "годинничок" завантаження

    # --- ДОДАВАННЯ ЗВИЧКИ ---
    if data == 'add_habit':
        await query.edit_message_text("Як додати?", reply_markup=habit_source_keyboard())
        return HabitTrackerStates.CHOOSING_HABIT

    if data == 'choose_default':
        await query.edit_message_text("Обери:", reply_markup=default_habits_keyboard())
        return HabitTrackerStates.CHOOSING_HABIT

    if data == 'add_custom':
        await query.edit_message_text("Напиши назву звички у чат 👇")
        return HabitTrackerStates.ENTERING_CUSTOM_HABIT

    if data.startswith('def_habit_'):
        index = int(data.split('_')[-1])
        habit_name = DEFAULT_HABITS[index]
        context.user_data['temp_habit_name'] = habit_name

        await query.edit_message_text(
            f"Звичка: {habit_name}. Скільки днів виконуємо?",
            reply_markup=goal_days_keyboard()
        )
        return HabitTrackerStates.SETTING_GOAL_DAYS

    if data.startswith('days_'):
        days = int(data.split('_')[-1])
        name = context.user_data.get('temp_habit_name', 'Нова звичка')

        db.add_habit(user_id, name, days)

        # Після успішного додавання теж видаляємо Inline і показуємо Reply
        await query.message.delete()
        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ Готово! Звичка '{name}' створена на {days} днів.",
            reply_markup=main_menu_reply_keyboard()
        )
        return HabitTrackerStates.MAIN_MENU

    # --- СПИСОК ЗВИЧОК ---
    if data == 'view_habits':
        user_habits = db.get_habits(user_id)
        if not user_habits:
            await query.edit_message_text("Список порожній 🤷‍♂️",
                                          reply_markup=main_menu_reply_keyboard())
            return HabitTrackerStates.MAIN_MENU

        await query.edit_message_text(
            "Твої звички (натисни для дій):",
            reply_markup=habits_list_keyboard(user_habits)
        )
        return HabitTrackerStates.MANAGING_HABITS

    if data.startswith('habit_'):
        habit_id = data.replace('habit_', '')
        habit = None
        for h in db.get_habits(user_id):
            if h.id == habit_id:
                habit = h
                break

        if habit:
            info = f"📝 **{habit.name}**\nЦіль: {habit.goal_days} днів"
            await query.edit_message_text(info, reply_markup=single_habit_keyboard(habit_id), parse_mode='Markdown')
        else:
            await query.edit_message_text("Помилка: звичку не знайдено")
        return HabitTrackerStates.MANAGING_HABITS

    # --- ДІЇ ЗІ ЗВИЧКОЮ ---
    if data.startswith('done_'):
        habit_id = data.replace('done_', '')
        if db.mark_completed(user_id, habit_id):
            await query.answer()

        user_habits = db.get_habits(user_id)
        await query.edit_message_text("Твої звички:", reply_markup=habits_list_keyboard(user_habits))
        return HabitTrackerStates.MAIN_MENU  # Залишаємось в перегляді списку, але технічно це стан MAIN_MENU або MANAGING

    if data.startswith('delete_'):
        habit_id = data.replace('delete_', '')
        db.delete_habit(user_id, habit_id)
        await query.answer()

        user_habits = db.get_habits(user_id)
        await query.edit_message_text("Твої звички:", reply_markup=habits_list_keyboard(user_habits))
        return HabitTrackerStates.MAIN_MENU

    # --- НАГАДУВАННЯ ---
    if data.startswith('remind_'):
        habit_id = data.replace('remind_', '')
        await query.edit_message_text(
            "О котрій годині нагадувати?",
            reply_markup=reminder_time_keyboard(habit_id)
        )
        return HabitTrackerStates.CHOOSING_REMINDER_TIME

    if data.startswith('time_'):
        parts = data.split('_')
        habit_id = parts[1]
        time = parts[2]

        db.set_reminder(user_id, habit_id, time)
        await query.answer()

        # Видаляємо повідомлення і вертаємось в головне меню
        await query.message.delete()
        await context.bot.send_message(
            chat_id=user_id,
            text="Готово! 👌",
            reply_markup=main_menu_reply_keyboard()
        )
        return HabitTrackerStates.MAIN_MENU

    return HabitTrackerStates.MAIN_MENU