from dataclasses import dataclass

from src.exceptions import (
    InvalidCountryCodeError,
    InvalidCountryError,
    NotConsistencyCodeCountryError,
)

countries: dict[str, int] = {
    "EEUU": 1,    # United States
    "CAN": 1,     # Canada
    "COL": 57,    # Colombia
    "CHI": 86,    # China
    "JAP": 81,    # Japan
    "ALE": 49,    # Germany
    "RUI": 44,    # United Kingdom
    "FRA": 33,    # France
    "IND": 91,    # India
    "ITA": 39,    # Italy
    "BRA": 55,    # Brazil
    "RUS": 7,     # Russia
    "COR": 82,    # South Korea
    "AUS": 61,    # Australia
    "ESP": 34,    # Spain
    "MEX": 52,    # Mexico
    "PBA": 31,    # Netherlands
    "SUI": 41,    # Switzerland
    "TUR": 90,    # Turkey
    "ARA": 966,   # Saudi Arabia
    "SIN": 65     # Singapore
}


@dataclass
class Country:
    """
    Represents a country entity associated with an international phone code.

    This class validates both the country abbreviation and its corresponding
    international dialing code, ensuring consistency between them.

    Attributes:
        _name (str): The abbreviated name of the country.
        _code (str): The international dialing code associated with the country.
    """

    _name: str
    _code: int

    def __post_init__(self) -> None:
        """
        Performs validation after the dataclass is initialized.

        This method validates the country name, the country code,
        and the consistency between both values.
        """
        self._validate_country_name(self._name)
        self._validate_country_code(self._code)
        self._check_consistency_between_code_and_name(
            self._name,
            self._code
        )

    @property
    def name(self) -> str:
        """
        Gets the country's abbreviated name.

        Returns:
            str: The country abbreviation.
        """
        return self._name

    @property
    def code(self) -> str:
        """
        Gets the country's international dialing code.

        Returns:
            str: The international dialing code.
        """
        return self._code

    def _validate_country_name(self, name: str) -> bool:
        """
        Validates that the provided country name exists
        in the supported countries dictionary.

        Args:
            name (str): The country abbreviation to validate.

        Returns:
            bool: True if the country name is valid.

        Raises:
            InvalidCountryError: If the country abbreviation
                                 is not supported.
        """
        if name not in countries:
            raise InvalidCountryError(name)

        return True

    def _validate_country_code(self, code: str) -> bool:
        """
        Validates that the provided country code exists
        in the supported dialing codes.

        Args:
            code (str): The dialing code to validate.

        Returns:
            bool: True if the country code is valid.

        Raises:
            InvalidCountryCodeError: If the dialing code
                                     is not supported.
        """
        if code not in countries.values():
            raise InvalidCountryCodeError(code)

        return True

    def _check_consistency_between_code_and_name(
        self,
        name: str,
        code: str
    ) -> bool:
        """
        Validates the consistency between the country name
        and its corresponding dialing code.

        Args:
            name (str): The country abbreviation.
            code (str): The international dialing code.

        Returns:
            bool: True if the country and code are consistent.

        Raises:
            NotConsistencyCodeCountryError: If the country
                                            does not match the provided code.
        """
        if countries[name] != code:
            raise NotConsistencyCodeCountryError(code, name)

        return True