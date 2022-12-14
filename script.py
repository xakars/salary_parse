from terminaltables import AsciiTable
from dotenv import load_dotenv
import os
from sj import get_job_statistic_from_sj
from hh import get_job_statistic_from_hh


def create_tabel(title, vacancies_statistic):
    table = [
        ('Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата'),
    ]
    for lang in vacancies_statistic:
        table_row = []
        table_row.append(lang)
        table_row.append(vacancies_statistic[lang]["vacancies_found"])
        table_row.append(vacancies_statistic[lang]["vacancies_processed"])
        table_row.append(vacancies_statistic[lang]["average_salary"])
        table.append(table_row)

    table_instance = AsciiTable(table, title)
    table_instance.justify_columns[4] = 'right'
    return table_instance.table


def main():
    load_dotenv()
    token = os.environ['SJ_TOKEN']
    popular_lang = ["Python", "C", "Java", "C++", "C#", "JavaScript", "PHP", "TypeScript"]
    print(create_tabel('HeadHunter Moscow', get_job_statistic_from_hh(popular_lang)))
    print(create_tabel('SuperJob Moscow', get_job_statistic_from_sj(token, popular_lang)))


if __name__ == '__main__':
    main()
