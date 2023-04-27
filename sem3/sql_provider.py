import os

from string import Template

#model mvc

class SQLProvider:
    def __init__(self, file_path: str) ->None:
        self._scripts = {}
        for file in os.listdir(file_path):# цикл по всем файлам в директории (file_path содержит адрес)
            self._scripts[file] = Template(open(f'{file_path}/{file}').read())# делаем объектом типа template

    def get(self, name, **kwargs) -> str:
        return self._scripts.get(name, '').substitute(**kwargs )# подстановка параметров в запрос

# Первый метод из директории file_path считывает все sql-шаблоны и создает словарь {имя_файла : sql_запрос}.
# Словарь перекастовывается в тип Template. Метод Template.substitute предоставляет возможность
# подставить в sql-запрос необходимые параметры (в нашем случае в параметр '$input').

# Второй метод по имени файла и списку параметров переходит к необходимому запросу и осуществляет
# подстановку параметров **kwargs в шаблон запроса методом substitute.