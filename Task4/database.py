import pymysql
from time import time
from config import host, user, password

db = pymysql.connect(host=host, user=user,
    password=password, db='students_in_rooms')

cursor = db.cursor()


def working_time(function):
    """Замеряет время выполнения функций"""
    def wrapper():
        time_start = time()
        result = function()
        wrapper.__name__ = function.__name__
        time_finish = time()
        print(f"Время выполенения функции {function.__name__} - {time_finish - time_start}")
        return result
    return wrapper


def delete_old_tables():
    """Удаляет две таблицы из БД."""
    cursor.execute("DROP TABLE Students")
    cursor.execute("DROP TABLE Rooms")


def create_new_tables():
    """Создаёт две таблицы в базе данных."""
    cursor.execute("CREATE TABLE Rooms (roomID int PRIMARY KEY, name VARCHAR(50))")
    cursor.execute("CREATE TABLE Students (birthday datetime NOT NULL, id int PRIMARY KEY, "
                   "name varchar(77) NOT NULL, room int REFERENCES Rooms(roomID), sex ENUM('M', 'F'))")
    db.commit()


def create_indexes():
    """Индексирует некоторые поля таблиц."""
    cursor.execute("ALTER TABLE Students ADD INDEX idx_students (birthday, name, sex)")
    cursor.execute("ALTER TABLE Rooms ADD INDEX idx_rooms (name, roomID)")
    db.commit()


def insert_into_tables(list_of_rooms, list_of_students):
    """Заполняет таблицы базы данных."""
    for room in list_of_rooms:
        cursor.execute("INSERT INTO Rooms (roomID, name) VALUES (%s, %s)", (room['id'], room['name']))
    for student in list_of_students:
        cursor.execute("INSERT INTO Students (birthday, id, name, room, sex) VALUES (%s, %s, %s, %s, %s)",
                       (student['birthday'], student['id'], student['name'], student['room'], student['sex']))
    db.commit()


@working_time
def show_rooms_with_students_count():
    """Возвращает список комнат и количество студентов в комнатах."""
    cursor.execute("SELECT Rooms.name, COUNT(Students.name) "
                   "FROM Rooms JOIN Students ON Rooms.roomID = Students.room GROUP BY Rooms.name ORDER BY Rooms.name")
    return list(cursor.fetchall())


@working_time
def show_top5_rooms_with_min_average_age():
    """Возвращает список комнат и средний возраст в днях всех жителей комнаты."""
    cursor.execute("SELECT Rooms.name, CAST(AVG(DATEDIFF(CURRENT_DATE(),birthday)) AS FLOAT) "
                   "FROM "
                   "Rooms JOIN Students ON Rooms.roomID = Students.room GROUP BY Rooms.name "
                   "ORDER BY AVG(DATEDIFF(CURRENT_DATE(),birthday)) LIMIT 5")
    return list(cursor.fetchall())


@working_time
def show_top5_rooms_with_max_age_diff():
    """Возвращает список комнат и разницу в возрасте в днях"""
    cursor.execute("SELECT Rooms.name, CAST(DATEDIFF(MAX(birthday),MIN(birthday)) AS FLOAT) "
                   "FROM "
                   "Rooms JOIN Students ON Rooms.roomID = Students.room GROUP BY Rooms.name "
                   "ORDER BY DATEDIFF(MAX(birthday),MIN(birthday)) DESC LIMIT 5")
    return list(cursor.fetchall())


@working_time
def show_rooms_with_different_sex_students():
    """Возвращает список комнат и количество уникальных полов студентов"""
    cursor.execute("SELECT Rooms.name, COUNT(DISTINCT sex) FROM "
                   "Rooms JOIN Students ON Rooms.roomID = Students.room GROUP BY Rooms.name "
                   "HAVING COUNT(DISTINCT sex) = 2")
    return list(cursor.fetchall())
