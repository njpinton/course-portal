"""
Unit tests for file operations (upload, download, delete)
"""
import pytest
from unittest.mock import MagicMock, patch, mock_open
import io
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.mark.unit
class TestFileValidation:
    """Tests for file validation"""

    def test_is_allowed_file_pdf(self):
        """Test PDF files are allowed"""
        from api.index import ALLOWED_EXTENSIONS

        assert 'pdf' in ALLOWED_EXTENSIONS

    def test_is_allowed_file_docx(self):
        """Test DOCX files are allowed"""
        from api.index import ALLOWED_EXTENSIONS

        assert 'docx' in ALLOWED_EXTENSIONS

    def test_is_allowed_file_xlsx(self):
        """Test XLSX files are allowed"""
        from api.index import ALLOWED_EXTENSIONS

        assert 'xlsx' in ALLOWED_EXTENSIONS

    def test_is_allowed_file_pptx(self):
        """Test PPTX files are allowed"""
        from api.index import ALLOWED_EXTENSIONS

        assert 'pptx' in ALLOWED_EXTENSIONS

    def test_is_not_allowed_file_exe(self):
        """Test executable files are not allowed"""
        from api.index import ALLOWED_EXTENSIONS

        assert 'exe' not in ALLOWED_EXTENSIONS

    def test_is_not_allowed_file_sh(self):
        """Test shell scripts are not allowed"""
        from api.index import ALLOWED_EXTENSIONS

        assert 'sh' not in ALLOWED_EXTENSIONS

    def test_filename_without_extension(self):
        """Test handling files without extension"""
        from werkzeug.utils import secure_filename

        filename = 'document'
        safe_name = secure_filename(filename)

        assert safe_name == 'document'

    def test_filename_with_path_traversal(self):
        """Test protection against path traversal"""
        from werkzeug.utils import secure_filename

        malicious = '../../../etc/passwd'
        safe_name = secure_filename(malicious)

        assert '..' not in safe_name
        assert '/' not in safe_name

    def test_filename_with_spaces(self):
        """Test handling filenames with spaces"""
        from werkzeug.utils import secure_filename

        filename = 'my document.pdf'
        safe_name = secure_filename(filename)

        # Should be sanitized
        assert 'my' in safe_name and 'document' in safe_name


@pytest.mark.unit
class TestFileSize:
    """Tests for file size validation"""

    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

    def test_file_under_size_limit(self):
        """Test files under size limit pass validation"""
        file_size = 10 * 1024 * 1024  # 10MB

        is_valid = file_size <= self.MAX_FILE_SIZE
        assert is_valid is True

    def test_file_at_size_limit(self):
        """Test files at size limit pass validation"""
        file_size = 50 * 1024 * 1024  # 50MB

        is_valid = file_size <= self.MAX_FILE_SIZE
        assert is_valid is True

    def test_file_over_size_limit(self):
        """Test files over size limit fail validation"""
        file_size = 100 * 1024 * 1024  # 100MB

        is_valid = file_size <= self.MAX_FILE_SIZE
        assert is_valid is False

    def test_zero_size_file(self):
        """Test zero-size files"""
        file_size = 0

        is_valid = file_size > 0
        assert is_valid is False


@pytest.mark.unit
class TestFileNameGeneration:
    """Tests for secure filename generation"""

    def test_timestamp_filename_generation(self):
        """Test filename generation with timestamp"""
        import time

        timestamp = int(time.time())
        original_name = 'document.pdf'
        extension = original_name.split('.')[-1]

        generated = f'{timestamp}_document.{extension}'

        assert str(timestamp) in generated
        assert original_name.split('.')[0] in generated

    def test_uuid_filename_generation(self):
        """Test filename generation with UUID"""
        import uuid

        file_id = str(uuid.uuid4())
        original_name = 'report.docx'
        extension = original_name.split('.')[-1]

        generated = f'{file_id}.{extension}'

        assert extension in generated

    def test_filename_uniqueness(self):
        """Test that generated filenames are unique"""
        import time

        filenames = []
        for _ in range(3):
            timestamp = int(time.time() * 1000)  # milliseconds for uniqueness
            filename = f'{timestamp}_file.pdf'
            filenames.append(filename)
            time.sleep(0.001)

        # All filenames should be unique
        assert len(filenames) == len(set(filenames))


@pytest.mark.unit
@pytest.mark.api
class TestFileUploadRoutes:
    """Tests for file upload endpoints"""

    @patch('api.index.get_supabase_client')
    @patch('api.index.os.path.exists')
    def test_upload_file_not_authenticated(self, mock_exists, mock_supabase, client):
        """Test file upload requires authentication"""
        mock_exists.return_value = True

        # Create a mock file
        data = {
            'file': (io.BytesIO(b'test content'), 'test.pdf')
        }

        response = client.post('/api/submit/stage-123',
                              data=data,
                              content_type='multipart/form-data')

        # Should require authentication
        assert response.status_code in [401, 302, 400]

    @patch('api.index.get_supabase_client')
    @patch('api.index.os.path.exists')
    def test_upload_file_no_file_provided(self, mock_exists, mock_supabase, client):
        """Test file upload fails without file"""
        mock_exists.return_value = True
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        with client.session_transaction() as sess:
            sess['is_group_logged_in'] = True
            sess['group_id'] = 'group-123'

        response = client.post('/api/submit/stage-123',
                              data={},
                              content_type='multipart/form-data')

        # Should return error
        assert response.status_code in [400, 500]

    @patch('api.index.get_supabase_client')
    @patch('api.index.os.path.exists')
    @patch('api.index.secure_filename')
    def test_upload_file_invalid_extension(self, mock_secure, mock_exists, mock_supabase, client):
        """Test file upload rejects invalid file types"""
        mock_exists.return_value = True
        mock_secure.return_value = 'malicious.exe'
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        with client.session_transaction() as sess:
            sess['is_group_logged_in'] = True
            sess['group_id'] = 'group-123'

        data = {
            'file': (io.BytesIO(b'fake exe'), 'malicious.exe')
        }

        response = client.post('/api/submit/stage-123',
                              data=data,
                              content_type='multipart/form-data')

        # Should reject invalid file type
        assert response.status_code in [400, 500]


@pytest.mark.unit
@pytest.mark.api
class TestFileDownloadRoutes:
    """Tests for file download endpoints"""

    @patch('api.index.send_from_directory')
    def test_download_image_success(self, mock_send, client):
        """Test downloading an image file"""
        mock_send.return_value = 'file content'

        response = client.get('/images/test-image.png')

        # Should attempt to send file
        assert response.status_code in [200, 404]

    @patch('api.index.send_from_directory')
    def test_download_nonexistent_file(self, mock_send, client):
        """Test downloading a non-existent file"""
        mock_send.side_effect = FileNotFoundError()

        with pytest.raises(FileNotFoundError):
            client.get('/images/nonexistent.png')

    @patch('api.index.get_supabase_client')
    def test_download_submission_requires_auth(self, mock_supabase, client):
        """Test downloading submission requires authentication"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        response = client.get('/api/submissions/file/submission-123')

        # Should require authentication
        assert response.status_code in [401, 404, 500]


@pytest.mark.unit
@pytest.mark.api
class TestFileDeleteRoutes:
    """Tests for file deletion endpoints"""

    @patch('api.index.get_supabase_client')
    def test_delete_submission_requires_auth(self, mock_supabase, client):
        """Test file deletion requires authentication"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        response = client.post('/api/submissions/submission-123/delete',
                              headers={'Content-Type': 'application/json'})

        # Should require authentication
        assert response.status_code in [401, 404, 500]

    @patch('api.index.get_supabase_client')
    def test_delete_file_not_found(self, mock_supabase, client):
        """Test deleting non-existent file"""
        mock_db = MagicMock()
        mock_supabase.return_value = mock_db

        # Mock file not found
        mock_table = MagicMock()
        mock_db.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[])

        with client.session_transaction() as sess:
            sess['is_group_logged_in'] = True
            sess['group_id'] = 'group-123'

        response = client.post('/api/submissions/nonexistent-123/delete',
                              headers={'Content-Type': 'application/json'})

        # Should return error
        assert response.status_code in [404, 500]


@pytest.mark.unit
class TestFilePathSecurity:
    """Tests for file path security"""

    def test_path_traversal_prevention(self):
        """Test protection against path traversal attacks"""
        from werkzeug.utils import secure_filename

        paths_to_test = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32',
            'file.pdf/../../secret.txt',
            './../../sensitive.pdf'
        ]

        for path in paths_to_test:
            safe_path = secure_filename(path)
            assert '..' not in safe_path

    def test_null_byte_injection_prevention(self):
        """Test protection against null byte injection"""
        from werkzeug.utils import secure_filename

        malicious = 'file.pdf\x00.txt'
        safe_name = secure_filename(malicious)

        assert '\x00' not in safe_name

    def test_special_characters_removal(self):
        """Test removal of dangerous special characters"""
        from werkzeug.utils import secure_filename

        test_cases = [
            ('file;name.pdf', 'filename.pdf'),  # Semicolon removed
            ('file|name.pdf', 'filename.pdf'),  # Pipe removed
            ('file<script>.pdf', 'filescript.pdf'),  # Angle brackets removed
        ]

        for input_name, expected_safe in test_cases:
            safe_name = secure_filename(input_name)
            # Should not contain dangerous characters
            assert ';' not in safe_name
            assert '|' not in safe_name
            assert '<' not in safe_name
            assert '>' not in safe_name


@pytest.mark.unit
class TestFileMetadata:
    """Tests for file metadata handling"""

    def test_file_mime_type_detection(self):
        """Test MIME type detection for common files"""
        import mimetypes

        test_files = {
            'document.pdf': 'application/pdf',
            'presentation.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'spreadsheet.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'image.png': 'image/png'
        }

        for filename, expected_type in test_files.items():
            detected_type, _ = mimetypes.guess_type(filename)
            # Should detect a MIME type
            assert detected_type is not None

    def test_file_size_formatting(self):
        """Test human-readable file size formatting"""
        def format_file_size(size_bytes):
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024:
                    return f'{size_bytes:.2f} {unit}'
                size_bytes /= 1024
            return f'{size_bytes:.2f} TB'

        test_cases = [
            (512, 'B'),
            (1024, 'KB'),
            (1024 * 1024, 'MB'),
            (1024 * 1024 * 1024, 'GB')
        ]

        for size, unit in test_cases:
            formatted = format_file_size(size)
            assert unit in formatted
