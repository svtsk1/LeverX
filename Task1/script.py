# Пример ввода: python script.py -s students.json -r rooms.json -f xml

import argparse
import json
import xml.etree.ElementTree as ET


class Serializer(object):
    """Аттрибутом класса является словарь, который получается после объединения двух файлов."""
    def __init__(self, students_dict_to_serialize):
        self.students_dict_to_serialize = students_dict_to_serialize


class JSONSerializer(Serializer):
    """Метод класса сериализует полученный список в json. Аттрибут - словарь, который нужно сериализовать."""

    def __init__(self, students_dict_to_serialize):
        super().__init__(students_dict_to_serialize)

    def create_json(self):
        """Полученный json будет иметь следующий вид:
        {"Room #0": ["William Perez",...], "Room #1": [...], ...}"""
        json_string = json.dumps(self.students_dict_to_serialize)
        return json_string


class XMLSerializer(Serializer):
    """Метод класса сериализует полученный список в xml. Аттрибут - словарь, который нужно сериализовать"""

    def __init__(self, students_dict_to_serialize):
        super().__init__(students_dict_to_serialize)

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
        return mydata


def write_file(data, file_format):
    with open(f'result.{file_format}', 'w') as file:
        file.write(data)


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


def main():
    my_parser = create_parser()
    args = my_parser.parse_args()
    list_of_students = json.load(args.students)
    list_of_rooms = json.load(args.rooms)
    result_dict = put_students_in_rooms(list_of_rooms, list_of_students)

    if args.format == 'xml':
        result_data = XMLSerializer(result_dict).create_xml()
    elif args.format == 'json':
        result_data = JSONSerializer(result_dict).create_json()
    write_file(result_data, args.format)


if __name__ == '__main__':
    main()
