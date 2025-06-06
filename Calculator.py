import tkinter  # Імпорт бібліотеки для створення GUI та математичних функцій
from math import sin, cos, tan, log, sqrt, radians

class Calculator:   # Клас калькулятора
    def __init__(self, master):
        # Ініціалізація головного вікна
        self.master = master
        master.title("Продвинутий калькулятор")
        master.geometry("450x450")

        self.dark_mode = False  # Стан темної теми (False = світла)

        self.history = []   # Список для історії обчислень

        # Текстове поле для вводу виразів
        self.entry = tkinter.Entry(master, width=30, font=('Arial', 18), borderwidth=2, relief="groove")
        self.entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
        self.entry.bind("<Button-3>", self.show_context_menu)   # ПКМ викликає контекстне меню

        self.create_buttons()   # Створення кнопки калькулятора

        # Кнопка перемикання темної/світлої теми
        self.toggle_theme_button = tkinter.Button(master, text="Тема", command=self.toggle_theme)
        self.toggle_theme_button.grid(row=5, column=4, columnspan=2)
        self.apply_theme()  # Застосування теми

        # Поле виводу історії обчислень
        self.history_box = tkinter.Text(master, height=6, width=45, font=('Arial', 10))
        self.history_box.grid(row=6, column=0, columnspan=5, padx=10, pady=5)
        self.history_box.configure(state='disabled')

        # Контекстне меню
        self.context_menu = tkinter.Menu(master, tearoff=0)
        self.context_menu.add_command(label="Скопіювати", command=self.copy_text)
        self.context_menu.add_command(label="Вставити", command=self.paste_text)
        self.context_menu.add_command(label="Очистити", command=self.clear_entry)

    # Створення кнопок калькулятора
    def create_buttons(self):
        # Кожна кнопка має текст, позицію (рядок, колонка)
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('√', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('^', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('log', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('C', 4, 4),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2),('ctg', 5, 3)
        ]

        # Для кожної кнопки створюється об'єкт Button з відповідною функцією при натисканні
        for (text, row, col) in buttons:
            tkinter.Button(
                self.master,
                text=text,
                width=6,
                height=2,
                font=('Arial', 14),
                command=lambda t=text: self.on_button_click(t)  # Передавання тексту кнопки в обробник
            ).grid(row=row, column=col, padx=2, pady=2)

    # Обробка натискання кнопки
    def on_button_click(self, char):
        global result
        if char == '=':
            # При натискані "=", обчислюється вираз
            try:
                expression = self.entry.get().replace('^', '**')    # Заміна ^ на ** для Python
                parsed = self.parse_expression(expression)          # Заміна √ на sqrt
                result = eval(parsed)                               # eval виконує математичний вираз
                self.add_to_history(expression, result)             # Зберігання результат в історії
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, str(result))         # Виводить результат у поле
            except Exception:
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, "Помилка")

        # Якщо "C" — очищаємо поле
        elif char == 'C':
            self.entry.delete(0, tkinter.END)
        elif char in ('sin', 'cos', 'tan', 'log', '√', 'ctg'):  # Обробка математичних функцій
            try:
                expr = self.entry.get()

                if expr == "":
                    return
                value = float(eval(self.parse_expression(expr))) #Обчислення звичайних мат. дій

                # Обчислення відповідної функції
                if char == '√':
                    result = sqrt(value)
                elif char == 'sin':
                    result = sin(radians(value))
                elif char == 'cos':
                    result = cos(radians(value))
                elif char == 'tan':
                    result = tan(radians(value))
                elif char == 'ctg':
                    result = 1/tan(radians(value))
                elif char == 'log':
                    result = log(value)
                self.add_to_history(f"{char}({expr})", result)  # Запис до історії
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, str(result))
            except Exception:
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, "Помилка")
        else:
            self.entry.insert(tkinter.END, char)    # Якщо звичайний символ (цифра, +, -, .) — він додається до поля вводу

    def parse_expression(self, expr):   # Заміна √ на функцію sqrt для Python
        return expr.replace('√', 'sqrt')

    def add_to_history(self, expr, result): # Додаємо новий рядок до історії
        entry = f"{expr} = {result}"                            # Формується запис
        self.history.append(entry)                              # Додається в список
        self.history_box.configure(state='normal')              # Дозволяється редагування
        self.history_box.insert(tkinter.END, entry + '\n')      # Додається запис
        self.history_box.configure(state='disabled')            # Блокується редагування знову

    # Показ контекстного меню при натисканні ПКМ
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    # Скопіювати текст з поля вводу
    def copy_text(self):
        text = self.entry.get()
        self.master.clipboard_clear()
        self.master.clipboard_append(text)

    # Вставити текст із буфера обміну
    def paste_text(self):
        try:
            text = self.master.clipboard_get()
            self.entry.insert(tkinter.END, text)
        except:
            pass    # Якщо буфер порожній — нічого не робити

    # Очистити поле вводу
    def clear_entry(self):
        self.entry.delete(0, tkinter.END)

    # Перемикання темної/світлої теми
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    # Застосувати обрану тему до всіх елементів GUI
    def apply_theme(self):
        backg = "#1e1e1e" if self.dark_mode else "#ffffff"          # Фон
        text = "#ffffff" if self.dark_mode else "#000000"           # Колір тексту
        entry_backg = "#2e2e2e" if self.dark_mode else "#ffffff"    # Фон поля вводу

        self.master.configure(bg=backg)
        self.entry.configure(bg=entry_backg, fg=text, insertbackground=text)
        for widget in self.master.winfo_children(): #Пробігає по всім елементам та задіює зміну Теми
            if isinstance(widget, tkinter.Button):
                widget.configure(bg=backg, fg=text, activebackground=entry_backg, activeforeground=text, highlightbackground=backg)
            elif isinstance(widget, tkinter.Entry):
                widget.configure(bg=entry_backg, fg=text)

    # Запуск програми
if __name__ == "__main__":
    root = tkinter.Tk()
    calculator = Calculator(root)
    root.mainloop()