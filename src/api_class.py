import abc
import os
import requests      # Для запросов по API
import json          # Для обработки полученных результатов
import time          # Для задержки между запросами


class All_api(abc.ABC):
    """Абстрактный класс для классов HH и SJ"""
    @abc.abstractmethod
    def get_data(self, *args, **qwargs):
        pass


class HH_api(All_api):
    """Класс для получения данных по API с сайта HH.ru """

    URL = "https://api.hh.ru/vacancies"

    @classmethod
    def get_data(cls, keyword, region_id=113, c_page=1, count=100) -> json:
        """
        Получает данные через URL и возвращает в переменную для дальнейшей работы.
        :param keyword: ключевое слово (название профессии)
        :param region_id: id региона (города или области) 1-Россия
        :param c_page: кол-во страниц
        :param count: количество вакансий на странице (100 вакансий)
        :return: список вакансий, в формате json
        """

        params = {"area": region_id,
                  "text": keyword,
                  "per_page": count,
                  "currency": "RUR"
                  }

        all_vacancies = []

        for page in range(1, c_page + 1):
            params['page'] = page

            response = requests.get(HH_api.URL, params=params)

            if response.ok:
                vacancies = response.json()["items"]
                all_vacancies.extend(vacancies)
            else:
                time.sleep(0.2)
                print("Error:", response.status_code)
                print(f'Ошибка при выполнении запроса на странице {page}')

        print(f"Кол-во вакансий с сайта HH.ru {len(all_vacancies)}")
        # сохраняем полученные данные в файл
        with open('test_hh.json', 'w', encoding='utf-8') as f:
            json.dump(all_vacancies, f, ensure_ascii=False, indent=4)



class SJ_api(All_api):
    """Класс для получения данных по API с сайта superjob.ru """
    # токен для работы с superjob
    __SJ_API_KEY: str = os.getenv('SJ_API_KEY')

    # адрес сайта
    URL = "https://api.superjob.ru/2.0/vacancies/"

    @classmethod
    def get_data(cls, keyword: str, region_id=1, c_page=1, count=100) -> json:
        """
        Метод для отправки запроса на api superjob
        :param keyword: ключевое слово (название профессии)
        :param region_id: id региона (города или области) 1-Россия
        :param c_page: кол-во страниц
        :param count: количество вакансий на странице (100 вакансий)
        :return: список вакансий, соответствующих требованиям в формате json
        """
        headers = {'X-Api-App-Id': SJ_api.__SJ_API_KEY}
        params = {"keyword": keyword, "с": region_id, "count": count}

        all_vacancies = []

        for page in range(1, c_page + 1):
            params['page'] = page

            response = requests.get(SJ_api.URL, headers=headers, params=params)

            if response.ok:
                vacancies = response.json()['objects']
                all_vacancies.extend(vacancies)
            else:
                time.sleep(0.2)
                print("Error:", response.status_code)
                print(f'Ошибка при выполнении запроса на странице {page}')

        print(f"Кол-во вакансий с сайта superjob.ru {len(all_vacancies)}")

        # сохраняем полученные данные в файл
        with open('test_sj.json', 'w', encoding='utf-8') as f:
            json.dump(all_vacancies, f, ensure_ascii=False, indent=4)

