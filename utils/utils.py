import psycopg2

from utils.config import config
from classes.hh_parser import HHParser


def create_database(db_name: str) -> None:
    """Создаёт базу данных."""
    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cursor.execute(f'CREATE DATABASE {db_name}')
    cursor.close()
    conn.close()


def create_tables(db_name: str) -> None:
    """Создаёт таблицы в базе данных."""
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE employers (employer_id INTEGER PRIMARY KEY, '
                        'name VARCHAR(150) NOT NULL)')
            cur.execute('CREATE TABLE vacancies (vacancy_id INTEGER PRIMARY KEY, name VARCHAR(150),'
                        'link VARCHAR(150), salary_from INTEGER, salary_to INTEGER,'
                        'employer_id INTEGER REFERENCES employers(employer_id))')
    conn.close()


def insert_data_in_tables(db_name: str) -> None:
    """Записывает данные о компаниях и вакансиях в базу данных."""
    hh = HHParser()
    employers = hh.get_employers()
    vacancies = hh.get_vacancies()
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute('INSERT INTO employers VALUES (%s, %s)', (employer['id'], employer['name']))
            for vacancy in vacancies:
                cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)',
                            (vacancy['id'], vacancy['name'], vacancy['link'], vacancy['salary_from'],
                             vacancy['salary_to'], vacancy['employer']))
    conn.close()
