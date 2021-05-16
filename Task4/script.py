import argparse
import json
import xml.etree.ElementTree as ET
from database import insert_into_tables, delete_old_tables, create_new_tables, create_indexes, \
    show_rooms_with_students_count, show_top5_rooms_with_min_average_age, show_top5_rooms_with_max_age_diff, \
    show_rooms_with_different_sex_students


class JSONSerializer(object):
    """Аттрибутом класса является список, полученный после sql запроса.
    Метод класса сериализует полученный список в json и создаёт соответсвующий файл."""

    def __init__(self, list_to_serialize, name_of_file):
        self.list_to_serialize = list_to_serialize
        self.name_of_file = name_of_file

    def create_json(self):
        with open(f'results/{self.name_of_file}', 'w') as file:
            json.dump(self.list_to_serialize, file)


class XMLSerializer(object):
    """Aттрибутом класса является список, полученный после sql запроса.
    Метод класса сериализует полученный список в xml и создаёт соответсвующий файл."""

    def __init__(self, list_to_serialize, name_of_file):
        self.list_to_serialize = list_to_serialize
        self.name_of_file = name_of_file

    def create_xml(self):
        """В полученном xml будет следующая иерархия:
        <rooms>
            <room number="Room #0" count = "1" />
            ...
        </rooms>"""

        rooms = ET.Element('rooms')

        for room in self.list_to_serialize:
            room_number, count = room[0], room[1]
            one_room = ET.SubElement(rooms, 'room')
            one_room.set('number', f'{room_number}')
            one_room.set('count', f'{count}')

        mydata = ET.tostring(rooms, encoding='unicode')
        with open(f'results/{self.name_of_file}', 'w') as file:
            file.write(mydata)


def create_parser():
    """Парсер, принимающий три аргумента:
        -путь к файлу со студентами
        -путь к файлу с комнатами
        -формат сериализации(xml или json)"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--students', type=argparse.FileType('r'))
    parser.add_argument('-r', '--rooms', type=argparse.FileType('r'))
    parser.add_argument('-f', '--format', choices=['json', 'xml'])
    return parser


if __name__ == '__main__':
    my_parser = create_parser()
    args = my_parser.parse_args()
    list_of_students = json.load(args.students)
    list_of_rooms = json.load(args.rooms)

    delete_old_tables()
    create_new_tables()
    create_indexes()
    insert_into_tables(list_of_rooms, list_of_students)

    functions = [show_rooms_with_students_count, show_top5_rooms_with_min_average_age,
                 show_top5_rooms_with_max_age_diff, show_rooms_with_different_sex_students]
    if args.format == 'json':
        for func in functions:
            JSONSerializer(func(), f'{func.__name__}.json'[5:]).create_json()
    if args.format == 'xml':
        for func in functions:
            XMLSerializer(func(), f'{func.__name__}.xml'[5:]).create_xml()
