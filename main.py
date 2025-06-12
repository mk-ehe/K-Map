from tkinter import *

window = Tk()

window.geometry("1000x500")
window.resizable(False, False)
window.title("K-Map Solver")


def changeSign(button):
    signs = ['0','1','-']
    if button.cget('text') == '0':
        button.config(text=signs[1])
    elif button.cget('text') == '1':
        button.config(text=signs[2])
    else:
        button.config(text=signs[0])

button_frame = Frame(window)
button_frame.pack(pady=40, anchor='n', expand=True)

button_0x0 = Button(button_frame,
                     text='0',
                     width=3,
                     height=1,
                     font=('arial',16,'bold'),
                     command=lambda:changeSign(button_0x0))
button_0x0.grid(column=0, row=0)

button_0x1 = Button(button_frame,
                     text='0',
                     width=3,
                     height=1,
                     font=('arial',16,'bold'),
                     command=lambda:changeSign(button_0x1))
button_0x1.grid(column=1, row=0)

button_1x0 = Button(button_frame,
                     text='0',
                     width=3,
                     height=1,
                     font=('arial',16,'bold'),
                     command=lambda:changeSign(button_1x0))
button_1x0.grid(column=0, row=1)

button_1x1 = Button(button_frame,
                     text='0',
                     width=3,
                     height=1,
                     font=('arial',16,'bold'),
                     command=lambda:changeSign(button_1x1))
button_1x1.grid(column=1, row=1)



window.mainloop()