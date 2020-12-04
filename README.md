# PythonMVC

A small library that has MVC implementation concepts.
This library will help you in creating your HTTP controllers and services to create your MVC context as below:
```python
from mvc.http.httpserver import HttpServer
from dev.controllers.mycontroller import MyController
from dev.service.simpleservice import SimpleService

HttpServer.registerComponents([
    MyController(), SimpleService()
]).start(port=2000)

```

## HTTP Controller Creation:

You can create a controller class and bind its methods using the followings sample functions decorators:

- Use HttpServer.mapping to bind the http GET method on URL '/hi' as below: 

```python
    @HttpServer.mapping(path='/hi', method='GET')
```
    
- Use HttpServer.service to get the registered service as below
```python
 @HttpServer.service
```
    
    Sample Controller:
    
```python
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
```
        
## DAO Service creation

Please check the sample service impl to use in-memory data access (Service class should extend BaseDao class):


```python
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
```

## View Creation: 

You can create any view class by extending the class AppView as below:

```python
from dev.views.appview import AppView


class SampleView(AppView):
    def __init__(self, data):
        super(SampleView, self).__init__(data=data)

```

For any view class, html template file will be same as class name by default and will have a path of 'templates/classname.html'. For example of the above view, html template will be created with relative path to class file path as 
'templates/SampleView.html'. Below is sample html template file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title><%py $self.data['title'] %></title>

    <style>
        li {
            background-color: blue;
            color: white;
            margin-top: 10px;
            list-style: none;
            width: 300px;
            text-align: center;
            padding: 10px;
            border-radius: 15px;
        }
    </style>
</head>
<body>

<p>Data length is <%py$len(self.data['items'])%></p>
<%py
from dev.views.subview import SubView

for item in self.data['items']:
    self.out('<li>%s<li>' % str(item))
%>

<p>
</p>
</body>
</html>

```

You can check the complete sample under
https://github.com/HaithamMubarak/PythonMVC/tree/main/sample-mvc/source/dev
