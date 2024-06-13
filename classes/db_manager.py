import psycopg2
from utils.config import config


class DBManager:
    def __init__(self, db_name):
        self.__db_name = db_name

    def __execute_query(self, query):
        """Возвращает результат запроса."""
        conn = psycopg2.connect(dbname=self.__db_name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        query = ('SELECT employers.name, COUNT (*) FROM employers JOIN vacancies USING '
                 '(employer_id) GROUP BY employer_id')
        return self.__execute_query(query)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,

        названия вакансии, зарплаты и ссылки на вакансию.
        """
        query = ('SELECT employers.name, vacancies.name, vacancies.salary_from, '
                 'vacancies.salary_to, vacancies.link FROM vacancies JOIN '
                 'employers USING (employer_id)')
        return self.__execute_query(query)

    def get_avg_salary(self):
        """Получает среднюю зарплату по всем вакансиям."""
        query = 'SELECT AVG(salary_to) FROM vacancies'
        return self.__execute_query(query)[0][0]

    def get_vacancies_with_higher_salary(self):
        """Получает список вакансий с зарплатой выше средней по всем вакансиям."""
        query = (f'SELECT name, salary_from, salary_to, link FROM vacancies '
                 f'WHERE salary_from > {self.get_avg_salary()} '
                 f'OR salary_to > {self.get_avg_salary()}')
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, word):
        """Получает список всех вакансий содержащих указанное слово."""
        query = f"SELECT name, salary_from, salary_to, link FROM vacancies WHERE name ILIKE '%{word}%'"
        return self.__execute_query(query)