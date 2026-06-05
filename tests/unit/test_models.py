import pytest
from src.models.person import Person
from src.models.number import Number
from src.models.country import Country
from src.models.contact import Contact
from src.exceptions import (
    InvalidIdError,
    InvalidNumberDataError,
    InvalidCountryError,
    InvalidCountryCodeError,
    NotConsistencyCodeCountryError,
)


def test_person_creation_valid() -> None:
    """
    Test that a Person entity is created successfully with valid numeric ID.
    """
    person: Person = Person(_id="12345678", _name="Juan", _last_name="Hoyos")
    assert person.id == "12345678"
    assert person.name == "Juan"
    assert person.last_name == "Hoyos"


def test_person_creation_invalid_id_raises_error() -> None:
    """
    Raises an error when the person ID contains non-numeric characters.
    """
    with pytest.raises(InvalidIdError):
        Person(_id="12345A78", _name="Juan", _last_name="Hoyos")


def test_number_creation_valid() -> None:
    """
    Test that a Number entity is created successfully with digits only.
    """
    phone: Number = Number(_number="3001234567")
    assert phone.number == "3001234567"


def test_number_creation_invalid_digits_raises_error() -> None:
    """
    Raises an error when the phone number contains non-numeric characters.
    """
    with pytest.raises(InvalidNumberDataError):
        Number(_number="3001234e67")


def test_country_creation_valid() -> None:
    """
    Test that a Country entity is created successfully with matching code and name.
    """
    country: Country = Country(_name="COL", _code=57)
    assert country.name == "COL"
    assert country.code == 57


def test_country_creation_invalid_name_raises_error() -> None:
    """
    Raises an error when the country abbreviation is not supported.
    """
    with pytest.raises(InvalidCountryError):
        Country(_name="MED", _code=57)


def test_country_creation_invalid_code_raises_error() -> None:
    """
    Raises an error when the international dialing code is not supported.
    """
    with pytest.raises(InvalidCountryCodeError):
        Country(_name="COL", _code=999)


def test_country_inconsistency_raises_error() -> None:
    """
    Raises an error when the country abbreviation does not match the dialing code.
    """
    with pytest.raises(NotConsistencyCodeCountryError):
        Country(_name="COL", _code=1)


def test_contact_creation_valid() -> None:
    """
    Test that a Contact aggregates all valid sub-entities successfully.
    """
    person: Person = Person(_id="123456", _name="Juan", _last_name="Hoyos")
    country: Country = Country(_name="COL", _code=57)
    phone: Number = Number(_number="3001234567")

    contact: Contact = Contact(_person=person, _country=country, _number=phone)
    assert contact.person == person
    assert contact.country == country
    assert contact.number == phone


def test_contact_string_representation() -> None:
    """
    Test that the __repr__ method formats the contact information correctly.
    """
    person: Person = Person(_id="98765", _name="Juan Carlos", _last_name="Hoyos Perez")
    country: Country = Country(_name="EEUU", _code=1)
    phone: Number = Number(_number="5551234")

    contact: Contact = Contact(_person=person, _country=country, _number=phone)
    expected_output: str = "ID: 98765 \nName: Juan Hoyos. \nNumber: +1 5551234"
    assert repr(contact) == expected_output