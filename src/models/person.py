from dataclasses import dataclass

from src.exceptions import InvalidIdError


@dataclass
class Person:
    """
    Represents a person with identification and personal information.

    This class stores the basic data of a person and validates
    the provided identification number upon instantiation.

    Attributes:
        _id (str): The unique identification number of the person.
        _name (str): The first name of the person.
        _last_name (str): The last name of the person.
    """

    _id: str
    _name: str
    _last_name: str

    def __post_init__(self) -> None:
        """
        Performs validation after the dataclass is initialized.

        This method ensures that the provided ID contains only numeric
        characters according to the application's validation rules.
        """
        self._validate_id(self._id)

    @property
    def id(self) -> str:
        """
        Gets the person's identification number.

        Returns:
            str: The person's ID.
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Gets the person's first name.

        Returns:
            str: The person's first name.
        """
        return self._name

    @property
    def last_name(self) -> str:
        """
        Gets the person's last name.

        Returns:
            str: The person's last name.
        """
        return self._last_name

    def _validate_id(self, id: str) -> bool:
        """
        Validates that the provided ID contains only numeric characters.

        Args:
            id (str): The identification number to validate.

        Returns:
            bool: True if the ID is valid.

        Raises:
            InvalidIdError: If the ID contains non-numeric characters.
        """
        if not id.isdigit():
            raise InvalidIdError(id)

        return True
        