from tkinter import *

class KMapSolver:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x500")
        self.master.resizable(False, False)
        self.master.title("K-Map Solver")

        self.button_frame = Frame(self.master, pady=20)
        self.button_frame.place(relx=0.5, y=40, anchor='n')

        self.value = ""
        
        self.dropdown_var = StringVar(self.master)
        self.dropdown_var.set("Select Map")

        self.options = ["2x2", "2x4", "4x4", "4x8"]
        self.dropdown = OptionMenu(self.master,
                                   self.dropdown_var,
                                   *self.options,
                                   command=self.changeDimensions)
        self.dropdown.config(width=10)
        self.dropdown.place(relx=0.5, y=10, anchor='n')


    def createMap(self, rows, columns):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.buttons = []

        for r in range(int(rows)):
            row = []
            for c in range(int(columns)):
                btn = Button(
                    self.button_frame,
                    text='0',
                    width=3,
                    height=1,
                    font=('arial', 16, 'bold'),
                    command=lambda b=None: self.changeSign(b))
                btn.grid(row=r, column=c)
                row.append(btn)
            self.buttons.append(row)

        for r in range(rows):
            for c in range(columns):
                self.buttons[r][c].config(command=lambda b=self.buttons[r][c]: self.changeSign(b))


    def changeSign(self, button):
        signs = ['0', '1', '-']
        current = button.cget('text')
        if current == '0':
            button.config(text=signs[1])
        elif current == '1':
            button.config(text=signs[2])
        else:
            button.config(text=signs[0])
    

    def changeDimensions(self, value):
        self.value = self.dropdown.cget('text')

        if self.value == "2x2":
            self.createMap(2,2)
        elif self.value == "2x4":
            self.createMap(2,4)
        elif self.value == "4x4":
            self.createMap(4,4)
        elif self.value == "4x8":
            self.createMap(4,8)


if __name__ == "__main__":
    root = Tk()
    app = KMapSolver(root)
    root.mainloop()