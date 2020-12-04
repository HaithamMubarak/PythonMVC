from abc import abstractmethod


class BaseDao:

    def __init__(self):
        pass

    @abstractmethod
    def count(self, entityName):
        return 0

    @abstractmethod
    def items(self, entityName):
        pass

    @abstractmethod
    def add_item(self, entityName, item):
        pass

    @abstractmethod
    def delete_item(self, entityName, itemToDelete):
      pass