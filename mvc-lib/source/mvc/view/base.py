import os
import re
import traceback
from abc import abstractmethod


class AbstractView:

    def __init__(self, templatefile=None, data={}):
        self.templatefile = templatefile
        self.data = data

    def __str__(self):
        f = open(self.templatefile, "r")
        return self.process(f.read())

    @abstractmethod
    def process(self, templatestring):
        pass


class DefaultView(AbstractView):

    __pattern = '(.+?)<%py(.+?)%>(.+)'
    __out = ''

    def out(self, message, end='\n'):
        self.__out += str(message) + str(end)

    def process(self, templatestring):

        match = re.search(self.__pattern, templatestring, re.DOTALL)
        newtemplate = ''

        def myExec(code):
            self.__out = ''
            try:
                code = code.strip()
                if "$" in code and code.index("$") == 0:
                    code = ("self.out(%s, end='')" % (code[1:]))
                exec(code)
            except Exception:
                print("Exec error in code", code.strip())
                traceback.print_exc()
            return self.__out

        while match is not None:

            code = match.group(2)
            #print(self, 'code', code)
            newtemplate += '%s%s' % (match.group(1), myExec(code))
            templatestring = match.group(3)

            match = re.search(self.__pattern, templatestring, re.DOTALL)

        newtemplate += templatestring
        return newtemplate

