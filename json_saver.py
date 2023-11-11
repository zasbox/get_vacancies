import json
from abc import ABC, abstractmethod
from typing import Union

from vacancy import Vacancy


class VacancyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Vacancy):
            return {"name": obj.name, "url": obj.url, "salary": obj.salary, "requirement": obj.requirement}
        return json.JSONEncoder.default(self, obj)


class VacancyDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.default)

    def default(self, data) -> Vacancy:
        if 'name' in data:
            return Vacancy(data["name"], data["url"], data["salary"], data['requirement'])
        return data


class Saver(ABC):
    @abstractmethod
    def load_vacancies(self):
        pass

    @abstractmethod
    def save_vacancies(self, vacancies):
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary: int):
        pass

    @abstractmethod
    def get_vacancies_by_keywords(self, keywords: list):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(Saver):
    def __init__(self, file_name):
        self.__file_name = file_name

    def load_vacancies(self):
        """
        Получение вакансий из файла
        :return: список вакансий
        """
        try:
            with open(self.__file_name, "r", encoding="utf8") as file:
                data = json.load(file, cls=VacancyDecoder)
        except Union[FileNotFoundError, EOFError]:
            print("Ошибка доступа к файлу")
        else:
            return data

    def save_vacancies(self, vacancies):
        """
        Сохранение вакансий в файл
        :param vacancies: список вакансий
        """
        with open(self.__file_name, "wt", encoding="utf8") as file:
            json.dump(vacancies, file, cls=VacancyEncoder, indent=4, ensure_ascii=False)

    def add_vacancy(self, vacancy):
        """
        Добавление вакансии в файл
        :param vacancy: объект класса Vacancy
        """
        data = self.load_vacancies()
        data.append(vacancy)
        self.save_vacancies(data)

    def get_vacancies_by_salary(self, salary: int):
        """
        Получение вакансий с зарплатой не ниже указанной в параметре salary
        :param salary: величина зарплаты
        :return:
        """
        vacancies = self.load_vacancies()
        return [vacancy for vacancy in vacancies if vacancy.salary >= salary]

    def get_vacancies_by_keywords(self, keywords: list):
        """
        Получение вакансий по ключевым словам
        :param keywords: списо ключевых слов
        :return:
        """
        vacancies = self.load_vacancies()
        if not len(keywords):
            return vacancies
        result_list = []

        for vacancy in vacancies:
            for keyword in keywords:
                if keyword in vacancy.requirement:
                    result_list.append(vacancy)
        return result_list

    def delete_vacancy(self, vacancy):
        """
        Удаление указанной вакансии
        :param vacancy: объект типа Vacancy
        """
        data = self.load_vacancies()
        data.remove(vacancy)
        self.save_vacancies(data)
