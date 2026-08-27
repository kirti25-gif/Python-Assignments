from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Interface-like abstraction for payment processing."""

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass


class CardPayment(PaymentProcessor):
    def __init__(self, masked_card: str):
        # Only a masked identifier is kept; sensitive card data is not stored.
        if not masked_card.strip():
            raise ValueError("Masked card information is required.")
        self._masked_card = masked_card

    def process_payment(self, amount: float) -> bool:
        if amount <= 0:
            return False
        print(f"Card payment processed using {self._masked_card}.")
        return True


class UPIPayment(PaymentProcessor):
    def __init__(self, upi_id: str):
        if not upi_id.strip():
            raise ValueError("UPI ID is required.")
        self._upi_id = upi_id

    def process_payment(self, amount: float) -> bool:
        if amount <= 0:
            return False
        print(f"UPI payment processed using {self._upi_id}.")
        return True
