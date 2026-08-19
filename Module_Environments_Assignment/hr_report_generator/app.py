
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from prettytable import PrettyTable

from employee_system.employee import get_all_employees


def generate_employee_report(employee):
    template_directory = Path(__file__).parent / "templates"

    environment = Environment(
        loader=FileSystemLoader(template_directory)
    )

    template = environment.get_template("employee_report.txt")

    return template.render(employee=employee)


def create_employee_table(employees):
    table = PrettyTable()

    table.field_names = [
        "ID",
        "Name",
        "Department",
        "Salary"
    ]

    for employee in employees:
        table.add_row([
            employee["id"],
            employee["name"],
            employee["department"],
            employee["salary"]
        ])

    return table


def main():
    employees = get_all_employees()

    print("=" * 40)
    print(" HR EMPLOYEE REPORT")
    print("=" * 40)

    for employee in employees:
        print(generate_employee_report(employee))
        print()

    print("Employee Table")
    print("==============")

    table = create_employee_table(employees)
    print(table)


if __name__ == "__main__":
    main()