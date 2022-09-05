import requests
from tools import predict_salary


def get_job_statistic_from_hh(popular_lang):
    dev_job_id = 96
    moscow_town_id = 1
    result = {}
    for lang in popular_lang:
        page = 0
        pages_number = 1
        all_pages_data = []
        while page < pages_number:
            url = "https://api.hh.ru/vacancies"
            payload = {
                "professional_role": dev_job_id,
                "area": moscow_town_id,
                "text": f"Программист {lang}",
                "page": page
            }
            page_response  = requests.get(url, params=payload)
            page_response.raise_for_status()
            response = page_response.json()
            all_pages_data.append(response["items"])
            pages_number = response["pages"]
            page += 1
        vacancies_found, vacancies_processed, average_salary = get_salary_statistic(all_pages_data)
        result[lang] = {
                "vacancies_found": vacancies_found,
                "vacancies_processed": vacancies_processed,
                "average_salary": average_salary
        }
    return result


def get_salary_statistic(all_vacancies):
    vacancies_found = 0
    salaries = []
    for vacancies in all_vacancies:
        vacancies_found += len(vacancies)
        for vacancy in vacancies:
            salary = vacancy.get("salary")
            if not salary or salary["currency"] != "RUR":
                continue
            salaries.append(predict_salary(salary["from"], salary["to"]))
    filtered_salaries = list(filter(lambda x: x, salaries))
    vacancies_processed = len(filtered_salaries)
    if vacancies_processed == 0:
        average_salary = 0
    else:
        average_salary = sum(filtered_salaries)/vacancies_processed
    return vacancies_found, vacancies_processed, int(average_salary)
