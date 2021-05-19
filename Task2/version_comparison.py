from functools import total_ordering
from itertools import zip_longest


@total_ordering
class Version:
    """Переопределены методы сравнения(явно тольно методы lt и eq, остальное добавлено декоратором).
    Следует учитывать, что сравнение происходит но некоторым правилам:
        1. Если в номере версии присутствует 'alpha' или  сокращённое 'a', то это соответствует числу 0.
        2. Если в номере версии присутствует 'beta' или  сокращённое 'b', то это соответствует числу 1.
        3. Если в номере версии присутствует обозначение 'rc'(выпуск-кандидат), то ему присваивается числу 2.
    Какие номера версий считаются валидными:
        1.Между цифрами, обзначающими major,minor,patch,prerelease или что-либо ещё, должны стоять точки или дефисы.
        2.Перед сокращением беты 'b' не должно стоять дефиса.
        3.После обозначения 'rc' следует ставить дефис."""
    def __init__(self, version):
        """Заменяет все буквенные обозначения соответствующим им числам,
        а затем разделяет строку по дефисам и точкам.
        Если появится необходимость сравнивать версии с другими буквенными обозначениями,
            то достаточно просто добавить новый метод .replace для них.
        Полученная версия представляет собой список из элементов, где каждый элемент - major, minor, patch и т.д."""
        replacement_rules = {"alpha": '0', "beta": '1', "a": '-0', "b": '-1', "rc": '2', "-": '.'}
        for key in replacement_rules.keys():
            version = version.replace(key, replacement_rules[key])
        self.version = version.split('.')

    def __lt__(self, other):
        """Сравнивает попарно версии в цикле.
        Если в паре первое число меньше второго, то и весь номер версии меньше, соответственно возвращает True.
        Если в паре первое число больше второго, то и весь номер версии больше, соответственно возвращает False.
        Если в паре числа равны друг-другу, то переходит к следующей паре.
        Если все пары равны, то возвращает False."""
        couples = zip_longest(self.version, other.version, fillvalue='0')
        for first, second in couples:
            first, second = int(first), int(second)
            if first < second:
                return True
            if first > second:
                return False
            if first == second:
                continue
        return False

    def __eq__(self, other):
        """Сравнивает попарно версии в цикле.
        Если в паре первое число меньше или больше второго, то номера версий не равны, соответственно возвращает False.
        Если в паре числа равны друг-другу, то переходит к следующей паре.
        Если все пары равны, то возвращает True."""
        couples = zip_longest(self.version, other.version, fillvalue='0')
        for first, second in couples:
            first, second = int(first), int(second)
            if first < second or first > second:
                return False
            if first == second:
                continue
        return True


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "lt failed"
        assert Version(version_2) > Version(version_1), "gt failed"
        assert Version(version_2) != Version(version_1), "neq failed"
        print(f"Couple {version_1, version_2} passed the tests.")


if __name__ == "__main__":
    main()
