import requests


def get_job_statistic_from_sj(token, popular_lang):
    result = {}
    for lang in popular_lang:
        page = 0
        pages_data = []
        while True:
            url = "https://api.superjob.ru/2.0/vacancies/"
            header = {
                "X-Api-App-Id": token
            }
            payloads = {
                "t": 4,
                "catalogues": 48,
                "keyword": f"Программист {lang}",
                "page": page
            }
            page_response = requests.get(url, params=payloads, headers=header)
            page_response.raise_for_status()
            page_response_as_json = page_response.json()
            pages_data.append(page_response_as_json["objects"])
            page += 1
            if not page_response_as_json["more"]:
                break
        vacancies_found, vacancies_processed, average_salary = get_salary_statistic(pages_data)
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
            salaries.append(predict_salary(
                vacancy["payment_from"],
                vacancy["payment_to"],
                vacancy["currency"]))
    filtered_salaries = list(filter(lambda x: x, salaries))
    vacancies_processed = len(filtered_salaries)
    average_salary = sum(filtered_salaries)/vacancies_processed
    return vacancies_found, vacancies_processed, int(average_salary)


def predict_salary(salary_from, salary_to, salary_currency):
    if not salary_currency:
        return None
    if salary_from and salary_to:
        return (salary_from + salary_to)//2
    else:
        if not salary_from:
            return salary_to * 0.8
        else:
            return salary_from * 1.2
