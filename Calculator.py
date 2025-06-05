import tkinter
from math import sin, cos, tan, log, sqrt, radians, factorial, exp, fabs, floor, ceil

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Продвинутий калькулятор")

        self.history = []

        self.entry = tkinter.Entry(master, width=30, font=('Arial', 18), borderwidth=2, relief="groove")
        self.entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
        self.entry.bind("<Button-3>", self.show_context_menu)

        self.create_buttons()

        self.history_box = tkinter.Text(master, height=6, width=45, font=('Arial', 10))
        self.history_box.grid(row=6, column=0, columnspan=5, padx=10, pady=5)
        self.history_box.configure(state='disabled')

        self.context_menu = tkinter.Menu(master, tearoff=0)
        self.context_menu.add_command(label="Скопіювати", command=self.copy_text)
        self.context_menu.add_command(label="Вставити", command=self.paste_text)
        self.context_menu.add_command(label="Очистити", command=self.clear_entry)

    def create_buttons(self):
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('√', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('^', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('log', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('C', 4, 4),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2),('ctg', 5, 3)
        ]

        for (text, row, col) in buttons:
            tkinter.Button(
                self.master,
                text=text,
                width=6,
                height=2,
                font=('Arial', 14),
                command=lambda t=text: self.on_button_click(t)
            ).grid(row=row, column=col, padx=2, pady=2)

    def on_button_click(self, char):
        if char == '=':
            try:
                expression = self.entry.get().replace('^', '**')
                parsed = self.parse_expression(expression)
                result = eval(parsed)
                self.add_to_history(expression, result)
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
                value = float(eval(self.parse_expression(expr)))
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
                self.add_to_history(f"{char}({expr})", result)
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, str(result))
            except Exception:
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, "Помилка")
        else:
            self.entry.insert(tkinter.END, char)

    def parse_expression(self, expr):
        return expr.replace('√', 'sqrt')

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


if __name__ == "__main__":
    root = tkinter.Tk()
    calculator = Calculator(root)
    root.mainloop()
