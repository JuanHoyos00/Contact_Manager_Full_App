from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """System configuration settings loaded from environmental variables.

    Attributes:
        supabase_url (str): The absolute API URL endpoint provided by Supabase.
        supabase_key (str): The secret public or service role API key for authentication.
    """
    supabase_url: str
    supabase_key: str

    class Config:
        """Pydantic configuration parameters adjustment."""
        extra = "ignore"

settings: Settings = Settings()