import requests


class HHParser:
    """Работает с данными с HH.ru."""

    @staticmethod
    def __get_response() -> list[dict]:
        """Получает данные о 10 компаниях с наибольшим количеством вакансий."""
        params = {'sort_by': 'by_vacancies_open', 'per_page': 10}
        response = requests.get('https://api.hh.ru/employers', params=params)
        if response.status_code == 200:
            return response.json()['items']

    def get_employers(self) -> list[dict]:
        """Получает id и имена компаний."""
        data = self.__get_response()
        employers = []
        for employer in data:
            employers.append({'id': employer['id'], 'name': employer['name']})
        return employers

    def get_vacancies(self) -> list[dict]:
        """Получает вакансии по выбранным компаниям."""
        employers = self.get_employers()
        vacancies = []
        for employer in employers:
            params = {'employer_id': employer['id']}
            response = requests.get('https://api.hh.ru/vacancies', params=params)
            if response.status_code == 200:
                filtered_vacancies = self.__filter_vacancies(response.json()['items'])
                vacancies.extend(filtered_vacancies)
        return vacancies

    @staticmethod
    def __filter_vacancies(vacancies) -> list[dict]:
        """Отфильтровывает данные по выбранным полям."""
        filtered_vacancies = []
        for vacancy in vacancies:
            if vacancy['salary'] is None:
                salary_from = 0
                salary_to = 0
            else:
                salary_from = vacancy['salary']['from'] if vacancy['salary']['from'] else 0
                salary_to = vacancy['salary']['to'] if vacancy['salary']['to'] else 0
            filtered_vacancies.append({
                'id': vacancy['id'],
                'name': vacancy['name'],
                'link': vacancy['alternate_url'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'employer': vacancy['employer']['id']
            })
        return filtered_vacancies
