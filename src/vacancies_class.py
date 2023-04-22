"""
Создать класс для работы с вакансиями. В этом классе самостоятельно определить атрибуты, такие как название
вакансии, ссылка на вакансию, зарплата, краткое описание или требования и т. п. (не менее четырех) Класс
должен поддерживать методы сравнения вакансий между собой по зарплате и валидировать данные, которыми
инициализируются его атрибуты.
"""
import json
from typing import List


class Vacancies:
    """Класс для работы с вакансиями"""
    __vacancies_id = 0  # счетчик вакансий
    all_vacancies = []

    def __init__(self, name, area, url, salary_min, salary_max,  currency, requirement, responsibility):
        self.name = name  # data["name"] Наименование вакансии
        self.area = area # data["area"]["name"] Наименование региона
        self.url = url  # data["url"] Ссылка на вакансию
        self.salary_min = salary_min  # data["salary"]["from"] Зарплата от
        self.salary_max = salary_max # data["salary"]["to"] Зарплата до
        self.currency = currency  # data["salary"]["currency"] Валюта
        self.requirement = requirement  # data["snippet"]["requirement"] Требования к вакансии
        self.responsibility = responsibility  # data["snippet"]["responsibility"] Обязанности
        Vacancies.__vacancies_id += 1  # увеличение счетчика экземпляров класса на 1
        self.id = Vacancies.__vacancies_id  # id вакансии
        Vacancies.all_vacancies.append(self)


    @classmethod
    def get_from_json(cls, hh_path=None, sj_path=None) -> list:
        """Загружает из файлов .json данные и создает на их основе экземпляры класса Vacancies"""
        __vacancies_id = 0
        all_vacancies = []

        if hh_path:
            with open(hh_path, 'r', encoding='UTF-8') as hh_file:
                hh_data = json.load(hh_file)
                if hh_data:
                    for row in hh_data:
                        if row['salary']:
                            salary_min = row['salary']['from'] if row['salary']['from'] else row['salary']['to']
                            salary_max = row['salary']['to'] if row['salary']['to'] else salary_min
                            currency = row["salary"]["currency"] if row["salary"]["currency"] else None
                        else:
                            salary_min = None
                            salary_max = None
                            currency = None

                        requirement = row['snippet']['requirement'] if row['snippet']['requirement'] \
                            else 'Нет требований'
                        responsibility = row['snippet']['responsibility'] if row['snippet']['responsibility'] \
                            else 'Нет описания'

                        all_vacancies.append(Vacancies(row['name'],
                                                       row["area"]["name"],
                                                       row["url"],
                                                       salary_min,
                                                       salary_max,
                                                       currency,
                                                       requirement,
                                                       responsibility))

        if sj_path:
            with open(sj_path, 'r', encoding='UTF-8') as sj_file:
                sj_data = json.load(sj_file)
                if sj_data:
                    for row in sj_data:
                        requirement = row['candidat'] if row['candidat'] else 'Нет требований'
                        responsibility = row['work'] if row['work'] else 'Нет описания'

                        all_vacancies.append(cls(name=row['profession'],
                                                 area=row['town']['title'],
                                                 url=row['link'],
                                                 salary_min=row['payment_from'],
                                                 salary_max=row['payment_to'],
                                                 currency=row['currency'],
                                                 requirement=requirement,
                                                 responsibility=responsibility))

        return all_vacancies


    def __str__(self) -> str:
        """Строковое представление вакансии"""
        return f'Вакансия в регионе {self.area}: {self.name}\n' \
               f'Зарплата от {self.salary_min} до {self.salary_max} {self.currency}\n' \
               f'Требования к кандидату: {self.requirement}\n' \
               f'Описание вакансии: {self.responsibility}\n' \
               f'Ссылка на вакансию: {self.url}\n' \
               f'Id вакансии: {self.id}'

    def __gt__(self, other):
        if isinstance(other, Vacancies):
            return self.salary_min > other.salary_min
        else:
            return self.salary_min > other

    def __ge__(self, other):
        if isinstance(other, Vacancies):
            return self.salary_min >= other.salary_min
        else:
            return self.salary_min >= other

    def __lt__(self, other):
        if isinstance(other, Vacancies):
            return self.salary_min < other.salary_min
        else:
            return self.salary_min < other

    def __le__(self, other):
        if isinstance(other, Vacancies):
            return self.salary_min <= other.salary_min
        else:
            return self.salary_min <= other








    def get_vacancies(self, path_1, path_2):
        """Получение вакансий из файлов"""
        data = []
        # загружаем текущие данные из файла
        with open('vacancies.json', 'r', encoding='utf-8') as f:
            current_data = json.load(f)

        # добавляем новые данные к текущим данным
        data.extend(current_data)

        # сохраняем новые данные в файл
        with open('vacancies.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

