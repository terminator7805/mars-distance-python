from tkinter import *
window = Tk()
#window.overrideredirect(True)
window.title('Mars')
window.iconphoto(False, PhotoImage(file='resources/3D_Mars.png'))
text1 = Label(text='Prueba')
text1.pack()

def enviar():
    prueba = Label(text="A")
    prueba.pack()
boton = Button(text="Enviar", command=enviar)
boton.pack()
window.mainloop()