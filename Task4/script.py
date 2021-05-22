import argparse
import json
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from database import connect_to_database, create_cursor, insert_into_tables, delete_old_tables, create_new_tables, \
    create_indexes, show_rooms_with_students_count, show_top5_rooms_with_min_average_age, \
    show_top5_rooms_with_max_age_diff, show_rooms_with_different_sex_students, show_working_time


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


def create_json(dict_to_serialize):
    """
    Структура полученного json:
    {
        "rooms_with_students_count": [
            [
                "Room #0",
                9
            ],
            ...
        ]
        "result_of_another_func":[
        ]
        ...
    """
    result = json.dumps(dict_to_serialize, indent=4)
    return result


def create_xml(dict_to_serialize):
    """
    Структура полученного дерева:
    <root>
        <rooms_with_students_count>
            <room name="Room #0" value="9"/>
            ...
        </rooms_with_students_count>
        <result_of_another_func>
        ...
    </root>
    """
    root_el = ET.Element('root')
    for key in dict_to_serialize:
        result_of_one_func = ET.SubElement(root_el, f'{key}')

        for room in dict_to_serialize[key]:
            room_number, count = room[0], room[1]
            one_room = ET.SubElement(result_of_one_func, 'room')
            one_room.set('name', f'{room_number}')
            one_room.set('value', f'{count}')

    result = ET.tostring(root_el, encoding='unicode')
    result = parseString(result)
    return result.toprettyxml()


class Serializer(object):
    """Аттрибутами класса является словарь, который получается после объединения двух файлов
    и имя файла, который нужно создать."""

    def __init__(self, dict_to_serialize, file_name):
        self.dict_to_serialize = dict_to_serialize
        self.file_name = file_name

    def write_file(self):
        with open(f'results/{self.file_name}', 'w') as file:
            file.write(self.dict_to_serialize)


class JSONSerializer(Serializer):
    """Метод класса создаёт файл соответствующего формата,
    используя результат соответсвуюей функции сериализации."""

    def write_file(self):
        self.dict_to_serialize = create_json(self.dict_to_serialize)
        super().write_file()


class XMLSerializer(Serializer):
    """Метод класса создаёт файл соответствующего формата,
    используя результат соответсвуюей функции сериализации."""

    def write_file(self):
        self.dict_to_serialize = create_xml(self.dict_to_serialize)
        super().write_file()


def main():
    my_parser = create_parser()
    args = my_parser.parse_args()
    list_of_students = json.load(args.students)
    list_of_rooms = json.load(args.rooms)

    db = connect_to_database()
    cursor = create_cursor(db)
    delete_old_tables(cursor)
    create_new_tables(cursor, db)
    create_indexes(cursor, db)
    insert_into_tables(cursor, db, list_of_rooms, list_of_students)

    functions = [show_rooms_with_students_count, show_top5_rooms_with_min_average_age,
                 show_top5_rooms_with_max_age_diff, show_rooms_with_different_sex_students, show_working_time]
    data = {}
    for func in functions:
        data[func.__name__[5:]] = func(cursor, db)
    if args.format == 'json':
        JSONSerializer(data, f'result.json').write_file()
    if args.format == 'xml':
        XMLSerializer(data, f'result.xml').write_file()


if __name__ == '__main__':
    main()
