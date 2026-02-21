"""Business logic for profile operations."""

import logging
import uuid

from app.errors import NotFoundError
from app.models import Profile, Job, Skill, Project, Accomplishment
from app.storage import json_store

logger = logging.getLogger(__name__)


def _generate_id(prefix: str) -> str:
    """Generate a unique ID with the given prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def get_profile(user_id: str) -> Profile:
    """
    Load a user's profile.

    Args:
        user_id: The user ID

    Returns:
        Profile object

    Raises:
        NotFoundError: If profile doesn't exist
    """
    data = json_store.load_profile(user_id)
    if data is None:
        raise NotFoundError(f"Profile not found for user {user_id}")

    profile = Profile.model_validate(data)
    logger.info(f"Retrieved profile for user {user_id}")
    return profile


def update_profile(user_id: str, profile: Profile) -> Profile:
    """
    Update a user's full profile.

    Args:
        user_id: The user ID
        profile: Complete profile data

    Returns:
        Saved profile
    """
    # Convert to dict with camelCase keys for storage
    data = profile.model_dump(by_alias=True)
    json_store.save_profile(user_id, data)
    logger.info(f"Updated profile for user {user_id}")
    return profile


# ---------------------------------------------------------------------------
# Job operations
# ---------------------------------------------------------------------------


def add_job(user_id: str, job: Job) -> Job:
    """
    Add a job to the user's profile.

    Args:
        user_id: The user ID
        job: Job to add (ID will be generated)

    Returns:
        The added job with generated ID
    """
    profile = get_profile(user_id)

    # Generate ID if not provided
    if not job.id or job.id == "":
        job.id = _generate_id("job")

    profile.jobs.append(job)
    update_profile(user_id, profile)
    logger.info(f"Added job {job.id} for user {user_id}")
    return job


def update_job(user_id: str, job_id: str, updated_job: Job) -> Job:
    """
    Update an existing job.

    Args:
        user_id: The user ID
        job_id: ID of job to update
        updated_job: New job data

    Returns:
        Updated job

    Raises:
        NotFoundError: If job not found
    """
    profile = get_profile(user_id)

    # Find and replace job
    for i, job in enumerate(profile.jobs):
        if job.id == job_id:
            updated_job.id = job_id  # Preserve ID
            profile.jobs[i] = updated_job
            update_profile(user_id, profile)
            logger.info(f"Updated job {job_id} for user {user_id}")
            return updated_job

    raise NotFoundError(f"Job {job_id} not found for user {user_id}")


def delete_job(user_id: str, job_id: str) -> None:
    """
    Delete a job from the user's profile.

    Args:
        user_id: The user ID
        job_id: ID of job to delete

    Raises:
        NotFoundError: If job not found
    """
    profile = get_profile(user_id)

    # Find and remove job
    original_count = len(profile.jobs)
    profile.jobs = [job for job in profile.jobs if job.id != job_id]

    if len(profile.jobs) == original_count:
        raise NotFoundError(f"Job {job_id} not found for user {user_id}")

    update_profile(user_id, profile)
    logger.info(f"Deleted job {job_id} for user {user_id}")


# ---------------------------------------------------------------------------
# Skill operations
# ---------------------------------------------------------------------------


def add_skill(user_id: str, skill: Skill) -> Skill:
    """Add a skill to the user's profile."""
    profile = get_profile(user_id)

    if not skill.id or skill.id == "":
        skill.id = _generate_id("skill")

    profile.skills.append(skill)
    update_profile(user_id, profile)
    logger.info(f"Added skill {skill.id} for user {user_id}")
    return skill


def update_skill(user_id: str, skill_id: str, updated_skill: Skill) -> Skill:
    """Update an existing skill."""
    profile = get_profile(user_id)

    for i, skill in enumerate(profile.skills):
        if skill.id == skill_id:
            updated_skill.id = skill_id
            profile.skills[i] = updated_skill
            update_profile(user_id, profile)
            logger.info(f"Updated skill {skill_id} for user {user_id}")
            return updated_skill

    raise NotFoundError(f"Skill {skill_id} not found for user {user_id}")


def delete_skill(user_id: str, skill_id: str) -> None:
    """Delete a skill from the user's profile."""
    profile = get_profile(user_id)

    original_count = len(profile.skills)
    profile.skills = [skill for skill in profile.skills if skill.id != skill_id]

    if len(profile.skills) == original_count:
        raise NotFoundError(f"Skill {skill_id} not found for user {user_id}")

    update_profile(user_id, profile)
    logger.info(f"Deleted skill {skill_id} for user {user_id}")


# ---------------------------------------------------------------------------
# Project operations
# ---------------------------------------------------------------------------


def add_project(user_id: str, project: Project) -> Project:
    """Add a project to the user's profile."""
    profile = get_profile(user_id)

    if not project.id or project.id == "":
        project.id = _generate_id("project")

    profile.projects.append(project)
    update_profile(user_id, profile)
    logger.info(f"Added project {project.id} for user {user_id}")
    return project


def update_project(user_id: str, project_id: str, updated_project: Project) -> Project:
    """Update an existing project."""
    profile = get_profile(user_id)

    for i, project in enumerate(profile.projects):
        if project.id == project_id:
            updated_project.id = project_id
            profile.projects[i] = updated_project
            update_profile(user_id, profile)
            logger.info(f"Updated project {project_id} for user {user_id}")
            return updated_project

    raise NotFoundError(f"Project {project_id} not found for user {user_id}")


def delete_project(user_id: str, project_id: str) -> None:
    """Delete a project from the user's profile."""
    profile = get_profile(user_id)

    original_count = len(profile.projects)
    profile.projects = [proj for proj in profile.projects if proj.id != project_id]

    if len(profile.projects) == original_count:
        raise NotFoundError(f"Project {project_id} not found for user {user_id}")

    update_profile(user_id, profile)
    logger.info(f"Deleted project {project_id} for user {user_id}")


# ---------------------------------------------------------------------------
# Accomplishment operations
# ---------------------------------------------------------------------------


def add_accomplishment(user_id: str, accomplishment: Accomplishment) -> Accomplishment:
    """Add an accomplishment to the user's profile."""
    profile = get_profile(user_id)

    if not accomplishment.id or accomplishment.id == "":
        accomplishment.id = _generate_id("accomplishment")

    profile.accomplishments.append(accomplishment)
    update_profile(user_id, profile)
    logger.info(f"Added accomplishment {accomplishment.id} for user {user_id}")
    return accomplishment


def update_accomplishment(
    user_id: str, accomplishment_id: str, updated_accomplishment: Accomplishment
) -> Accomplishment:
    """Update an existing accomplishment."""
    profile = get_profile(user_id)

    for i, accomplishment in enumerate(profile.accomplishments):
        if accomplishment.id == accomplishment_id:
            updated_accomplishment.id = accomplishment_id
            profile.accomplishments[i] = updated_accomplishment
            update_profile(user_id, profile)
            logger.info(f"Updated accomplishment {accomplishment_id} for user {user_id}")
            return updated_accomplishment

    raise NotFoundError(
        f"Accomplishment {accomplishment_id} not found for user {user_id}"
    )


def delete_accomplishment(user_id: str, accomplishment_id: str) -> None:
    """Delete an accomplishment from the user's profile."""
    profile = get_profile(user_id)

    original_count = len(profile.accomplishments)
    profile.accomplishments = [
        acc for acc in profile.accomplishments if acc.id != accomplishment_id
    ]

    if len(profile.accomplishments) == original_count:
        raise NotFoundError(
            f"Accomplishment {accomplishment_id} not found for user {user_id}"
        )

    update_profile(user_id, profile)
    logger.info(f"Deleted accomplishment {accomplishment_id} for user {user_id}")
