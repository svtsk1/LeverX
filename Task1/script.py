# Пример ввода: python script.py -s students.json -r rooms.json -f xml

import argparse
import json
import xml.etree.ElementTree as ET


class Serializer(object):
    """Аттрибутом класса является список студентов, который получается после объединения двух файлов.
    Методы класса сериализуют полученный список либо в xml, либо в json и создают соответсвующий файл.
    При необходимости добавления сериализации данных в другой формат можно легко добавить новый метод."""

    def __init__(self, students_list_to_serialize):
        self.students_list_to_serialize = students_list_to_serialize

    def create_xml(self):
        """В полученном xml будет следующая иерархия:
        <data>
            <rooms>
                <room name='Номер комнаты'>
                    <student id=''>
                        <name>
                            'Имя студента'
                        </name>
                    </student>
                    ...
                </room>
                ...
            </rooms>
        </data>"""

        data = ET.Element('data')
        rooms = ET.SubElement(data, 'rooms')

        for room in self.students_list_to_serialize:
            one_room = ET.SubElement(rooms, 'room')
            one_room.set('name', f'{room[0]}')

            for student in room[1]:
                one_student = ET.SubElement(one_room, 'student')
                student_id = student['id']
                student_name = student['name']
                one_student.set('id', f'{student_id}')
                name = ET.SubElement(one_student, 'name')
                name.text = f'{student_name}'

        mydata = ET.tostring(data, encoding='unicode')
        with open('result.xml', 'w') as file:
            file.write(mydata)

    def create_json(self):
        """Полученный json будет иметь следующий вид:
        [['Номер комнаты', [{*вся информация о студенте из исходного файла*}, {...}, ...]], ...]"""
        with open('result.json', 'w') as file:
            json.dump(self.students_list_to_serialize, file)


class MainLogic(object):
    """Аттрибутами класса являются файл со студентами и файл с комнатами.
    Здесь реализован один метод, который соединяет информацию из двух этих списков для последующей сериализации.
    При необходимости класс можно легко расширить новыми действиями, которые нужно совершить над файлами."""
    def __init__(self, file_with_students, file_with_rooms):
        self.file_with_students = file_with_students
        self.file_with_rooms = file_with_rooms

    def put_students_in_rooms(self):
        """Соединяет информацию так, как того требует задание. Возвращает список, который нужно сериализовывать.
        Сначала из файла с комнатами в отдельный список выносятся все номера комнат.
        Полученный список состоит из кортежей, где первый элемент - Номер комнаты, второй элемент - пустой список,
            куда в последствии будут добавляться студенты.
        Затем, открыв файл со студентами и запустив цикл по полученному ранее списку, выбираем студентов,
            у которых указанный номер комнаты совпадает с тем, на котором сейчас находится цикл, и добавляются в
            соответствующий список.
        Полученный список является конечным для данного алгоритма."""
        list_of_rooms_with_students = []
        with open(f"{self.file_with_rooms}", "r") as list_of_rooms:
            data = json.load(list_of_rooms)
            for i in range(len(data)):
                list_of_rooms_with_students.append((data[i]['name'], []))

        with open(f"{self.file_with_students}", "r") as list_of_students:
            data = json.load(list_of_students)
            for room in list_of_rooms_with_students:
                room_number = int(room[0][6:])
                students_in_this_room = list(filter(lambda student: student['room'] == room_number, data))
                room[1].extend(students_in_this_room)
        return list_of_rooms_with_students


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

    logic = MainLogic(json_with_students, json_with_rooms)

    try:
        result_list = logic.put_students_in_rooms()
        serializer = Serializer(result_list)
        if args.format == 'xml':
            serializer.create_xml()
        elif args.format == 'json':
            serializer.create_json()
        else:
            print('Incorrect format. Print "xml" or "json".')
    except FileNotFoundError:
        print('Incorrect path to file/files.')
