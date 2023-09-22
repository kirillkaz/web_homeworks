import pandas as pd
from db_requests import select_books_1word_before2020y,\
    select_book_count,\
    select_popular_genre_books,\
    return_reader_book_in_lib,\
    books_statistics,\
    select_books_more_3

class Printer:
    def column_print(data: list):
        for i in data:
            print(i)
    
    def row_print(data: list):
        print(data)

    def pd_print(data: pd.DataFrame):
        print(data)


class HomeworkChecker:
    db_name = 'library_db.db'
    printer = Printer

    def show_homework_0(self):
        result = select_books_more_3(self.db_name)
        print(result)

    def show_homework_1(self):
        result = select_books_1word_before2020y(self.db_name)
        self.printer.column_print(result)

    def show_homework_2(self):
        result = select_book_count(self.db_name)
        self.printer.column_print(result)

    def show_homework_3(self):
        result = select_popular_genre_books(self.db_name)
        print(result)

    def show_homework_4(self, reader_name):
        return_reader_book_in_lib(self.db_name, reader_name)

    def show_homework_5(self):
        result = books_statistics(self.db_name)
        print(result)