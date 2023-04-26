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
    """
    Функция получения от пользователя целого числа, не более значения count.
    :param question: Вопрос для пользователя.
    :param count: Число ограниечение.
    :return: Целое число.
    """
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


def get_id(question, vacancies_list):
    """
    Функция получения от пользователя значения ID вакансии, присутствующее в массиве данных.
    :param question: Вопрос задаваемы пользователю.
    :param vacancies_list: Массив данных.
    :return: Целое число
    """
    print(question)
    while True:
        n = input()
        if n.isdigit():
            n = int(n)
            for vacancy in vacancies_list:
                if vacancy.id == n:
                    return n
            print("Ошибка! Вакансии с таким ID нет в списке. Повторите ввод.")
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
    if filtered_data:
        print(f'По Вашему запросу найдено {len(filtered_data)} вакансий')
    else:
        print('Нет вакансий, соответствующих заданным критериям')

    return filtered_data if len(filtered_data) > 0 else data


def compare_vacancies_by_salary(vacancy_id_1: int, vacancy_id_2: int, vacancies_list) -> str:
    """
    Функция сравнения двух экземпляров класса вакансий по минимальной зарплате.
    :param vacancy_id_1: ID первой вакансии для сравнения.
    :param vacancy_id_2: ID второй вакансии для сравнения.
    :param vacancies_list: список экземпляров класса вакансий.
    :return: строку с результатом сравнения.
    """
    vacancy_1 = next((v for v in vacancies_list if v.id == vacancy_id_1), None)
    vacancy_2 = next((v for v in vacancies_list if v.id == vacancy_id_2), None)

    if not vacancy_1 or not vacancy_2:
        return "Ошибка: одной из вакансий нет в списке"

    if vacancy_1.salary_min is None or vacancy_2.salary_min is None:
        return "Ошибка: одна или обе вакансии не имеют указанной минимальной зарплаты"

    if vacancy_1.salary_min > vacancy_2.salary_min:
        return f"Вакансия {vacancy_id_1} имеет большую минимальную зарплату, чем вакансия {vacancy_id_2}"
    elif vacancy_1.salary_min < vacancy_2.salary_min:
        return f"Вакансия {vacancy_id_2} имеет большую минимальную зарплату, чем вакансия {vacancy_id_1}"
    else:
        return f"Минимальная зарплата вакансии {vacancy_id_1} равна минимальной зарплате вакансии {vacancy_id_2}"


def get_vacancy_by_id(vacancy_id: int, vacancies: list):
    """
    Функция возвращает вакансию по её ID.
    :param vacancy_id: номер ID.
    :param vacancies: список вакансий.
    :return: словарь.
    """
    for vacancy in vacancies:
        if vacancy.id == vacancy_id:
            return vacancy
