from typing import Any, Dict, List

from supabase import Client, create_client

from src.api.config import settings
from src.models.contact import Contact
from src.models.country import Country
from src.models.number import Number
from src.models.person import Person
from src.storage.base import Storage


class SupabaseStorage(Storage):
    """Concrete implementation of the storage protocol utilizing Supabase as the database backend."""

    def __init__(self) -> None:
        """Initializes the Supabase client connection using environment configurations."""
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key)

    def load(self) -> List[Contact]:
        """Loads and hydrats all contacts from the database via a remote procedure call.

        Returns:
            List[Contact]: A collection of fully hydrated domain contact models.
        """
        response: Any = self.client.rpc("get_hydrated_contacts", {}).execute()
        hydrated_contacts: List[Contact] = []
        
        if not response.data:
            return hydrated_contacts

        for record in response.data:
            person_data: Dict[str, Any] = record["people"]
            country_data: Dict[str, Any] = record["countries"]

            person: Person = Person(
                _id=person_data["id"], 
                _name=person_data["first_name"], 
                _last_name=person_data["last_name"]
            )
            country: Country = Country(
                _name=country_data["id"],  
                _code=int(country_data["dial_code"])
            )
            number: Number = Number(_number=record["phone_number"])

            contact: Contact = Contact(_person=person, _country=country, _number=number)
            hydrated_contacts.append(contact)

        return hydrated_contacts

    def save(self, contact_list: List[Contact]) -> None:
        """Synchronizes and inserts a new contact sequence into the remote database.

        Args:
            contact_list (List[Contact]): The collection of domain contacts to process.

        Returns:
            None
        """
        if not contact_list:
            return

        target: Contact = contact_list[-1]

        self.client.table("people").upsert({
            "id": target.person.id,
            "first_name": target.person.name,
            "last_name": target.person.last_name
        }).execute()

        country_id: str = str(getattr(target.country, "name", getattr(target.country, "_name", "COL")))
        country_code: str = str(getattr(target.country, "code", getattr(target.country, "_code", 57)))

        self.client.table("countries").upsert({
            "id": country_id,
            "dial_code": country_code,
            "full_name": country_id
        }).execute()

        phone_val: Any = getattr(target.number, "number", getattr(target.number, "_number", ""))
        if hasattr(phone_val, "number"): 
            phone_val = phone_val.number

        self.client.table("contacts").insert({
            "person_id": target.person.id,
            "country_id": country_id,
            "phone_number": str(phone_val)
        }).execute()

    def delete_by_id(self, person_id: str) -> None:
        """Removes a contact record clearing relational constraints sequentially.

        Args:
            person_id (str): The identification string matching the target record.

        Returns:
            None
        """
        self.client.table("contacts").delete().eq("person_id", person_id).execute()
        self.client.table("people").delete().eq("id", person_id).execute()

    def update_phone_by_id(self, person_id: str, new_phone: str) -> None:
        """Updates the phone number column data directly for a given target person ID.

        Args:
            person_id (str): The unique identification string of the person.
            new_phone (str): The newly structured phone number payload.

        Returns:
            None
        """
        self.client.table("contacts").update({
            "phone_number": new_phone
        }).eq("person_id", person_id).execute()