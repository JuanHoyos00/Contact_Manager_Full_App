from typing import List, Protocol

from src.models.contact import Contact


class Storage(Protocol):
    """Structural protocol defining persistent storage interface operations for contacts.

    Any concrete storage class implementation must conform to these boundaries
    to satisfy dependency inversion layers.
    """

    def load(self) -> List[Contact]:
        """Loads and retrieves all existing contact entities from the backend engine.

        Returns:
            List[Contact]: A sequence collection containing loaded domain contacts.
        """
        ...

    def save(self, contact_list: List[Contact]) -> None:
        """Synchronizes and saves contact state changes into the remote data warehouse.

        Args:
            contact_list (List[Contact]): The sequence collection of contact models.

        Returns:
            None
        """
        ...

    def delete_by_id(self, person_id: str) -> None:
        """Performs atomic cascading deletion of a single contact using their unique ID.

        Args:
            person_id (str): The identification string representing the target person.

        Returns:
            None
        """
        ...

    def update_phone_by_id(self, person_id: str, new_phone: str) -> None:
        """Updates the phone number string value associated to a target person identity.

        Args:
            person_id (str): The identification string representing the target person.
            new_phone (str): The newly formatted phone string data to assign.

        Returns:
            None
        """
        ...