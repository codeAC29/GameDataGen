from tkinter import *

class App:
    def __init__(self):
        self.master = Tk()
        self.master.wm_title("Entry Name")
        # Text field storing text details
        self.text_field = Entry(self.master)
        self.text_field.pack()
        self.text_field.focus_set()
        self.text_value = None

        # button grabbing the text value
        accept = Button(self.master, text="Ok", fg="red", width=10, command=self.grab_value)
        accept.pack()
        self.master.mainloop()

    # Fetch text entry
    def grab_value(self):
        self.text_value = self.text_field.get()
        self.master.destroy()
