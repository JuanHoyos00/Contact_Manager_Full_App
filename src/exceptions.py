class AppError(Exception):
    """
    Base exception for all custom application errors.

    This class serves as the root exception for the application's
    custom exception hierarchy, allowing all domain-specific errors
    to be caught under a single parent exception.
    """

    pass


class ContactError(AppError):
    """
    Base exception for errors related to contact management.

    This exception acts as a parent class for all errors associated
    with contact operations, validation, and persistence.
    """

    pass


class InvalidCountryError(ContactError):
    """
    Raised when an unsupported or invalid country is provided.

    This exception is triggered when the specified country does not
    belong to the list of supported countries in the application.
    """

    def __init__(self, country: str) -> None:
        """
        Initializes the exception with the invalid country value.

        Args:
            country (str): The invalid country provided by the user.
        """
        super().__init__(f'The country {country} is invalid.')


class InvalidIdError(ContactError):
    """
    Raised when a contact ID contains invalid characters.

    This exception is triggered when the provided ID is not strictly
    numeric as required by the application rules.
    """

    def __init__(self, id: str) -> None:
        """
        Initializes the exception with the invalid ID value.

        Args:
            id (str): The invalid contact ID.
        """
        super().__init__(f'The ID {id} must contain only numbers.')


class InvalidCountryCodeError(ContactError):
    """
    Raised when an invalid country calling code is provided.

    This exception is triggered when the country code format or value
    does not match the supported international dialing codes.
    """

    def __init__(self, country_code: str) -> None:
        """
        Initializes the exception with the invalid country code.

        Args:
            country_code (str): The invalid country calling code.
        """
        super().__init__(f'The code {country_code} is invalid.')


class InvalidNumberDataError(ContactError):
    """
    Raised when a phone number contains invalid data.

    This exception is triggered when the phone number format,
    length, or content is invalid according to the application's
    validation rules.
    """

    def __init__(self, number: str) -> None:
        """
        Initializes the exception with the invalid phone number.

        Args:
            number (str): The invalid phone number.
        """
        super().__init__(f'The number {number} is invalid.')


class NotConsistencyCodeCountryError(ContactError):
    """
    Raised when a country code does not match its associated country.

    This exception ensures consistency between the international
    dialing code and the specified country.
    """

    def __init__(self, country_code: str, country: str) -> None:
        """
        Initializes the exception with the inconsistent country data.

        Args:
            country_code (str): The provided country calling code.
            country (str): The provided country abbreviation.
        """
        super().__init__(
            f'The code {country_code} does not match the country {country}.'
        )


class ContactAlreadyExistError(ContactError):
    """
    Raised when attempting to create a contact that already exists.

    A contact may already exist either by duplicated phone number
    or duplicated contact ID.
    """

    def __init__(
        self,
        number: str | bool,
        id: str | bool
    ) -> None:
        """
        Initializes the exception with the duplicated contact data.

        Args:
            number (str | bool): The duplicated phone number, if applicable.
            id (str | bool): The duplicated contact ID, if applicable.
        """
        if number:
            super().__init__(f'The number {number} already exists.')
        else:
            super().__init__(f'The person whit the id {id} already exists.')


class ContactNotFoundError(ContactError):
    """
    Raised when a requested contact cannot be found.

    This exception is triggered when searching for a contact
    by phone number or ID that does not exist in the system.
    """

    def __init__(
        self,
        number: str | bool,
        id: str | bool
    ) -> None:
        """
        Initializes the exception with the missing contact data.

        Args:
            number (str | bool): The missing phone number, if applicable.
            id (str | bool): The missing contact ID, if applicable.
        """
        if number:
            super().__init__(f'The number {number} does not exist.')
        else:
            super().__init__(f'The ID {id} does not exist.')


class ContactListIsEmptyError(ContactError):
    """
    Raised when attempting to access contacts from an empty contact list.

    This exception indicates that no contacts are currently stored
    in the application's contact repository.
    """

    def __init__(self) -> None:
        """
        Initializes the exception for an empty contact list.
        """
        super().__init__('There are no contacts in the contact list.')

class ContactNameNotFoundError(ContactError):
    """
    Raised when a requested contact cannot be found by their name.

    This exception is triggered when searching for a contact
    by their first name to perform an operation, but no match is found.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the exception with the missing contact name.

        Args:
            name (str): The name of the contact that was not found.
        """
        super().__init__(f'The contact with the name {name} does not exist.')