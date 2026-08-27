from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List


class Vehicle(ABC):
    """Abstract base class for all rentable vehicles."""

    def __init__(
        self,
        vehicle_id: str,
        registration_number: str,
        brand: str,
        model: str,
        daily_rate: float,
    ):
        if not all(
            str(value).strip()
            for value in [vehicle_id, registration_number, brand, model]
        ):
            raise ValueError("Vehicle details cannot be empty.")
        if daily_rate <= 0:
            raise ValueError("Daily rental rate must be greater than zero.")

        self._vehicle_id = vehicle_id
        self._registration_number = registration_number
        self._brand = brand
        self._model = model
        self._daily_rate = float(daily_rate)
        self._available = True

    @property
    def vehicle_id(self) -> str:
        return self._vehicle_id

    @property
    def registration_number(self) -> str:
        return self._registration_number

    @property
    def brand(self) -> str:
        return self._brand

    @property
    def model(self) -> str:
        return self._model

    @property
    def daily_rate(self) -> float:
        return self._daily_rate

    @property
    def available(self) -> bool:
        return self._available

    @property
    @abstractmethod
    def vehicle_type(self) -> str:
        pass

    @abstractmethod
    def calculate_rental_cost(self, days: int) -> float:
        pass

    def display_details(self) -> str:
        status = "Available" if self._available else "Rented"
        return (
            f"{self.vehicle_id} | {self.vehicle_type} | {self.brand} "
            f"{self.model} | Rs. {self.daily_rate:,.2f}/day | {status}"
        )

    def mark_as_rented(self) -> None:
        if not self._available:
            raise ValueError("Vehicle is already rented.")
        self._available = False

    def mark_as_available(self) -> None:
        self._available = True


class Car(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "Car"

    def calculate_rental_cost(self, days: int) -> float:
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")
        return self.daily_rate * days


class Bike(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "Bike"

    def calculate_rental_cost(self, days: int) -> float:
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")

        total = self.daily_rate * days
        if days > 5:
            total *= 0.95
        return total


class Van(Vehicle):
    def __init__(
        self,
        vehicle_id: str,
        registration_number: str,
        brand: str,
        model: str,
        daily_rate: float,
        service_charge: float,
    ):
        super().__init__(
            vehicle_id, registration_number, brand, model, daily_rate
        )
        if service_charge < 0:
            raise ValueError("Service charge cannot be negative.")
        self._service_charge = float(service_charge)

    @property
    def vehicle_type(self) -> str:
        return "Van"

    @property
    def service_charge(self) -> float:
        return self._service_charge

    def calculate_rental_cost(self, days: int) -> float:
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")
        return (self.daily_rate * days) + self.service_charge


class Customer:
    def __init__(
        self,
        customer_id: str,
        name: str,
        email: str,
        licence_number: str,
    ):
        if not all(
            str(value).strip()
            for value in [customer_id, name, email, licence_number]
        ):
            raise ValueError("Customer details cannot be empty.")

        self._customer_id = customer_id
        self._name = name
        self._email = email
        self._licence_number = licence_number
        self._rental_history: List["Rental"] = []

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def licence_number(self) -> str:
        return self._licence_number

    @property
    def rental_history(self) -> tuple:
        return tuple(self._rental_history)

    def add_rental(self, rental: "Rental") -> None:
        self._rental_history.append(rental)

    def display_rental_history(self) -> None:
        if not self._rental_history:
            print("No rental history.")
            return

        for rental in self._rental_history:
            print(
                f"{rental.rental_id} | {rental.vehicle.vehicle_id} | "
                f"{rental.days} days | Status: {rental.status} | "
                f"Final: Rs. {rental.final_amount:,.2f}"
            )


class Rental:
    def __init__(
        self,
        rental_id: str,
        customer: Customer,
        vehicle: Vehicle,
        days: int,
        rental_date: date,
    ):
        if days <= 0:
            raise ValueError("Rental days must be greater than zero.")

        self._rental_id = rental_id
        self._customer = customer
        self._vehicle = vehicle
        self._rental_date = rental_date
        self._expected_return_date = rental_date + timedelta(days=days)
        self._return_date = None
        self._days = days
        self._base_amount = vehicle.calculate_rental_cost(days)
        self._late_fee = 0.0
        self._final_amount = self._base_amount
        self._status = "Confirmed"
        self._payment = None
        self._invoice = None

    @property
    def rental_id(self):
        return self._rental_id

    @property
    def customer(self):
        return self._customer

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def rental_date(self):
        return self._rental_date

    @property
    def expected_return_date(self):
        return self._expected_return_date

    @property
    def return_date(self):
        return self._return_date

    @property
    def days(self):
        return self._days

    @property
    def base_amount(self):
        return self._base_amount

    @property
    def late_fee(self):
        return self._late_fee

    @property
    def final_amount(self):
        return self._final_amount

    @property
    def status(self):
        return self._status

    @property
    def payment(self):
        return self._payment

    @property
    def invoice(self):
        return self._invoice

    def set_payment(self, payment) -> None:
        self._payment = payment

    def complete_return(self, return_date: date) -> None:
        if self._status == "Returned":
            raise ValueError("Rental has already been returned.")

        if return_date < self._rental_date:
            raise ValueError("Return date cannot be before rental date.")

        self._return_date = return_date
        late_days = max(0, (return_date - self._expected_return_date).days)
        self._late_fee = late_days * (0.20 * self.vehicle.daily_rate)
        self._final_amount = self._base_amount + self._late_fee
        self._status = "Returned"
        self._vehicle.mark_as_available()

    def attach_invoice(self, invoice) -> None:
        self._invoice = invoice


class Invoice:
    def __init__(self, rental: Rental):
        self._rental = rental

    def generate(self) -> dict:
        late_days = 0
        if self._rental.return_date:
            late_days = max(
                0,
                (self._rental.return_date - self._rental.expected_return_date).days,
            )

        return {
            "rental_id": self._rental.rental_id,
            "customer": self._rental.customer.name,
            "vehicle": self._rental.vehicle.vehicle_id,
            "base_amount": self._rental.base_amount,
            "late_days": late_days,
            "late_fee": self._rental.late_fee,
            "final_amount": self._rental.final_amount,
        }

    def display(self) -> None:
        data = self.generate()
        print("\nFinal Invoice")
        print("-" * 40)
        print(f"Rental ID:          {data['rental_id']}")
        print(f"Customer:            {data['customer']}")
        print(f"Vehicle:             {data['vehicle']}")
        print(f"Base rental amount:  Rs. {data['base_amount']:,.2f}")
        print(f"Late days:           {data['late_days']}")
        print(f"Late fee:            Rs. {data['late_fee']:,.2f}")
        print(f"Final amount:        Rs. {data['final_amount']:,.2f}")
        print("-" * 40)
