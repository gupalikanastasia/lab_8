import logging
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ConversationHandler
)
from config import BOT_TOKEN
from states.user_states import HabitTrackerStates
from database import db

from handlers.start import start_command, help_command, cancel_command
from handlers.messages import custom_habit_handler, main_menu_text_handler
from handlers.callbacks import button_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
) #Вигляд повідомлень в консолі


async def send_reminders(context):                             #Перевірка/відправка нагадувань
    current_time = datetime.now().strftime('%H:%M')            # Отримуємо поточний час, наприклад "14:30"
    habits = db.get_habits_with_reminders()                    # Питаємо базу: кому треба нагадати?
    for user_id, habit in habits:                              # Перебираємо всіх знайдених людей
        if habit.reminder_time == current_time:
            try:
                await context.bot.send_message(chat_id=user_id, text=f"🔔 Час для звички: {habit.name}")
            except:
                pass


def main():
    print("Запуск бота...")
    app = Application.builder().token(BOT_TOKEN).build() #Створюємо бота

    text_filter = filters.TEXT & ~filters.COMMAND    # Спільний фільтр для текстових повідомлень

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)], #Команда старт
        states={
            # ГОЛОВНЕ МЕНЮ
            HabitTrackerStates.MAIN_MENU: [
                MessageHandler(text_filter, main_menu_text_handler),
                CallbackQueryHandler(button_handler)
            ],

            HabitTrackerStates.CHOOSING_HABIT: [
                CallbackQueryHandler(button_handler),
                MessageHandler(text_filter, main_menu_text_handler)
            ],

            HabitTrackerStates.ENTERING_CUSTOM_HABIT: [
                MessageHandler(text_filter, custom_habit_handler)
            ],

            HabitTrackerStates.SETTING_GOAL_DAYS: [
                CallbackQueryHandler(button_handler),
                MessageHandler(text_filter, main_menu_text_handler)
            ],

            HabitTrackerStates.MANAGING_HABITS: [
                CallbackQueryHandler(button_handler),
                MessageHandler(text_filter, main_menu_text_handler)
            ],

            HabitTrackerStates.SETTING_REMINDER: [
                CallbackQueryHandler(button_handler),
                MessageHandler(text_filter, main_menu_text_handler)
            ],

            HabitTrackerStates.CHOOSING_REMINDER_TIME: [
                CallbackQueryHandler(button_handler),
                MessageHandler(text_filter, main_menu_text_handler)
            ],

            HabitTrackerStates.VIEWING_STATS: [
                CallbackQueryHandler(button_handler),
                MessageHandler(text_filter, main_menu_text_handler)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)], #Вихід
    )

    app.add_handler(conv_handler) #Додаємо карту діалогів в бота
    app.add_handler(CommandHandler('help', help_command)) #Команда допомоги

    if app.job_queue:
        app.job_queue.run_repeating(send_reminders, interval=60, first=10) #Перевірка нагадувань кожні 60 секунд

    app.run_polling() #Нескінченна перевірка на нові повідомлення


if __name__ == '__main__':

    main()

