from src.api_class import HH_api, SJ_api


def get_data_from(source, keyword, c_page):
    """
    Функция выбора ресурса, откуда производим парсинг
    :param source: выбор ресурса
    :param keyword: слово для поиска вакансии
    :param c_page: количество страниц для парсинга
    :return: Список словарей
    """
    hh_data = None
    sj_data = None
    if source == 1:
        hh_data = HH_api.get_data(keyword=keyword, c_page=c_page)
    elif source == 2:
        sj_data = SJ_api.get_data(keyword=keyword, c_page=c_page)
    elif source == 3:
        hh_data = HH_api.get_data(keyword=keyword, c_page=c_page)
        sj_data = SJ_api.get_data(keyword=keyword, c_page=c_page)
    return hh_data, sj_data


def get_user_answer(question, count):

    print(question)
    while True:
        n = input()
        if n.isdigit():
            n = int(n)
            if 0 < n < count + 1:
                return n
            else:
                print(f"Ошибка! Введенное число должно быть от 1 до {count}. Повторите ввод.")
        else:
            print("Ошибка! Введенное значение не является числом. Повторите ввод.")


def get_n_for_top(data):

    while True:
        n = input(f'Введите число вакансий для вывода, не более {len(data)}\n')
        if n.isdigit():
            n = int(n)
            if 0 < n < len(data):
                return n
            else:
                print(f"Ошибка! Введенное число должно быть от 1 до {len(data)}. Повторите ввод.")
        else:
            print("Ошибка! Введенное значение не является числом. Повторите ввод.")


# Топ N вакансий по зарплате
def get_top_by_salary(data: list, n: int) -> list:
    """
    Функция вывода последних значений сортированных данных по зарплате.
    :param data: Список словарей.
    :param n: Количество данных для вывода.
    :return: Список словарей.
    """
    data = sorted(data, key=lambda x: (x.salary_min or 0), reverse=True)
    return data[:n]


def get_filtered_by_area(data: list, area: str) -> list:
    """
    Фильтрует данные по ключу "area".
    :param data: Список словарей.
    :param area: type -> str фильтрация по ключу "from".
    :return: Список словарей.
    """
    filtered_data = [x for x in data if "area" in x and x["area"] == area]
    return filtered_data


def get_filtered_by_responsibility(data: list, text: str) -> list:
    """
    Фильтрует данные по наличию слова в описании к вакансии.
    :param data: Список словарей.
    :param text: Фильтрация по наличию слова в описании или требованиях к вакансии.
    :return: Список словарей.
    """
    filtered_data = []
    for x in data:
        words = x.responsibility
        words_split = words.split()
        if text in words_split:
            filtered_data.append(x)
    return filtered_data
