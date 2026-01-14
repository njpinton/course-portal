"""Input validation utilities."""
from ..config import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES


def allowed_file(filename: str, mime_type: str = None) -> bool:
    """Validate file type against allowed extensions and MIME types."""
    if not filename or '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False

    # Additional MIME type check if provided
    if mime_type and mime_type not in ALLOWED_MIME_TYPES:
        return False

    return True


def validate_input(value: str, max_length: int = 255, field_name: str = "input") -> tuple:
    """Validate string input for length and null bytes."""
    if not isinstance(value, str):
        return False, f"{field_name} must be a string"

    if not value or len(value.strip()) == 0:
        return False, f"{field_name} cannot be empty"

    if len(value) > max_length:
        return False, f"{field_name} exceeds maximum length of {max_length}"

    if '\x00' in value:
        return False, f"{field_name} contains invalid characters"

    return True, ""
