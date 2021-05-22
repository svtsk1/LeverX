import pymysql
from time import time
from config import host, user, password


def connect_to_database():
    db = pymysql.connect(host=host, user=user,
        password=password, db='students_in_rooms')
    return db


def create_cursor(db):
    cursor = db.cursor()
    return cursor


def working_time(function):
    """Замеряет время выполнения функций и заносит это время в таблицу Markdown"""
    def wrapper(cursor, db):
        time_start = time()
        result = function(cursor, db)
        wrapper.__name__ = function.__name__
        time_finish = time()
        cursor.execute("INSERT INTO Markdown (func_name, working_time) VALUES (%s, %s)",
                       (function.__name__, time_finish-time_start))
        db.commit()
        return result
    return wrapper


def delete_old_tables(cursor):
    """Удаляет две таблицы из БД."""
    cursor.execute("DROP TABLE Students")
    cursor.execute("DROP TABLE Rooms")
    cursor.execute("DROP TABLE Markdown")


def create_new_tables(cursor, db):
    """Создаёт три таблицы в базе данных."""
    cursor.execute("""CREATE TABLE Rooms 
    (roomID int PRIMARY KEY, 
    name VARCHAR(50))""")
    cursor.execute("""CREATE TABLE Students 
    (birthday datetime NOT NULL, 
    id int PRIMARY KEY, 
    name varchar(77) NOT NULL, 
    room int REFERENCES Rooms(roomID), 
    sex ENUM('M', 'F'))""")
    cursor.execute("""CREATE TABLE Markdown 
    (func_name VARCHAR(77) PRIMARY KEY, 
    working_time float)""")
    db.commit()


def create_indexes(cursor, db):
    """Индексирует некоторые поля таблиц."""
    cursor.execute("ALTER TABLE Students ADD INDEX idx_students (birthday, name, sex)")
    cursor.execute("ALTER TABLE Rooms ADD INDEX idx_rooms (name, roomID)")
    db.commit()


def insert_into_tables(cursor, db, list_of_rooms, list_of_students):
    """Заполняет таблицы базы данных."""
    for room in list_of_rooms:
        cursor.execute("INSERT INTO Rooms (roomID, name) VALUES (%s, %s)", (room['id'], room['name']))
    for student in list_of_students:
        cursor.execute("INSERT INTO Students (birthday, id, name, room, sex) VALUES (%s, %s, %s, %s, %s)",
                       (student['birthday'], student['id'], student['name'], student['room'], student['sex']))
    db.commit()


@working_time
def show_rooms_with_students_count(cursor, db):
    """Возвращает список комнат и количество студентов в комнатах."""
    cursor.execute("""SELECT Rooms.name, COUNT(Students.name) 
    FROM Rooms JOIN Students ON Rooms.roomID = Students.room 
    GROUP BY Rooms.name ORDER BY Rooms.name""")
    return list(cursor.fetchall())


@working_time
def show_top5_rooms_with_min_average_age(cursor, db):
    """Возвращает список комнат и средний возраст в днях всех жителей комнаты."""
    cursor.execute("""SELECT Rooms.name, CAST(AVG(DATEDIFF(CURRENT_DATE(),birthday)) AS FLOAT) 
    FROM Rooms JOIN Students ON Rooms.roomID = Students.room 
    GROUP BY Rooms.name ORDER BY AVG(DATEDIFF(CURRENT_DATE(),birthday)) LIMIT 5""")
    return list(cursor.fetchall())


@working_time
def show_top5_rooms_with_max_age_diff(cursor, db):
    """Возвращает список комнат и разницу в возрасте в днях"""
    cursor.execute("""SELECT Rooms.name, CAST(DATEDIFF(MAX(birthday),MIN(birthday)) AS FLOAT) 
    FROM Rooms JOIN Students ON Rooms.roomID = Students.room 
    GROUP BY Rooms.name ORDER BY DATEDIFF(MAX(birthday),MIN(birthday)) DESC LIMIT 5""")
    return list(cursor.fetchall())


@working_time
def show_rooms_with_different_sex_students(cursor, db):
    """Возвращает список комнат и количество уникальных полов студентов"""
    cursor.execute("""SELECT Rooms.name, COUNT(DISTINCT sex) 
    FROM Rooms JOIN Students ON Rooms.roomID = Students.room 
    GROUP BY Rooms.name HAVING COUNT(DISTINCT sex) = 2""")
    return list(cursor.fetchall())


def show_working_time(cursor, db):
    """Возвращает список функций и время их работы"""
    cursor.execute("SELECT * FROM Markdown")
    return list(cursor.fetchall())
