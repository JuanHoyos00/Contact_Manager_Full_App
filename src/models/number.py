from dataclasses import dataclass

from src.exceptions import InvalidNumberDataError


@dataclass
class Number:
    """
    Represents a phone number entity.

    This class stores and validates a phone number, ensuring
    that it contains only numeric characters according to
    the application's validation rules.

    Attributes:
        _number (str): The phone number value.
    """

    _number: str

    def __post_init__(self) -> None:
        """
        Performs validation after the dataclass is initialized.

        This method ensures that the provided phone number
        contains only numeric characters.
        """
        self._validate_number(self._number)

    @property
    def number(self) -> str:
        """
        Gets the phone number value.

        Returns:
            str: The validated phone number.
        """
        return self._number
    
    

    def _validate_number(self, number: str) -> bool:
        """
        Validates that the provided phone number contains only digits.

        Args:
            number (str): The phone number to validate.

        Returns:
            bool: True if the phone number is valid.

        Raises:
            InvalidNumberDataError: If the phone number contains
                                    non-numeric characters.
        """
        if not number.isdigit():
            raise InvalidNumberDataError(number)

        return True