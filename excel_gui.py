__author__ = 'jessem'

#from tkinter import *
from tkinter import ttk, filedialog, Button, END, LEFT, Tk, RIGHT, N, S, E, W, Label, Entry
from tkinter.scrolledtext import ScrolledText
from process_file import process_file

class App:

    def __init__(self, master):

        nb = ttk.Notebook(master)
        nb.pack()

        main_tab = ttk.Frame(nb, padding=(3,3,12,12))
        settings_tab = ttk.Frame(nb, padding=(3,3,12,12))
        main_tab.grid(column=0, row=0, sticky=(N, S, E, W))
        settings_tab.grid(column=0, row=0, sticky=(N, S, E, W))

        nb.add(main_tab, text='Main')
        nb.add(settings_tab, text='Settings')

        nb.pack(expand=1, fill="both")


        self.quit_button = Button(
            main_tab, text="Quit", command=nb.quit
            )
        self.quit_button.grid(column=1, row=5, columnspan=1, sticky=(N, S, E, W))
        self.process_button = Button(
            main_tab, text="Process", command=self.process
            )
        self.process_button.grid(column=1, row=0, columnspan=1, sticky=(N, S, E, W), padx=5)

        self.open_file_button = Button(
            main_tab, text="Open file", command=self.open_file
            )
        self.open_file_button.grid(column=0, row=0, columnspan=1, sticky=(N, S, E, W), padx=5)

        self.text =  ScrolledText(main_tab)
        self.text.grid(column=0, row=3, columnspan=2, rowspan=2, sticky=(N, S, E, W))
        self.text.config(state='disabled')

        self.user_label = Label(main_tab, text="Username")
        self.password_label = Label(main_tab, text="Password")

        self.username = Entry(main_tab)
        self.password = Entry(main_tab, show="*")

        self.user_label.grid(row=1, column=0, sticky=W)
        self.password_label.grid(row=2, column=0, sticky=W)
        self.username.grid(row=1, column=0, sticky=E)
        self.password.grid(row=2, column=0, sticky=E)

        main_tab.rowconfigure(3, weight=3)
        main_tab.columnconfigure(0, weight=1)
        main_tab.columnconfigure(1, weight=1)

    def open_file(self):

        ftypes = [('Excel', '*.xlsx'), ('All files', '*')]
        self.file_reference = filedialog.askopenfilename(filetypes = ftypes)

    def process(self):

        if self.file_reference:
            transaction_results = process_file(self.file_reference, self.username.get(), self.password.get())

            self.text.config(state='normal')

            for i in transaction_results:
                self.text.insert(END, i['result'] + '\n')
                self.text.insert(END, '\n')

            self.text.config(state='disabled')


def main():

    root = Tk()

    app = App(root)

    root.mainloop()
    #root.destroy() # optional; see description below

if __name__ == '__main__':
    main()