# Vehicle Rental Management System

A console-based Python OOP implementation of the **Vehicle Rental Management System** case study.

## Requirements

- VS Code
- No external packages are required.

## Project structure

```text
vehicle_rental_system/
├── main.py
├── models.py
├── payments.py
├── services.py
├── exceptions.py
├── tests.py
├── class_diagram.md
└── README.md
```

## How to run in VS Code

1. Open the `vehicle_rental_system` folder in VS Code.
2. Open the VS Code terminal.
3. Run:

```bash
python main.py
```

4. Run tests:

```bash
python -m unittest tests.py -v
```

## Terminal menu

When `python main.py` is executed, the program shows:

```text
==================================================
 VEHICLE RENTAL MANAGEMENT SYSTEM
==================================================
1. Add Vehicle
2. Add Customer
3. View All Vehicles
4. View Available Vehicles
5. View All Customers
6. Search Vehicles
7. Rent Vehicle
8. Return Vehicle
9. View Customer Rental History
10. Run Assignment Demonstration
11. Exit
```

### Add a vehicle from the terminal

Choose option `1`.

For a car or bike, enter:

```text
Enter vehicle type (car/bike/van): car
Enter vehicle ID: V104
Enter registration number: KA04XY1234
Enter brand: Honda
Enter model: City
Enter daily rental rate: 2500
```

For a van, the program additionally asks for the service charge:

```text
Enter vehicle type (car/bike/van): van
Enter vehicle ID: V105
Enter registration number: KA05XY5678
Enter brand: Tata
Enter model: Winger
Enter daily rental rate: 3000
Enter van service charge: 500
```

After adding a vehicle, choose option `3` to see all vehicles or option `4` to see only available vehicles.

# choose option '2' for adding customers

The program validates empty vehicle details, positive rental rates, non-negative van service charges, duplicate vehicle IDs, and invalid vehicle types.

## Class responsibilities

- **Vehicle**: abstract base class containing common vehicle data and availability operations.
- **Car**: normal daily-rate calculation.
- **Bike**: 5% discount when rental exceeds five days.
- **Van**: daily-rate calculation plus a service charge.
- **Customer**: customer details and rental history.
- **Rental**: connects a customer, vehicle, rental dates, amount and payment result.
- **Invoice**: generates and displays the final rental breakdown.
- **PaymentProcessor**: payment abstraction/interface.
- **CardPayment / UPIPayment**: concrete payment implementations.
- **RentalService**: coordinates search, rental, payment, return and invoice creation.
- **Exceptions**: meaningful business-rule errors.

## OOP concepts demonstrated

### Encapsulation
Fields are private/protected by convention using `_field_name`, and read access is controlled through properties. Constructors validate required data.

### Abstraction
`Vehicle` and `PaymentProcessor` are abstract contracts. The rest of the application does not need to know how a particular vehicle calculates its cost or how a payment is processed.

### Inheritance
`Car`, `Bike`, and `Van` inherit from `Vehicle`.

### Polymorphism
`Rental` calls:

```python
vehicle.calculate_rental_cost(days)
```

without checking whether the object is a car, bike, or van. Python dispatches to the appropriate overridden method.

This avoids long `if/elif` blocks based on vehicle type and makes adding a new vehicle type easier.

### Method overriding
Each vehicle subclass overrides `calculate_rental_cost()`.

### Interface / dependency inversion
`RentalService.rent_vehicle()` receives a `PaymentProcessor`. It can therefore work with `CardPayment`, `UPIPayment`, or another implementation without changing rental logic.

### Composition
A `Rental` contains references to a `Customer`, `Vehicle`, payment result and `Invoice`.

### Method overloading equivalent in Python
Python does not support Java-style method overloading by signature. The `search_vehicles()` method uses optional parameters so the same method can search by vehicle ID, vehicle type, price range, or combinations of criteria.

## Business rules implemented

- Rental days must be greater than zero.
- A customer cannot rent an unavailable vehicle.
- A vehicle cannot be rented by two customers at the same time.
- Vehicle registration number and other required fields cannot be empty.
- Payment must succeed before the rental is confirmed.
- Sensitive payment information is not stored as plain text; the card implementation keeps only a masked identifier.
- A returned vehicle becomes available.
- Late fee = late days × 20% × vehicle daily rental rate.
- Vehicle IDs must be unique.
- Vehicle details can be entered interactively from the terminal.

## Mandatory scenario

Option `10` runs the assignment demonstration:

1. One car, one bike and one van.
2. Two customers.
3. Available vehicle listing.
4. Customer A rents the car for three days.
5. Customer B attempts to rent the same car and receives an unavailable message.
6. Customer A's payment succeeds.
7. Customer A returns the car one day late.
8. Base amount = Rs. 6,000.
9. Late fee = 1 × 20% × Rs. 2,000 = Rs. 400.
10. Final amount = Rs. 6,400.
11. The car becomes available again.
12. Customer A's rental history is displayed.

## Test cases

`tests.py` covers:

- Car rental calculation.
- Bike discount.
- Van service charge.
- Unavailable vehicle failure.
- Payment failure and confirmation protection.
- Late-fee calculation and vehicle return.




