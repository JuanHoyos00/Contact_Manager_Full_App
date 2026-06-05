from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from src.api.dependencies import get_contact_service
from src.api.schemas import ContactCreate, ContactResponse
from src.models.contact import Contact
from src.services import ContactService

router = APIRouter(prefix="/contacts", tags=["Contacts"])

class UpdatePhonePayload(BaseModel):
    id: str = Field(..., description="The unique identity id of the person")
    new_number: str = Field(..., description="The new phone number string")


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(payload: ContactCreate, service: ContactService = Depends(get_contact_service)) -> ContactResponse:
    """Creates a new contact with personal information, country code, and phone number.

    Args:
        payload (ContactCreate): The data container with person details and phone info.
        service (ContactService): The business logic service dependency.

    Returns:
        ContactResponse: The structured representations of the created contact.

    Raises:
        HTTPException: If an error occurs during the persistent creation process.
    """
    try:
        contact: Contact = service.add_contact(
            id=payload.id, name=payload.name, last_name=payload.last_name,
            country_name=payload.country_name, country_code=payload.country_code, number_=payload.number_
        )
        return ContactResponse(
            id=contact.person.id,
            full_name=f"{contact.person.name} {contact.person.last_name}",
            country=contact.country.name,
            phone_number=contact.number.number
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ContactResponse])
def get_all_contacts(service: ContactService = Depends(get_contact_service)) -> List[ContactResponse]:
    """Retrieves all registered contacts from the persistent storage.

    Args:
        service (ContactService): The business logic service dependency.

    Returns:
        List[ContactResponse]: A list containing all contact entities transformed into payloads.
    """
    try:
        contact_list: List[Contact] = service.get_all_contacts()
        return [
            ContactResponse(
                id=c.person.id,
                full_name=f"{c.person.name} {c.person.last_name}",
                country=c.country.name,
                phone_number=c.number.number
            ) for c in contact_list
        ]
    except Exception:
        return []


@router.get("/{id}", response_model=ContactResponse)
def get_contact_by_id(id: str, service: ContactService = Depends(get_contact_service)) -> ContactResponse:
    """Fetches a specific contact record using their unique identity identification.

    Args:
        id (str): The identification string of the person.
        service (ContactService): The business logic service dependency.

    Returns:
        ContactResponse: The matched contact record info.

    Raises:
        HTTPException: If no record matches the provided identity identification.
    """
    try:
        contact: Contact = service.get_contact_by_id(id)
        return ContactResponse(
            id=contact.person.id,
            full_name=f"{contact.person.name} {contact.person.last_name}",
            country=contact.country.name,
            phone_number=contact.number.number
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/number/{number}", response_model=ContactResponse)
def get_contact_by_number(number: str, service: ContactService = Depends(get_contact_service)) -> ContactResponse:
    """Finds a single contact record filtering exactly by their phone number.

    Args:
        number (str): The unique string phone number to look up.
        service (ContactService): The business logic service dependency.

    Returns:
        ContactResponse: The contact information matching the exact number.

    Raises:
        HTTPException: If the specific phone number does not exist in storage.
    """
    try:
        contact: Contact = service.get_contact_by_number(number)
        return ContactResponse(
            id=contact.person.id,
            full_name=f"{contact.person.name} {contact.person.last_name}",
            country=contact.country.name,
            phone_number=contact.number.number
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/update-number", response_model=ContactResponse)
def update_contact_number(
    payload: UpdatePhonePayload, 
    service: ContactService = Depends(get_contact_service)
    ) -> ContactResponse:
    
    """Updates the phone number string associated with a specific person ID.

    Args:
        payload (UpdatePhonePayload): Target identity id and the new number value.
        service (ContactService): The business logic service dependency.

    Returns:
        ContactResponse: The contact representation containing the updated phone information.

    Raises:
        HTTPException: If the modification constraint fails or the identity id is invalid.
    """
    try:
        contact: Contact = service.update_contact_number_by_id(id=payload.id, new_number=payload.new_number)
        return ContactResponse(
            id=contact.person.id,
            full_name=f"{contact.person.name} {contact.person.last_name}",
            country=contact.country.name,
            phone_number=contact.number.number
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact_by_id(id: str, service: ContactService = Depends(get_contact_service)) -> None:
    """Removes a contact association and personal record filtering by identity identification.

    Args:
        id (str): The identification string of the target person to delete.
        service (ContactService): The business logic service dependency.

    Raises:
        HTTPException: If the target identification does not exist.
    """
    try:
        service.delete_contact_by_id(id)
        return
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/number/{number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact_by_number(number: str, service: ContactService = Depends(get_contact_service)) -> None:
    """Removes a contact entity looking up directly by its phone number value.

    Args:
        number (str): The phone number value belonging to the record to remove.
        service (ContactService): The business logic service dependency.

    Raises:
        HTTPException: If the target phone number record cannot be located.
    """
    try:
        service.delete_contact_by_number(number)
        return
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))