def calculate_salary(basic_salary, allowance=0, deduction=0):
    return basic_salary + allowance - deduction


def calculate_bonus(salary, percentage=10):
    return salary * percentage / 100