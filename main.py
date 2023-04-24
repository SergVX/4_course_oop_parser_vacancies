from src.utils import get_data_from, get_top_by_salary, get_filtered_by_responsibility, \
    get_user_answer, get_n_for_top
from src.vacancies_class import Vacancies
from src.file_operations_class import Json_file_worker

if __name__ == '__main__':

    print("\nWelcome to Course Project of OOP Parser of vacancies by Ionov Serg\n")
    print("Выберите ресурс по его номеру:\n")
    question = ('1 - Head Hunter\n'
                '2 - Super Job\n'
                '3 - - Оба ресурса')
    count = 3
    answer = get_user_answer(question, count)

    keyword = input("Введите название вакансии: ").strip()
    if not keyword:
        keyword = "python"

    question = "Введите количество страниц для парсинга <=10, на 1 станице 100 вакансий:"
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

    # print(len(vacancies_list))

    while True:
        print('\nКакие операции хотите произвести с вакансиями?\n')
        question = ('1 - Сортировка вакансий по зарплате\n'
                    '2 - Фильтрация вакансий по региону (пока не работает)\n'
                    '3 - Фильтрация вакансий по слову в описании\n'
                    '4 - Пропуск данного шага -> ')
        count = 4
        answer = get_user_answer(question, count)

        if answer == 4:
            break
        elif answer == 1:  # Сортировка вакансий по зарплате
            n = get_n_for_top(vacancies_data)
            vacancies_data = get_top_by_salary(vacancies_data, n)
        elif answer == 2:  # Фильтрация вакансий по региону
            pass
        elif answer == 3:  # Фильтрация вакансий по слову в описании
            text = input('Ведите текст для поиска слова в описании вакансий')
            vacancies_data = get_filtered_by_responsibility(vacancies_data, text)

        if vacancies_data:
            print(f'По Вашему запросу найдено {len(vacancies_data)} вакансий')

        else:
            print('Нет вакансий, соответствующих заданным критериям')
            break

    while True:
        print('\nКакие операции хотите произвести с вакансиями?\n')
        question = ('1 - Сохранить результаты работы в json-файл\n'
                    '2 - Удалить из списка вакансию по ее ID\n'
                    '3 - Вывести в консоль результат парсинга\n'
                    '4 - Завершить работу программы -> \n')
        count = 4
        answer: int = get_user_answer(question, count)

        if answer == 4:
            break
        # Сохранение отфильтрованных и отсортированных вакансий в json-файл
        elif answer == 1:

            file_name = input("Введите имя файла для сохранения результатов поиска:\n")
            file_name = f"{file_name}.json"
            file_saver = Json_file_worker(file_name)
            file_saver.save_to_file(vacancies_data, file_name)

        # Удаление вакансии из списка
        elif answer == 2:

            file_name = input("Введите имя файла для сохранения результатов поиска:\n")
            file_name = f"{file_name}.json"
            file_saver = Json_file_worker(file_name)
            file_saver.save_to_file(vacancies_data, file_name)
            vacancy_id = input(f'Введите ID вакансии для ее удаления из файла {file_name}.json: ')
            file_saver.read_file()
            file_saver.remove_from_file(int(vacancy_id))

        elif answer == 3:
            for row in vacancies_data:
                print(row)
