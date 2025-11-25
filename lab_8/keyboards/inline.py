from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import DEFAULT_HABITS, DEFAULT_REMINDER_TIMES

def habit_source_keyboard():
    keyboard = [
        [InlineKeyboardButton("💡 Вибрати з готових", callback_data='choose_default')],
        [InlineKeyboardButton("✍️ Написати свою", callback_data='add_custom')],
    ]
    return InlineKeyboardMarkup(keyboard)


def default_habits_keyboard():
    keyboard = []
    for i, habit in enumerate(DEFAULT_HABITS):
        keyboard.append([InlineKeyboardButton(habit, callback_data=f'def_habit_{i}')])
    return InlineKeyboardMarkup(keyboard)


def habits_list_keyboard(user_habits):
    keyboard = []
    if not user_habits:
        return InlineKeyboardMarkup([])

    for habit in user_habits:
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        status = "✅" if today in habit.completed_days else "🔹"
        keyboard.append([InlineKeyboardButton(f"{status} {habit.name}", callback_data=f'habit_{habit.id}')])

    return InlineKeyboardMarkup(keyboard)


def single_habit_keyboard(habit_id):
    keyboard = [
        [InlineKeyboardButton("✅ Виконано сьогодні", callback_data=f'done_{habit_id}')],
        [InlineKeyboardButton("⏰ Нагадування", callback_data=f'remind_{habit_id}')],
        [InlineKeyboardButton("🗑 Видалити", callback_data=f'delete_{habit_id}')],
    ]
    return InlineKeyboardMarkup(keyboard)


def goal_days_keyboard():
    keyboard = []
    days = [7, 21, 30, 90]
    row = []
    for d in days:
        row.append(InlineKeyboardButton(f"{d} днів", callback_data=f'days_{d}'))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row: keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)


def reminder_time_keyboard(habit_id):
    keyboard = []
    for time in DEFAULT_REMINDER_TIMES:
        keyboard.append([InlineKeyboardButton(f"⏰ {time}", callback_data=f'time_{habit_id}_{time}')])
    return InlineKeyboardMarkup(keyboard)