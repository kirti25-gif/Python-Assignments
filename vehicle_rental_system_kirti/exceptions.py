class RentalError(Exception):
    """Base exception for rental business-rule failures."""


class VehicleUnavailableError(RentalError):
    pass


class PaymentFailedError(RentalError):
    pass


class InvalidRentalError(RentalError):
    pass
