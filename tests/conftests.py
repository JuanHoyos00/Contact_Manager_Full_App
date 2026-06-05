"""Configuration file for pytest fixtures and structural system-wide mocks."""

import pytest
from unittest.mock import MagicMock, Mock
from typing import Generator
from src.services import ContactService


@pytest.fixture
def mock_supabase_client() -> Generator[MagicMock, None, None]:
    """Creates a comprehensive MagicMock instance mimicking the Supabase Client structural behavior.

    Yields:
        MagicMock: A simulated Supabase database interface client.
    """
    mock_client = MagicMock()
    
    # Simula la estructura encadenada de Supabase: client.table().upsert().execute()
    mock_client.table.return_value = mock_client
    mock_client.upsert.return_value = mock_client
    mock_client.insert.return_value = mock_client
    mock_client.delete.return_value = mock_client
    mock_client.update.return_value = mock_client
    mock_client.eq.return_value = mock_client
    
    # Simula llamadas a Procedimientos Almacenados: client.rpc().execute()
    mock_client.rpc.return_value = mock_client
    
    # Respuesta por defecto para .execute()
    mock_response = Mock()
    mock_response.data = []
    mock_client.execute.return_value = mock_response
    
    yield mock_client


@pytest.fixture
def mock_storage(mock_supabase_client: MagicMock) -> Generator[MagicMock, None, None]:
    """Creates a mock instance of the SupabaseStorage class.

    Args:
        mock_supabase_client (MagicMock): The mocked core third-party client connection.

    Yields:
        MagicMock: A mocked storage strategy instance conforming to the Storage Protocol.
    """
    from src.storage.supabase import SupabaseStorage
    
    storage_instance = SupabaseStorage()
    # Inyectamos el cliente simulado dentro de la propiedad del almacenamiento
    storage_instance.client = mock_supabase_client
    
    yield storage_instance


@pytest.fixture
def contact_service(mock_storage: MagicMock) -> ContactService:
    """Provides a functional ContactService instance pre-injected with the mocked storage layer.

    Args:
        mock_storage (MagicMock): The simulated persistence strategy.

    Returns:
        ContactService: The isolated service orchestrator ready for unit testing.
    """
    return ContactService(storage=mock_storage)