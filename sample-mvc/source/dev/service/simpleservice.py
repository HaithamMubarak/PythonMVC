import json
from mvc.dao.base import BaseDao


class SimpleService(BaseDao):
    data = {
        "student": [
            {
                "name": "Haitham",
                "id": "1081275"
            }
        ]
    }

    def __init__(self):
        pass

    def __getData(self, entityName):
        if entityName not in self.data:
            self.data[entityName] = []
        return self.data[entityName]

    @staticmethod
    def _check_json(data):
        if isinstance(data, str):
            data = json.loads(data)
        return data

    def count(self, entityName):
        return len(self.items(entityName))

    def items(self, entityName):
        return self.__getData(entityName)

    def add_item(self, entityName, item):
        self.__getData(entityName).append(self._check_json(item))

    def delete_item(self, entityName, itemToDelete):
        itemToDelete = self._check_json(itemToDelete)
        count = 0
        index = 0
        for item in self.__getData(entityName):
            match = len(itemToDelete.keys()) > 0
            for key in itemToDelete.keys():
                if itemToDelete[key] in item[key]:
                    self.data.pop(index)
                    count += 1
            index += 1
