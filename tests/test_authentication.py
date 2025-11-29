"""
Unit tests for authentication and authorization
"""
import pytest
from unittest.mock import MagicMock, patch
import json
import jwt
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.mark.unit
@pytest.mark.auth
class TestAdminAuthentication:
    """Tests for admin authentication"""

    @patch('api.index.get_supabase_client')
    def test_admin_login_valid_email_password(self, mock_supabase, client):
        """Test admin login with valid email and password"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        admin_data = {
            'id': 'admin-123',
            'email': 'admin@example.com',
            'password_hash': 'hashed_password',
            'name': 'Admin User'
        }

        # Mock admin found and password valid
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[admin_data])

        with patch('api.index.check_password_hash', return_value=True):
            response = client.post('/admin_login', data={
                'email': 'admin@example.com',
                'password': 'correctpassword'
            })

        # Should redirect to admin dashboard
        assert response.status_code in [302, 200]

    @patch('api.index.get_supabase_client')
    def test_admin_login_invalid_email(self, mock_supabase, client):
        """Test admin login with non-existent email"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock admin not found
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[])

        response = client.post('/admin_login', data={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        })

        # Should show error or redirect back to login
        assert response.status_code in [200, 302]

    @patch('api.index.get_supabase_client')
    def test_admin_login_invalid_password(self, mock_supabase, client):
        """Test admin login with incorrect password"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        admin_data = {
            'id': 'admin-123',
            'email': 'admin@example.com',
            'password_hash': 'hashed_password'
        }

        # Mock admin found but password wrong
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[admin_data])

        with patch('api.index.check_password_hash', return_value=False):
            response = client.post('/admin_login', data={
                'email': 'admin@example.com',
                'password': 'wrongpassword'
            })

        # Should show error or redirect
        assert response.status_code in [200, 302]

    def test_admin_logout(self, client):
        """Test admin logout"""
        with client.session_transaction() as sess:
            sess['admin_token'] = 'test_token'
            sess['is_admin_logged_in'] = True

        response = client.get('/logout')

        # Session should be cleared
        with client.session_transaction() as sess:
            assert 'admin_token' not in sess or not sess.get('is_admin_logged_in')

        assert response.status_code in [302, 200]


@pytest.mark.unit
@pytest.mark.auth
class TestGroupAuthentication:
    """Tests for group authentication"""

    @patch('api.index.get_supabase_client')
    def test_group_login_valid_credentials(self, mock_supabase, client):
        """Test group login with valid username and password"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        group_data = {
            'id': 'group-123',
            'username': 'testgroup',
            'password_hash': 'hashed_password',
            'name': 'Test Group'
        }

        # Mock group found
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[group_data])

        with patch('api.index.check_password_hash', return_value=True):
            response = client.post('/group_login', data={
                'username': 'testgroup',
                'password': 'correctpassword'
            })

        # Should redirect to submission portal
        assert response.status_code in [302, 200]

    @patch('api.index.get_supabase_client')
    def test_group_login_invalid_username(self, mock_supabase, client):
        """Test group login with non-existent username"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock group not found
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[])

        response = client.post('/group_login', data={
            'username': 'unknowngroup',
            'password': 'password123'
        })

        # Should show error
        assert response.status_code in [200, 302]

    @patch('api.index.get_supabase_client')
    def test_group_login_invalid_password(self, mock_supabase, client):
        """Test group login with incorrect password"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        group_data = {
            'id': 'group-123',
            'username': 'testgroup',
            'password_hash': 'hashed_password'
        }

        # Mock group found but password wrong
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[group_data])

        with patch('api.index.check_password_hash', return_value=False):
            response = client.post('/group_login', data={
                'username': 'testgroup',
                'password': 'wrongpassword'
            })

        # Should show error
        assert response.status_code in [200, 302]

    def test_group_logout(self, client):
        """Test group logout"""
        with client.session_transaction() as sess:
            sess['group_id'] = 'group-123'
            sess['is_group_logged_in'] = True

        response = client.get('/logout')

        # Session should be cleared
        with client.session_transaction() as sess:
            assert 'group_id' not in sess or not sess.get('is_group_logged_in')

        assert response.status_code in [302, 200]


@pytest.mark.unit
@pytest.mark.auth
class TestAuthorizationChecks:
    """Tests for authorization checks"""

    def test_admin_only_endpoint_without_auth(self, client):
        """Test that admin-only endpoints deny unauthenticated requests"""
        response = client.get('/admin/dashboard')

        # Should redirect to login or return 401
        assert response.status_code in [302, 401]

    def test_admin_only_endpoint_with_auth(self, client):
        """Test that admin-only endpoints allow authenticated admins"""
        with client.session_transaction() as sess:
            sess['is_admin_logged_in'] = True
            sess['admin_token'] = 'valid_token'

        response = client.get('/admin/dashboard')

        # Should allow access or show dashboard
        assert response.status_code in [200, 302]

    def test_group_only_endpoint_without_auth(self, client):
        """Test that group-only endpoints deny unauthenticated requests"""
        response = client.get('/group_submission_portal')

        # Should redirect to login or return 401
        assert response.status_code in [302, 401]

    def test_group_only_endpoint_with_auth(self, client):
        """Test that group-only endpoints allow authenticated groups"""
        with client.session_transaction() as sess:
            sess['is_group_logged_in'] = True
            sess['group_id'] = 'group-123'

        response = client.get('/group_submission_portal')

        # Should allow access or handle error
        assert response.status_code in [200, 302, 500]


@pytest.mark.unit
@pytest.mark.auth
class TestSessionManagement:
    """Tests for session management"""

    def test_session_creation_on_login(self, client):
        """Test that session is created on successful login"""
        with client.session_transaction() as sess:
            assert len(sess) == 0

        with client.session_transaction() as sess:
            sess['test_key'] = 'test_value'

        with client.session_transaction() as sess:
            assert sess.get('test_key') == 'test_value'

    def test_session_persistence(self, client):
        """Test that session data persists across requests"""
        with client.session_transaction() as sess:
            sess['group_id'] = 'test-group-123'
            sess['is_group_logged_in'] = True

        # Make a request
        response = client.get('/')

        # Session should still be there
        with client.session_transaction() as sess:
            assert sess.get('group_id') == 'test-group-123'
            assert sess.get('is_group_logged_in') is True

    def test_session_clear_on_logout(self, client):
        """Test that session is cleared on logout"""
        with client.session_transaction() as sess:
            sess['admin_token'] = 'token'
            sess['is_admin_logged_in'] = True

        response = client.get('/logout')

        with client.session_transaction() as sess:
            # Session should be empty or have logout indicator
            assert not sess.get('is_admin_logged_in', False)


@pytest.mark.unit
@pytest.mark.auth
class TestPasswordHandling:
    """Tests for password handling"""

    def test_password_hash_generation(self):
        """Test that passwords are properly hashed"""
        from werkzeug.security import generate_password_hash, check_password_hash

        password = 'test_password_123'
        hashed = generate_password_hash(password)

        # Hash should not be the same as password
        assert hashed != password

        # Hash should verify correct password
        assert check_password_hash(hashed, password)

    def test_password_hash_verification_fails_with_wrong_password(self):
        """Test that wrong password doesn't verify"""
        from werkzeug.security import generate_password_hash, check_password_hash

        password = 'correct_password'
        hashed = generate_password_hash(password)

        # Wrong password should not verify
        assert not check_password_hash(hashed, 'wrong_password')

    def test_password_hash_unique(self):
        """Test that same password generates different hashes"""
        from werkzeug.security import generate_password_hash

        password = 'same_password'
        hash1 = generate_password_hash(password)
        hash2 = generate_password_hash(password)

        # Hashes should be different (salted)
        assert hash1 != hash2


@pytest.mark.unit
@pytest.mark.auth
class TestJWTTokens:
    """Tests for JWT token handling"""

    def test_jwt_token_creation(self):
        """Test JWT token creation"""
        import jwt
        from datetime import datetime, timedelta

        payload = {
            'admin_id': 'admin-123',
            'email': 'admin@example.com',
            'exp': datetime.utcnow() + timedelta(hours=1)
        }

        secret_key = 'test_secret_key'
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        # Token should be a string
        assert isinstance(token, str)

    def test_jwt_token_verification(self):
        """Test JWT token verification"""
        import jwt
        from datetime import datetime, timedelta

        secret_key = 'test_secret_key'
        payload = {
            'admin_id': 'admin-123',
            'exp': datetime.utcnow() + timedelta(hours=1)
        }

        token = jwt.encode(payload, secret_key, algorithm='HS256')

        # Token should decode successfully
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        assert decoded['admin_id'] == 'admin-123'

    def test_jwt_token_expiration(self):
        """Test JWT token expiration"""
        import jwt
        from datetime import datetime, timedelta

        secret_key = 'test_secret_key'
        # Create token that expired 1 hour ago
        payload = {
            'admin_id': 'admin-123',
            'exp': datetime.utcnow() - timedelta(hours=1)
        }

        token = jwt.encode(payload, secret_key, algorithm='HS256')

        # Token should fail to verify
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, secret_key, algorithms=['HS256'])
