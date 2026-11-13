from tkinter import *
window = Tk()
label = Label(window,
              text="Hello",
              font=('Arial',48,'bold'),
              fg="#57B057",
              bg='black',
              )
label.pack()
label.place(x=0,y=0)
window.geometry("420x420")
window.title("Case CLosed")

window.config(background="white")
window.mainloop()