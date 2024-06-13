from tabulate import tabulate

from classes.db_manager import DBManager
from utils.utils import create_database, create_tables, insert_data_in_tables

db_name = 'course_work'
create_database(db_name)
create_tables(db_name)
insert_data_in_tables(db_name)

db = DBManager('course_work')


def print_data(data: list[tuple], headers: list[str]) -> None:
    """Функция вывода данных на экран."""
    print(tabulate(data, headers=headers, tablefmt='grid'))


def handle_companies_and_vacancies() -> None:
    """Выводит имена компаний с количеством вакансий."""
    data = db.get_companies_and_vacancies_count()
    headers = ['Компания', 'Количество вакансий']
    print_data(data, headers)


def handle_all_vacancies() -> None:
    """Выводит все компании с вакансиями, заработной платой и ссылкой."""
    data = db.get_all_vacancies()
    headers = ['Компания', 'Вакансия', 'Зар.плата от', 'Зар.плата до', 'Ссылка на вакансию']
    print('Список всех вакансий:')
    print_data(data, headers)


def handle_avg_salary() -> None:
    """Выводит среднюю зарплату по всем вакансиям."""
    data = db.get_avg_salary()
    print(f'Средняя зарплата по всем вакансиям: {round(data, 2)} рублей')


def handle_vacancies_with_higher_salary() -> None:
    """Выводит вакансии с зарплатой выше средней."""
    data = db.get_vacancies_with_higher_salary()
    headers = ['Вакансия', 'Зарплата от', 'Зарплата до', 'Ссылка на вакансию']
    print('Список вакансий с зарплатой больше средней:')
    print_data(data, headers)


def handle_vacancies_with_keyword() -> None:
    """Выводит вакансии в названии которых содержится введённая подстрока."""
    user_word = input('Введите слово для поиска: ')
    data = db.get_vacancies_with_keyword(user_word)
    headers = ['Вакансия', 'Зарплата от', 'Зарплата до', 'Ссылка на вакансию']
    print_data(data, headers)


def main():
    """Основная функция программы."""
    while True:
        print('Возможные действия:')
        print("""
        1 - Посмотреть список всех компаний с количеством вакансий.
        2 - Посмотреть список всех вакансий с названием компании, зарплаты и ссылкой.
        3 - Посмотреть среднюю зарплату по вакансиям.
        4 - Посмотреть вакансии с зарплатой выше средней.
        5 - Посмотреть вакансии названия которых содержат определённые слова.
        Или любой другой символ для выхода.""")
        user_answer = input('Введите номер действия: ')
        if user_answer == '1':
            handle_companies_and_vacancies()
        elif user_answer == '2':
            handle_all_vacancies()
        elif user_answer == '3':
            handle_avg_salary()
        elif user_answer == '4':
            handle_vacancies_with_higher_salary()
        elif user_answer == '5':
            handle_vacancies_with_keyword()
        else:
            break


if __name__ == '__main__':
    main()
