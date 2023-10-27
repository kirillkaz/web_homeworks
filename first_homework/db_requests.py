import sqlite3
import pandas as pd
import datetime


'''
task0

Отобрать информацию о книгах, количество которых больше 3. Столбцы назвать
Книга, Жанр, Издательство и Количество.
Вывести отобранную информацию:
- в виде таблицы;
'''
def select_books_more_3(db_name: str) -> pd.DataFrame:
    con = sqlite3.connect(db_name)
    data = pd.read_sql('''

        SELECT title, genre_name, publisher_name, available_numbers
        FROM book
        JOIN genre USING (genre_id)
        JOIN publisher USING (publisher_id)
        WHERE available_numbers > 3;

''', con)
    
    data = data.rename(columns={
        'title': 'Книга',
        'genre_name': 'Жанр',
        'publisher_name': 'Издательство',
        'available_numbers': 'Количество'
    })

    con.close()
    return data


'''
task1

Вывести книги, название которых состоит из одного слова, изданные до 2020 года.
Указать их жанр, издательство и год издания. Столбцы назвать Название, Жанр, Издательство, Год_издания соответственно.
Информацию отсортировать сначала по возрастанию года издания, потом по названиям книг в алфавитном порядке.
'''
def select_books_1word_before2020y(db_name: str) -> list:
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    result = cursor.execute('''
                            
        SELECT *
        FROM book
        WHERE title NOT LIKE "% %" and year_publication < 2020
        ORDER BY year_publication, title;
                            
    ''').fetchall()

    con.close()
    return result


'''
task2

Посчитать общее количество экземпляров каждой книги в библиотеке.
Общее количество экземпляров книги определяется как сумма доступного количества экземпляров книги в таблице book и
количества экземпляров этой книги "на руках" у читателя. Вывести название книги (столбец Книга), ее авторов,
если авторов несколько - перечислить их через запятую в алфавитном порядке, в одном поле (Авторы), жанр книги (Жанр), издательство (Издательство) и
количество экземпляров (Количество). Информацию отсортировать сначала по названиям книг в алфавитном порядке,
а затем по фамилиям автора тоже в алфавитном порядке.
'''

def select_book_count(db_name: str) -> list:
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    result = cursor.execute('''
                            
        SELECT
            final_records.title,
            GROUP_CONCAT(final_records.author_name, ', ') AS authors,
            final_records.genre_name,
            final_records.publisher_name,
            final_records.book_sum
        -- делаю выборку внутри вложенного селекта для сортировки авторов внутри конкатинации
        FROM (
            SELECT *
            FROM author
            JOIN book_author ON author.author_id = book_author.author_id
            JOIN book ON book_author.book_id = book.book_id
            JOIN genre ON book.genre_id = genre.genre_id
            JOIN publisher ON book.publisher_id = publisher.publisher_id
            -- делаю выборку суммы книг
            JOIN (
                SELECT 
                    book.book_id, book.available_numbers + readers_books.books_count as book_sum
                FROM book
                    -- делаю выборку суммы книг читалетей
                    JOIN (
                        SELECT book_id, sum(1) as books_count
                        FROM book_reader
                        GROUP BY book_id
                    ) as readers_books on book.book_id = readers_books.book_id
                GROUP BY book.book_id
            ) as sum_of_books on book.book_id = sum_of_books.book_id
            ORDER BY author_name
        ) as final_records
        GROUP BY final_records.title
        ORDER BY final_records.title, authors;
                            
    ''').fetchall()

    con.close()

    return result


'''
task3
править
Найти информацию о книгах тех жанров, у которых количество уникальных книг в библиотеке максимально.
Вывести жанр, название книг и их доступное количество. Информацию отсортировать сначала по жанрам в алфавитном порядке,
затем по возрастанию доступного количества и, наконец, по названиям книг в алфавитном порядке.
'''
def select_popular_genre_books(db_name: str):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    result = cursor.execute(
    '''
    --окно для вывода таблицы с жанрами, где больше всего уникальных книг
    WITH get_unic_books AS (
        SELECT 
            DISTINCT genre_id,
            genre_name,
            COUNT(title) OVER book_genre_window AS books_count,
            MAX(COUNT(title)) OVER book_genre_window AS books_max
            FROM book JOIN genre USING(genre_id)
            WINDOW book_genre_window AS (PARTITION BY genre_id)
            ORDER BY books_count DESC
    )
    SELECT genre_name, title, available_numbers 
        FROM book JOIN get_unic_books USING (genre_id)
        ORDER BY genre_name, available_numbers, title;

    ''').fetchall()

    con.close()
    return result



'''
task4

Читатель Самарин С.С. возвращает последнюю взятую книгу в библиотеку. Необходимо актуализировать базу данных:

занести текущую дату в столбец return_date соответствующей записи таблицы book_reader;
увеличить в таблице book на 1 количество доступных книг (available_numbers) для сдаваемой книги.
Пояснение. В запросах использовать Фамилии И.О. читателя, а не его id.
'''
def return_reader_book_in_lib(db_name: str, reader_name: str):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    data = cursor.execute(f'''
                          
        SELECT
            book_reader_id, *
        FROM
            reader JOIN book_reader USING (reader_id)
        WHERE return_date IS NULL and reader_name = "{reader_name}"
        ORDER BY borrow_date desc;

    ''')


    ''' updating book_reader return_date '''
    cur_book_reader = data.fetchone()
    str_date = datetime.date.today()
    book_reader_id = cur_book_reader[0]

    cursor.execute('''
                   
        UPDATE book_reader
        SET return_date = ?
        WHERE book_reader_id = ?;
                   
        ''', (str_date, book_reader_id))


    ''' return book in library '''
    book_id = cur_book_reader[4]
    cursor.execute('''
                   
        UPDATE book
        SET available_numbers = available_numbers + 1
        WHERE book_id = ?;
                   
        ''', (book_id,))
    con.commit()


    print(f'{reader_name} успешно вернул книгу!')
    con.close()



'''
task5
править
Для каждой книги вывести насколько больше (или меньше) количество ее доступных экземпляров,
чем округленное до целого среднее количество доступных экземпляров в библиотеке. Вывести название книги, ее жанр,
в каком издательстве книга опубликована и сообщение, состоящее из двух частей:

"больше на " или "меньше на ";
разница между средним количеством всех доступных экземпляров и количеством экземпляров каждой книги (по модулю).
Например, если количество книг в наличии больше среднего значения на 3, то должно быть выведено "больше на 3".

Если количество книг равно среднему - вывести "равно среднему".

Последний столбец назвать Отклонение. Информацию отсортировать сначала по названию книги в алфавитном порядке,
а затем по столбцу Отклонение тоже в алфавитном порядке.

Примечание. Для решения задания № 5 использовать оконные функции.
'''
def books_statistics(db_name: str) -> pd.DataFrame:
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    result = cursor.execute(
    '''

    SELECT DISTINCT title AS Название_книги,
	genre_name AS Жанр_книги,
	publisher_name AS Издательство,
	"Меньше на " || CAST(avg_count - available_numbers AS INTEGER) AS Отклонение
	FROM book
		JOIN genre USING(genre_id)
		JOIN publisher USING(publisher_id), (
		select book_id, ROUND(AVG(available_numbers)) AS avg_count
		FROM book) AS avg_book_count
		where available_numbers < avg_count
    --
    UNION 
    --
    SELECT DISTINCT title AS Название_книги,
        genre_name AS Жанр_книги,
        publisher_name AS Издательство,
        "Равно среднему" AS Отклонение
        FROM book
            JOIN genre USING(genre_id)
            JOIN publisher USING(publisher_id), (
            SELECT book_id, ROUND(AVG(available_numbers)) AS avg_count
            FROM book) AS avg_book_count
            where available_numbers = avg_count
    --
    UNION 
    --
    SELECT DISTINCT title AS Название_книги,
        genre_name AS Жанр_книги,
        publisher_name AS Издательство,
        "Больше на " || CAST(available_numbers - avg_count AS INTEGER) AS Отклонение
        FROM book
            JOIN genre USING(genre_id)
            JOIN publisher USING(publisher_id), (
            SELECT book_id,
                ROUND(AVG(available_numbers)) AS avg_count
                FROM book) AS avg_book_count
                WHERE available_numbers > avg_count
        ORDER BY Название_книги, Отклонение;

    ''').fetchall()

    return result
    