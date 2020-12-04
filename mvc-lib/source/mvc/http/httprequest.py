import re


class HttpRequest:

    def __init__(self, message):
        headers = {}
        body = ''
        payloadmode = False
        method, path, httpVersion = None, None, None
        while len(message) > 0:
            if payloadmode:
                body = message
                message = ''
            else:
                index = message.index('\n')
                line = message[0:index].strip()
                message = message[index + 1:]
                if line == '':
                    payloadmode = True
                elif method is None:
                    method, path, httpVersion = line.split(' ')
                else:
                    match = re.match(r'([^:]+): ?([^:]+)', line)
                    headers[match.group(1)] = match.group(2)

        self.httpVersion = httpVersion
        self.headers = headers
        self.method = method
        self.body = body
        self.path = path

    def __str__(self):
        return "Version: %s, Path: %s, Method: %s, Headers:\n%s, Body:\n%s" % (
            self.httpVersion, self.path, self.method, self.headers, self.body
        )
