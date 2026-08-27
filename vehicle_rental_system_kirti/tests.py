import unittest
from datetime import date, timedelta

from exceptions import PaymentFailedError, VehicleUnavailableError
from models import Bike, Car, Customer, Van
from payments import CardPayment, PaymentProcessor
from services import RentalService


class FailingPayment(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        return False


class VehicleRentalTests(unittest.TestCase):
    def setUp(self):
        self.service = RentalService()
        self.car = Car("V101", "KA01AB1234", "Toyota", "Camry", 2000)
        self.bike = Bike("V102", "KA02CD5678", "Yamaha", "FZ", 700)
        self.van = Van("V103", "KA03EF9012", "Tata", "Winger", 3000, 500)

        self.service.add_vehicle(self.car)
        self.service.add_vehicle(self.bike)
        self.service.add_vehicle(self.van)

        self.customer = Customer(
            "C001", "Ananya Sharma", "ananya@example.com", "DL1234567890"
        )
        self.service.add_customer(self.customer)

        self.rental_date = date(2026, 8, 21)

    def test_car_cost(self):
        self.assertEqual(self.car.calculate_rental_cost(3), 6000)

    def test_bike_discount_after_five_days(self):
        self.assertEqual(self.bike.calculate_rental_cost(6), 3990)

    def test_van_service_charge(self):
        self.assertEqual(self.van.calculate_rental_cost(2), 6500)

    def test_unavailable_vehicle(self):
        self.service.rent_vehicle(
            "C001", "V101", 3, CardPayment("CARD-****-1234"), self.rental_date
        )

        with self.assertRaises(VehicleUnavailableError):
            self.service.rent_vehicle(
                "C001", "V101", 2, CardPayment("CARD-****-1234"), self.rental_date
            )

    def test_payment_failure_does_not_confirm_rental(self):
        with self.assertRaises(PaymentFailedError):
            self.service.rent_vehicle(
                "C001", "V101", 3, FailingPayment(), self.rental_date
            )

        self.assertTrue(self.car.available)

    def test_late_fee_and_return(self):
        rental = self.service.rent_vehicle(
            "C001", "V101", 3, CardPayment("CARD-****-1234"), self.rental_date
        )

        return_date = rental.expected_return_date + timedelta(days=1)
        invoice = self.service.return_vehicle(rental.rental_id, return_date)

        self.assertEqual(rental.base_amount, 6000)
        self.assertEqual(rental.late_fee, 400)
        self.assertEqual(rental.final_amount, 6400)
        self.assertTrue(self.car.available)
        self.assertEqual(invoice.generate()["final_amount"], 6400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
