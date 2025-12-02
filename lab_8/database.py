import json
import os
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict

DATA_FILE = 'habits.json'

@dataclass              #Шаблон Звички
class Habit:
    id: str             # Унікальний номер
    user_id: int        #ID користувача
    name: str           # Назва
    goal_days: int      # Ціль
    completed_days: list  # Список дат, коли виконано
    reminder_time: str = None  # Час нагадування


class Database:
    def __init__(self):
        self.data = {}      # Створюємо порожню полицю в пам'яті
        self.load()         # Одразу пробуємо завантажити дані з файлу

    def load(self):
        if os.path.exists(DATA_FILE):       # Чи існує файл habits.json?
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.data = json.load(f)     # Якщо так — читай і перетворюємо текст у словник Python

    def save(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:     # Записуємо дані з пам'яті у файл на диск
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_habit(self, user_id, name, goal_days):
        habit_id = str(uuid.uuid4())[:5]  # Генеруємо ID

        new_habit = Habit(
            id=habit_id,
            user_id=user_id,
            name=name,
            goal_days=goal_days,
            completed_days=[]
        )
        # Якщо ми ще не знаємо цього користувача — створюємо для нього папку
        if str(user_id) not in self.data:
            self.data[str(user_id)] = []
        # Кладемо заповнений бланк у папку користувача
        self.data[str(user_id)].append(asdict(new_habit))
        self.save()

    def get_habits(self, user_id):
        habits_list = self.data.get(str(user_id), [])
        return [Habit(**h) for h in habits_list]

    def mark_completed(self, user_id, habit_id):
        today = datetime.now().strftime('%Y-%m-%d')
        user_habits = self.data.get(str(user_id), [])

        for habit in user_habits:
            if habit['id'] == habit_id:                     # Шукаємо потрібну звичку за ID
                if today not in habit['completed_days']:    # Перевірка: чи не натиснув він це вже сьогодні?
                    habit['completed_days'].append(today)   # Додаємо дату
                    self.save()
                    return True
        return False

    def delete_habit(self, user_id, habit_id):
        if str(user_id) in self.data:
            # Залишаємо тільки ті звички, у яких ID не співпадає з тим, що видаляємо
            self.data[str(user_id)] = [h for h in self.data[str(user_id)] if h['id'] != habit_id]
            self.save()

    def get_habits_with_reminders(self):
        tasks = []
        for user_id, habits in self.data.items():   # Проходимо по ВСІХ людях у базі
            for h in habits:
                habit_obj = Habit(**h)
                if habit_obj.reminder_time:     # Якщо у звички є час нагадування
                    tasks.append((int(user_id), habit_obj)) # Додаємо в список завдань
        return tasks

    def set_reminder(self, user_id, habit_id, time):    # Знаходимо звичку і просто змінюємо поле reminder_time
        user_habits = self.data.get(str(user_id), [])
        for habit in user_habits:
            if habit['id'] == habit_id:
                habit['reminder_time'] = time
                self.save()
                return True
        return False



db = Database()
