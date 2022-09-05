from terminaltables import AsciiTable
from dotenv import load_dotenv
import os
from sj import get_job_statistic_from_sj
from hh import get_job_statistic_from_hh


def create_tabel(title, data):
    table_data = [
        ('Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата'),
    ]
    for lang in data:
        tmp_data = []
        tmp_data.append(lang)
        tmp_data.append(data[lang]["vacancies_found"])
        tmp_data.append(data[lang]["vacancies_processed"])
        tmp_data.append(data[lang]["average_salary"])
        table_data.append(tmp_data)

    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[4] = 'right'
    return table_instance.table


def main():
    token = os.environ['SJ_TOKEN']
    popular_lang = ["Python", "C", "Java", "C++", "C#", "JavaScript", "PHP", "TypeScript"]
    print(create_tabel('HeadHunter Moscow', get_job_statistic_from_hh(popular_lang)))
    print(create_tabel('SuperJob Moscow', get_job_statistic_from_sj(token, popular_lang)))


if __name__ == '__main__':
    load_dotenv()
    main()
