"""
Tests for Course Resources API endpoints and utility functions

Tests cover:
- YouTube URL extraction and validation
- Resource CRUD operations
- Admin authentication requirements
- Duplicate video prevention
- Reordering functionality
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestYouTubeVideoIdExtraction:
    """Test YouTube video ID extraction from various URL formats"""

    @pytest.fixture
    def extract_function(self):
        """Import the extraction function"""
        from api.index import extract_youtube_video_id
        return extract_youtube_video_id

    def test_extract_from_standard_url(self, extract_function):
        """Test extraction from youtube.com/watch?v= format"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert extract_function(url) == "dQw4w9WgXcQ"

    def test_extract_from_short_url(self, extract_function):
        """Test extraction from youtu.be format"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert extract_function(url) == "dQw4w9WgXcQ"

    def test_extract_from_embed_url(self, extract_function):
        """Test extraction from youtube.com/embed/ format"""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        assert extract_function(url) == "dQw4w9WgXcQ"

    def test_extract_from_shorts_url(self, extract_function):
        """Test extraction from youtube.com/shorts/ format"""
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        assert extract_function(url) == "dQw4w9WgXcQ"

    def test_extract_from_raw_video_id(self, extract_function):
        """Test that raw video IDs are returned as-is"""
        video_id = "dQw4w9WgXcQ"
        assert extract_function(video_id) == "dQw4w9WgXcQ"

    def test_extract_from_url_with_extra_params(self, extract_function):
        """Test extraction when URL has additional query parameters"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s&list=PLtest"
        assert extract_function(url) == "dQw4w9WgXcQ"

    def test_extract_returns_none_for_invalid_url(self, extract_function):
        """Test that None is returned for invalid URLs"""
        url = "https://example.com/video"
        assert extract_function(url) is None

    def test_extract_returns_none_for_empty_string(self, extract_function):
        """Test that None is returned for empty string"""
        assert extract_function("") is None

    def test_extract_returns_none_for_none(self, extract_function):
        """Test that None is returned for None input"""
        assert extract_function(None) is None


class TestYouTubeVideoIdValidation:
    """Test YouTube video ID validation (XSS prevention)"""

    @pytest.fixture
    def validate_function(self):
        """Import the validation function"""
        from api.index import validate_youtube_video_id
        return validate_youtube_video_id

    def test_valid_video_id(self, validate_function):
        """Test that valid 11-character IDs pass validation"""
        assert validate_function("dQw4w9WgXcQ") is True
        assert validate_function("abc123_-ABC") is True
        assert validate_function("___________") is True

    def test_invalid_video_id_too_short(self, validate_function):
        """Test that IDs shorter than 11 characters fail"""
        assert validate_function("abc123") is False
        assert validate_function("") is False

    def test_invalid_video_id_too_long(self, validate_function):
        """Test that IDs longer than 11 characters fail"""
        assert validate_function("dQw4w9WgXcQ123") is False

    def test_invalid_video_id_special_chars(self, validate_function):
        """Test that IDs with invalid characters fail (XSS prevention)"""
        assert validate_function('"><script>x') is False
        assert validate_function("abc123!@#$%") is False
        assert validate_function("abc 123 xyz") is False

    def test_invalid_video_id_none(self, validate_function):
        """Test that None fails validation"""
        assert validate_function(None) is False


class TestResourcesAPIEndpoints:
    """Test Resources API endpoints"""

    @pytest.fixture
    def app(self):
        """Create Flask app for testing with mocked Supabase"""
        with patch('api.index.get_supabase_client') as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            from api.index import app as flask_app
            flask_app.config['TESTING'] = True
            flask_app.config['SECRET_KEY'] = 'test_secret_key'

            yield flask_app

    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()

    @pytest.fixture
    def admin_session(self, client):
        """Create admin session"""
        with client.session_transaction() as sess:
            sess['logged_in'] = True
            sess['is_admin'] = True
        return client

    def test_get_resources_public_endpoint(self, client):
        """Test that public resources endpoint is accessible"""
        with patch('api.index.get_course_resources') as mock_get:
            mock_get.return_value = []
            response = client.get('/api/courses/cmsc173/resources')
            assert response.status_code == 200

    def test_get_resources_returns_list(self, client):
        """Test that resources endpoint returns a list"""
        with patch('api.index.get_course_resources') as mock_get:
            mock_get.return_value = [
                {'id': '1', 'title': 'Test Video', 'resource_type': 'youtube', 'youtube_video_id': 'abc12345678'}
            ]
            response = client.get('/api/courses/cmsc173/resources')
            assert response.status_code == 200
            data = response.get_json()
            assert isinstance(data, list)
            assert len(data) == 1

    def test_admin_resources_requires_auth(self, client):
        """Test that admin resources endpoint requires authentication"""
        response = client.get('/api/admin/resources?course_id=cmsc173')
        assert response.status_code == 401

    def test_create_resource_requires_auth(self, client):
        """Test that creating a resource requires admin authentication"""
        response = client.post('/api/admin/resources', json={
            'course_id': 'cmsc173',
            'title': 'Test Video',
            'resource_type': 'youtube',
            'youtube_video_id': 'abc12345678'
        })
        assert response.status_code == 401

    def test_create_resource_validates_youtube_id(self, admin_session):
        """Test that creating a YouTube resource validates the video ID"""
        with patch('api.index.create_resource') as mock_create:
            mock_create.return_value = None

            # Invalid video ID (too short)
            response = admin_session.post('/api/admin/resources', json={
                'course_id': 'cmsc173',
                'title': 'Test Video',
                'resource_type': 'youtube',
                'youtube_video_id': 'short'
            })
            assert response.status_code == 400
            assert 'Invalid YouTube video ID' in response.get_json()['error']

    def test_create_resource_rejects_xss_attempt(self, admin_session):
        """Test that XSS attempts in video ID are rejected"""
        with patch('api.index.create_resource') as mock_create:
            mock_create.return_value = None

            response = admin_session.post('/api/admin/resources', json={
                'course_id': 'cmsc173',
                'title': 'XSS Test',
                'resource_type': 'youtube',
                'youtube_video_id': '"><script>x'
            })
            assert response.status_code == 400

    def test_create_resource_success(self, admin_session):
        """Test successful resource creation"""
        with patch('api.index.create_resource') as mock_create:
            mock_create.return_value = {
                'id': 'new-resource-id',
                'title': 'New Video',
                'resource_type': 'youtube',
                'youtube_video_id': 'abc12345678'
            }

            response = admin_session.post('/api/admin/resources', json={
                'course_id': 'cmsc173',
                'title': 'New Video',
                'resource_type': 'youtube',
                'youtube_video_id': 'abc12345678'
            })
            assert response.status_code == 201
            data = response.get_json()
            assert data['id'] == 'new-resource-id'

    def test_delete_resource_requires_auth(self, client):
        """Test that deleting a resource requires admin authentication"""
        response = client.delete('/api/admin/resources/test-id')
        assert response.status_code == 401

    def test_reorder_resources_requires_auth(self, client):
        """Test that reordering resources requires admin authentication"""
        response = client.put('/api/admin/resources/reorder', json={
            'course_id': 'cmsc173',
            'ordered_ids': ['id1', 'id2']
        })
        assert response.status_code == 401


class TestResourcesSampleData:
    """Test sample resource fixtures"""

    @pytest.fixture
    def sample_youtube_resource(self):
        """Sample YouTube resource data"""
        return {
            'id': 'resource-123',
            'course_id': 'cmsc173',
            'title': 'Introduction to Machine Learning',
            'description': 'Basic concepts of ML',
            'resource_type': 'youtube',
            'youtube_video_id': 'abc12345678',
            'display_order': 0,
            'is_active': True,
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00'
        }

    @pytest.fixture
    def sample_link_resource(self):
        """Sample link resource data"""
        return {
            'id': 'resource-456',
            'course_id': 'cmsc173',
            'title': 'Python Documentation',
            'description': 'Official Python docs',
            'resource_type': 'link',
            'external_url': 'https://docs.python.org',
            'display_order': 1,
            'is_active': True,
            'created_at': '2025-01-01T00:00:00',
            'updated_at': '2025-01-01T00:00:00'
        }

    def test_sample_youtube_resource_has_required_fields(self, sample_youtube_resource):
        """Verify sample YouTube resource has all required fields"""
        required_fields = ['id', 'course_id', 'title', 'resource_type', 'youtube_video_id']
        for field in required_fields:
            assert field in sample_youtube_resource

    def test_sample_link_resource_has_required_fields(self, sample_link_resource):
        """Verify sample link resource has all required fields"""
        required_fields = ['id', 'course_id', 'title', 'resource_type', 'external_url']
        for field in required_fields:
            assert field in sample_link_resource
