from mvc.http.httpserver import HttpServer
from dev.views.sampleview import SampleView


class MyController:

    entityName = 'student'

    def __init__(self):
        pass

    @HttpServer.service
    def service(self):
        return None

    @HttpServer.mapping(path='/hi', method='GET')
    def getWelcome(self, request, io):
        return "Hello World!"

    @HttpServer.mapping(path='/student', method='GET')
    def getData(self, request, io):
        io.send_json(data=self.service().items('student'))

    @HttpServer.mapping(path='/student', method='POST')
    def postData(self, request, io):
        self.service().add_item(self.entityName, request.body)
        io.send(data="New item is added, current data size is %d" % self.service().count(self.entityName))

    @HttpServer.mapping(path='/student', method='DELETE')
    def deleteData(self, request, io):
        self.service().deleteItem(self.entityName, request.body)
        io.send(data="Item is removed, current data size is %d" % self.service().count(self.entityName))

    @HttpServer.mapping(path='/student/view', method='GET')
    def getView(self, request, io):
        return SampleView({'title': 'Simple MVC', 'items': self.service().items(self.entityName)})
