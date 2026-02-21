"""JSON file storage for user profiles."""

import json
import logging
import os
from pathlib import Path
from typing import Optional

from app.config import settings
from app.errors import StorageError

logger = logging.getLogger(__name__)


def _get_profile_path(user_id: str) -> Path:
    """Get the file path for a user's profile."""
    return Path(settings.DATA_DIR) / user_id / "profile.json"


def load_profile(user_id: str) -> Optional[dict]:
    """
    Load a user's profile from disk.

    Args:
        user_id: The user ID

    Returns:
        Profile data as dict, or None if file doesn't exist

    Raises:
        StorageError: If file exists but can't be read or parsed
    """
    path = _get_profile_path(user_id)

    if not path.exists():
        logger.info(f"Profile not found for user {user_id}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded profile for user {user_id}")
        return data
    except (OSError, PermissionError) as e:
        logger.error(f"Failed to read profile for user {user_id}: {e}")
        raise StorageError(f"Failed to read profile: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in profile for user {user_id}: {e}")
        raise StorageError(f"Invalid JSON in profile: {e}")


def save_profile(user_id: str, profile: dict) -> None:
    """
    Save a user's profile to disk.

    Uses atomic writes (write to temp file, then rename) to prevent corruption.

    Args:
        user_id: The user ID
        profile: Profile data as dict

    Raises:
        StorageError: If file can't be written
    """
    path = _get_profile_path(user_id)

    # Create user directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Atomic write: write to temp file, then rename
    temp_path = path.with_suffix(".tmp")
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        temp_path.replace(path)
        logger.info(f"Saved profile for user {user_id}")
    except (OSError, PermissionError) as e:
        logger.error(f"Failed to write profile for user {user_id}: {e}")
        # Clean up temp file if it exists
        if temp_path.exists():
            temp_path.unlink()
        raise StorageError(f"Failed to write profile: {e}")


def delete_profile(user_id: str) -> bool:
    """
    Delete a user's profile from disk.

    Args:
        user_id: The user ID

    Returns:
        True if profile was deleted, False if it didn't exist

    Raises:
        StorageError: If file exists but can't be deleted
    """
    path = _get_profile_path(user_id)

    if not path.exists():
        logger.info(f"Profile not found for deletion: user {user_id}")
        return False

    try:
        path.unlink()
        logger.info(f"Deleted profile for user {user_id}")
        return True
    except (OSError, PermissionError) as e:
        logger.error(f"Failed to delete profile for user {user_id}: {e}")
        raise StorageError(f"Failed to delete profile: {e}")
