from tools import HomeworkChecker
from db_creator import create_db_by_dump


if __name__ == '__main__':
    create_db_by_dump('library_db.db', 'library.db')

    home_checker = HomeworkChecker()
    
    home_checker.show_homework_0()
    