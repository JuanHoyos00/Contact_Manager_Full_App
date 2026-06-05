import json
from pathlib import Path
from typing import List

from src.models.contact import Contact
from src.models.country import Country
from src.models.number import Number
from src.models.person import Person
from src.storage.base import Storage


class JSONStorage(Storage):
    """
    A concrete storage implementation that saves contacts to a JSON file.

    This class implements the Storage protocol, handling the serialization
    and deserialization of Contact objects to and from a specified JSON file.

    Attributes:
        filepath (Path): The path to the JSON file where contacts are stored.
    """

    def __init__(self, filepath: Path) -> None:
        """
        Initializes the JSONStorage with a specific file path.

        Args:
            filepath (Path): The path object pointing to the JSON file.
        """
        self.filepath = filepath

    def load(self) -> List[Contact]:
        """
        Loads contacts from the JSON file specified during initialization.

        If the file does not exist, it returns an empty list. Otherwise, it
        reads the file, deserializes the JSON data, and reconstructs a list
        of Contact objects by hydrating their internal sub-entities.

        Returns:
            List[Contact]: A list of hydrated Contact objects.
        """
        if not self.filepath.exists():
            return []

        with open(self.filepath, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []

        hydrated_contacts: List[Contact] = []
        for item in data:
            # Reconstruimos los sub-modelos internos a partir del diccionario plano
            person = Person(_id=item["id"], _name=item["name"], _last_name=item["last_name"])
            country = Country(_name=item["country_name"], _code=int(item["country_code"]))
            number = Number(_number=item["number_"])
            
            # Ensamblamos el objeto Contact principal
            contact = Contact(_person=person, _country=country, _number=number)
            hydrated_contacts.append(contact)

        return hydrated_contacts

    def save(self, contact_list: List[Contact]) -> None:
        """
        Saves a list of contacts to the JSON file.

        This method serializes each Contact object in the list into a dictionary
        and writes the entire list to the JSON file with human-readable indentation.

        Args:
            contact_list (List[Contact]): The list of Contact objects to save.
        """
        with open(self.filepath, "w") as f:
            serializable_list = [contact.to_dict() for contact in contact_list]
            json.dump(serializable_list, f, indent=4)