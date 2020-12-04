from mvc.http.httpserver import HttpServer
from dev.controllers.mycontroller import MyController
from dev.service.simpleservice import SimpleService


HttpServer.registerComponents([
    MyController(), SimpleService()
]).start(port=2000)

