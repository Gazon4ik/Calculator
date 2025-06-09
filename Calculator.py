import tkinter  # Імпорт бібліотеки для створення GUI
from math import sin, cos, tan, log, sqrt, radians  # Імпорт математичних функцій
import re

class Calculator:
    # Клас калькулятора - організує весь функціонал калькулятора

    def __init__(self, master):
        # Ініціалізація головного вікна і початкових параметрів калькулятора
        self.master = master
        master.title("Продвинутий калькулятор")
        master.geometry("450x600")

        # Початковий режим роботи калькулятора
        self.mode = "Звичайний"
        self.mode_buttons = {}

        # Стан темної теми (False = світла)
        self.dark_mode = False

        # Список для зберігання історії обчислень
        self.history = []

        # Поле вводу для виразів
        self.entry = tkinter.Entry(master, width=30, font=('Arial', 18), borderwidth=2, relief="groove")
        self.entry.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        # Прив’язка ПКМ для виклику контекстного меню
        self.entry.bind("<Button-3>", self.show_context_menu)

        # Створення кнопок калькулятора відповідно до режиму
        self.create_buttons()

        # Фрейм для хедера (кнопки теми і меню режимів)
        self.header_frame = tkinter.Frame(master)
        self.header_frame.grid(row=0, column=0, columnspan=5, pady=(30, 0), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        # Кнопка для перемикання теми (світла/темна)
        self.toggle_theme_button = tkinter.Button(self.header_frame, text="Тема", font=('Arial', 12),
                                                  command=self.toggle_theme)
        self.toggle_theme_button.grid(row=0, column=0, sticky="w", padx=(10, 0))


        # Текстове поле для виводу історії обчислень (недоступне для редагування)
        self.history_box = tkinter.Text(master, height=6, width=45, font=('Arial', 10))
        self.history_box.grid(row=8, column=0, columnspan=5, padx=10, pady=5)
        self.history_box.configure(state='disabled')

        # Створення контекстного меню для поля вводу
        self.context_menu = tkinter.Menu(master, tearoff=0)
        self.context_menu.add_command(label="Скопіювати", command=self.copy_text)
        self.context_menu.add_command(label="Вставити", command=self.paste_text)
        self.context_menu.add_command(label="Очистити", command=self.clear_entry)

        # Список режимів калькулятора
        self.modes = ["Звичайний", "Інженерний", "Продвинутий"]

        # Кнопка-меню для вибору режиму
        self.mode_menu_button = tkinter.Menubutton(self.header_frame, text="Режим", font=('Arial', 10), relief="raised")
        self.mode_menu_button.grid(row=0, column=2, sticky="e", padx=5)

        # Меню режимів, що відкривається з кнопки
        self.mode_menu = tkinter.Menu(self.mode_menu_button, tearoff=0)
        self.mode_menu_button.configure(menu=self.mode_menu)

        # Змінна для відслідковування вибраного режиму
        self.mode_var = tkinter.StringVar(value=self.mode)
        for mode in self.modes:
            # Додаємо опції у меню з можливістю вибору радіокнопкою
            self.mode_menu.add_radiobutton(label=mode, variable=self.mode_var,
                                           value=mode,
                                           command=lambda m=mode: self.set_mode(m))
        # Застосування початкової теми
        self.apply_theme()

    def create_buttons(self):
        # Функція створює кнопки калькулятора залежно від вибраного режиму

        # Спочатку видаляємо старі кнопки, крім кнопок меню та теми
        for widget in self.master.grid_slaves():
            if isinstance(widget, tkinter.Button) and widget not in self.mode_buttons.values() and widget != self.toggle_theme_button:
                widget.destroy()

        # Визначення кнопок для кожного режиму
        if self.mode == "Звичайний":
            buttons = [
                ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
                ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
                ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
                ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
                ('C', 6, 0),
            ]
        elif self.mode == "Інженерний":
            buttons = [
                ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('√', 2, 4),
                ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('^', 3, 4),
                ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('log', 4, 4),
                ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3), ('C', 5, 4),
            ]
        else:  # Продвинутий режим
            buttons = [
                ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('√', 2, 4),
                ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('^', 3, 4),
                ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('log', 4, 4),
                ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3), ('C', 5, 4),
                ('sin', 6, 0), ('cos', 6, 1), ('tan', 6, 2), ('ctg', 6, 3),
                ('%', 6, 4),  # Додано кнопку відсотків
            ]

        # Створення кнопок з відповідним текстом і позицією
        for (text, row, col) in buttons:
            btn = tkinter.Button(
                self.master,
                text=text,
                width=6,
                height=2,
                font=('Arial', 14),
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

            # Застосування кольорів відповідно до теми
            bg = "#1e1e1e" if self.dark_mode else "#ffffff"
            fg = "#ffffff" if self.dark_mode else "#000000"
            active_bg = "#2e2e2e" if self.dark_mode else "#e0e0e0"
            btn.configure(bg=bg, fg=fg, activebackground=active_bg, activeforeground=fg, highlightbackground=bg)

    def on_button_click(self, char):
        # Обробка події натискання на кнопку калькулятора

        global result
        if char == '=':
            # Якщо натиснули "=", обчислюємо вираз
            try:
                expression = self.entry.get().replace('^', '**')  # Заміна оператора степеня
                expression = self.parse_percent(expression)       # Обробка відсотків
                parsed = self.parse_expression(expression)        # Заміна символів (√ -> sqrt)
                result = eval(parsed)                              # Виконання обчислення
                self.add_to_history(expression, result)           # Додавання в історію
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, str(result))       # Відображення результату
            except Exception:
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, "Помилка")

        elif char == 'C':
            # Очищення поля вводу
            self.entry.delete(0, tkinter.END)

        elif char in ('sin', 'cos', 'tan', 'log', '√', 'ctg'):
            # Обробка математичних функцій, що беруть один аргумент
            try:
                expr = self.entry.get()
                if expr == "":
                    return

                # Обчислення поточного виразу
                value = float(eval(self.parse_expression(self.parse_percent(expr))))

                # Виклик відповідної функції
                if char == '√':
                    result = sqrt(value)
                elif char == 'sin':
                    result = sin(radians(value))
                elif char == 'cos':
                    result = cos(radians(value))
                elif char == 'tan':
                    result = tan(radians(value))
                elif char == 'ctg':
                    result = 1 / tan(radians(value))
                elif char == 'log':
                    result = log(value)

                self.add_to_history(f"{char}({expr})", result)  # Додавання результату в історію
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, str(result))
            except Exception:
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, "Помилка")

        else:
            # Для звичайних символів просто додаємо їх до поля вводу
            self.entry.insert(tkinter.END, char)

    def parse_percent(self, expr):
        # Функція для обробки виразів із відсотками

        def repl(match):
            a = match.group(1)      # Перше число
            op = match.group(2)     # Оператор
            b = match.group(3)      # Друге число (з відсотком)

            try:
                a_val = float(a)
                b_val = float(b)
            except:
                return match.group(0)

            if op in ('+', '-'):
                # Для додавання/віднімання замінюємо b% на (a*b/100)
                return f"{a}{op}({a}*{b}/100)"
            elif op in ('*', '/'):
                # Для множення/ділення замінюємо b% на (b/100)
                return f"{a}{op}({b}/100)"
            else:
                return match.group(0)

        # Патерн для пошуку виразів виду a + b%
        pattern = r'(\d+\.?\d*)([\+\-\*/])(\d+\.?\d*)%'
        while re.search(pattern, expr):
            expr = re.sub(pattern, repl, expr)

        # Окремо замінюємо прості відсотки (наприклад, 5%)
        expr = re.sub(r'(\d+\.?\d*)%', r'(\1/100)', expr)
        return expr

    def parse_expression(self, expr):
        # Функція замінює символи у виразі для eval
        expr = expr.replace('√', 'sqrt')
        expr = expr.replace('^', '**')
        return expr

    def add_to_history(self, expression, result):
        # Додає обчислення у текстове поле історії

        self.history.append(f"{expression} = {result}")
        self.history_box.configure(state='normal')
        self.history_box.insert(tkinter.END, f"{expression} = {result}\n")
        self.history_box.configure(state='disabled')
        self.history_box.see(tkinter.END)

    def toggle_theme(self):
        # Змінює тему між світлою і темною
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.create_buttons()

    def apply_theme(self):
        # Застосовує кольори теми до елементів GUI

        if self.dark_mode:
            backg = "#1e1e1e"
            text = "#ffffff"
            entry_backg = "#3e3e3e"
        else:
            backg = "#ffffff"
            text = "#000000"
            entry_backg = "#ffffff"

        self.master.configure(bg=backg)
        self.entry.configure(bg=entry_backg, fg=text, insertbackground=text)
        self.header_frame.configure(bg=backg)
        self.history_box.configure(bg=entry_backg, fg=text)

        # Застосування кольорів до кнопки теми і меню режимів
        self.toggle_theme_button.configure(bg=backg, fg=text, activebackground=entry_backg, activeforeground=text)
        self.mode_menu_button.configure(bg=backg, fg=text, activebackground=entry_backg, activeforeground=text)

    def set_mode(self, mode):
        # Змінює режим калькулятора, оновлює кнопки та заголовок

        self.mode = mode
        self.master.title(f"Продвинутий калькулятор - {mode}")
        self.create_buttons()

    def show_context_menu(self, event):
        # Показує контекстне меню у полі вводу (ПКМ)

        self.context_menu.tk_popup(event.x_root, event.y_root)

    def copy_text(self):
        # Копіює виділений текст з поля вводу в буфер обміну

        try:
            self.master.clipboard_clear()
            selected = self.entry.selection_get()
            self.master.clipboard_append(selected)
        except:
            pass

    def paste_text(self):
        # Вставляє текст із буфера обміну у поле вводу

        try:
            pasted = self.master.clipboard_get()
            self.entry.insert(tkinter.END, pasted)
        except:
            pass

    def clear_entry(self):
        # Очищає поле вводу

        self.entry.delete(0, tkinter.END)


if __name__ == "__main__":
    # Основний блок запуску програми
    root = tkinter.Tk()
    calculator = Calculator(root)
    root.mainloop()
