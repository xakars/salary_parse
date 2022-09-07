import requests
from tools import predict_salary


def get_job_statistic_from_sj(token, popular_lang):
    dev_job_id = 48
    moscow_town_id = 4
    vacancies_statistic = {}
    for lang in popular_lang:
        page = 0
        all_pages = []
        while True:
            url = "https://api.superjob.ru/2.0/vacancies/"
            header = {
                "X-Api-App-Id": token
            }
            payloads = {
                "t": moscow_town_id,
                "catalogues": dev_job_id,
                "keyword": f"Программист {lang}",
                "page": page
            }
            page_response = requests.get(url, params=payloads, headers=header)
            page_response.raise_for_status()
            response = page_response.json()
            all_pages.append(response["objects"])
            page += 1
            if not response["more"]:
                break
        vacancies_found, vacancies_processed, average_salary = get_salary_statistic(all_pages)
        vacancies_statistic[lang] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary
        }
    return vacancies_statistic


def get_salary_statistic(all_vacancies):
    vacancies_found = 0
    salaries = []
    for vacancies in all_vacancies:
        vacancies_found += len(vacancies)
        for vacancy in vacancies:
            if vacancy["currency"] != 'rub':
                continue
            salaries.append(predict_salary(
                vacancy["payment_from"],
                vacancy["payment_to"]))
    filtered_salaries = list(filter(lambda x: x, salaries))
    vacancies_processed = len(filtered_salaries)
    if vacancies_processed == 0:
        average_salary = 0
    else:
        average_salary = sum(filtered_salaries)/vacancies_processed
    return vacancies_found, vacancies_processed, int(average_salary)
