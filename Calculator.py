import tkinter  # Імпорт бібліотеки для створення GUI та математичних функцій
from math import sin, cos, tan, log, sqrt, radians
import re

class Calculator:   # Клас калькулятора
    def __init__(self, master):
        self.master = master
        master.title("Продвинутий калькулятор")
        master.geometry("500x600")
        self.mode = "Звичайний"
        self.mode_buttons = {}

        self.dark_mode = False  # Стан темної теми (False = світла)

        self.history = []   # Список для історії обчислень

        self.entry = tkinter.Entry(master, width=30, font=('Arial', 18), borderwidth=2, relief="groove")
        self.entry.grid(row=1, column=0, columnspan=5, padx=10, pady=10)
        self.entry.bind("<Button-3>", self.show_context_menu)

        self.create_buttons()

        self.header_frame = tkinter.Frame(master)
        self.header_frame.grid(row=0, column=0, columnspan=5, pady=(30, 0), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.toggle_theme_button = tkinter.Button(self.header_frame, text="Тема", font=('Arial', 12),
                                                  command=self.toggle_theme)
        self.toggle_theme_button.grid(row=0, column=0, sticky="w", padx=(10, 0))

        self.history_box = tkinter.Text(master, height=6, width=45, font=('Arial', 10))
        self.history_box.grid(row=8, column=0, columnspan=5, padx=10, pady=5)
        self.history_box.configure(state='disabled')

        self.context_menu = tkinter.Menu(master, tearoff=0)
        self.context_menu.add_command(label="Скопіювати", command=self.copy_text)
        self.context_menu.add_command(label="Вставити", command=self.paste_text)
        self.context_menu.add_command(label="Очистити", command=self.clear_entry)

        self.modes = ["Звичайний", "Інженерний", "Продвинутий"]

        self.mode_menu_button = tkinter.Menubutton(self.header_frame, text="Режим", font=('Arial', 10), relief="raised")
        self.mode_menu_button.grid(row=0, column=2, sticky="e", padx=5)

        self.mode_menu = tkinter.Menu(self.mode_menu_button, tearoff=0)
        self.mode_menu_button.configure(menu=self.mode_menu)

        self.mode_var = tkinter.StringVar(value=self.mode)
        for mode in self.modes:
            self.mode_menu.add_radiobutton(label=mode, variable=self.mode_var,
                                           value=mode,
                                           command=lambda m=mode: self.set_mode(m))
        self.apply_theme()

    def create_buttons(self):
        for widget in self.master.grid_slaves():
            if isinstance(widget,
                          tkinter.Button) and widget not in self.mode_buttons.values() and widget != self.toggle_theme_button:
                widget.destroy()

        if self.mode == "Звичайний":
            buttons = [
                ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
                ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
                ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
                ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
                ('C', 6, 0), ('%', 6, 1),
            ]
        elif self.mode == "Інженерний":
            buttons = [
                ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('√', 2, 4),
                ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('^', 3, 4),
                ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('log', 4, 4),
                ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3), ('C', 5, 4), ('%', 6, 4),
            ]
        else:  # Продвинутий
            buttons = [
                ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('√', 2, 4),
                ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('^', 3, 4),
                ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('log', 4, 4),
                ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3), ('C', 5, 4), ('%', 6, 4),
                ('sin', 6, 0), ('cos', 6, 1), ('tan', 6, 2), ('ctg', 6, 3),
            ]

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

            bg = "#1e1e1e" if self.dark_mode else "#ffffff"
            fg = "#ffffff" if self.dark_mode else "#000000"
            active_bg = "#2e2e2e" if self.dark_mode else "#e0e0e0"
            btn.configure(bg=bg, fg=fg, activebackground=active_bg, activeforeground=fg, highlightbackground=bg)

    def on_button_click(self, char):
        global result
        if char == '=':
            try:
                expression = self.entry.get().replace('^', '**')
                expression = self.parse_percent(expression)
                expression = self.parse_expression(expression)
                result = eval(expression)
                self.add_to_history(self.entry.get(), result)
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, str(result))
            except Exception:
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, "Помилка")

        elif char == 'C':
            self.entry.delete(0, tkinter.END)
        elif char in ('sin', 'cos', 'tan', 'log', '√', 'ctg'):
            try:
                expr = self.entry.get()
                if expr == "":
                    return
                value = float(eval(self.parse_percent(self.parse_expression(expr))))

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
                self.add_to_history(f"{char}({expr})", result)
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, str(result))
            except Exception:
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, "Помилка")
        elif char == '%':
            # Просто додамо '%' у поле, обробляти будемо при '='
            self.entry.insert(tkinter.END, char)
        else:
            self.entry.insert(tkinter.END, char)

    def parse_expression(self, expr):
        return expr.replace('√', 'sqrt')

    def parse_percent(self, expr):
        # Заміна виразів виду a + b% на a + (a * b / 100)
        # Працює для +, -, *, /
        # Використовуємо регулярні вирази для пошуку "число операція число%"
        def repl(match):
            a = match.group(1)
            op = match.group(2)
            b = match.group(3)
            try:
                a_val = float(a)
                b_val = float(b)
            except:
                return match.group(0)
            if op in ('+', '-'):
                return f"{a}{op}({a}*{b}/100)"
            elif op in ('*', '/'):
                # Тут просто замінюємо b% на (b/100)
                return f"{a}{op}({b}/100)"
            else:
                return match.group(0)

        pattern = r'([-+]?\d*\.?\d+)\s*([\+\-\*/])\s*([-+]?\d*\.?\d+)%'
        while re.search(pattern, expr):
            expr = re.sub(pattern, repl, expr)
        # Якщо у виразі є просто число зі знаком %, замінимо на (число/100)
        expr = re.sub(r'(\d+\.?\d*)%', r'(\1/100)', expr)
        return expr

    def add_to_history(self, expr, result):
        entry = f"{expr} = {result}"
        self.history.append(entry)
        self.history_box.configure(state='normal')
        self.history_box.insert(tkinter.END, entry + '\n')
        self.history_box.configure(state='disabled')

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def copy_text(self):
        text = self.entry.get()
        self.master.clipboard_clear()
        self.master.clipboard_append(text)

    def paste_text(self):
        try:
            text = self.master.clipboard_get()
            self.entry.insert(tkinter.END, text)
        except:
            pass

    def clear_entry(self):
        self.entry.delete(0, tkinter.END)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        backg = "#1e1e1e" if self.dark_mode else "#ffffff"
        text = "#ffffff" if self.dark_mode else "#000000"
        entry_backg = "#2e2e2e" if self.dark_mode else "#ffffff"
        menu_backg = "#2e2e2e" if self.dark_mode else "SystemMenu"
        menu_fg = "#ffffff" if self.dark_mode else "#000000"

        self.master.configure(bg=backg)
        self.entry.configure(bg=entry_backg, fg=text, insertbackground=text)

        for widget in self.master.winfo_children():
            if isinstance(widget, tkinter.Button):
                widget.configure(bg=backg, fg=text, activebackground=entry_backg, activeforeground=text,
                                 highlightbackground=backg)
            elif isinstance(widget, tkinter.Entry):
                widget.configure(bg=entry_backg, fg=text)

        self.mode_menu_button.configure(bg=backg, fg=text, activebackground=entry_backg, activeforeground=text,
                                        highlightbackground=backg)

        self.mode_menu.configure(background=menu_backg, foreground=menu_fg, activebackground=entry_backg,
                                 activeforeground=text)
        self.header_frame.configure(bg=backg)
        self.toggle_theme_button.configure(bg=backg, fg=text, activebackground=entry_backg, activeforeground=text,
                                           highlightbackground=backg)

        self.update_mode_buttons()

    def set_mode(self, mode):
        self.mode = mode
        self.create_buttons()
        self.mode_menu_button.config(text=f"Режим: {mode}")

    def update_mode_buttons(self):
        for m, btn in self.mode_buttons.items():
            if m == self.mode:
                btn.config(relief="sunken", bg="#888888" if self.dark_mode else "#cccccc",
                           fg="#ffffff" if self.dark_mode else "#000000")
            else:
                btn.config(relief="raised", bg="#1e1e1e" if self.dark_mode else "SystemButtonFace",
                           fg="#ffffff" if self.dark_mode else "#000000")

if __name__ == "__main__":
    root = tkinter.Tk()
    calculator = Calculator(root)
    root.mainloop()
