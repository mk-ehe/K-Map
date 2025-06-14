from tkinter import *
from itertools import cycle

def gray_labels(n):
    return [format(i ^ (i >> 1), f'0{n}b') for i in range(2**n)]

class KMapSolver:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x500")
        self.master.resizable(False, False)
        self.master.title("K-Map Solver")

        self.button_frame = Frame(self.master, pady=30)
        self.button_frame.place(relx=0.5, y=40, anchor='n')

        self.function_label_row = Label(master, text="", font=('arial', 14, 'bold'), justify="right", anchor="e")
        self.function_label_col = Label(master, text="", font=('arial', 14, 'bold'))

        self.value = ""
        
        self.dropdown_var = StringVar(self.master)
        self.dropdown_var.set("Select Map")
        self.options = ["2x2", "2x4", "4x4", "4x8"]
        self.choose_map = OptionMenu(self.master, self.dropdown_var, *self.options, command=self.changeDimensions)
        self.choose_map.config(width=10)
        self.choose_map.place(x=400, y=10)


        self.dropdown_gr = StringVar(self.master)
        self.dropdown_gr.set("Select Grouping")
        self.gr_options = ["0", "1"]
        self.group = OptionMenu(self.master, self.dropdown_gr, *self.gr_options, command=self.groupBy)
        self.group.config(width=14)
        self.group.place(x=510, y=10)

        self.groupBy_called = False


    def createMap(self, rows, columns):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.buttons = []

        row_vars = {2:1, 4:2, 8:3}.get(rows, 1)
        col_vars = {2:1, 4:2, 8:3}.get(columns, 1)

        row_labels = gray_labels(row_vars)      
        col_labels = gray_labels(col_vars)     
        
        for c, label in enumerate(col_labels):
            lbl = Label(self.button_frame, text=label, font=('arial', 14, 'bold'))
            lbl.grid(row=0, column=c+1, padx=2, pady=2)

        for r, row_label in enumerate(row_labels):
            lbl = Label(self.button_frame, text=row_label, font=('arial', 14, 'bold'))
            lbl.grid(row=r+1, column=0, padx=2, pady=2)
            row_buttons = []

            for c in range(len(col_labels)):
                btn = Button(self.button_frame, text='0', width=3, height=1, font=('arial', 16, 'bold'), command=lambda b=None: self.changeSign(b))
                btn.grid(row=r+1, column=c+1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        for r in range(len(row_labels)):
            for c in range(len(col_labels)):
                self.buttons[r][c].config(command=lambda b=self.buttons[r][c]: self.changeSign(b))


    def getKmapValues(self):
        try:
            return [[btn.cget('text') for btn in row] for row in self.buttons]
        except AttributeError:
            pass
    

    def groupBy(self, group_by):
        self.dropdown_gr.set("Select Grouping")
        kmap = self.getKmapValues()
        group_number = 1
        grouped = [[None for row in range(len(kmap[0]))] for col in range(len(kmap))]
        color_cycle = cycle(["#FF6767", "#8AFF8A", "#6E6EFF", "#FFFF87", "#00FFFF", "#FF71FF", "#FFB01D", "#8F2D8F", "#008000", "#39398F", "#FFC0CB", "#808080", "#883535", "#00FFC8"])
        if kmap:
            self.groupBy_called = True
            for r, row in enumerate(kmap):
                color = next(color_cycle)
                for c, val in enumerate(row):
                    self.buttons[r][c].config(bg="SystemButtonFace")
                    
                    if row[c] == "1":
                        color = next(color_cycle)
                        self.buttons[r][c].config(bg=color)
                        grouped[r][c] = str(group_number)
                        
                    if all(val == group_by or val == "-" for val in row):
                        color = next(color_cycle)
                        for i in range(len(row)):
                            self.buttons[r][i].config(bg=color)
                            grouped[r][i] = str(group_number)
                            

                    elif row.count(group_by) + row.count("-") == 2 or row.count(group_by) + row.count("-") == 3:
                        for c in range(len(row) - 1):
                            if (row[c] == group_by) and (row[c+1] == group_by or row[c+1] == "-"):
                                color = next(color_cycle)
                                self.buttons[r][c].config(bg=color)
                                self.buttons[r][c+1].config(bg=color)
                                grouped[r][c] = str(group_number)
                                grouped[r][c+1] = str(group_number)
                                group_number += 1

                            elif (row[c] == group_by) and (row[c-1] == group_by or row[c-1] == "-"):
                                color = next(color_cycle)
                                self.buttons[r][c].config(bg=color)
                                self.buttons[r][c-1].config(bg=color)
                                grouped[r][c] = str(group_number)
                                grouped[r][c-1] = str(group_number)
                                group_number += 1
                                
                            elif (row[c] == group_by) and (row[-1] == group_by or row[-1] == "-"):
                                color = next(color_cycle)
                                self.buttons[r][c].config(bg=color)
                                self.buttons[r][-1].config(bg=color)
                                grouped[r][c] = str(group_number)
                                grouped[r][-1] = str(group_number)
                                group_number += 1

        print(grouped)




    def changeSign(self, button):
        signs = ['0', '1', '-']
        current = button.cget('text')
        if current == '0':
            button.config(text=signs[1])
        elif current == '1':
            button.config(text=signs[2])
        else:
            button.config(text=signs[0])

        kmap = self.getKmapValues()
        if kmap and self.groupBy_called == True:
            for r, row in enumerate(kmap):
                for c, val in enumerate(row):
                    self.buttons[r][c].config(bg="SystemButtonFace")
                    self.groupBy_called = False
                    

    def changeDimensions(self, value):
        self.value = self.choose_map.cget('text')

        if self.value == "2x2":
            self.createMap(2,2)
            self.function_label_row.config(text="A")
            self.function_label_col.config(text="B")
            self.function_label_row.place(x=440, y=143, anchor="e")
            self.function_label_col.place(x=500, y=44)
            
        elif self.value == "2x4":
            self.createMap(2,4)
            self.function_label_row.config(text="A")
            self.function_label_col.config(text="BC")
            self.function_label_row.place(x=390, y=143, anchor="e")
            self.function_label_col.place(x=493, y=44)

        elif self.value == "4x4":
            self.createMap(4,4)
            self.function_label_row.config(text="AB")
            self.function_label_col.config(text="CD")
            self.function_label_row.place(x=380, y=185, anchor="e")
            self.function_label_col.place(x=498, y=44)
            
        elif self.value == "4x8":
            self.createMap(4,8)
            self.function_label_row.config(text="AB")
            self.function_label_col.config(text="CDE")
            self.function_label_row.place(x=280, y=185, anchor="e")
            self.function_label_col.place(x=491, y=44)


if __name__ == "__main__":
    root = Tk()
    app = KMapSolver(root)
    root.mainloop()