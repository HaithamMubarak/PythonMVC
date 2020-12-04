from builtins import staticmethod
from mvc.http.tcpserver import TcpServer
from mvc.view.base import AbstractView
from mvc.dao.base import BaseDao


class HttpServer:

    contexts = {}
    binds = []
    serviceInterface = None

    def __init__(self):
        pass

    @staticmethod
    def registerComponents(components):
        for component in components:
            if isinstance(component, BaseDao):
                HttpServer.serviceInterface = component
            else:
                HttpServer.registerController(component)

        return HttpServer

    @staticmethod
    def registerController(c):
        for f in [f for f in dir(c) if callable(getattr(c, f)) and not f.startswith('__')]:
            fun = getattr(c, f)

            if fun.__func__ in HttpServer.contexts.keys():
                matcher = type('matcher', (object,), {})()
                context = HttpServer.contexts[fun.__func__]
                for key in context:
                    setattr(matcher, key, context[key])

                HttpServer.binds.append({'matcher': matcher, 'handler': getattr(c, f), 'self': c})

    @staticmethod
    def service(*mappingargs, **mappingkwargs):

        def inline(*args, **kwargs):
            if HttpServer.serviceInterface is None:
                raise Exception("DAO service is not Registered!")
            return HttpServer.serviceInterface
        return inline

    @staticmethod
    def mapping(**mappingkwargs):
        def inline(*args, **kwargs):
            fun = list(args).pop(0)

            #def inline2(*args, **kwargs):
            #    return fun(*args, **kwargs)

            HttpServer.contexts[fun] = mappingkwargs
            return fun

        return inline

    @staticmethod
    def start(host='localhost', port=1234):
        server = TcpServer(host, port)

        def handler(httprequest, io):
            print("HTTP Request: %s" % httprequest)
            controllerMethod = None
            for bind in HttpServer.binds:
                matcher = bind['matcher']
                if matcher.path == httprequest.path and httprequest.method.upper() in matcher.method.upper():
                    controllerMethod = bind['handler']
                    break

            if controllerMethod is None:
                io.send(status='404 Not Found')
            else:
                try:
                    result = controllerMethod(httprequest, io)
                    if isinstance(result, str):
                        io.send(result)
                    elif isinstance(result, AbstractView):
                        io.send(str(result), contentType='text/html')
                except Exception as e:
                    io.send(str(e), status='500 Internal Server Error')

        # Starts the server
        server.start(handler=handler)


