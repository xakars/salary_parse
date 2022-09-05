

def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to)//2
    else:
        if not salary_from:
            return salary_to * 0.8
        else:
            return salary_from * 1.2
