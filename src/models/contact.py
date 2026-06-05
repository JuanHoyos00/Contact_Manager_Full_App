from dataclasses import dataclass

from src.models.country import Country
from src.models.number import Number
from src.models.person import Person


@dataclass
class Contact:
    """
    Represents a complete contact entity.

    This class aggregates a person's information, country data,
    and phone number into a single contact object.

    Attributes:
        _person (Person): The personal information associated with the contact.
        _country (Country): The country and dialing code information.
        _number (Number): The phone number information.
    """

    _person: Person
    _country: Country
    _number: Number

    @property
    def person(self) -> Person:
        """
        Gets the contact's personal information.

        Returns:
            Person: The associated person entity.
        """
        return self._person

    @property
    def country(self) -> Country:
        """
        Gets the contact's country information.

        Returns:
            Country: The associated country entity.
        """
        return self._country

    @property
    def number(self) -> Number:
        """
        Gets the contact's phone number information.

        Returns:
            Number: The associated phone number entity.
        """
        return self._number
    
    @number.setter
    def number(self, new_number_obj):
        self._number = new_number_obj

        
    def to_dict(self) -> dict:
        """
        Serializes the contact object and its sub-entities into a flat dictionary.

        Returns:
            dict: A dictionary containing the contact's complete structured details.
        """
        return {
            "id": self._person.id,
            "name": self._person.name,
            "last_name": self._person.last_name,
            "country_name": self._country.name,
            "country_code": self._country.code,
            "number_": self._number.number
        }

    def __repr__(self) -> str:
        """
        Provides a human-readable string representation of the contact.

        The representation includes:
        - The person's ID.
        - A shortened version of the full name.
        - The complete international phone number.

        Returns:
            str: A formatted string representation of the contact.
        """
        number: str = f'+{self._country.code} {self._number.number}'
        name: str = ''

        for char in self._person.name:
            if char == ' ':
                name += char
                break

            name += char

        for char in self._person.last_name:
            if char == ' ':
                name += '.'
                break

            name += char

        return (
            f'ID: {self._person.id} '
            f'\nName: {name} '
            f'\nNumber: {number}'
        )