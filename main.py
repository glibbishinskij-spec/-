import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageOps, ImageTk
import json
import os
import random
import re

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

DATA_FILE = "studydesk_data.json"


# Вбудований банк навчальних завдань. Для кожного завдання є відповідь
# для автоматичної перевірки; список перемішується при запуску програми.
TASK_BANK = {
    "Математика": [
        {"id":"math1", "question":"Обчисли: 7 · 8", "answer":"56", "hint":"Помнож 7 на 8."},
        {"id":"math2", "question":"Розв’яжи рівняння: x + 9 = 17", "answer":"8", "hint":"Від 17 відніми 9."},
        {"id":"math3", "question":"Обчисли: 3/4 + 1/4 (відповідь дробом або числом)", "answer":"1", "hint":"Знаменники однакові — додай чисельники."},
        {"id":"math4", "question":"Знайди периметр квадрата зі стороною 6 см (см не пиши).", "answer":"24", "hint":"Периметр квадрата дорівнює 4a."},
        {"id":"math5", "question":"Скільки буде 15% від 200?", "answer":"30", "hint":"10% від 200 — це 20, 5% — це 10."},
        {"id":"math6", "question":"Розв’яжи: 5x = 45", "answer":"9", "hint":"Поділи обидві частини на 5."},
        {"id":"math7", "question":"Обчисли: 2³ + 4", "answer":"12", "hint":"2³ = 2 · 2 · 2."},
        {"id":"math8", "question":"Площа прямокутника зі сторонами 5 см і 7 см (число).", "answer":"35", "hint":"Площа дорівнює добутку сторін."},
        {"id":"math9", "question":"Обчисли: 0,6 + 1,25", "answer":"1.85", "hint":"Запиши 0,6 як 0,60."},
        {"id":"math10", "question":"Яке число є простим: 9, 11, 15 чи 21? Напиши число.", "answer":"11", "hint":"Просте число має лише два натуральні дільники."},
    ],
    "Фізика": [
        {"id":"phys1", "question":"Яка одиниця вимірювання сили в SI?", "answer":"ньютон", "hint":"Названа на честь ученого Ісаака Ньютона."},
        {"id":"phys2", "question":"Формула швидкості: шлях поділити на що?", "answer":"час", "hint":"v = s / t."},
        {"id":"phys3", "question":"Тіло пройшло 100 м за 20 с. Знайди швидкість у м/с.", "answer":"5", "hint":"v = 100 / 20."},
        {"id":"phys4", "question":"Який прилад вимірює температуру?", "answer":"термометр", "hint":"Назва приладу походить від слова «термо»."},
        {"id":"phys5", "question":"У яких одиницях у SI вимірюють масу?", "answer":"кілограм", "hint":"Позначення — кг."},
        {"id":"phys6", "question":"Формула густини: маса поділити на що?", "answer":"об’єм", "hint":"ρ = m / V."},
        {"id":"phys7", "question":"Скільки секунд у 3 хвилинах?", "answer":"180", "hint":"Одна хвилина має 60 секунд."},
        {"id":"phys8", "question":"Як називається сила, з якою Земля притягує тіла?", "answer":"сила тяжіння", "hint":"Вона спрямована до центра Землі."},
        {"id":"phys9", "question":"Яка енергія пов’язана з рухом тіла?", "answer":"кінетична", "hint":"Протилежність потенціальній енергії."},
        {"id":"phys10", "question":"Як називається одиниця роботи в SI?", "answer":"джоуль", "hint":"Скорочено — Дж."},
    ],
    "Біологія": [
        {"id":"bio1", "question":"Яка частина клітини містить спадкову інформацію та керує її роботою?", "answer":"ядро", "hint":"У еукаріотичних клітинах це органела з ДНК."},
        {"id":"bio2", "question":"Як називається процес утворення органічних речовин на світлі у рослин?", "answer":"фотосинтез", "hint":"Під час процесу поглинається вуглекислий газ."},
        {"id":"bio3", "question":"Який орган людини перекачує кров?", "answer":"серце", "hint":"Це м’язовий орган грудної порожнини."},
        {"id":"bio4", "question":"Як називаються клітини, що передають нервові імпульси?", "answer":"нейрони", "hint":"Інша назва — нервові клітини."},
        {"id":"bio5", "question":"Який газ людина поглинає під час дихання?", "answer":"кисень", "hint":"Його хімічна формула O₂."},
        {"id":"bio6", "question":"Яка система органів забезпечує опору й захист тіла?", "answer":"опорно-рухова", "hint":"До неї належать кістки та м’язи."},
        {"id":"bio7", "question":"Як називається основна структурна одиниця живого організму?", "answer":"клітина", "hint":"З неї складаються тканини."},
        {"id":"bio8", "question":"Який орган рослини зазвичай поглинає воду з ґрунту?", "answer":"корінь", "hint":"Він також закріплює рослину в ґрунті."},
        {"id":"bio9", "question":"Як називається рідина, що переносить речовини в організмі людини?", "answer":"кров", "hint":"Вона рухається кровоносними судинами."},
        {"id":"bio10", "question":"Яка частина рослини зазвичай утворює насіння після запилення й запліднення?", "answer":"квітка", "hint":"Це орган статевого розмноження рослин."},
    ],
    "Інформатика": [
        {"id":"it1", "question":"Яка команда Python виводить текст на екран?", "answer":"print", "hint":"Приклад: print('Привіт')."},
        {"id":"it2", "question":"Який тип даних Python зберігає значення True або False?", "answer":"bool", "hint":"Повна назва — boolean."},
        {"id":"it3", "question":"Який символ використовують для коментаря в Python?", "answer":"#", "hint":"Усе після нього в рядку не виконується як код."},
        {"id":"it4", "question":"Який тип даних зберігає пари ключ-значення?", "answer":"dict", "hint":"Скорочено від dictionary."},
        {"id":"it5", "question":"Що поверне len('cat')? Напиши число.", "answer":"3", "hint":"Порахуй кількість символів."},
        {"id":"it6", "question":"Який оператор перевіряє рівність двох значень у Python?", "answer":"==", "hint":"Один знак = присвоює значення."},
        {"id":"it7", "question":"Який тип даних Python використовують для впорядкованої змінної колекції, яку можна змінювати?", "answer":"list", "hint":"Літерали записують у квадратних дужках."},
        {"id":"it8", "question":"Яка функція перетворює рядок цифр '12' на ціле число?", "answer":"int", "hint":"Наприклад: int('12')."},
        {"id":"it9", "question":"Що виведе print(2 + 3 * 4)? Напиши число.", "answer":"14", "hint":"Спочатку виконується множення."},
        {"id":"it10", "question":"Яке ключове слово створює функцію в Python?", "answer":"def", "hint":"Після нього пишуть ім’я функції."},
    ],
    "Українська мова": [
        {"id":"ua1", "question":"Скільки букв в українському алфавіті? Напиши число.", "answer":"33", "hint":"Порахуй літери від А до Я."},
        {"id":"ua2", "question":"Яка частина мови називає предмет і відповідає на питання хто? що?", "answer":"іменник", "hint":"Наприклад: книга, учень, місто."},
        {"id":"ua3", "question":"Яка частина мови називає ознаку предмета?", "answer":"прикметник", "hint":"Відповідає на питання який? чий?"},
        {"id":"ua4", "question":"Скільки відмінків в українській мові? Напиши число.", "answer":"7", "hint":"Називний, родовий, давальний, знахідний, орудний, місцевий, кличний."},
        {"id":"ua5", "question":"Як називається головний член речення, який найчастіше означає дію?", "answer":"присудок", "hint":"У парі з підметом утворює граматичну основу."},
        {"id":"ua6", "question":"Який знак ставлять у кінці питального речення?", "answer":"?", "hint":"Цей знак має форму гачка й крапки."},
        {"id":"ua7", "question":"Як називається слово, протилежне за значенням до слова «високий»?", "answer":"низький", "hint":"Наприклад, про невисоку будівлю."},
        {"id":"ua8", "question":"Яка частина мови означає дію або стан предмета?", "answer":"дієслово", "hint":"Наприклад: читати, бігти, спати."},
        {"id":"ua9", "question":"Як називаються слова з близьким значенням?", "answer":"синоніми", "hint":"Наприклад: гарний — красивий."},
        {"id":"ua10", "question":"Який префікс у слові «прочитати»? Напиши префікс.", "answer":"про", "hint":"Це частина слова перед коренем чит-."},
    ],
    "Історія": [
        {"id":"hist1", "question":"Як називалася держава, до складу якої входила більшість українських земель у IX–XIII ст.?", "answer":"київська русь", "hint":"Її центром був Київ."},
        {"id":"hist2", "question":"У якому році хрестив Русь князь Володимир?", "answer":"988", "hint":"Кінець X століття."},
        {"id":"hist3", "question":"Як називався козацький виборний керівник війська й держави?", "answer":"гетьман", "hint":"Відомий приклад — Богдан Хмельницький."},
        {"id":"hist4", "question":"У якому році почалася Друга світова війна?", "answer":"1939", "hint":"Вона почалася 1 вересня."},
        {"id":"hist5", "question":"Як називалася козацька держава, що виникла внаслідок повстання середини XVII ст.?", "answer":"гетьманщина", "hint":"Назва походить від посади гетьмана."},
        {"id":"hist6", "question":"Яке місто було столицею Галицько-Волинської держави за князя Данила?", "answer":"холм", "hint":"Князь переніс туди свою резиденцію."},
        {"id":"hist7", "question":"У якому році Україна проголосила незалежність?", "answer":"1991", "hint":"Акт проголошення незалежності ухвалили 24 серпня."},
        {"id":"hist8", "question":"Як називали воїнів, які жили на Запорозькій Січі?", "answer":"козаки", "hint":"Вони були відомі кіннотою та піхотою."},
        {"id":"hist9", "question":"Який князь, за літописною традицією, заснував Київ разом із братами?", "answer":"кий", "hint":"Місто назване на його честь."},
        {"id":"hist10", "question":"Який документ 1710 року пов’язують із Пилипом Орликом?", "answer":"конституція", "hint":"Його часто називають однією з ранніх європейських конституцій."},
    ],
}


class StudyDesk(ctk.CTk):
    def __init__(self):
        super().__init__()

        super().title("StudyDesk")
        self.geometry("1150x720")
        self.minsize(950, 600)

        self.data = self.load_data()
        ctk.set_appearance_mode("dark" if self.data.get("theme") == "dark" else "light")
        self.last_random_task = {}
        self.current_image = None
        self.current_page = self.show_home

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.show_home()

    # ---------- DATA ----------
    def load_data(self):
        default = {
            "name": "Глеб",
            "tasks": [
                {"title": "Задача з фізики", "subject": "Фізика", "done": False},
                {"title": "Python-проєкт", "subject": "Інформатика", "done": True},
                {"title": "Конспект з біології", "subject": "Біологія", "done": False}
            ],
            "theme": "light",
            "solutions": {}
        }
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    saved = json.load(file)
                if isinstance(saved, dict):
                    default.update(saved)
            except (OSError, json.JSONDecodeError):
                pass
        if not isinstance(default.get("tasks"), list):
            default["tasks"] = []
        if not isinstance(default.get("solutions"), dict):
            default["solutions"] = {}
        for task in default["tasks"]:
            task.setdefault("done", False)
        return default

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    # ---------- SIDEBAR ----------
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=220, corner_radius=0, fg_color=("white", "#202124")
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(
            self.sidebar,
            text="📚 StudyDesk",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#6336a8"
        ).grid(row=0, column=0, padx=20, pady=(30, 35))

        buttons = [
            ("🏠  Головна", self.show_home),
            ("📝  Завдання", self.show_tasks),
            ("📚  Предмети", self.show_subjects),
            ("🧠  Тести", self.show_tests),
            ("🖼  Зображення", self.show_editor),
            ("🌐  Сервер", self.show_server),
            ("⚙  Налаштування", self.show_settings)
        ]

        for i, (text, command) in enumerate(buttons, start=1):
            ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=45,
                corner_radius=10,
                fg_color="transparent",
                hover_color=("#e5ddff", "#383044"),
                text_color=("#4d4770", "#ddd7ee"),
                anchor="w",
                font=ctk.CTkFont(size=14)
            ).grid(row=i, column=0, padx=12, pady=4, sticky="ew")

        ctk.CTkLabel(
            self.sidebar,
            text="● Система готова",
            text_color="#70a900",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=9, column=0, padx=20, pady=(10, 20), sticky="w")

    # ---------- COMMON ----------
    def clear_content(self):
        if hasattr(self, "content"):
            self.content.destroy()

        self.content = ctk.CTkFrame(
            self, corner_radius=0, fg_color=("white", "#18191c")
        )
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)

    def page_title(self, text, subtitle=""):
        ctk.CTkLabel(
            self.content,
            text=text,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#343149", "#f2f0f7")
        ).pack(anchor="w", padx=35, pady=(30, 3))

        if subtitle:
            ctk.CTkLabel(
                self.content,
                text=subtitle,
                text_color=("#858197", "#b9b5c7"),
                font=ctk.CTkFont(size=14)
            ).pack(anchor="w", padx=35, pady=(0, 20))

    # ---------- HOME ----------
    def show_home(self):
        self.current_page = self.show_home
        self.clear_content()
        self.page_title(
            f"Привіт, {self.data['name']}! 👋",
            "Твій навчальний центр"
        )

        stats = ctk.CTkFrame(self.content, fg_color="transparent")
        stats.pack(fill="x", padx=25, pady=10)

        total = len(self.data["tasks"])
        done = sum(task["done"] for task in self.data["tasks"])
        percent = int(done / total * 100) if total else 0

        self.stat_card(stats, "📚", str(total), "Усього завдань", 0)
        self.stat_card(stats, "✅", str(done), "Виконано", 1)
        self.stat_card(stats, "📊", f"{percent}%", "Прогрес", 2)

        ctk.CTkLabel(
            self.content,
            text="Ближчі завдання",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#403b58", "#eeeaf7")
        ).pack(anchor="w", padx=35, pady=(30, 10))

        box = ctk.CTkScrollableFrame(
            self.content,
            fg_color=("#f8f7fc", "#222329"),
            corner_radius=15
        )
        box.pack(fill="both", expand=True, padx=30, pady=(0, 25))

        for task in self.data["tasks"]:
            self.task_row(box, task)

    def stat_card(self, parent, icon, value, text, column):
        card = ctk.CTkFrame(
            parent, corner_radius=15,
            fg_color=("#f5f1ff", "#29243a")
        )
        card.grid(row=0, column=column, padx=8, sticky="ew")
        parent.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            card, text=icon, font=ctk.CTkFont(size=25)
        ).pack(pady=(15, 3))

        ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#6336a8"
        ).pack()

        ctk.CTkLabel(
            card, text=text, text_color=("#77738a", "#aaa5b5")
        ).pack(pady=(0, 15))

    def task_row(self, parent, task):
        row = ctk.CTkFrame(parent, corner_radius=10, fg_color=("white", "#18191c"))
        row.pack(fill="x", padx=10, pady=6)

        status = "☑" if task["done"] else "☐"
        color = "#70a900" if task["done"] else "#6336a8"

        ctk.CTkLabel(
            row, text=status,
            font=ctk.CTkFont(size=22),
            text_color=color
        ).pack(side="left", padx=15, pady=10)

        ctk.CTkLabel(
            row, text=task["title"],
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            row, text=task["subject"],
            text_color=("#858197", "#b9b5c7")
        ).pack(side="right", padx=15)

    # ---------- TASKS ----------
    def show_tasks(self):
        self.current_page = self.show_tasks
        self.clear_content()
        self.page_title("📝 Завдання", "Створюй та відмічай виконані завдання")

        add = ctk.CTkFrame(self.content, fg_color=("#f5f1ff", "#29243a"), corner_radius=15)
        add.pack(fill="x", padx=30, pady=10)

        self.task_entry = ctk.CTkEntry(
            add, placeholder_text="Назва завдання..."
        )
        self.task_entry.grid(row=0, column=0, padx=12, pady=15, sticky="ew")

        self.subject_entry = ctk.CTkEntry(
            add, placeholder_text="Предмет..."
        )
        self.subject_entry.grid(row=0, column=1, padx=12, pady=15)

        ctk.CTkButton(
            add, text="＋ Додати",
            command=self.add_task,
            fg_color="#8b55d9",
            hover_color="#7340bf"
        ).grid(row=0, column=2, padx=12, pady=15)

        add.grid_columnconfigure(0, weight=1)

        self.tasks_list = ctk.CTkScrollableFrame(
            self.content, fg_color=("#f8f7fc", "#222329")
        )
        self.tasks_list.pack(fill="both", expand=True, padx=30, pady=15)

        self.refresh_tasks()

    def refresh_tasks(self):
        for widget in self.tasks_list.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.data["tasks"]):
            row = ctk.CTkFrame(
                self.tasks_list, corner_radius=12,
                fg_color=("white", "#18191c")
            )
            row.pack(fill="x", pady=5)

            check = ctk.CTkCheckBox(
                row,
                text=f"{task['title']}   —   {task['subject']}",
                command=lambda i=index: self.toggle_task(i)
            )
            check.pack(side="left", padx=15, pady=12)

            if task["done"]:
                check.select()

            ctk.CTkButton(
                row, text="🗑",
                width=45,
                fg_color=("#eeeeee", "#34353a"),
                text_color=("#555555", "#dddddd"),
                hover_color=("#dddddd", "#45464d"),
                command=lambda i=index: self.delete_task(i)
            ).pack(side="right", padx=10)

    def add_task(self):
        title = self.task_entry.get().strip()
        subject = self.subject_entry.get().strip()

        if not title or not subject:
            messagebox.showwarning("Помилка", "Заповни назву та предмет.")
            return

        self.data["tasks"].append({
            "title": title,
            "subject": subject,
            "done": False
        })

        self.save_data()
        self.task_entry.delete(0, "end")
        self.subject_entry.delete(0, "end")
        self.refresh_tasks()

    def toggle_task(self, index):
        self.data["tasks"][index]["done"] = not self.data["tasks"][index]["done"]
        self.save_data()

    def delete_task(self, index):
        del self.data["tasks"][index]
        self.save_data()
        self.refresh_tasks()

    # ---------- SUBJECTS ----------
    def show_subjects(self):
        self.current_page = self.show_subjects
        self.clear_content()
        self.page_title("📚 Предмети", "Твої навчальні предмети")

        subjects = [
            ("📐", "Математика"),
            ("⚛", "Фізика"),
            ("🧬", "Біологія"),
            ("💻", "Інформатика"),
            ("🇺🇦", "Українська мова"),
            ("🌍", "Історія")
        ]

        grid = ctk.CTkFrame(self.content, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=30, pady=20)

        for i, (icon, name) in enumerate(subjects):
            card = ctk.CTkFrame(
                grid, corner_radius=15,
                fg_color=("#f5f1ff", "#29243a")
            )
            card.grid(
                row=i // 3, column=i % 3,
                padx=10, pady=10, sticky="nsew"
            )

            ctk.CTkLabel(
                card, text=icon,
                font=ctk.CTkFont(size=35)
            ).pack(pady=(25, 8))

            ctk.CTkLabel(
                card, text=name,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=("#4d4770", "#ddd7ee")
            ).pack(pady=(0, 12))

            # Кнопка открывает выбранный предмет
            ctk.CTkButton(
                card,
                text="Відкрити",
                height=38,
                width=130,
                fg_color="#8b55d9",
                hover_color="#7340bf",
                command=lambda subject=name: self.open_subject(subject)
            ).pack(pady=(0, 20))

            grid.grid_columnconfigure(i % 3, weight=1)
            grid.grid_rowconfigure(i // 3, weight=1)

    def open_subject(self, subject, force_new=False):
        self.current_subject = subject
        self.current_page = lambda: self.open_subject(subject)
        self.clear_content()
        self.page_title(subject, "Випадкові навчальні завдання, власні записи та збережені відповіді")

        # Вбудоване завдання змінюється при кожному відкритті предмета.
        bank = TASK_BANK.get(subject, [])
        current = None
        if bank:
            previous = self.last_random_task.get(subject)
            choices = [item for item in bank if item["id"] != previous]
            if not choices:
                choices = bank[:]
            current = random.choice(choices)
            self.last_random_task[subject] = current["id"]

        if current:
            card = ctk.CTkFrame(self.content, corner_radius=16, fg_color=("#f5f1ff", "#29243a"))
            card.pack(fill="x", padx=30, pady=(4, 12))
            ctk.CTkLabel(card, text="🎲 Випадкове завдання", font=ctk.CTkFont(size=18, weight="bold"), text_color="#8b55d9").pack(anchor="w", padx=18, pady=(15, 6))
            ctk.CTkLabel(card, text=current["question"], wraplength=800, justify="left", font=ctk.CTkFont(size=17, weight="bold"), text_color=("#343149", "#f2f0f7")).pack(anchor="w", padx=18, pady=(0, 10))

            saved = self.data["solutions"].get(current["id"], {})
            answer_box = ctk.CTkEntry(card, placeholder_text="Введи свою відповідь…", height=38)
            answer_box.pack(fill="x", padx=18, pady=5)
            if saved.get("answer"):
                answer_box.insert(0, saved["answer"])

            feedback = ctk.CTkLabel(card, text=saved.get("feedback", "Відповідь ще не перевірена"), text_color=("#77738a", "#aaa5b5"), wraplength=800)
            feedback.pack(anchor="w", padx=18, pady=5)

            def normalized(value):
                value = value.strip().lower().replace(",", ".")
                value = value.replace("’", "'").replace("`", "'")
                value = re.sub(r"\s+", " ", value)
                return value.rstrip(".! ")

            def save_answer(show_message=False):
                value = answer_box.get().strip()
                if not value:
                    messagebox.showwarning("Відповідь", "Спочатку введи відповідь.")
                    return
                record = self.data["solutions"].setdefault(current["id"], {})
                record["answer"] = value
                record.setdefault("feedback", "Відповідь збережена")
                self.save_data()
                if show_message:
                    messagebox.showinfo("Збережено", "Твою відповідь збережено.")

            def check_answer():
                value = answer_box.get().strip()
                if not value:
                    messagebox.showwarning("Перевірка", "Спочатку введи відповідь.")
                    return
                correct = normalized(value) == normalized(current["answer"])
                if correct:
                    message = "✅ Правильно! Чудова робота."
                else:
                    message = "❌ Поки неправильно. Підказка: " + current["hint"]
                record = self.data["solutions"].setdefault(current["id"], {})
                record["answer"] = value
                record["feedback"] = message
                record["correct"] = correct
                self.save_data()
                feedback.configure(text=message, text_color="#70a900" if correct else "#d97757")

            buttons = ctk.CTkFrame(card, fg_color="transparent")
            buttons.pack(fill="x", padx=14, pady=(5, 15))
            ctk.CTkButton(buttons, text="✓ Перевірити", command=check_answer, fg_color="#8b55d9", hover_color="#7340bf").pack(side="left", padx=4)
            ctk.CTkButton(buttons, text="💾 Зберегти відповідь", command=lambda: save_answer(True), fg_color=("#e8e2f7", "#403650"), text_color=("#4d4770", "#eeeaf7")).pack(side="left", padx=4)
            ctk.CTkButton(buttons, text="🎲 Наступне завдання", command=lambda: self.open_subject(subject, True), fg_color="#5279b8", hover_color="#3d6097").pack(side="right", padx=4)

        # Додавання власного завдання до цього предмета.
        add = ctk.CTkFrame(self.content, corner_radius=12, fg_color=("#f8f7fc", "#222329"))
        add.pack(fill="x", padx=30, pady=(0, 10))
        custom_title = ctk.CTkEntry(add, placeholder_text="Додати власне завдання…")
        custom_title.pack(side="left", fill="x", expand=True, padx=12, pady=12)
        def add_custom():
            title = custom_title.get().strip()
            if not title:
                messagebox.showwarning("Завдання", "Напиши назву або умову завдання.")
                return
            self.data["tasks"].append({"title": title, "subject": subject, "done": False, "answer": ""})
            self.save_data()
            self.open_subject(subject)
        ctk.CTkButton(add, text="＋ Додати", command=add_custom, fg_color="#8b55d9").pack(side="right", padx=12, pady=12)

        subject_tasks = [task for task in self.data["tasks"] if task.get("subject", "").strip().lower() == subject.strip().lower()]
        ctk.CTkLabel(self.content, text=f"📋 Твої завдання ({len(subject_tasks)})", font=ctk.CTkFont(size=18, weight="bold"), text_color=("#403b58", "#eeeaf7")).pack(anchor="w", padx=35, pady=(4, 4))
        box = ctk.CTkScrollableFrame(self.content, fg_color=("#f8f7fc", "#222329"), corner_radius=12)
        box.pack(fill="both", expand=True, padx=30, pady=(0, 10))
        if not subject_tasks:
            ctk.CTkLabel(box, text="Тут поки немає власних завдань. Додай перше вище.", text_color=("#77738a", "#aaa5b5")).pack(padx=15, pady=18)
        for task in subject_tasks:
            row = ctk.CTkFrame(box, corner_radius=10, fg_color=("white", "#18191c"))
            row.pack(fill="x", padx=7, pady=5)
            status = "☑" if task.get("done", False) else "☐"
            ctk.CTkLabel(row, text=status, text_color="#70a900", font=ctk.CTkFont(size=19)).pack(side="left", padx=12, pady=10)
            ctk.CTkLabel(row, text=task.get("title", "Без назви"), wraplength=550, justify="left").pack(side="left", padx=5, pady=10, fill="x", expand=True)
            ctk.CTkButton(row, text="✓ Виконано" if not task.get("done", False) else "↩ Повернути", width=100, command=lambda t=task: self.toggle_subject_task(t, subject)).pack(side="right", padx=10, pady=7)

        ctk.CTkButton(self.content, text="← Назад до предметів", command=self.show_subjects, fg_color=("#eeeeee", "#34353a"), hover_color=("#dddddd", "#45464d"), text_color=("#4d4770", "#ddd7ee")).pack(pady=(0, 15))

    def toggle_subject_task(self, task, subject):
        task["done"] = not task.get("done", False)
        self.save_data()
        self.open_subject(subject)

    # ---------- TESTS ----------
    def show_tests(self):
        self.current_page = self.show_tests
        self.clear_content()
        self.page_title("🧠 Міні-тест Python", "Перевір свої знання")

        self.test_questions = [
            (
                "Що виведе print([1, 2, 3][1])?",
                ["1", "2", "3", "Помилка"],
                1,
                "Індексація списку починається з нуля, тому індекс 1 означає другий елемент."
            ),
            (
                "Яка команда створює кнопку в CustomTkinter?",
                ["CTkButton()", "ButtonPython()", "CreateButton()", "NewButton()"],
                0,
                "У бібліотеці CustomTkinter кнопки створюються класом CTkButton."
            ),
            (
                "Який тип даних зберігає пари ключ:значення?",
                ["list", "tuple", "dict", "set"],
                2,
                "Словник dict зберігає дані у вигляді пар ключ:значення."
            )
        ]

        self.test_index = 0
        self.test_score = 0
        self.test_answered = False
        self.show_question()

    def show_question(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        question, answers, correct, explanation = self.test_questions[self.test_index]
        self.test_answered = False

        ctk.CTkLabel(
            self.content,
            text=f"Питання {self.test_index + 1} з {len(self.test_questions)}",
            text_color="#8b55d9",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            self.content,
            text=question,
            wraplength=700,
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=("#363249", "#f2f0f7")
        ).pack(pady=15)

        self.test_answer_buttons = []
        for i, answer_text in enumerate(answers):
            btn = ctk.CTkButton(
                self.content,
                text=answer_text,
                height=45,
                fg_color=("#f0ebff", "#302a40"),
                hover_color=("#dfd5ff", "#43365a"),
                text_color=("#49308f", "#e1d7ff"),
                command=lambda x=i: self.answer(x)
            )
            btn.pack(fill="x", padx=100, pady=5)
            self.test_answer_buttons.append(btn)

        self.test_feedback = ctk.CTkLabel(
            self.content, text="", wraplength=700, justify="left",
            font=ctk.CTkFont(size=16), text_color=("#363249", "#f2f0f7")
        )
        self.test_feedback.pack(pady=(12, 5))

        self.test_next_button = ctk.CTkButton(
            self.content, text="Наступне питання →", command=self.next_question,
            fg_color="#8b55d9", state="disabled"
        )
        self.test_next_button.pack(pady=10)

    def answer(self, selected):
        if self.test_answered:
            return
        self.test_answered = True
        question, answers, correct, explanation = self.test_questions[self.test_index]
        is_correct = selected == correct
        if is_correct:
            self.test_score += 1

        # Показуємо зелений правильний варіант і червоний вибір, якщо він помилковий.
        for i, btn in enumerate(self.test_answer_buttons):
            if i == correct:
                btn.configure(fg_color="#238636", hover_color="#238636", text_color="#ffffff")
            elif i == selected:
                btn.configure(fg_color="#c93636", hover_color="#c93636", text_color="#ffffff")
            else:
                btn.configure(state="disabled")

        if is_correct:
            message = "✅ Правильно!\n" + explanation
            self.test_feedback.configure(text=message, text_color=("#16752c", "#75e08a"))
        else:
            message = f"❌ Неправильно. Правильна відповідь: {answers[correct]}\n{explanation}"
            self.test_feedback.configure(text=message, text_color=("#b42323", "#ff8b8b"))

        self.test_next_button.configure(state="normal")
        if self.test_index == len(self.test_questions) - 1:
            self.test_next_button.configure(text="Показати результат →")

    def next_question(self):
        if not self.test_answered:
            return
        self.test_index += 1
        if self.test_index < len(self.test_questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        score = self.test_score
        total = len(self.test_questions)

        ctk.CTkLabel(
            self.content,
            text="🎉 Тест завершено!",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#6336a8"
        ).pack(pady=(80, 20))

        ctk.CTkLabel(
            self.content,
            text=f"Результат: {score} / {total}",
            font=ctk.CTkFont(size=24)
        ).pack(pady=10)

        ctk.CTkLabel(
            self.content,
            text=f"Успішність: {int(score / total * 100)}%",
            font=ctk.CTkFont(size=20),
            text_color="#70a900"
        ).pack(pady=10)

        ctk.CTkButton(
            self.content,
            text="Пройти ще раз",
            command=self.show_tests,
            fg_color="#8b55d9"
        ).pack(pady=20)

        ctk.CTkButton(
            self.content, text="← На головну", command=self.show_home,
            fg_color=("#eeeeee", "#34353a"),
            text_color=("#4d4770", "#ddd7ee")
        ).pack(pady=5)

    # ---------- IMAGE EDITOR ----------
    def show_editor(self):
        self.current_page = self.show_editor
        self.clear_content()
        self.page_title("🖼 Easy Editor", "Простий редактор зображень")

        controls = ctk.CTkFrame(self.content, fg_color=("#f5f1ff", "#29243a"))
        controls.pack(fill="x", padx=30, pady=10)

        ctk.CTkButton(
            controls, text="📂 Відкрити",
            command=self.open_image
        ).pack(side="left", padx=8, pady=10)

        ctk.CTkButton(
            controls, text="↻ Повернути",
            command=self.rotate_image
        ).pack(side="left", padx=8, pady=10)

        ctk.CTkButton(
            controls, text="⚫ Чорно-біле",
            command=self.gray_image
        ).pack(side="left", padx=8, pady=10)

        ctk.CTkButton(
            controls, text="💾 Зберегти",
            command=self.save_image,
            fg_color="#8b55d9"
        ).pack(side="left", padx=8, pady=10)

        self.image_label = ctk.CTkLabel(
            self.content,
            text="Відкрий зображення",
            font=ctk.CTkFont(size=20),
            text_color=("#88859a", "#aaa6b5")
        )
        self.image_label.pack(expand=True)

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )

        if not path:
            return

        try:
            self.current_image = Image.open(path)
            self.display_image()
        except Exception as error:
            messagebox.showerror("Помилка", str(error))

    def display_image(self):
        if self.current_image is None:
            return

        image = self.current_image.copy()
        image.thumbnail((650, 450))

        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=self.tk_image, text="")

    def rotate_image(self):
        if self.current_image is None:
            return

        self.current_image = self.current_image.rotate(90, expand=True)
        self.display_image()

    def gray_image(self):
        if self.current_image is None:
            return

        self.current_image = ImageOps.grayscale(self.current_image)
        self.display_image()

    def save_image(self):
        if self.current_image is None:
            messagebox.showwarning("Увага", "Спочатку відкрий зображення.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )

        if path:
            self.current_image.save(path)
            messagebox.showinfo("Готово", "Зображення збережено.")

    # ---------- SERVER ----------
    def show_server(self):
        self.current_page = self.show_server
        self.clear_content()
        self.page_title("🌐 Сервер", "Навчальний екран сервера")

        card = ctk.CTkFrame(
            self.content, corner_radius=18,
            fg_color=("#f5f1ff", "#29243a")
        )
        card.pack(fill="x", padx=80, pady=30)

        ctk.CTkLabel(
            card,
            text="●  SERVER ONLINE",
            text_color="#70a900",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(30, 15))

        ctk.CTkLabel(
            card,
            text="IP: 127.0.0.1\nПорт: 8080\nКористувачів онлайн: 3",
            justify="left",
            font=ctk.CTkFont(size=17),
            text_color=("#55516c", "#c8c3d2")
        ).pack(pady=10)

        ctk.CTkButton(
            card,
            text="Запустити сервер",
            fg_color="#8b55d9",
            hover_color="#7340bf",
            command=lambda: messagebox.showinfo(
                "Сервер", "Демонстраційний сервер запущено!"
            )
        ).pack(pady=(15, 30))

    # ---------- SETTINGS ----------
    def show_settings(self):
        self.current_page = self.show_settings
        self.clear_content()
        self.page_title("⚙ Налаштування", "Налаштуй StudyDesk під себе")

        box = ctk.CTkFrame(
            self.content, corner_radius=15,
            fg_color=("#f5f1ff", "#29243a")
        )
        box.pack(fill="x", padx=40, pady=20)

        ctk.CTkLabel(
            box, text="Ім'я користувача",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))

        name = ctk.CTkEntry(box)
        name.insert(0, self.data["name"])
        name.pack(fill="x", padx=20, pady=(0, 15))

        def save_settings():
            new_name = name.get().strip()

            if new_name:
                self.data["name"] = new_name
                self.save_data()
                messagebox.showinfo("Готово", "Налаштування збережено.")

        ctk.CTkButton(
            box,
            text="💾 Зберегти",
            command=save_settings,
            fg_color="#8b55d9"
        ).pack(anchor="w", padx=20, pady=(0, 20))

        ctk.CTkLabel(
            box,
            text="Тема",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))

        theme = ctk.CTkOptionMenu(
            box,
            values=["Світла", "Темна"],
            command=self.change_theme
        )
        theme.set("Світла" if self.data["theme"] == "light" else "Темна")
        theme.pack(anchor="w", padx=20, pady=(0, 20))

    def change_theme(self, value):
        # Змінюємо тему CustomTkinter і одразу перебудовуємо інтерфейс.
        if value == "Темна":
            ctk.set_appearance_mode("dark")
            self.data["theme"] = "dark"
        else:
            ctk.set_appearance_mode("light")
            self.data["theme"] = "light"

        self.save_data()

        # Sidebar і сторінка містять фіксовані кольори,
        # тому перебудовуємо їх після зміни теми.
        old_page = self.current_page
        self.sidebar.destroy()
        self.create_sidebar()
        old_page()



if __name__ == "__main__":
    app = StudyDesk()
    app.mainloop()
