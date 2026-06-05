from typing import List, Union

from src.exceptions import ContactAlreadyExistError, ContactNotFoundError
from src.models.contact import Contact
from src.models.country import Country
from src.models.number import Number
from src.models.person import Person
from src.storage.base import Storage


class ContactService:
    """Business logic orchestration layer handling management routines for database domain contacts."""

    def __init__(self, storage: Storage) -> None:
        """Initializes the service engine injecting a compliant persistent storage strategy.

        Args:
            storage (Storage): An instance conforming to the abstract Storage Protocol interface.
        """
        self.storage: Storage = storage

    def add_contact(
        self, id: str, name: str, last_name: str, 
        country_name: str, country_code: int, number_: str
    ) -> Contact:
        """Creates, validates uniqueness constraints, and saves a fresh contact entity record.

        Args:
            id (str): Unique identification string of the target person.
            name (str): First name string value.
            last_name (str): Family surname string value.
            country_name (str): Region identification flag value or string name.
            country_code (int): Regional international calling dial code prefix integer.
            number_ (str): Target phone number data string.

        Returns:
            Contact: The newly assembled and validated domain contact entity instance.

        Raises:
            ContactAlreadyExistError: If identity id or phone number overlaps with active records.
        """
        person: Person = Person(id, name, last_name)
        country: Country = Country(country_name, country_code)
        number: Number = Number(number_)
        new_contact: Contact = Contact(person, country, number)

        contact_list: List[Contact] = self.storage.load()
        self._validate_contact_is_unique(contact_list, new_contact.number.number, new_contact.person.id)
        
        contact_list.append(new_contact)
        self.storage.save(contact_list)
        return new_contact

    def delete_contact_by_id(self, id: str) -> None:
        """Removes a target contact record from persistence using its identifier code key.

        Args:
            id (str): The unique identity representation of the person to clear out.

        Returns:
            None

        Raises:
            ContactNotFoundError: If no entry matches the specified identification criteria.
        """
        contact_list: List[Contact] = self.storage.load()
        self._validate_contact_exists(contact_list, number=False, id=id)
        self.storage.delete_by_id(id)

    def delete_contact_by_number(self, number: str) -> None:
        """Locates and clear a contact entry from persistence targeting its unique phone sequence.

        Args:
            number (str): The target phone number sequence string to filter and wipe out.

        Returns:
            None

        Raises:
            ContactNotFoundError: If the requested number sequence is missing from the data records.
        """
        contact_list: List[Contact] = self.storage.load()
        contact: Union[Contact, None] = next((c for c in contact_list if c.number.number == number), None)
        if not contact:
            raise ContactNotFoundError(number, False)
        
        self.storage.delete_by_id(contact.person.id)

    def get_contact_by_id(self, id: str) -> Contact:
        """Queries and fetches a matching contact filtering exactly by identification keys.

        Args:
            id (str): The identification token string to search for.

        Returns:
            Contact: The structural representation of the matching contact model.

        Raises:
            ContactNotFoundError: If the identity value cannot be located.
        """
        contact_list: List[Contact] = self.storage.load()
        self._validate_contact_exists(contact_list, number=False, id=id)
        return next(contact for contact in contact_list if contact.person.id == id)

    def get_contact_by_number(self, number: str) -> Contact:
        """Queries and fetches a matching contact filtering exactly by its phone sequence value.

        Args:
            number (str): The unique target phone number string data to search for.

        Returns:
            Contact: The structural representation of the matching contact model.

        Raises:
            ContactNotFoundError: If the phone sequence does not map into an existing profile.
        """
        contact_list: List[Contact] = self.storage.load()
        self._validate_contact_exists(contact_list, number=number, id=False)
        return next(contact for contact in contact_list if contact.number.number == number)

    def get_all_contacts(self) -> List[Contact]:
        """Queries and unrolls all structural profile entities available inside storage.

        Returns:
            List[Contact]: A sequence collection containing every active domain model record.
        """
        return self.storage.load()
    
    def update_contact_number_by_id(self, id: str, new_number: str) -> Contact:
        """Safely mutates the telephone attribute mapping associated with a target client id.

        Args:
            id (str): The unique identification code of the person profile to update.
            new_number (str): The freshly proposed sequence data string to allocate.

        Returns:
            Contact: The newly mutated domain profile containing structural data updates.

        Raises:
            ContactNotFoundError: If the target identification context cannot be tracked.
            ContactAlreadyExistError: If the proposed number value collides with another user.
        """
        contact_list: List[Contact] = self.storage.load()
        self._validate_contact_exists(contact_list, number=False, id=id)

        # Cambiamos el bucle 'for' por una expresión generadora plana con any()
        if any(c.number.number == new_number and c.person.id != id for c in contact_list):
            raise ContactAlreadyExistError(new_number, False)

        self.storage.update_phone_by_id(id, new_number)
        
        updated_list: List[Contact] = self.storage.load()
        return next(c for c in updated_list if c.person.id == id)

    def _validate_contact_is_unique(self, contact_list: List[Contact], number: str, id: str) -> None:
        """Internal routine validating structural invariants to block overlapping entries."""
        for contact in contact_list:
            if contact.number.number == number:
                raise ContactAlreadyExistError(number, False)
            if contact.person.id == id:
                raise ContactAlreadyExistError(False, id)

    def _exists_by_number(self, contact_list: List[Contact], number: str) -> bool:
        """Helper to verify cellular network sequence existence constraints."""
        return any(contact.number.number == number for contact in contact_list)

    def _exists_by_id(self, contact_list: List[Contact], id_str: str) -> bool:
        """Helper to verify primary identification key matching constraints."""
        return any(contact.person.id == id_str for contact in contact_list)
    
    def _validate_contact_exists(
        self, contact_list: List[Contact], number: Union[str, bool], id: Union[str, bool]
    ) -> None:
        """Internal constraint routine ensuring query execution bounds resolve successfully."""
        if number and not self._exists_by_number(contact_list, str(number)):
            raise ContactNotFoundError(str(number), False)
        if not number and not self._exists_by_id(contact_list, str(id)):
            raise ContactNotFoundError(False, str(id))