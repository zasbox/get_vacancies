import json
import re
from abc import ABC, abstractmethod

import requests

from json_saver import JSONSaver
from vacancy import Vacancy


class PlatformAPI(ABC):
    def __init__(self):
        self._vacancies = []

    @abstractmethod
    def get_vacancies(self, name: str):
        pass


class HeadHunterAPI(PlatformAPI, JSONSaver):
    def save_to_json(self, file_name):
        """
        Сохранение вакансий в json-файл
        :param file_name: имя файла
        """
        JSONSaver(file_name).save_vacancies(self._vacancies)

    def get_vacancies(self, name: str):
        """
        Получение вакансий с сайта hh.ru
        :param name: поисковый запрос на названию вакансии
        :return: список вакансий
        """
        params = {'text': name}
        headers = {'User-Agent': 'GetVacancies/1.0'}
        res = requests.get('https://api.hh.ru/vacancies', headers=headers, params=params)
        json_data = res.json()

        for item in json_data['items']:
            name = item['name']
            url = item['area']['url']
            salary = item['salary']['to'] if item['salary'] else 0
            if salary is None:
                salary = 0
            requirement = re.sub('<.*?>', '', item['snippet']['requirement']) \
                if item['snippet']['requirement'] is not None else None
            vacancy = Vacancy(name, url, salary, requirement)
            self._vacancies.append(vacancy)
        return self._vacancies


class SuperJobAPI(PlatformAPI, JSONSaver):

    def save_to_json(self, file_name):
        """
        Сохранение вакансий в json-файл
        :param file_name: имя файла
        """
        JSONSaver(file_name).save_vacancies(self._vacancies)

    def get_vacancies(self, name: str):
        """
        Получение вакансий с сайта SuperJob.ru
        :param name: поисковый запрос по названию вакансии
        :return: список вакансий
        """
        secret_key = "v3.r.137944988.5c8e8676bce63afcb75da2ce663d38dc64c9511b.69321b84197b3e09cc238f9f527287811c37718a"

        params = {'keywords[0][srws]': 10, 'keywords[0][keys]': name, 'order_field': 'payment',
                  'order_direction': 'asc'}
        headers = {'X-Api-App-Id': secret_key}
        res = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=params)
        json_data = res.json()

        for item in json_data['objects']:
            name = item['profession']
            url = item['client']['link'] if 'link' in item['client'] else None
            salary = item['payment_to']
            requirement = re.sub('<.*?>', '', item['candidat'])
            vacancy = Vacancy(name, url, salary, requirement)
            self._vacancies.append(vacancy)
        return self._vacancies
