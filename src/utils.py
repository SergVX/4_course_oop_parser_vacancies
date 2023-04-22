from src.api_class import HH_api, SJ_api


# Топ N вакансий по зарплате
def get_top_by_salary(data: list, n: int) -> list:
    """
    Функция вывода последних значений сортированных данных по зарплате.
    :param self:
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
    data = [x for x in data if "area" in x and x["area"] == area]
    return data


def get_filtered_by_responsibility(data: list, text: str) -> list:
    """
    Фильтрует данные по ключу "area".
    :param data: Список словарей.
    :param text: Фильтрация по наличию слова в описании или требованиях к вакансии.
    :return: Список словарей.
    """
#    data = [x for x in data if text in x["responsibility"].split()]
    filtered_data = []
    for x in data:
        words = x.responsibility
        words_split = words.split()
        if text in words_split:
            filtered_data.append(x)
    return filtered_data

