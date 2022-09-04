import requests


def get_job_statistic_from_hh(popular_lang):
    result = {}
    for lang in popular_lang:
        page = 0
        pages_number = 1
        page_data = []
        while page < pages_number:
            url = "https://api.hh.ru/vacancies"
            payload = {
                "professional_role": 96,
                "area": 1,
                "text": f"Программист {lang}",
                "page": page
            }
            page_response  = requests.get(url, params=payload)
            page_response.raise_for_status()
            response_as_json = page_response.json()
            page_data.append(response_as_json["items"])
            pages_number = response_as_json["pages"]
            page += 1
        vacancies_found, vacancies_processed, average_salary = get_salary_statistic(page_data)
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
            salaries.append(predict_rub_salary_hh(vacancy))
    filtered_salaries = list(filter(lambda x: x, salaries))
    vacancies_processed = len(filtered_salaries)
    average_salary = sum(filtered_salaries)/vacancies_processed
    return vacancies_found, vacancies_processed, int(average_salary)


def predict_rub_salary_hh(vacancy):
    salary = vacancy.get("salary")
    if not salary or salary["currency"] != "RUR":
        return None
    elif salary["from"] and salary["to"]:
        return (salary["from"] + salary["to"])//2
    else:
        if not salary["from"]:
            return salary["to"] * 0.8
        else:
            return salary["from"] * 1.2
