"""
RM-DDD Value Objects

Value Object implementations with immutability and value semantics.
"""

from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime

from ..core.types import ValidationResult


class ValueObject(ABC):
    """Base class for value objects"""

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))

    @abstractmethod
    def validate(self) -> ValidationResult:
        """Validate value object constraints"""
        pass

    def __post_init__(self):
        """Validate value object after initialization"""
        validation_result = self.validate()
        if not validation_result.is_valid:
            raise ValueError(f"Invalid value object: {validation_result.errors}")


@dataclass(frozen=True)
class ImmutableValueObject(ValueObject):
    """Immutable value object base class"""

    def __post_init__(self):
        """Validate immutable value object after initialization"""
        validation_result = self.validate()
        if not validation_result.is_valid:
            raise ValueError(f"Invalid value object: {validation_result.errors}")


# Common value object examples
@dataclass(frozen=True)
class Money(ImmutableValueObject):
    """Money value object"""

    amount: float
    currency: str

    def validate(self) -> ValidationResult:
        """Validate money constraints"""
        result = ValidationResult(is_valid=True)

        if self.amount < 0:
            result.add_error("Money amount cannot be negative")

        if not self.currency or len(self.currency) != 3:
            result.add_error("Currency must be a 3-letter code")

        return result

    def add(self, other: "Money") -> "Money":
        """Add money amounts (same currency)"""
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: float) -> "Money":
        """Multiply money amount by factor"""
        return Money(self.amount * factor, self.currency)


@dataclass(frozen=True)
class Email(ImmutableValueObject):
    """Email value object"""

    value: str

    def validate(self) -> ValidationResult:
        """Validate email format"""
        result = ValidationResult(is_valid=True)

        if not self.value or "@" not in self.value:
            result.add_error("Invalid email format")

        return result


@dataclass(frozen=True)
class Address(ImmutableValueObject):
    """Address value object"""

    street: str
    city: str
    state: str
    zip_code: str
    country: str

    def validate(self) -> ValidationResult:
        """Validate address constraints"""
        result = ValidationResult(is_valid=True)

        if not self.street or not self.city or not self.country:
            result.add_error("Street, city, and country are required")

        return result


@dataclass(frozen=True)
class DateRange(ImmutableValueObject):
    """Date range value object"""

    start_date: datetime
    end_date: datetime

    def validate(self) -> ValidationResult:
        """Validate date range constraints"""
        result = ValidationResult(is_valid=True)

        if self.start_date >= self.end_date:
            result.add_error("Start date must be before end date")

        return result

    def contains(self, date: datetime) -> bool:
        """Check if date is within range"""
        return self.start_date <= date <= self.end_date

    def overlaps(self, other: "DateRange") -> bool:
        """Check if date ranges overlap"""
        return self.start_date <= other.end_date and self.end_date >= other.start_date


@dataclass(frozen=True)
class Percentage(ImmutableValueObject):
    """Percentage value object"""

    value: float

    def validate(self) -> ValidationResult:
        """Validate percentage constraints"""
        result = ValidationResult(is_valid=True)

        if not 0 <= self.value <= 100:
            result.add_error("Percentage must be between 0 and 100")

        return result

    def as_decimal(self) -> float:
        """Convert percentage to decimal (0.0 to 1.0)"""
        return self.value / 100.0

    def of(self, amount: float) -> float:
        """Calculate percentage of an amount"""
        return amount * self.as_decimal()
