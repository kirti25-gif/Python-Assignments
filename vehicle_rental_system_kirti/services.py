from datetime import date
from typing import Dict, List, Optional

from exceptions import (
    InvalidRentalError,
    PaymentFailedError,
    RentalError,
    VehicleUnavailableError,
)
from models import Customer, Invoice, Rental, Vehicle


class RentalService:
    """Coordinates vehicles, customers, rentals, payments and invoices."""

    LATE_FEE_RATE = 0.20

    def __init__(self):
        self._vehicles: Dict[str, Vehicle] = {}
        self._customers: Dict[str, Customer] = {}
        self._rentals: Dict[str, Rental] = {}
        self._next_rental_number = 1

    def add_vehicle(self, vehicle: Vehicle) -> None:
        if vehicle.vehicle_id in self._vehicles:
            raise RentalError("Vehicle ID already exists.")
        self._vehicles[vehicle.vehicle_id] = vehicle

    def add_customer(self, customer: Customer) -> None:
        if customer.customer_id in self._customers:
            raise RentalError("Customer ID already exists.")
        self._customers[customer.customer_id] = customer

    def get_all_customers(self) -> List[Customer]:
        return list(self._customers.values())

    def get_customer(self, customer_id: str) -> Customer:
        if customer_id not in self._customers:
            raise RentalError("Customer not found.")
        return self._customers[customer_id]

    # Python-friendly method overloading: optional criteria support
    # search by ID, type, or price range.
    def search_vehicles(
        self,
        vehicle_id: Optional[str] = None,
        vehicle_type: Optional[str] = None,
        max_daily_rate: Optional[float] = None,
        available_only: bool = False,
    ) -> List[Vehicle]:
        vehicles = list(self._vehicles.values())

        if vehicle_id:
            vehicles = [
                vehicle for vehicle in vehicles
                if vehicle.vehicle_id.lower() == vehicle_id.lower()
            ]

        if vehicle_type:
            vehicles = [
                vehicle for vehicle in vehicles
                if vehicle.vehicle_type.lower() == vehicle_type.lower()
            ]

        if max_daily_rate is not None:
            vehicles = [
                vehicle for vehicle in vehicles
                if vehicle.daily_rate <= max_daily_rate
            ]

        if available_only:
            vehicles = [vehicle for vehicle in vehicles if vehicle.available]

        return vehicles

    def rent_vehicle(
        self,
        customer_id: str,
        vehicle_id: str,
        days: int,
        payment_processor,
        rental_date: Optional[date] = None,
    ) -> Rental:
        if days <= 0:
            raise InvalidRentalError("Rental days must be greater than zero.")

        if customer_id not in self._customers:
            raise RentalError("Customer not found.")

        if vehicle_id not in self._vehicles:
            raise RentalError("Vehicle not found.")

        vehicle = self._vehicles[vehicle_id]
        customer = self._customers[customer_id]

        if not vehicle.available:
            raise VehicleUnavailableError(
                f"Vehicle {vehicle.vehicle_id} is unavailable."
            )

        rental_date = rental_date or date.today()
        rental_id = f"R{self._next_rental_number:03d}"

        # Calculate the amount before changing vehicle state.
        rental = Rental(
            rental_id,
            customer,
            vehicle,
            days,
            rental_date,
        )

        # Payment must succeed before the rental is confirmed/vehicle is marked rented.
        if not payment_processor.process_payment(rental.base_amount):
            raise PaymentFailedError("Payment failed. Rental was not confirmed.")

        rental.set_payment(payment_processor)
        vehicle.mark_as_rented()
        self._rentals[rental_id] = rental
        customer.add_rental(rental)
        self._next_rental_number += 1

        return rental

    def return_vehicle(self, rental_id: str, return_date: date) -> Invoice:
        if rental_id not in self._rentals:
            raise RentalError("Rental not found.")

        rental = self._rentals[rental_id]
        rental.complete_return(return_date)

        invoice = Invoice(rental)
        rental.attach_invoice(invoice)
        return invoice
