# Пример ввода: python script.py -s students.json -r rooms.json -f xml

import argparse
import json
import xml.etree.ElementTree as ET


class Serializer(object):
    """Аттрибутом класса является словарь со студентами, который получается после объединения двух файлов.
    Методы класса сериализуют полученный список либо в xml, либо в json и создают соответсвующий файл."""

    def __init__(self, students_dict_to_serialize):
        self.students_dict_to_serialize = students_dict_to_serialize

    def create_xml(self):
        """В полученном xml будет следующая иерархия:
        <rooms>
            <room number="Room #0">
                <student name="William Perez" />
                ...
            </room>
            ...
        </rooms>"""

        rooms = ET.Element('rooms')

        for room in self.students_dict_to_serialize:
            one_room = ET.SubElement(rooms, 'room')
            one_room.set('number', f'{room}')

            for student in self.students_dict_to_serialize[room]:
                one_student = ET.SubElement(one_room, 'student')
                one_student.set('name', f'{student}')

        mydata = ET.tostring(rooms, encoding='unicode')
        with open('result.xml', 'w') as file:
            file.write(mydata)

    def create_json(self):
        """Полученный json будет иметь следующий вид:
        {"Room #0": ["William Perez", ...], ...}"""
        with open('result.json', 'w') as file:
            json.dump(self.students_dict_to_serialize, file)


def put_students_in_rooms(file_with_rooms, file_with_students):
    """Возвращает словарь, который нужно сериализовывать.
    Сначала из файла с комнатами выносятся все номера комнат.
    Пары полученного словара представляют собой номер комнаты и пустые списки, куда будут заносится студенты.
    Затем имена студентов из файла со студентами добавляются в соответствующие списки."""
    dict_of_rooms_with_students = {}
    with open(f"{file_with_rooms}", "r") as list_of_rooms:
        list_of_rooms = json.load(list_of_rooms)
        for i in range(len(list_of_rooms)):
            room_number = list_of_rooms[i]['name']
            dict_of_rooms_with_students[room_number] = []

    with open(f"{file_with_students}", "r") as list_of_students:
        list_of_students = json.load(list_of_students)
        for student in list_of_students:
            dict_of_rooms_with_students[f"Room #{student['room']}"].append(student['name'])
    return dict_of_rooms_with_students


def create_parser():
    """Парсер, принимающий три аргумента:
        -путь к файлу со студентами
        -путь к файлу с комнатами
        -формат сериализации(xml или json)"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--students')
    parser.add_argument('-r', '--rooms')
    parser.add_argument('-f', '--format')
    return parser


if __name__ == '__main__':
    my_parser = create_parser()
    args = my_parser.parse_args()
    json_with_students = args.students
    json_with_rooms = args.rooms

    try:
        result_dict = put_students_in_rooms(json_with_rooms, json_with_students)
        serializer = Serializer(result_dict)
        if args.format == 'xml':
            serializer.create_xml()
        elif args.format == 'json':
            serializer.create_json()
        else:
            print('Incorrect format. Print "xml" or "json".')
    except FileNotFoundError:
        print('Incorrect path to file/files.')
