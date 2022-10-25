import mysql.connector
import author
import book
import publisher


class HenryDAO:

    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='fish_guy', host='localhost',
                                           database='comp3421')
        self.my_cursor = self.cnx.cursor()

    def get_author_data(self):
        self.my_cursor.execute("""select distinct a.AUTHOR_NUM, AUTHOR_FIRST, AUTHOR_LAST
            from henry_author a
            join henry_wrote w
            on a.AUTHOR_NUM=w.AUTHOR_NUM
            where BOOK_CODE in (
                SELECT BOOK_CODE
                FROM henry_inventory);""")
        my_result = self.my_cursor.fetchall()
        names = []
        for i in my_result:
            author_guy = author.Author(i[0], i[2], i[1])
            names.append(author_guy)
        return names

    def get_books_for_author(self, in_author):
        self.my_cursor.execute("""select BOOK_CODE, TITLE, PRICE
            from henry_book
            where BOOK_CODE in (
                select BOOK_CODE
                from henry_wrote
                where AUTHOR_NUM=""" + str(in_author.id) + ");")
        my_result = self.my_cursor.fetchall()
        books = []
        for i in my_result:
            book_guy = book.Book(i[0], i[1], i[2])
            books.append(book_guy)
        return books

    def get_book_data(self, in_book):
        self.my_cursor.execute("""select BRANCH_NAME, ON_HAND
            from henry_inventory i
            join henry_branch b
            on b.BRANCH_NUM=i.BRANCH_NUM
            where BOOK_CODE = '""" + str(in_book.id) + "';")
        my_result = self.my_cursor.fetchall()
        branch_dat = []
        for i in my_result:
            branch_dat.append(i)
        return branch_dat

    def get_category_data(self):
        self.my_cursor.execute("""select distinct type
            from henry_book
            where BOOK_CODE in (
                SELECT BOOK_CODE
                FROM henry_inventory);;""")
        my_result = self.my_cursor.fetchall()
        categories = []
        for i in my_result:
            categories.append(i[0])
        return categories

    def get_books_for_cat(self, in_cat):
        self.my_cursor.execute("""select BOOK_CODE, TITLE, PRICE
            from henry_book
            where type='""" + in_cat + "';")
        my_result = self.my_cursor.fetchall()
        books = []
        for i in my_result:
            book_guy = book.Book(i[0], i[1], i[2])
            books.append(book_guy)
        return books

    def get_publishers(self):
        self.my_cursor.execute("""select distinct b.PUBLISHER_CODE, PUBLISHER_NAME
            from henry_book b 
            left join henry_publisher p
            on p.PUBLISHER_CODE=b.PUBLISHER_CODE
            where BOOK_CODE in (
                SELECT BOOK_CODE
                FROM henry_inventory);""")
        my_result = self.my_cursor.fetchall()
        publishers = []
        for i in my_result:
            pub_guy = publisher.Publisher(i[0], i[1])
            publishers.append(pub_guy)
        return publishers

    def get_books_for_pub(self, in_pat):
        self.my_cursor.execute("""select BOOK_CODE, TITLE, PRICE
            from henry_book
            where PUBLISHER_CODE='""" + str(in_pat.code) + "';")
        my_result = self.my_cursor.fetchall()
        books = []
        for i in my_result:
            book_guy = book.Book(i[0], i[1], i[2])
            books.append(book_guy)
        return books

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.my_cursor.close()
        self.cnx.close()
        print("Connection closed")
