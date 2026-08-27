from datetime import date, timedelta

from models import Car, Bike, Van, Customer
from payments import CardPayment, UPIPayment
from services import RentalService
from exceptions import RentalError


def print_available_vehicles(service):
    print("\nAvailable Vehicles")
    print("-" * 80)
    vehicles = service.search_vehicles(available_only=True)
    if not vehicles:
        print("No available vehicles.")
        return
    for vehicle in vehicles:
        print(vehicle.display_details())


def print_all_vehicles(service):
    print("\nAll Vehicles")
    print("-" * 80)
    vehicles = service.search_vehicles()
    if not vehicles:
        print("No vehicles have been added yet.")
        return
    for vehicle in vehicles:
        print(vehicle.display_details())


def print_all_customers(service):
    print("\nAll Customers")
    print("-" * 80)
    customers = service.get_all_customers()
    if not customers:
        print("No customers have been added yet.")
        return
    for customer in customers:
        print(
            f"{customer.customer_id} | {customer.name} | "
            f"{customer.email} | Licence: {customer.licence_number}"
        )


def add_vehicle_from_terminal(service):
    print("\n--- Add Vehicle ---")
    try:
        vehicle_type = input("Enter vehicle type (car/bike/van): ").strip().lower()
        vehicle_id = input("Enter vehicle ID: ").strip()
        registration_number = input("Enter registration number: ").strip()
        brand = input("Enter brand: ").strip()
        model = input("Enter model: ").strip()
        daily_rate = float(input("Enter daily rental rate: "))

        if vehicle_type == "car":
            vehicle = Car(vehicle_id, registration_number, brand, model, daily_rate)
        elif vehicle_type == "bike":
            vehicle = Bike(vehicle_id, registration_number, brand, model, daily_rate)
        elif vehicle_type == "van":
            service_charge = float(input("Enter van service charge: "))
            vehicle = Van(
                vehicle_id,
                registration_number,
                brand,
                model,
                daily_rate,
                service_charge,
            )
        else:
            print("Invalid vehicle type. Please enter car, bike, or van.")
            return

        service.add_vehicle(vehicle)
        print("\nVehicle added successfully!")
        print(vehicle.display_details())
    except ValueError as error:
        print(f"Could not add vehicle: {error}")
    except RentalError as error:
        print(f"Could not add vehicle: {error}")


def add_customer_from_terminal(service):
    print("\n--- Add Customer ---")
    try:
        customer_id = input("Enter customer ID: ").strip()
        name = input("Enter customer name: ").strip()
        email = input("Enter email: ").strip()
        licence_number = input("Enter driving licence number: ").strip()

        customer = Customer(customer_id, name, email, licence_number)
        service.add_customer(customer)

        print("\nCustomer added successfully!")
        print(
            f"{customer.customer_id} | {customer.name} | "
            f"{customer.email} | Licence: {customer.licence_number}"
        )
    except ValueError as error:
        print(f"Could not add customer: {error}")
    except RentalError as error:
        print(f"Could not add customer: {error}")


def rent_vehicle_from_terminal(service):
    print("\n--- Rent Vehicle ---")
    try:
        print_all_customers(service)
        customer_id = input("Enter customer ID: ").strip()

        print_available_vehicles(service)
        vehicle_id = input("Enter vehicle ID: ").strip()
        days = int(input("Enter number of rental days: "))

        print("\nPayment method")
        print("1. Card")
        print("2. UPI")
        payment_choice = input("Choose payment method: ").strip()

        if payment_choice == "1":
            masked_card = input("Enter masked card number (example CARD-****-1234): ").strip()
            payment_processor = CardPayment(masked_card)
        elif payment_choice == "2":
            upi_id = input("Enter UPI ID: ").strip()
            payment_processor = UPIPayment(upi_id)
        else:
            print("Invalid payment method.")
            return

        rental = service.rent_vehicle(
            customer_id=customer_id,
            vehicle_id=vehicle_id,
            days=days,
            payment_processor=payment_processor,
        )

        print("\nRental confirmed successfully!")
        print(f"Rental ID: {rental.rental_id}")
        print(f"Base rental amount: Rs. {rental.base_amount:,.2f}")
        print(f"Expected return date: {rental.expected_return_date}")
    except (ValueError, RentalError) as error:
        print(f"Could not complete rental: {error}")


def return_vehicle_from_terminal(service):
    print("\n--- Return Vehicle ---")
    try:
        rental_id = input("Enter rental ID: ").strip()
        return_date_text = input(
            "Enter return date (YYYY-MM-DD), or press Enter for today: "
        ).strip()

        if return_date_text:
            return_date = date.fromisoformat(return_date_text)
        else:
            return_date = date.today()

        invoice = service.return_vehicle(rental_id, return_date)
        print("\nVehicle returned successfully!")
        invoice.display()
    except (ValueError, RentalError) as error:
        print(f"Could not return vehicle: {error}")


def show_customer_history(service):
    print("\n--- Customer Rental History ---")
    try:
        print_all_customers(service)
        customer_id = input("Enter customer ID: ").strip()
        customer = service.get_customer(customer_id)
        print(f"\nRental history for {customer.name}")
        print("-" * 80)
        customer.display_rental_history()
    except RentalError as error:
        print(f"Could not find customer: {error}")


def search_vehicles_from_terminal(service):
    print("\n--- Search Vehicles ---")
    print("1. Search by vehicle ID")
    print("2. Search by vehicle type")
    print("3. Search by maximum daily rate")
    print("4. Show all available vehicles")
    choice = input("Enter choice: ").strip()

    try:
        if choice == "1":
            vehicle_id = input("Enter vehicle ID: ").strip()
            vehicles = service.search_vehicles(vehicle_id=vehicle_id)
        elif choice == "2":
            vehicle_type = input("Enter type (car/bike/van): ").strip()
            vehicles = service.search_vehicles(vehicle_type=vehicle_type)
        elif choice == "3":
            max_rate = float(input("Enter maximum daily rate: "))
            vehicles = service.search_vehicles(max_daily_rate=max_rate)
        elif choice == "4":
            vehicles = service.search_vehicles(available_only=True)
        else:
            print("Invalid search choice.")
            return

        print("\nSearch Results")
        print("-" * 80)
        if not vehicles:
            print("No matching vehicles found.")
            return
        for vehicle in vehicles:
            print(vehicle.display_details())
    except ValueError as error:
        print(f"Invalid input: {error}")


def setup_demo_data(service):
    """Create the vehicles and customers used in the assignment demonstration."""
    car = Car("V101", "KA01AB1234", "Toyota", "Camry", 2000)
    bike = Bike("V102", "KA02CD5678", "Yamaha", "FZ", 700)
    van = Van("V103", "KA03EF9012", "Tata", "Winger", 3000, service_charge=500)
    service.add_vehicle(car)
    service.add_vehicle(bike)
    service.add_vehicle(van)

    customer_a = Customer("C001", "Ananya Sharma", "ananya@example.com", "DL1234567890")
    customer_b = Customer("C002", "Rahul Verma", "rahul@example.com", "DL0987654321")
    service.add_customer(customer_a)
    service.add_customer(customer_b)
    return car, bike, van, customer_a, customer_b


def run_mandatory_demo():
    service = RentalService()
    car, bike, van, customer_a, customer_b = setup_demo_data(service)
    print_available_vehicles(service)
    print("\nCustomer:", customer_a.name)
    print("Selected vehicle:", car.vehicle_id)
    print("Rental duration: 3 days")
    rental_date = date.today()

    try:
        rental = service.rent_vehicle(
            customer_id="C001",
            vehicle_id="V101",
            days=3,
            payment_processor=CardPayment("CARD-****-1234"),
            rental_date=rental_date,
        )
        print(f"Base rental amount: Rs. {rental.base_amount:,.0f}")
        print("Payment completed successfully.")
    except RentalError as error:
        print("Rental failed:", error)
        return

    print("\nCustomer B attempts to rent the same car...")
    try:
        service.rent_vehicle(
            customer_id="C002",
            vehicle_id="V101",
            days=2,
            payment_processor=UPIPayment("rahul@upi"),
            rental_date=rental_date,
        )
    except RentalError as error:
        print("Vehicle unavailable:", error)

    return_date = rental.expected_return_date + timedelta(days=1)
    invoice = service.return_vehicle(rental.rental_id, return_date)
    invoice.display()
    print("\nVehicle available again:", car.available)
    print("\nCustomer A Rental History")
    print("-" * 80)
    customer_a.display_rental_history()


def show_menu():
    print("\n" + "=" * 60)
    print(" VEHICLE RENTAL MANAGEMENT SYSTEM")
    print("=" * 60)
    print("1. Add Vehicle")
    print("2. Add Customer")
    print("3. View All Vehicles")
    print("4. View Available Vehicles")
    print("5. View All Customers")
    print("6. Search Vehicles")
    print("7. Rent Vehicle")
    print("8. Return Vehicle")
    print("9. View Customer Rental History")
    print("10. Run Assignment Demonstration")
    print("11. Exit")


def main():
    # All vehicles, customers and rentals added here remain available
    # during this program session. You can add as many as you want.
    service = RentalService()

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_vehicle_from_terminal(service)
        elif choice == "2":
            add_customer_from_terminal(service)
        elif choice == "3":
            print_all_vehicles(service)
        elif choice == "4":
            print_available_vehicles(service)
        elif choice == "5":
            print_all_customers(service)
        elif choice == "6":
            search_vehicles_from_terminal(service)
        elif choice == "7":
            rent_vehicle_from_terminal(service)
        elif choice == "8":
            return_vehicle_from_terminal(service)
        elif choice == "9":
            show_customer_history(service)
        elif choice == "10":
            run_mandatory_demo()
        elif choice == "11":
            print("\nThank you for using the Vehicle Rental Management System!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 11.")


if __name__ == "__main__":
    main()
