import tkinter as tk
from tkinter import ttk
import DAO


class HenrySBA:

    def fix_price(self):
        if self.cur_book.__class__ == list:
            price = self.cur_book[0].price
        else:
            price = self.cur_book.price
        label = ttk.Label(self.tab_guy)
        label.grid(column=2, row=0)
        label['text'] = "Price: \t$" + str(price)

    def populate_table(self, num=0):

        # go to DAO to get the branch information
        if self.cur_book.__class__ == list:
            dat = self.dao_guy.get_book_data(self.cur_book[num])
        else:
            dat = self.dao_guy.get_book_data(self.cur_book)

        # paste it to the tab
        tree = ttk.Treeview(self.tab_guy, columns=('Branch', 'Copies'), show='headings')
        tree.heading('Branch', text='Branch Name')
        tree.heading('Copies', text='Copies Available')
        tree.grid(column=1, row=0)
        for i in tree.get_children():  # Remove any old values in tree list
            tree.delete(i)
        for k in dat:
            tree.insert("", "end", values=k)

    def comCallback(self, event):
        # get will get its value - note that this is always a string
        index_guy = event.widget.current()

        # go to DAO to find the author's books
        books = self.dao_guy.get_books_for_author(self.authors_list[index_guy])

        # update the book combobox
        com2 = ttk.Combobox(self.tab_guy, width=20, state="readonly")
        com2['values'] = books
        com2.current(0)
        com2.bind("<<ComboboxSelected>>", self.other_callback)
        com2.grid(column=2, row=2)

        # save the current books
        self.cur_book = books

        # call the populate function to populate the table
        self.populate_table()

        # call price function to fix the price
        self.fix_price()

    def other_callback(self, event):

        # get book
        index = event.widget.current()
        book = self.cur_book[index]

        # populate the table
        self.populate_table(index)

        # set price
        label = ttk.Label(self.tab_guy)
        label.grid(column=2, row=0)
        label['text'] = "Price: \t$" + str(book.price)

    def __init__(self, tc, dao_g):
        # create the tab
        tab = ttk.Frame(tc)
        tc.add(tab, text="Search by Author")
        self.tab_guy = tab

        # create the DAO and get authors
        self.dao_guy = dao_g
        self.authors_list = self.dao_guy.get_author_data()

        # set first author and first book
        self.cur_author = self.authors_list[0]
        book = self.dao_guy.get_books_for_author(self.cur_author)[0]
        if book.__class__ == list:
            self.cur_book = book[0]
        else:
            self.cur_book = book

        # author stuff
        label1 = ttk.Label(tab)
        label1.grid(column=1, row=1)
        label1['text'] = "Author Selection"

        combo1 = ttk.Combobox(tab, width=20, state="readonly")
        combo1['values'] = self.authors_list
        combo1.current(0)
        combo1.bind("<<ComboboxSelected>>", self.comCallback)
        combo1.grid(column=1, row=2)

        # call function to add price
        self.fix_price()

        # call function to populate branch info
        self.populate_table()

        # book stuff
        label3 = ttk.Label(tab)
        label3.grid(column=2, row=1)
        label3['text'] = "Book Selection"

        com2 = ttk.Combobox(tab, width=20, state="readonly")
        com2['values'] = self.cur_book
        com2.current(0)
        com2.bind("<<ComboboxSelected>>", self.other_callback)
        com2.grid(column=2, row=2)


class HenrySBC:

    def fix_price(self):
        if self.book.__class__ == list:
            price = self.book[0].price
        else:
            price = self.book.price
        label = ttk.Label(self.tab_guy)
        label.grid(column=2, row=0)
        label['text'] = "Price: \t$" + str(price)

    def populate_table(self, num=0):
        # go to DAO to get the branch information
        if self.book.__class__ == list:
            dat = self.dao_guy.get_book_data(self.book[num])
        else:
            dat = self.dao_guy.get_book_data(self.book)

        # paste it to the tab
        tree = ttk.Treeview(self.tab_guy, columns=('Branch', 'Copies'), show='headings')
        tree.heading('Branch', text='Branch Name')
        tree.heading('Copies', text='Copies Available')
        tree.grid(column=1, row=0)
        for i in tree.get_children():  # Remove any old values in tree list
            tree.delete(i)
        for k in dat:
            tree.insert("", "end", values=k)

    def comCallback(self, event):
        # get will get its value - note that this is always a string
        index_guy = event.widget.current()

        # go to DAO to find the books for a given category
        books = self.dao_guy.get_books_for_cat(self.category_list[index_guy])

        # update the book combobox
        com2 = ttk.Combobox(self.tab_guy, width=20, state="readonly")
        com2['values'] = books
        com2.current(0)
        com2.bind("<<ComboboxSelected>>", self.other_callback)
        com2.grid(column=2, row=2)

        # save the current books
        self.book = books

        # call the populate function to populate the table
        self.populate_table()

        # call price function to fix the price
        self.fix_price()

    def other_callback(self, event):
        # get book id
        index = event.widget.current()
        self.populate_table(index)

        # set price
        label = ttk.Label(self.tab_guy)
        label.grid(column=2, row=0)
        label['text'] = "Price: \t$" + str(self.book[index].price)

    def __init__(self, tc, dao_g):
        # create the tab
        tab = ttk.Frame(tc)
        tc.add(tab, text="Search by Category")
        self.tab_guy = tab

        # create the DAO and get categories
        self.dao_guy = dao_g
        self.category_list = self.dao_guy.get_category_data()

        # set first category and first books and first book
        self.cur_cat = self.category_list[0]
        self.book = self.dao_guy.get_books_for_cat(self.cur_cat)
        if self.book.__class__ == list:
            self.cur_book = self.book[0]
        else:
            self.cur_book = self.book

        # category selection tab
        label1 = ttk.Label(tab)
        label1.grid(column=1, row=1)
        label1['text'] = "Category Selection"

        combo1 = ttk.Combobox(tab, width=20, state="readonly")
        combo1['values'] = self.category_list
        combo1.current(0)
        combo1.bind("<<ComboboxSelected>>", self.comCallback)
        combo1.grid(column=1, row=2)
        
        # call function to add price
        self.fix_price()

        # call function to populate branch info
        self.populate_table()

        # book stuff
        label3 = ttk.Label(tab)
        label3.grid(column=2, row=1)
        label3['text'] = "Book Selection"

        com2 = ttk.Combobox(tab, width=20, state="readonly")
        com2['values'] = self.book
        com2.current(0)
        com2.bind("<<ComboboxSelected>>", self.other_callback)
        com2.grid(column=2, row=2)


class HenrySBP:

    def fix_price(self):
        if self.book.__class__ == list:
            price = self.book[0].price
        else:
            price = self.book.price
        label = ttk.Label(self.tab_guy)
        label.grid(column=2, row=0)
        label['text'] = "Price: \t$" + str(price)

    def populate_table(self, num=0):
        # go to DAO to get the branch information
        if self.book.__class__ == list:
            dat = self.dao_guy.get_book_data(self.book[num])
        else:
            dat = self.dao_guy.get_book_data(self.book)

        # paste it to the tab
        tree = ttk.Treeview(self.tab_guy, columns=('Branch', 'Copies'), show='headings')
        tree.heading('Branch', text='Branch Name')
        tree.heading('Copies', text='Copies Available')
        tree.grid(column=1, row=0)
        for i in tree.get_children():  # Remove any old values in tree list
            tree.delete(i)
        for k in dat:
            tree.insert("", "end", values=k)

    def comCallback(self, event):
        # get will get its value - note that this is always a string
        index_guy = event.widget.current()

        # go to DAO to find the books for a given publisher
        books = self.dao_guy.get_books_for_pub(self.publisher_list[index_guy])

        # update the book combobox
        com2 = ttk.Combobox(self.tab_guy, width=20, state="readonly")
        com2['values'] = books
        com2.current(0)
        com2.bind("<<ComboboxSelected>>", self.other_callback)
        com2.grid(column=2, row=2)

        # save the current book(s)
        self.book = books
        if self.book.__class__ == list:
            self.cur_book = self.book[0]
        else:
            b_guy = self.book

        # call the populate function to populate the table
        self.populate_table()

        # call price function to fix the price
        self.fix_price()

    def other_callback(self, event):
        # get book
        index = event.widget.current()
        if self.book.__class__ == list:
            self.cur_book = self.book[index]
        else:
            self.cur_book = self.book
        self.populate_table(index)

        # fix grid
        self.populate_table(index)

        # set price
        label = ttk.Label(self.tab_guy)
        label.grid(column=2, row=0)
        label['text'] = "Price: \t$" + str(self.cur_book.price)

    def __init__(self, tc, dao_g):
        # create the tab
        tab = ttk.Frame(tc)
        tc.add(tab, text="Search by Publisher")
        self.tab_guy = tab

        # create the DAO and get publishers
        self.dao_guy = dao_g
        self.publisher_list = self.dao_guy.get_publishers()

        # set first publisher and first books
        self.cur_pub = self.publisher_list[0]
        self.book = self.dao_guy.get_books_for_pub(self.cur_pub)
        if self.book.__class__ == list:
            self.cur_book = self.book[0]
        else:
            self.cur_book = self.book

        # category selection tab
        label1 = ttk.Label(tab)
        label1.grid(column=1, row=1)
        label1['text'] = "Category Selection"

        combo1 = ttk.Combobox(tab, width=20, state="readonly")
        combo1['values'] = self.publisher_list
        combo1.current(0)
        combo1.bind("<<ComboboxSelected>>", self.comCallback)
        combo1.grid(column=1, row=2)

        # call function to add price
        self.fix_price()

        # call function to populate branch info
        self.populate_table()

        # book stuff
        label3 = ttk.Label(tab)
        label3.grid(column=2, row=1)
        label3['text'] = "Book Selection"

        com2 = ttk.Combobox(tab, width=20, state="readonly")
        com2['values'] = self.book
        com2.current(0)
        com2.bind("<<ComboboxSelected>>", self.other_callback)
        com2.grid(column=2, row=2)


# Main window
root = tk.Tk()
root.title("Henry Bookstore")
root.geometry('800x400')

# Tab control
tabControl = ttk.Notebook(root)
dao_guy = DAO.HenryDAO()
HenrySBA(tabControl, dao_guy)
HenrySBC(tabControl, dao_guy)
HenrySBP(tabControl, dao_guy)
tabControl.pack(expand=1, fill="both")

# start
root.mainloop()
