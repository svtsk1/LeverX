# Пример ввода: python script.py -s students.json -r rooms.json -f xml

import argparse
import json
import xml.etree.ElementTree as ET


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


def put_students_in_rooms(room_list, student_list):
    """Возвращает словарь, который нужно сериализовывать.
    Сначала из cписка с комнатами выносятся все номера комнат.
    Пары полученного словара представляют собой номер комнаты и пустые списки, куда будут заносится студенты.
    Затем имена студентов из списка со студентами добавляются в соответствующие списки."""
    dict_of_rooms_with_students = {}
    for i in range(len(room_list)):
        room_number = room_list[i]['name']
        dict_of_rooms_with_students[room_number] = []

    for student in student_list:
        dict_of_rooms_with_students[f"Room #{student['room']}"].append(student['name'])
    return dict_of_rooms_with_students


def create_xml(data):
    """В полученном xml будет следующая иерархия:
    <rooms>
        <room number="Room #0">
            <student name="William Perez" />
            ...
        </room>
        ...
    </rooms>"""

    rooms = ET.Element('rooms')

    for room in data:
        one_room = ET.SubElement(rooms, 'room')
        one_room.set('number', f'{room}')

        for student in data[room]:
            one_student = ET.SubElement(one_room, 'student')
            one_student.set('name', f'{student}')

    xml_string = ET.tostring(rooms, encoding='unicode')
    return xml_string


def create_json(data):
    """Полученный json будет иметь следующий вид:
    {"Room #0": ["William Perez",...], "Room #1": [...], ...}"""
    json_string = json.dumps(data)
    return json_string


class Serializer(object):
    """Аттрибутоми класса является словарь, который получается после объединения двух файлов
    и формат файла, который нужно создать."""
    def __init__(self, students_dict_to_serialize, file_format):
        self.students_dict_to_serialize = students_dict_to_serialize
        self.format = file_format

    def write_file(self):
        with open(f'result.{self.format}', 'w') as file:
            file.write(self.students_dict_to_serialize)


class JSONSerializer(Serializer):
    """Метод класса записывает сериализованные данные в файл .json.
     Аттрибут - словарь, который нужно сериализовать."""

    def write_file(self):
        self.students_dict_to_serialize = create_json(self.students_dict_to_serialize)
        super().write_file()


class XMLSerializer(Serializer):
    """Метод класса записывает сериализованные данные в файл .xml.
    Аттрибут - словарь, который нужно сериализовать"""

    def write_file(self):
        self.students_dict_to_serialize = create_xml(self.students_dict_to_serialize)
        super().write_file()


def main():
    my_parser = create_parser()
    args = my_parser.parse_args()
    list_of_students = json.load(args.students)
    list_of_rooms = json.load(args.rooms)
    result_dict = put_students_in_rooms(list_of_rooms, list_of_students)

    if args.format == 'xml':
        XMLSerializer(result_dict, args.format).write_file()
    elif args.format == 'json':
        JSONSerializer(result_dict, args.format).write_file()


if __name__ == '__main__':
    main()
