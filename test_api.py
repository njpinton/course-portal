import pytest
import os
import tempfile
from unittest.mock import MagicMock, patch, mock_open
from io import BytesIO

# Set required environment variables before importing the app
os.environ['FLASK_SECRET_KEY'] = 'test_secret_key_for_testing_only'
os.environ['SUPABASE_URL'] = 'https://test.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'test_anon_key'
os.environ['VERCEL_ENV'] = 'development'  # Ensure we're in dev mode

from api.index import app, allowed_file, validate_input


@pytest.fixture
def client():
    """Create Flask test client with testing config."""
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def mock_supabase(monkeypatch):
    """Mock Supabase client."""
    mock_client = MagicMock()

    # Mock table operations
    mock_table = MagicMock()
    mock_client.table.return_value = mock_table

    # Mock insert chain
    mock_insert = MagicMock()
    mock_table.insert.return_value = mock_insert
    mock_insert.execute.return_value = MagicMock(
        data=[{"id": "test-group-id", "group_name": "Test Group", "project_title": "Test Project"}]
    )

    # Mock select chain
    mock_select = MagicMock()
    mock_table.select.return_value = mock_select
    mock_select.execute.return_value = MagicMock(data=[])
    mock_select.eq.return_value = mock_select

    # Mock RPC calls
    mock_client.rpc.return_value = MagicMock()
    mock_client.rpc.return_value.execute.return_value = MagicMock()

    monkeypatch.setattr('api.index.get_supabase_client', return_value=mock_client)
    return mock_client


def test_allowed_file():
    """Test file type validation."""
    assert allowed_file('document.pdf', 'application/pdf') is True
    assert allowed_file('document.txt', 'text/plain') is True
    assert allowed_file('spreadsheet.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') is True
    assert allowed_file('script.exe', 'application/octet-stream') is False
    assert allowed_file('image.png', 'image/png') is False
    assert allowed_file('noextension', None) is False


def test_validate_input():
    """Test input validation."""
    # Valid input
    is_valid, msg = validate_input("Valid Input", 255, "test_field")
    assert is_valid is True
    assert msg == ""

    # Empty input
    is_valid, msg = validate_input("", 255, "test_field")
    assert is_valid is False

    # Too long
    is_valid, msg = validate_input("x" * 300, 255, "test_field")
    assert is_valid is False

    # Null bytes
    is_valid, msg = validate_input("test\x00null", 255, "test_field")
    assert is_valid is False


def test_create_group_api_valid(client, mock_supabase):
    """Test creating a group with valid data."""
    response = client.post(
        '/api/groups',
        json={
            "group_name": "Test Group",
            "project_title": "Test Project",
            "members": ["Alice", "Bob"]
        }
    )
    assert response.status_code == 201


def test_create_group_api_missing_group_name(client, mock_supabase):
    """Test creating a group without group_name."""
    response = client.post(
        '/api/groups',
        json={
            "project_title": "Test Project"
        }
    )
    assert response.status_code == 400
    assert "group_name" in response.get_json()['error'].lower() or "empty" in response.get_json()['error'].lower()


def test_create_group_api_empty_json(client, mock_supabase):
    """Test creating a group with empty JSON body."""
    response = client.post(
        '/api/groups',
        json={}
    )
    assert response.status_code == 400


def test_create_group_api_invalid_members_type(client, mock_supabase):
    """Test creating a group with invalid members type."""
    response = client.post(
        '/api/groups',
        json={
            "group_name": "Test Group",
            "members": "not a list"
        }
    )
    assert response.status_code == 400
    assert "members must be a list" in response.get_json()['error']


def test_create_group_api_too_many_members(client, mock_supabase):
    """Test creating a group with too many members."""
    response = client.post(
        '/api/groups',
        json={
            "group_name": "Test Group",
            "members": [f"Member{i}" for i in range(60)]
        }
    )
    assert response.status_code == 400
    assert "too many members" in response.get_json()['error'].lower()


def test_get_groups_api(client, mock_supabase):
    """Test getting all groups."""
    mock_supabase.table.return_value.select.return_value.execute.return_value = MagicMock(
        data=[{"id": "group1", "group_name": "Group 1"}]
    )
    response = client.get('/api/groups')
    assert response.status_code == 200


def test_upload_document_no_file(client, mock_supabase):
    """Test document upload without file."""
    response = client.post(
        '/api/groups/group1/documents',
        data={'document_title': 'Test Doc'}
    )
    assert response.status_code == 400
    assert "file part" in response.get_json()['error'].lower()


def test_upload_document_invalid_file_type(client, mock_supabase):
    """Test document upload with invalid file type."""
    data = {
        'document_title': 'Test Doc',
        'file': (BytesIO(b'fake content'), 'script.exe')
    }
    response = client.post(
        '/api/groups/group1/documents',
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    assert "not allowed" in response.get_json()['error'].lower()


def test_upload_document_valid(client, mock_supabase):
    """Test valid document upload."""
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock(
        data=[{"id": "doc1", "group_id": "group1", "document_title": "Test Doc"}]
    )

    data = {
        'document_title': 'Test Doc',
        'file': (BytesIO(b'PDF content'), 'document.pdf')
    }

    with patch('api.index.allowed_file', return_value=True):
        response = client.post(
            '/api/groups/group1/documents',
            data=data,
            content_type='multipart/form-data'
        )
    assert response.status_code == 201


def test_admin_login_empty_credentials(client, mock_supabase):
    """Test login with empty credentials."""
    response = client.post(
        '/admin_login',
        data={'username': '', 'password': ''}
    )
    assert response.status_code == 200  # Returns form again
    # Check if error is in response
    assert b'required' in response.data.lower() or b'error' in response.data.lower()


def test_admin_login_missing_config(client, mock_supabase, monkeypatch):
    """Test login when admin config is missing."""
    monkeypatch.delenv('ADMIN_USERNAME', raising=False)
    monkeypatch.delenv('ADMIN_PASSWORD_HASH', raising=False)

    response = client.post(
        '/admin_login',
        data={'username': 'admin', 'password': 'password'}
    )
    assert response.status_code == 200
    # Should show misconfiguration error
