"""
Pytest configuration and fixtures for Presenter App tests
"""
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()


@pytest.fixture
def app():
    """Create Flask app for testing"""
    # Mock supabase_client before importing index
    with patch('api.index.get_supabase_client') as mock_supabase:
        mock_client = MagicMock()
        mock_supabase.return_value = mock_client

        # Import after patching
        from api.index import app as flask_app

        flask_app.config['TESTING'] = True
        flask_app.config['SESSION_COOKIE_SECURE'] = False
        flask_app.config['SESSION_COOKIE_HTTPONLY'] = False
        flask_app.config['SESSION_COOKIE_SAMESITE'] = None

        yield flask_app


@pytest.fixture
def client(app):
    """Create Flask test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create Flask CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def mock_supabase():
    """Mock Supabase client"""
    with patch('supabase_client.supabase') as mock:
        yield mock


@pytest.fixture
def mock_supabase_in_api():
    """Mock Supabase client in api.supabase_client"""
    with patch('api.supabase_client.supabase') as mock:
        yield mock


@pytest.fixture
def sample_group_data():
    """Sample group data for testing"""
    return {
        'id': 'test-group-123',
        'name': 'Test Group',
        'class_id': 'class-456',
        'username': 'testgroup',
        'password_hash': 'hashed_password',
        'created_at': '2025-01-01T00:00:00',
        'updated_at': '2025-01-01T00:00:00',
        'last_login': None,
        'is_archived': False
    }


@pytest.fixture
def sample_student_data():
    """Sample student data for testing"""
    return {
        'id': 'student-123',
        'first_name': 'John',
        'last_name': 'Doe',
        'campus_id': 'UP001',
        'class_id': 'class-456',
        'group_id': None,
        'created_at': '2025-01-01T00:00:00',
        'updated_at': '2025-01-01T00:00:00'
    }


@pytest.fixture
def sample_stage_data():
    """Sample stage data for testing"""
    return {
        'id': 'stage-123',
        'group_id': 'test-group-123',
        'stage_name': 'Stage 1',
        'status': 'in_progress',
        'started_at': '2025-01-01T00:00:00',
        'completed_at': None
    }


@pytest.fixture
def sample_submission_data():
    """Sample submission data for testing"""
    return {
        'id': 'submission-123',
        'group_id': 'test-group-123',
        'stage_id': 'stage-123',
        'submission_date': '2025-01-15T10:00:00',
        'file_name': 'project.pdf',
        'file_size': 1024000,
        'file_path': 'submissions/test-group-123/stage-123/project.pdf',
        'status': 'submitted'
    }


@pytest.fixture
def auth_headers():
    """Sample JWT authentication headers"""
    return {
        'Authorization': 'Bearer test_jwt_token_here'
    }


@pytest.fixture
def session_data():
    """Sample session data for logged-in user"""
    return {
        'user_id': 'user-123',
        'is_admin_logged_in': True,
        'admin_token': 'test_admin_token'
    }


@pytest.fixture
def group_session_data():
    """Sample session data for logged-in group"""
    return {
        'group_id': 'test-group-123',
        'is_group_logged_in': True,
        'group_username': 'testgroup'
    }


# Markers for test categorization
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "database: mark test as requiring database"
    )
    config.addinivalue_line(
        "markers", "auth: mark test as authentication-related"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API endpoint test"
    )
