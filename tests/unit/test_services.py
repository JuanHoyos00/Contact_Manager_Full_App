from unittest.mock import MagicMock
import pytest
from src.services import ContactService
from src.models.contact import Contact
from src.models.person import Person
from src.models.country import Country
from src.models.number import Number
from src.exceptions import (
    ContactAlreadyExistError,
    ContactNotFoundError,
    ContactListIsEmptyError
)


def test_add_contact_successfully() -> None:
    """
    Test whether a contact can be added successfully.
    """
    mock_storage: MagicMock = MagicMock()
    mock_storage.load.return_value = []
    service: ContactService = ContactService(mock_storage)
    
    result: Contact = service.add_contact(
        id="12345", 
        name="Juan", 
        last_name="Hoyos", 
        country_name="COL", 
        country_code=57, 
        number_="123456789"
    )
    
    assert result.person.id == "12345"
    mock_storage.save.assert_called_once()


def test_contact_already_exist_error() -> None:
    """
    Raises an error when trying to add a contact that already exists.
    """
    mock_storage: MagicMock = MagicMock()
    existing_contact: Contact = Contact(Person("12345", "Juan", "Hoyos"), Country("COL", 57), Number("123456789"))
    mock_storage.load.return_value = [existing_contact]
    service: ContactService = ContactService(mock_storage)
    
    with pytest.raises(ContactAlreadyExistError):
        service.add_contact(
            id="12345", 
            name="Juan", 
            last_name="Hoyos", 
            country_name="COL", 
            country_code=57, 
            number_="123456789"
        )


def test_delete_contact_successfully() -> None:
    """Test whether a contact can be deleted successfully."""
    mock_storage: MagicMock = MagicMock()
    existing_contact: Contact = Contact(
        Person("12345", "Juan", "Hoyos"), 
        Country("COL", 57), 
        Number("123456789")
    )
    mock_storage.load.return_value = [existing_contact]
    service: ContactService = ContactService(mock_storage)
    
    service.delete_contact_by_number("123456789")
    
    mock_storage.delete_by_id.assert_called_once_with("12345")


def test_get_contact_by_number() -> None:
    """
    Tests successful retrieval of a contact by number.
    """
    mock_storage: MagicMock = MagicMock()
    contact: Contact = Contact(Person("12345", "Juan", "Hoyos"), Country("COL", 57), Number("123456789"))
    mock_storage.load.return_value = [contact]
    service: ContactService = ContactService(mock_storage)
    
    assert service.get_contact_by_number("123456789") == contact


def test_contact_not_found_error() -> None:
    """
    Raises an error if the contact does not exist.
    """
    mock_storage: MagicMock = MagicMock()
    mock_storage.load.return_value = []
    service: ContactService = ContactService(mock_storage)
    
    with pytest.raises(ContactNotFoundError):
        service.delete_contact_by_number("123456789")


def test_get_all_contacts_successfully() -> None:
    """
    Test that get_all_contacts runs successfully and returns the list.
    """
    mock_storage: MagicMock = MagicMock()
    contact: Contact = Contact(Person("12345", "Juan", "Hoyos"), Country("COL", 57), Number("123456789"))
    mock_storage.load.return_value = [contact]
    service: ContactService = ContactService(mock_storage)
    
    result = service.get_all_contacts()
    assert len(result) == 1


def test_contact_list_empty() -> None:
    """Raises a ContactNotFoundError if attempting to query an empty contact storage."""
    mock_storage: MagicMock = MagicMock()
    mock_storage.load.return_value = []
    service: ContactService = ContactService(mock_storage)

    # CORRECCIÓN: El servicio lanza ContactNotFoundError si buscas un ID que no existe
    with pytest.raises(ContactNotFoundError):
        service.get_contact_by_id("12345")