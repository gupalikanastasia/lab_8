class HabitTrackerStates:
    (
        MAIN_MENU,              # Головне меню
        CHOOSING_HABIT,         # Вибір: готова звичка чи своя
        ENTERING_CUSTOM_HABIT,  # Введення назви своєї звички
        SETTING_GOAL_DAYS,      # Скільки днів виконувати
        MANAGING_HABITS,        # Меню управління (видалити/змінити)
        SETTING_REMINDER,       # Меню нагадувань
        CHOOSING_REMINDER_TIME, # Введення часу (14:00)
        VIEWING_STATS           # Перегляд статистики
    ) = range(8)