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
        self.choose_map = OptionMenu(self.master, self.dropdown_var, *self.options, command=self.changeMap)
        self.choose_map.config(width=10)
        self.choose_map.place(x=400, y=10)


        self.dropdown_gr = StringVar(self.master)
        self.dropdown_gr.set("Select Grouping")
        self.gr_options = ["0", "1"]
        self.group = OptionMenu(self.master, self.dropdown_gr, *self.gr_options, command=self.groupBy)
        self.group.config(width=14)
        self.group.place(x=510, y=10)


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
                btn = Button(self.button_frame, text='0', width=3, height=1, font=('arial', 16, 'bold'), command=lambda r=r, c=c: self.changeSign(self.buttons[r][c]))
                btn.grid(row=r+1, column=c+1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)


    def getKmapValues(self):
        try:
            return [[btn.cget('text') for btn in row] for row in self.buttons]
        except AttributeError:
            pass
    

    def colorGroups(self, grouped):
        group_colors = {}
        color_cycle = cycle([
            "#FF5C5C", "#AEFFAE", "#7070FF", "#E0E06B",
            "#9BFFFF", "#FF93FF", "#FFB56B", "#B061FF",
            "#61FFB0", "#ADFF5C", "#FF48A3", "#808080"
        ])
        for r in range(len(grouped)):
            for c in range(len(grouped[0])):
                group_id = grouped[r][c]
                if group_id is not None:
                    if group_id not in group_colors:
                        group_colors[group_id] = next(color_cycle)
                    color = group_colors[group_id]
                    self.buttons[r][c].config(bg=color)


    def groupBy(self, group_by):
        self.dropdown_gr.set("Select Grouping")
        kmap = self.getKmapValues()
        rows = len(kmap)
        cols = len(kmap[0])
        group_number = 1
        grouped = [[None for _ in range(cols)] for _ in range(rows)]

        # Reset all button colors
        for r in range(rows):
            for c in range(cols):
                self.buttons[r][c].config(bg="SystemButtonFace")

        if kmap:
            row_vars = {2:1, 4:2, 8:3}.get(rows, 1)
            col_vars = {2:1, 4:2, 8:3}.get(cols, 1)
            row_labels = gray_labels(row_vars)
            col_labels = gray_labels(col_vars)


            # Whole map group
            if all(val == group_by or val == "-" for row in kmap for val in row):
                for r in range(rows):
                    for c in range(cols):
                        grouped[r][c] = str(group_number)
                self.colorGroups(grouped)
                print("    ", end="")
                for label in col_labels:
                    print(f"{label:^5}", end="")
                print()
                for r, row in enumerate(grouped):
                    print(f"{row_labels[r]:>3} ", end="")
                    for val in row:
                        print(f"{str(val) if val is not None else '.':^5}", end="")
                    print()
                print()
                return



            # Vertical pairs
            for c in range(cols):
                for r in range(rows - 1):
                    if ((kmap[r][c] == group_by and (kmap[r+1][c] == group_by or kmap[r+1][c] == "-")) or
                        (kmap[r][c] == "-" and kmap[r+1][c] == group_by)):
                        grouped[r][c] = str(group_number)
                        grouped[r+1][c] = str(group_number)
                        group_number += 1

            # Main grouping logic
            for r, row in enumerate(kmap):
                # Horizontal pairs and wrap-around in row
                for cl in range(cols - 1):
                    if row.count(group_by) + row.count("-") in (2, 3):
                        if ((row[cl] == group_by and (row[cl+1] == group_by or row[cl+1] == "-")) or
                            (row[cl] == "-" and row[cl+1] == group_by)):
                            grouped[r][cl] = str(group_number)
                            grouped[r][cl+1] = str(group_number)
                            group_number += 1


                        # Horizontal wrap-around
                        if ((row[0] == group_by or row[0] == "-") and
                            (row[-1] == group_by or row[-1] == "-") and
                            (row[0] == group_by or row[-1] == group_by)):
                            grouped[r][0] = str(group_number)
                            grouped[r][-1] = str(group_number)
                            group_number += 1


                # Horizontal wrap-around 2x2 block
                cells = [kmap[r][0], kmap[r][-1], kmap[r-1][0], kmap[r-1][-1]]
                if all(cell == group_by or cell == "-" for cell in cells) and any(cell == group_by for cell in cells):
                    grouped[r][0] = str(group_number)
                    grouped[r][-1] = str(group_number)
                    grouped[r-1][0] = str(group_number)
                    grouped[r-1][-1] = str(group_number)
                    group_number += 1


            # Vertical wrap-around pairs and 2x2 block
            for c in range(cols):
                col_vals = [kmap[r][c] for r in range(rows)]
                if col_vals.count(group_by) + col_vals.count("-") in (2, 3):
                    if ((col_vals[0] == group_by or col_vals[0] == "-") and
                        (col_vals[-1] == group_by or col_vals[-1] == "-") and
                        (col_vals[0] == group_by or col_vals[-1] == group_by)):
                        grouped[0][c] = str(group_number)
                        grouped[-1][c] = str(group_number)
                        group_number += 1

                    cells = [kmap[0][c], kmap[-1][c], kmap[0][c-1], kmap[-1][c-1]]
                    if all(cell == group_by or cell == "-" for cell in cells) and any(cell == group_by for cell in cells):
                        grouped[0][c] = str(group_number)
                        grouped[-1][c] = str(group_number)
                        grouped[0][c-1] = str(group_number)
                        grouped[-1][c-1] = str(group_number)
                        group_number += 1


            # Corners
            if (kmap[0][0] == group_by or kmap[0][0] == "-") and (kmap[0][-1] == group_by or kmap[0][-1] == "-") and (
                kmap[-1][0] == group_by or kmap[-1][0] == "-") and (kmap[-1][-1] == group_by or kmap[-1][-1] == "-") and (
                not all(i == "-" for i in [kmap[0][0], kmap[0][-1], kmap[-1][0], kmap[-1][-1]])):
                grouped[0][0] = str(group_number)
                grouped[0][-1] = str(group_number)
                grouped[-1][0] = str(group_number)
                grouped[-1][-1] = str(group_number)
                group_number += 1


            # Full columns
            for c in range(cols):
                if all(kmap[r][c] == group_by or kmap[r][c] == "-" for r in range(rows)) and any(kmap[r][c] == group_by for r in range(rows)):
                    for r in range(rows):
                        grouped[r][c] = str(group_number)
                    group_number += 1


            # Full rows
            for r, row in enumerate(kmap):
                if all(col == group_by or col == "-" for col in row) and any(col == group_by for col in row):
                    for c in range(cols):
                        grouped[r][c] = str(group_number)
                    group_number += 1


            # All 2x2 and larger rectangles
            for r1 in range(rows):
                for r2 in range(r1+1, rows):
                    for c1 in range(cols):
                        for c2 in range(c1+1, cols):
                            cells = [kmap[r][c] for r in range(r1, r2+1) for c in range(c1, c2+1)]
                            if all(cell == group_by or cell == "-" for cell in cells) and any(cell == group_by for cell in cells):
                                for r in range(r1, r2+1):
                                    for c in range(c1, c2+1):
                                        grouped[r][c] = str(group_number)
                                group_number += 1


            # Adjacent rows
            for r in range(rows - 1):
                if all(col == group_by or col == "-" for col in kmap[r]) and any(col == group_by for col in kmap[r]) and (
                    all(col == group_by or col == "-" for col in kmap[r+1]) and any(col == group_by for col in kmap[r+1])):
                    for c in range(cols):
                        grouped[r][c] = str(group_number)
                        grouped[r+1][c] = str(group_number)
                    group_number += 1


            # Wrap-around rows
            if all(col == group_by or col == "-" for col in kmap[0]) and any(col == group_by for col in kmap[0]) and (
                all(col == group_by or col == "-" for col in kmap[-1]) and any(col == group_by for col in kmap[-1])):
                for c in range(cols):
                    grouped[0][c] = str(group_number)
                    grouped[-1][c] = str(group_number)
                group_number += 1


            # Adjacent columns
            for c in range(cols - 1):
                col1 = [kmap[r][c] for r in range(rows)]
                col2 = [kmap[r][c+1] for r in range(rows)]
                if (all(val == group_by or val == "-" for val in col1) and any(val == group_by for val in col1) and
                    all(val == group_by or val == "-" for val in col2) and any(val == group_by for val in col2)):
                    for r in range(rows):
                        grouped[r][c] = str(group_number)
                        grouped[r][c+1] = str(group_number)
                    group_number += 1


            # Wrap-around columns
            col_first = [kmap[r][0] for r in range(rows)]
            col_last = [kmap[r][cols-1] for r in range(rows)]
            if (all(val == group_by or val == "-" for val in col_first) and any(val == group_by for val in col_first) and
                all(val == group_by or val == "-" for val in col_last) and any(val == group_by for val in col_last)):
                for r in range(rows):
                    grouped[r][0] = str(group_number)
                    grouped[r][cols-1] = str(group_number)
                group_number += 1


            # Final single cell grouping (if not already grouped)
            for r, row in enumerate(kmap):
                for c, val in enumerate(row):
                    if val == group_by and grouped[r][c] is None:
                        grouped[r][c] = str(group_number)
                        group_number += 1


        group_map = {}
        next_group = 1
        for i, row in enumerate(grouped):
            for j, val in enumerate(row):
                if val is not None:
                    if val not in group_map:
                        group_map[val] = str(next_group)
                        next_group += 1
                    grouped[i][j] = group_map[val]

        self.colorGroups(grouped)
        
        print("    ", end="")
        for label in col_labels:
            print(f"{label:^5}", end="")
        print()
        for r, row in enumerate(grouped):
            print(f"{row_labels[r]:>3} ", end="")
            for val in row:
                print(f"{str(val) if val is not None else '.':^5}", end="")
            print()
        print()
                

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
        if kmap:
            for r, row in enumerate(kmap):
                for c, val in enumerate(row):
                    self.buttons[r][c].config(bg="SystemButtonFace")
                    

    def changeMap(self, value):
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