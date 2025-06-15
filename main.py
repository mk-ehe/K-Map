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
        rows = len(kmap)
        cols = len(kmap[0])
        group_number = 1
        grouped = [[None for row in range(len(kmap[0]))] for col in range(len(kmap))]
        color_cycle = cycle(["#FF0000","#00FF00","#0000FF","#FFFF00","#00FFFF","#FF00FF","#FF8000","#8000FF","#00FF80","#80FF00","#0080FF","#FF0080","#C0C0C0","#808080","#00FFFF","#7FFFD4","#A0CFCF","#FFE4C4","#FFEBCD","#8A2BE2","#A52A2A","#DEB887","#5F9EA0","#7FFF00","#FF7F50","#6495ED","#F5EBC3","#DC143C","#00FFFF","#00008B","#008B8B","#B8860B","#A9A9A9","#006400","#BDB76B","#8B008B","#556B2F","#FF8C00","#9932CC","#8B0000","#E9967A","#8FBC8F","#483D8B","#2F4F4F","#00CED1"])
        color = next(color_cycle)
        if kmap:
            self.groupBy_called = True

            if all(val == group_by or val == "-" for row in kmap for val in row):
                """checks if whole map is value to group by"""
                for r, row in enumerate(kmap):
                    for c, val in enumerate(row):
                        self.buttons[r][c].config(bg=color)
                        grouped[r][c] = str(group_number)
                print(grouped)
                return
            
            for r, row in enumerate(kmap):
                for c, col in enumerate(row):
                    self.buttons[r][c].config(bg="SystemButtonFace")

                    if row[c] == group_by:
                        """groups all values one by one"""
                        color = next(color_cycle)
                        self.buttons[r][c].config(bg=color)
                        grouped[r][c] = str(group_number)
                        group_number += 1


                    if row.count(group_by) + row.count("-") == 2 or row.count(group_by) + row.count("-") == 3:
                        for cl in range(len(row) - 1):
                            if (row[cl] == row[0] and row[cl] == group_by) and (row[-1] == group_by or row[-1] == "-"):
                                """groups(only 1 group of 2) value horizontally if on the other side(wrap-around)"""
                                color = next(color_cycle)
                                self.buttons[r][cl].config(bg=color)
                                self.buttons[r][-1].config(bg=color)
                                grouped[r][cl] = str(group_number)
                                grouped[r][-1] = str(group_number)
                                group_number += 1

                                
                            elif (row[cl] == group_by) and (row[cl+1] == group_by or row[cl+1] == "-"):
                                """groups(2) value horizontally if next to eachother"""
                                color = next(color_cycle)
                                self.buttons[r][cl].config(bg=color)
                                self.buttons[r][cl+1].config(bg=color)
                                grouped[r][cl] = str(group_number)
                                grouped[r][cl+1] = str(group_number)
                                group_number += 1
                            

                            elif (row[cl] == row[0] and (row[cl] == group_by or row[cl] == "-")) and (row[-1] == group_by or row[-1] == "-") and (
                                kmap[r-1][cl] == kmap[r-1][0] and (kmap[r-1][cl] == group_by or kmap[r-1][cl] == "-")) and (
                                kmap[r-1][-1] == group_by or kmap[r-1][-1] == "-") and (
                                not all(i[0] == "-" for i in [row[cl], row[-1], kmap[r-1][cl], kmap[r-1][-1]])
                                ):
                                """wrap-around group into one big group if next to eachother"""
                                color = next(color_cycle)
                                self.buttons[r][cl].config(bg=color)
                                self.buttons[r][-1].config(bg=color)
                                self.buttons[r-1][cl].config(bg=color)
                                self.buttons[r-1][-1].config(bg=color)
                                grouped[r][cl] = str(group_number)
                                grouped[r][-1] = str(group_number)
                                grouped[r-1][cl] = str(group_number)
                                grouped[r-1][-1] = str(group_number)
                                group_number += 1


                            elif (kmap[0][0] == group_by or kmap[0][0] == "-") and (kmap[0][-1] == group_by or kmap[0][-1] == "-") and (
                                kmap[-1][0] == group_by or kmap[-1][0] == "-") and (kmap[-1][-1] == group_by or kmap[-1][-1] == "-") and (
                                not all(i[0] == "-" for i in [kmap[0][0], kmap[0][-1], kmap[-1][0], kmap[-1][-1]])
                            ):
                                """checks corners and groups them"""
                                self.buttons[0][0].config(bg=color)
                                self.buttons[0][-1].config(bg=color)
                                self.buttons[-1][0].config(bg=color)
                                self.buttons[-1][-1].config(bg=color)
                                grouped[0][0] = str(group_number)
                                grouped[0][-1] = str(group_number)
                                grouped[-1][0] = str(group_number)
                                grouped[-1][-1] = str(group_number)
                                group_number += 1


                    if all(col == group_by or col == "-" for col in row) and any(col == group_by for col in row):
                        """groups whole rows where 4 same values one by one"""
                        color = next(color_cycle)
                        for c in range(cols):
                            self.buttons[r][c].config(bg=color)
                            grouped[r][c] = str(group_number)
                        group_number += 1


            for c in range(cols):
                if all(kmap[r][c] == group_by or kmap[r][c] == "-" for r in range(rows)) and any(kmap[r][c] == group_by for r in range(rows)):
                    """checks whole columns where 4 same values one by one"""
                    color = next(color_cycle)
                    for r in range(rows):
                        self.buttons[r][c].config(bg=color)
                        grouped[r][c] = str(group_number)
                    group_number += 1


        group_map = {}
        next_group = 1
        for i, row in enumerate(grouped):
            for j, val in enumerate(row):
                if val is not None:
                    if val not in group_map:
                        """correcting group number"""
                        print(group_map)
                        group_map[val] = str(next_group)
                        next_group += 1
                        print(group_map)
                    grouped[i][j] = group_map[val]

        for i in grouped:
            print(i)


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