class Vacancy:
    def __init__(self, name, url, salary, requirement):
        self.name = name
        self.url = url
        self.salary = salary
        self.requirement = requirement

    def __str__(self):
        return self.name

    def __ge__(self, other):
        if self.salary >= other.salary:
            return True

    def __eq__(self, other):
        if self.name == other.name:
            return True

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def salary(self):
        return self.__salary

    @property
    def requirement(self):
        return self.__requirement

    @name.setter
    def name(self, value):
        if len(value) == 0 or value is None:
            raise AttributeError("Имя не может быть пустым")
        self.__name = value

    @url.setter
    def url(self, value):
        self.__url = value

    @salary.setter
    def salary(self, value):
        if not isinstance(value, int) or value < 0:
            raise AttributeError("Величина зарплаты должна быть целым неотрицательным числом")
        self.__salary = value

    @requirement.setter
    def requirement(self, value):
        self.__requirement = value










