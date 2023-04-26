from src.utils import get_data_from, get_top_by_salary, get_filtered_by_responsibility, \
    get_user_answer, compare_vacancies_by_salary, get_id, get_vacancy_by_id
from src.vacancies_class import Vacancies
from src.file_operations_class import Json_file_worker

if __name__ == '__main__':

    print("\nWelcome to Course Project of OOP Parser of vacancies by Ionov Serg\n")
    print("Выберите ресурс по его номеру:\n")
    question = ('1 - Head Hunter\n'
                '2 - Super Job\n'
                '3 - Оба ресурса')
    count = 3
    answer = get_user_answer(question, count)

    keyword = input("Введите название вакансии:\n").strip()
    if not keyword:
        keyword = "python"

    question = "Введите количество страниц для парсинга <= 10, на 1 станице 100 вакансий:"
    count = 10
    c_page = get_user_answer(question, count)

    # Получаем данные с указанных ресурсов
    hh_data, sj_data = get_data_from(answer, keyword, c_page)

    # Проверка полученных данных
    if hh_data:
        print(f'Загружено {len(hh_data)} вакансий с сайта headhunter.ru')
    if sj_data:
        print(f'Загружено {len(sj_data)} вакансий с сайта superjob.ru')
    if not hh_data and not sj_data:
        print('Нет вакансий, соответствующих поисковому запросу')
        exit()

    # Очистка ранее созданных экземпляров класса Vacancies
    Vacancies.clear_all()

    # Создание экземпляров класса Vacancies из полученных данных
    vacancies_data = Vacancies.get_from_data(hh_data, sj_data)

    # Запуск цикла вопросов
    while True:
        print('\nКакие операции хотите произвести?\n')
        question = ('1 - Операции сортировки / фильтрации / сравнения вакансий\n'
                    '2 - Операции сохранения в файл / удаления из файла\n'
                    '3 - Выход из программы')
        count = 3
        answer = get_user_answer(question, count)

        # Выход из программы
        if answer == 3:
            exit()

        # Операции сортировки / фильтрации / сравнения вакансий
        elif answer == 1:
            # Запуск цикла вопросов
            while True:
                print('\nКакие операции хотите произвести с вакансиями?\n')
                question = ('1 - Назад\n'
                            '2 - Сортировка вакансий по зарплате\n'
                            '3 - Фильтрация вакансий по региону (пока не работает)\n'
                            '4 - Фильтрация вакансий по слову в описании\n'
                            '5 - Сравнение вакансий по минимальной зарплате\n'
                            '6 - Вывести в консоль результат\n'
                            '7 - Вывести в консоль вакансию по её ID')
                count = 7
                answer = get_user_answer(question, count)

                if answer == 1:
                    break

                # Сортировка вакансий по зарплате
                elif answer == 2:
                    question = f'Введите число вакансий для вывода, не более {len(vacancies_data)}:'
                    count = len(vacancies_data)
                    n = get_user_answer(question, count)
                    vacancies_data = get_top_by_salary(vacancies_data, n)

                # Фильтрация вакансий по региону
                elif answer == 3:
                    pass

                # Фильтрация вакансий по слову в описании
                elif answer == 4:
                    text = input('Ведите текст для поиска слова в описании вакансий: ')
                    vacancies_data = get_filtered_by_responsibility(vacancies_data, text)

                # Сравнение вакансий по минимальной зарплате
                elif answer == 5:
                    question = 'Введите ID вакансии №1 для сравнения:'
                    vacancy_id_1 = get_id(question, vacancies_data)
                    question = 'Введите ID вакансии №2 для сравнения:'
                    vacancy_id_2 = get_id(question, vacancies_data)
                    result = compare_vacancies_by_salary(vacancy_id_1, vacancy_id_2, vacancies_data)
                    print(result)

                # Вывести в консоль результат
                elif answer == 6:
                    for row in vacancies_data:
                        print(row)

                # Вывести в консоль вакансию по её ID
                elif answer == 7:
                    question = 'Введите ID вакансии для вывода информации:'
                    n = get_id(question, vacancies_data)
                    vacancy = get_vacancy_by_id(n, vacancies_data)
                    print(vacancy)

        # Операции сохранения в файл / удаления из файла
        elif answer == 2:
            # Запуск цикла вопросов
            while True:
                print('\nКакие операции хотите произвести с вакансиями?\n')
                question = ('1 - Назад\n'
                            '2 - Сохранить результаты работы в json-файл\n'
                            '3 - Удалить из списка вакансию по ее ID\n'
                            '4 - Вывести в консоль результат\n'
                            '5 - Вывести в консоль вакансию по её ID')
                count = 5
                answer = get_user_answer(question, count)

                if answer == 1:
                    break

                # Сохранение отфильтрованных и отсортированных вакансий в json-файл
                elif answer == 2:
                    file_name = input("Введите имя файла для сохранения результатов поиска:\n")
                    file_name = f"{file_name}.json"
                    file_saver = Json_file_worker(file_name)
                    file_saver.save_to_file(vacancies_data, file_name)

                # Удаление вакансии из списка по ID
                elif answer == 3:
                    file_name = input("Введите имя файла для сохранения результатов поиска:\n")
                    file_name = f"{file_name}.json"
                    file_saver = Json_file_worker(file_name)
                    file_saver.save_to_file(vacancies_data, file_name)
                    question = f'Введите ID вакансии для ее удаления из файла {file_name}:'
                    vacancy_id = get_id(question, vacancies_data)
                    file_saver.read_file()
                    file_saver.remove_from_file(int(vacancy_id))

                # Вывести в консоль результат
                elif answer == 4:
                    for row in vacancies_data:
                        print(row)

                # Вывести в консоль вакансию по её ID
                elif answer == 7:
                    question = 'Введите ID вакансии для вывода информации:'
                    n = get_id(question, vacancies_data)
                    vacancy = get_vacancy_by_id(n, vacancies_data)
                    print(vacancy)
