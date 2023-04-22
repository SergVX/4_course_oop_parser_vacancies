import os
from src.api_class import HH_api, SJ_api
from src.utils import get_data_from
from src.vacancies_class import Vacancies


if __name__ == '__main__':
    print("Welcome to Parser of vacancies by Serg")

#    source = int(input("Выберите сайт с вакансиями 1(HH) или 2(SJ) Введите цифру: "))
#    if source != 1 or source != 2:
#        source = input("Неверный ввод. Выберите сайт повторно 1(HH) или 2(SJ): ")
    keyword =  input("Введите название вакансии: ").strip()
    c_page = int(input("Введите количество страниц для парсинга (<=10): "))
#
#    get_data_from(source, keyword, c_page)
    HH_api.get_data(keyword=keyword, c_page=c_page)
    SJ_api.get_data(keyword=keyword, c_page=c_page)

    Vacancies.get_from_json() # создание объектов из данных файла
    print(len(Vacancies.all_vacancies))




