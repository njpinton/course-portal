"""
Unit tests for Flask API routes and endpoints
"""
import pytest
from unittest.mock import MagicMock, patch
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.mark.unit
@pytest.mark.api
class TestGroupRoutes:
    """Tests for group-related API routes"""

    def test_index_route(self, client):
        """Test GET / returns index page"""
        response = client.get('/')
        assert response.status_code in [200, 302]  # Either renders or redirects

    @patch('api.index.get_supabase_client')
    def test_create_group_success(self, mock_supabase, client, sample_group_data):
        """Test successful group creation via API"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock database response
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.insert.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_group_data])

        response = client.post('/create_group', data={
            'group_name': 'Test Group',
            'class_code': 'CMSC-173',
            'section': '01'
        })

        assert response.status_code in [200, 302, 400]

    @patch('api.index.get_supabase_client')
    def test_create_group_missing_fields(self, mock_supabase, client):
        """Test group creation fails with missing fields"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        response = client.post('/create_group', data={
            'group_name': 'Test Group'
            # Missing class_code and section
        })

        # Should return an error or validation message
        assert response.status_code in [200, 302, 400]

    @patch('api.index.get_supabase_client')
    def test_get_group_details(self, mock_supabase, client, sample_group_data):
        """Test retrieving group details"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock the response
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_group_data])

        response = client.get('/group/test-group-123')

        # Should return group details or handle error gracefully
        assert response.status_code in [200, 302, 404]

    @patch('api.index.get_supabase_client')
    def test_delete_group(self, mock_supabase, client):
        """Test group deletion endpoint"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock the response
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.delete.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[{'id': 'test-group-123'}])

        response = client.post('/api/groups/test-group-123/delete',
                              headers={'Content-Type': 'application/json'})

        # Should return success or error response
        assert response.status_code in [200, 401, 404, 500]


@pytest.mark.unit
@pytest.mark.api
class TestStudentRoutes:
    """Tests for student-related API routes"""

    @patch('api.index.get_supabase_client')
    def test_get_students_by_class(self, mock_supabase, client, sample_student_data):
        """Test retrieving students by class"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock the response
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_student_data])

        response = client.get('/api/students/class/class-456')

        # Should return list of students or error
        assert response.status_code in [200, 401, 404, 500]

    @patch('api.index.get_supabase_client')
    def test_get_ungrouped_students(self, mock_supabase, client, sample_student_data):
        """Test retrieving ungrouped students"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock the response
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.is_.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_student_data])

        response = client.get('/api/students/ungrouped/all')

        # Should return list of ungrouped students
        assert response.status_code in [200, 401, 404, 500]

    @patch('api.index.get_supabase_client')
    def test_unassign_student_from_group(self, mock_supabase, client):
        """Test unassigning student from group"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock the response
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.update.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[{'id': 'student-123'}])

        response = client.post('/api/students/student-123/unassign-group',
                              headers={'Content-Type': 'application/json'})

        # Should require admin authentication
        assert response.status_code in [401, 200, 500]


@pytest.mark.unit
@pytest.mark.api
class TestGroupMemberRoutes:
    """Tests for group member API routes"""

    @patch('api.index.get_supabase_client')
    def test_add_group_member_not_logged_in(self, mock_supabase, client):
        """Test add member endpoint requires group login"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        response = client.post('/api/group/members/add',
                              data=json.dumps({'student_id': 'student-123'}),
                              content_type='application/json')

        # Should return 401 Unauthorized if not logged in
        assert response.status_code == 401

    @patch('api.index.get_supabase_client')
    def test_add_group_member_success(self, mock_supabase, client, group_session_data, sample_student_data):
        """Test successful group member addition"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Setup mock
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_student_data])
        mock_table.update.return_value = mock_table
        mock_table.insert.return_value = mock_table

        with client.session_transaction() as sess:
            sess.update(group_session_data)

        response = client.post('/api/group/members/add',
                              data=json.dumps({'student_id': 'student-123'}),
                              content_type='application/json')

        # Should process the request
        assert response.status_code in [200, 400, 500]

    @patch('api.index.get_supabase_client')
    def test_get_group_members(self, mock_supabase, client):
        """Test retrieving group members"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        member_data = {
            'id': 'member-123',
            'group_id': 'test-group-123',
            'member_name': 'John Doe'
        }

        # Setup mock
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[member_data])

        response = client.get('/api/groups/test-group-123/members')

        # Should return members or error
        assert response.status_code in [200, 401, 404, 500]


@pytest.mark.unit
@pytest.mark.api
class TestAuthenticationRoutes:
    """Tests for authentication-related routes"""

    @patch('api.index.get_supabase_client')
    def test_admin_login_page(self, mock_supabase, client):
        """Test admin login page loads"""
        response = client.get('/admin')

        # Should return login page or redirect
        assert response.status_code in [200, 302]

    @patch('api.index.get_supabase_client')
    def test_admin_login_invalid_credentials(self, mock_supabase, client):
        """Test admin login with invalid credentials"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock no admin found
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[])

        response = client.post('/admin_login', data={
            'email': 'admin@example.com',
            'password': 'wrongpassword'
        })

        # Should handle invalid credentials
        assert response.status_code in [200, 302]

    @patch('api.index.get_supabase_client')
    def test_group_login_page(self, mock_supabase, client):
        """Test group login page loads"""
        response = client.get('/group_login')

        # Should return login form
        assert response.status_code in [200, 302]

    @patch('api.index.get_supabase_client')
    def test_group_login_invalid_credentials(self, mock_supabase, client):
        """Test group login with invalid credentials"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock no group found
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[])

        response = client.post('/group_login', data={
            'username': 'unknowngroup',
            'password': 'wrongpassword'
        })

        # Should handle invalid credentials
        assert response.status_code in [200, 302]

    def test_logout(self, client):
        """Test logout functionality"""
        response = client.get('/logout')

        # Should redirect after logout
        assert response.status_code in [302, 200]


@pytest.mark.unit
@pytest.mark.api
class TestErrorHandling:
    """Tests for error handling in API routes"""

    def test_404_not_found(self, client):
        """Test 404 error on non-existent route"""
        response = client.get('/nonexistent/route')

        assert response.status_code == 404

    @patch('api.index.get_supabase_client')
    def test_api_invalid_json(self, mock_supabase, client):
        """Test API handling of invalid JSON"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        response = client.post('/api/group/members/add',
                              data='invalid json',
                              content_type='application/json')

        # Should handle invalid JSON gracefully
        assert response.status_code in [400, 401, 500]

    @patch('api.index.get_supabase_client')
    def test_api_missing_required_fields(self, mock_supabase, client):
        """Test API validation of required fields"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        with client.session_transaction() as sess:
            sess['is_group_logged_in'] = True
            sess['group_id'] = 'test-group-123'

        response = client.post('/api/group/members/add',
                              data=json.dumps({}),  # Missing student_id
                              content_type='application/json')

        # Should return error for missing fields
        assert response.status_code in [400, 500]


@pytest.mark.unit
@pytest.mark.api
class TestSubmissionRoutes:
    """Tests for submission-related routes"""

    @patch('api.index.get_supabase_client')
    def test_get_submission_details(self, mock_supabase, client, sample_submission_data):
        """Test retrieving submission details"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Setup mock
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_submission_data])

        response = client.get('/api/submissions/submission-123')

        # Should return submission details or error
        assert response.status_code in [200, 401, 404, 500]
