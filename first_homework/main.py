import sqlite3
from tools import Printer
from db_creator import create_db
from db_requests import select_books_1word_before2020y,\
    select_book_count,\
    select_popular_genre_books,\
    return_reader_book_in_lib,\
    books_statistics,\
    select_books_more_3

if __name__ == '__main__':
    printer = Printer
    db_name = 'library_db.db'
    create_db(db_name)

    # task1_result = select_books_1word_before2020y(db_name)
    # task2_result = select_book_count(db_name)
    # task3_result = select_popular_genre_books(db_name)
    # return_reader_book_in_lib(db_name, 'Самарин С.С.')
    # task5_result = books_statistics(db_name)
    task0_result = select_books_more_3(db_name)
    # new_func(printer)
    printer.pd_print(task0_result)
    