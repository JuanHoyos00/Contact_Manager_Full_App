from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    """
    Shared attributes for contact operations.
    """
    country_name: str = Field(..., max_length=10, description="Abbreviation of the country (e.g., COL, EEUU)")
    country_code: int = Field(..., description="International dialing code (e.g., 57, 1)")
    number_: str = Field(..., description="The digits of the phone number")


class ContactCreate(ContactBase):
    """
    Schema for validating incoming data when creating or updating a contact.
    """
    id: str = Field(..., description="The unique numeric identifier of the person")
    name: str = Field(..., description="First name of the person")
    last_name: str = Field(..., description="Last name of the person")


class ContactResponse(BaseModel):
    """
    Schema for shaping outgoing HTTP responses. 
    Ensures decoupled delivery formatting from internal models.
    """
    id: str
    full_name: str
    country: str
    phone_number: str

    class Config:
        from_attributes = True



class ContactUpdateNumber(BaseModel):
    """
    Schema for updating a contact's phone number using their first name.
    """
    name: str = Field(..., description="The first name of the contact to update")
    new_number: str = Field(..., description="The new phone number value containing only digits")