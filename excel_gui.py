__author__ = 'jessem'

#from tkinter import *
from tkinter import ttk, filedialog, Button, END, LEFT, Tk, RIGHT
from tkinter.scrolledtext import ScrolledText
from process_file import process_file

class App:

    def __init__(self, master):

        nb = ttk.Notebook(master)
        nb.pack()

        main_tab = ttk.Frame(nb)

        settings_tab = ttk.Frame(nb)


        nb.add(main_tab, text='Main')
        nb.add(settings_tab, text='Settings')

        nb.pack(expand=1, fill="both")


        self.quit_button = Button(
            main_tab, text="QUIT", fg="red", command=nb.quit
            )
        self.quit_button.pack(side=RIGHT)

        self.process_button = Button(
            main_tab, text="Process", command=self.process
            )
        self.process_button.pack(side=LEFT)

        self.open_file_button = Button(main_tab, text="Open", command=self.open_file)
        self.open_file_button.pack(side=LEFT)

        self.text =  ScrolledText(main_tab)
        self.text.pack(expand=1, fill="both")

    def open_file(self):

        ftypes = [('Excel', '*.xlsx'), ('All files', '*')]
        self.file_reference = filedialog.askopenfilename(filetypes = ftypes)

    def process(self):
        if self.file_reference:
            transaction_results = process_file(self.file_reference)

            for i in transaction_results:
                self.text.insert(END, i)

def main():

    root = Tk()

    app = App(root)

    root.mainloop()
    #root.destroy() # optional; see description below

if __name__ == '__main__':
    main()