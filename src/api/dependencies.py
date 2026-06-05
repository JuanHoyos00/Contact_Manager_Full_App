from src.services import ContactService
from src.storage.supabase_storage import SupabaseStorage


def get_storage() -> SupabaseStorage:
    """
    Provides a singleton-like instance of the Supabase storage client.
    """
    return SupabaseStorage()

def get_contact_service() -> ContactService:
    """
    Provides a fully hydrated ContactService instance with its storage dependency.
    """
    storage: SupabaseStorage = get_storage()
    return ContactService(storage)