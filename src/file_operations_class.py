"""Определить абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл, получения
данных из файла по указанным критериям и удаления информации о вакансиях. Создать класс для сохранения информации
о вакансиях в JSON-файл. Дополнительно, по желанию, можно реализовать классы для работы с другими форматами,
например с CSV- или Excel-файлом, с TXT-файлом."""

from abc import ABC, abstractmethod
import json
import openpyxl


class File_worker(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def save_to_file(self, data, file_name):
        pass

    @abstractmethod
    def get_from_file(self, file_name):
        pass

    @abstractmethod
    def remove_from_file(self, vacancy_id):
        pass


class Json_file_worker(File_worker):
    """Класс для работы с Json файлами"""

    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies = []

    def save_to_file(self, data, file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_from_file(self, file_name):
        self.file_name = file_name
        self.vacancies = []
        try:
            with open(self.file_name) as f:
                self.vacancies = json.load(f)
        except FileNotFoundError:
            pass

    def remove_from_file(self, vacancy_id):
        self.vacancies = [v for v in self.vacancies if v.get('id') != vacancy_id]
        self.save()

    def save(self):
        with open(self.file_name, 'w') as f:
            json.dump(self.vacancies, f, indent=4)


class Excel_file_worker(File_worker):
    """Класс для работы с Excel файлами"""
    file_name: str

    def __init__(self, file_name):
        self.file_name = file_name
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.sheet.append(
            ['id', 'name', 'area', 'salary_min', 'salary_max', 'currency', 'requirement', 'responsibility'])

    def save_to_file(self, data, file_name):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['id', 'name', 'area', 'salary_min', 'salary_max', 'currency', 'requirement', 'responsibility'])
        for vacancy in data:
            sheet.append(
                [vacancy['id'], vacancy['name'], vacancy['area'], vacancy['salary_min'],
                 vacancy['salary_max'], vacancy['currency'], vacancy['requirement'], vacancy['responsibility']]
            )
        workbook.save(file_name)

    def add_vacancy(self, vacancy):
        vacancy_id = self.sheet.max_row
        self.sheet.append(
            [vacancy_id, vacancy['name'], vacancy['area'], vacancy['salary_min'],
             vacancy['salary_max'], vacancy['currency'], vacancy['requirement'], vacancy['responsibility']]
        )
        self.workbook.save(self.file_name)
        return vacancy_id

    def get_from_file(self, file_name):
        vacancies = []
        for row in self.sheet.iter_rows(min_row=2, values_only=True):
            vacancy = {
                'id': row[0],
                'name': row[1],
                'area': row[2],
                'salary_min': row[3],
                'salary_max': row[4],
                'currency': row[5],
                'requirement': row[6],
                'responsibility': row[7],
            }
            vacancies.append(vacancy)
        return vacancies

    def remove_from_file(self, vacancy_id):
        for row in self.sheet.iter_rows(min_row=2):
            if row[0].value == vacancy_id:
                self.sheet.delete_rows(row[0].row, amount=1)
                break
        self.workbook.save(self.file_name)
