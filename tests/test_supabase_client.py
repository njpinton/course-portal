"""
Unit tests for supabase_client module
"""
import pytest
from unittest.mock import MagicMock, patch, call
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.mark.unit
@pytest.mark.database
class TestGroupOperations:
    """Tests for group-related database operations"""

    @patch('supabase_client.supabase')
    def test_create_group_success(self, mock_supabase, sample_group_data):
        """Test successful group creation"""
        from supabase_client import create_group

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_group_data])

        # Call function
        result = create_group(
            'Test Group',
            'class-456',
            'testgroup',
            'hashed_password',
            'class-456'
        )

        # Assertions
        assert result is not None
        assert result['name'] == 'Test Group'
        mock_supabase.table.assert_called_with('groups')

    @patch('supabase_client.supabase')
    def test_create_group_failure(self, mock_supabase):
        """Test group creation failure"""
        from supabase_client import create_group

        # Setup mock to return None
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=None)

        # Call function
        result = create_group('Test', 'class-1', 'user', 'pass', 'class-1')

        # Assertions
        assert result is None

    @patch('supabase_client.supabase')
    def test_get_group_by_id(self, mock_supabase, sample_group_data):
        """Test retrieving group by ID"""
        from supabase_client import get_group_details

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_group_data])

        # Call function
        result = get_group_details('test-group-123')

        # Assertions
        assert result is not None
        assert result['id'] == 'test-group-123'
        mock_supabase.table.assert_called_with('groups')

    @patch('supabase_client.supabase')
    def test_get_group_by_username(self, mock_supabase, sample_group_data):
        """Test retrieving group by username"""
        from supabase_client import get_group_by_username

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_group_data])

        # Call function
        result = get_group_by_username('testgroup')

        # Assertions
        assert result is not None
        assert result['username'] == 'testgroup'

    @patch('supabase_client.supabase')
    def test_delete_group_success(self, mock_supabase):
        """Test successful group deletion"""
        from supabase_client import delete_group

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.delete.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[{'id': 'test-group-123'}])

        # Call function
        result = delete_group('test-group-123')

        # Assertions
        assert result is True

    @patch('supabase_client.supabase')
    def test_get_groups_by_class(self, mock_supabase, sample_group_data):
        """Test retrieving all groups for a class"""
        from supabase_client import get_groups

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_group_data])

        # Call function
        result = get_groups('class-456')

        # Assertions
        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]['class_id'] == 'class-456'


@pytest.mark.unit
@pytest.mark.database
class TestStudentOperations:
    """Tests for student-related database operations"""

    @patch('supabase_client.supabase')
    def test_get_student_by_id(self, mock_supabase, sample_student_data):
        """Test retrieving student by ID"""
        from supabase_client import get_student_by_id

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_student_data])

        # Call function
        result = get_student_by_id('student-123')

        # Assertions
        assert result is not None
        assert result['id'] == 'student-123'
        assert result['first_name'] == 'John'

    @patch('supabase_client.supabase')
    def test_get_ungrouped_students(self, mock_supabase, sample_student_data):
        """Test retrieving students without groups"""
        from supabase_client import get_ungrouped_students

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.is_.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_student_data])

        # Call function
        result = get_ungrouped_students('class-456')

        # Assertions
        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]['group_id'] is None

    @patch('supabase_client.supabase')
    def test_assign_student_to_group_success(self, mock_supabase, sample_student_data):
        """Test successful student assignment to group"""
        from supabase_client import assign_student_to_group

        # Setup mock - student exists and not in a group
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_student_data])
        mock_table.update.return_value = mock_table

        # Call function
        result = assign_student_to_group('test-group-123', 'student-123')

        # Assertions
        assert result is True

    @patch('supabase_client.supabase')
    def test_assign_student_to_group_already_in_group(self, mock_supabase):
        """Test assignment fails when student already in group"""
        from supabase_client import assign_student_to_group

        # Setup mock - student already in group
        student_in_group = {
            'id': 'student-123',
            'first_name': 'John',
            'last_name': 'Doe',
            'group_id': 'other-group-456'
        }
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[student_in_group])

        # Call function
        result = assign_student_to_group('test-group-123', 'student-123')

        # Assertions
        assert result is False

    @patch('supabase_client.supabase')
    def test_unassign_student_from_group(self, mock_supabase, sample_student_data):
        """Test unassigning student from group"""
        from supabase_client import unassign_student_from_group

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.update.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_student_data])

        # Call function
        result = unassign_student_from_group('student-123')

        # Assertions
        assert result is True


@pytest.mark.unit
@pytest.mark.database
class TestGroupMemberOperations:
    """Tests for group member operations"""

    @patch('supabase_client.supabase')
    def test_get_group_members(self, mock_supabase):
        """Test retrieving group members"""
        from supabase_client import get_group_members

        member_data = {
            'id': 'member-123',
            'group_id': 'test-group-123',
            'member_name': 'John Doe',
            'student_id': 'student-123'
        }

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[member_data])

        # Call function
        result = get_group_members('test-group-123')

        # Assertions
        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0]['member_name'] == 'John Doe'

    @patch('supabase_client.supabase')
    def test_add_group_member(self, mock_supabase):
        """Test adding member to group"""
        from supabase_client import add_group_member

        member_data = {
            'id': 'member-123',
            'group_id': 'test-group-123',
            'member_name': 'John Doe',
            'student_id': 'student-123'
        }

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[member_data])

        # Call function
        result = add_group_member('test-group-123', 'John Doe', 'student-123')

        # Assertions
        assert result is not None
        assert result['member_name'] == 'John Doe'


@pytest.mark.unit
@pytest.mark.database
class TestSubmissionOperations:
    """Tests for submission-related operations"""

    @patch('supabase_client.supabase')
    def test_get_group_submissions(self, mock_supabase, sample_submission_data):
        """Test retrieving group submissions"""
        from supabase_client import get_group_with_submissions

        # Setup mock
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_submission_data])

        # Call function
        result = get_group_with_submissions('test-group-123')

        # Assertions
        assert isinstance(result, list)


@pytest.mark.unit
@pytest.mark.database
class TestInputValidation:
    """Tests for input validation functions"""

    def test_validate_uuid_valid(self):
        """Test UUID validation with valid UUID"""
        from supabase_client import validate_uuid

        valid_uuid = 'f47ac10b-58cc-4372-a567-0e02b2c3d479'
        is_valid = validate_uuid(valid_uuid)
        assert is_valid is True

    def test_validate_uuid_invalid(self):
        """Test UUID validation with invalid UUID"""
        from supabase_client import validate_uuid

        invalid_uuid = 'not-a-uuid'
        is_valid = validate_uuid(invalid_uuid)
        assert is_valid is False

    def test_validate_uuid_none(self):
        """Test UUID validation with None"""
        from supabase_client import validate_uuid

        is_valid = validate_uuid(None)
        assert is_valid is False
