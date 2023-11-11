# Создание экземпляра класса для работы с API сайтов с вакансиями
from json_saver import JSONSaver
from platform_api import SuperJobAPI, HeadHunterAPI
from vacancy import Vacancy

hh_api = HeadHunterAPI()
superjob_api = SuperJobAPI()

# Получение вакансий с разных платформ
hh_vacancies = hh_api.get_vacancies("Python")
hh_api.save_to_json("hh.json")

superjob_vacancies = superjob_api.get_vacancies("Java")
superjob_api.save_to_json("superjob.json")

# Создание экземпляра класса для работы с вакансиями
vacancy1 = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", 100000,
                  "Требования: опыт работы от 3 лет...")

vacancy2 = Vacancy("Java Developer", "<https://hh.ru/vacancy/123456>", 120000,
                  "Требования: опыт работы от 5 лет...")

# Сохранение информации о вакансиях в файл
json_saver = JSONSaver("hh.json")

json_saver.add_vacancy(vacancy1)
json_saver.add_vacancy(vacancy2)
json_saver.get_vacancies_by_salary(100000)
json_saver.delete_vacancy(vacancy1)


# Функция для взаимодействия с пользователем
def sort_vacancies(vacancies: list):
    return sorted(vacancies, key=lambda v: int(v.salary), reverse=True)


def get_top_vacancies(vacancies, n):
    return vacancies[:n] if n != 0 else vacancies


def print_vacancies(vacancies):
    print("\n")
    for vacancy in vacancies:
        print("Название: ", vacancy.name)
        print("Ссылка: ", vacancy.url)
        print("Зарплата: ", vacancy.salary)
        print("Описание: ", vacancy.requirement, "\n")


def user_interaction():
    platforms = ["HeadHunterAPI", "SuperJobAPI"]
    while True:
        user_input = input("Укажите платформу для поиска вакансий (1 - headHunter, 2 - superJob): ")
        if user_input not in ["1", "2"]:
            print("укажите корректное значение")
            continue

        search_query = input("Введите поисковый запрос: ")
        platform = eval(platforms[int(user_input) - 1])()
        vacancies = platform.get_vacancies(search_query)

        json_saver = JSONSaver("vacancies.json")
        json_saver.save_vacancies(vacancies)

        top_n = int(input("Введите количество вакансий для вывода в топ N (0 - вывод всех вакансий): "))
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

        filtered_vacancies = json_saver.get_vacancies_by_keywords(filter_words)
        if not filtered_vacancies:
            print("Нет вакансий, соответствующих заданным критериям.")
            continue

        sorted_vacancies = sort_vacancies(filtered_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
        print_vacancies(top_vacancies)
        break


if __name__ == "__main__":
    user_interaction()
