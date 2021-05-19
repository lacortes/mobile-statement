import json
from typing import ItemsView, List


class Phones(object):
    def __init__(self):
        self._phones = {}

    def get_numbers(self) -> ItemsView[str, List[str]]:
        if len(self._phones) <= 0:
            self.__read_in_phones()
        return self._phones.items()

    def __read_in_phones(self):
        path = "phones.json"
        lines = ""
        with open(path, 'r') as readfile:
            for line in readfile:
                lines += line

        self._phones = json.loads(lines)
