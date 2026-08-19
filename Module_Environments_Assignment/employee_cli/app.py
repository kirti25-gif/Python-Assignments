from tabulate import tabulate

from rich.console import Console
from rich.table import Table

from employee_system.employee import get_all_employees


def display_tabulate(employees):
    print("Employee List - Tabulate")
    print("------------------------")

    print(
        tabulate(
            employees,
            headers="keys",
            tablefmt="grid"
        )
    )


def display_tabulate_simple(employees):
    print("Employee List - Simple")
    print("----------------------")

    print(
        tabulate(
            employees,
            headers="keys",
            tablefmt="simple"
        )
    )


def display_rich(employees):
    console = Console()

    table = Table(
        title="Employee Details"
    )

    table.add_column(
        "ID",
        justify="center"
    )

    table.add_column(
        "Name",
        justify="left"
    )

    table.add_column(
        "Department",
        justify="left"
    )

    table.add_column(
        "Salary",
        justify="right"
    )

    for employee in employees:
        table.add_row(
            employee["id"],
            employee["name"],
            employee["department"],
            str(employee["salary"])
        )

    console.print(table)


def main():
    employees = get_all_employees()

    print("=" * 40)
    print(" EMPLOYEE CLI APPLICATION")
    print("=" * 40)

    display_tabulate(employees)

    print()

    display_tabulate_simple(employees)

    print()

    print("Employee List - Rich")
    print("--------------------")

    display_rich(employees)


if __name__ == "__main__":
    main()