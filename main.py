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
button_frame.place()

button_0x00 = Button(button_frame,
                     text='0',
                     width=3,
                     height=1,
                     font=('arial',16,'bold'),
                     command=lambda:changeSign(button_0x00))


button_0x00.grid(column=0, row=0)


button_0x01 = Button(button_frame,
                     text='0',
                     width=3,
                     height=1,
                     font=('arial',16,'bold'),
                     command=lambda:changeSign(button_0x01))

button_0x01.grid(column=1, row=0)



window.mainloop()