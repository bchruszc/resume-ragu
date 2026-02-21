"""HTTP routes for profile CRUD operations."""

from fastapi import APIRouter, status
from fastapi.responses import Response

from app.models import Profile, Job, Skill, Project, Accomplishment
from app.services import profile_service

router = APIRouter(prefix="/profile", tags=["profile"])


# ---------------------------------------------------------------------------
# Profile operations
# ---------------------------------------------------------------------------


@router.get("/{user_id}", response_model=Profile)
async def get_profile(user_id: str) -> Profile:
    """Get a user's full profile."""
    return profile_service.get_profile(user_id)


@router.put("/{user_id}", response_model=Profile)
async def update_profile(user_id: str, profile: Profile) -> Profile:
    """Update a user's full profile."""
    return profile_service.update_profile(user_id, profile)


# ---------------------------------------------------------------------------
# Job operations
# ---------------------------------------------------------------------------


@router.post("/{user_id}/jobs", response_model=Job, status_code=status.HTTP_201_CREATED)
async def add_job(user_id: str, job: Job) -> Job:
    """Add a job to the user's profile."""
    return profile_service.add_job(user_id, job)


@router.put("/{user_id}/jobs/{job_id}", response_model=Job)
async def update_job(user_id: str, job_id: str, job: Job) -> Job:
    """Update an existing job."""
    return profile_service.update_job(user_id, job_id, job)


@router.delete("/{user_id}/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(user_id: str, job_id: str) -> Response:
    """Delete a job from the user's profile."""
    profile_service.delete_job(user_id, job_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Skill operations
# ---------------------------------------------------------------------------


@router.post(
    "/{user_id}/skills", response_model=Skill, status_code=status.HTTP_201_CREATED
)
async def add_skill(user_id: str, skill: Skill) -> Skill:
    """Add a skill to the user's profile."""
    return profile_service.add_skill(user_id, skill)


@router.put("/{user_id}/skills/{skill_id}", response_model=Skill)
async def update_skill(user_id: str, skill_id: str, skill: Skill) -> Skill:
    """Update an existing skill."""
    return profile_service.update_skill(user_id, skill_id, skill)


@router.delete("/{user_id}/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(user_id: str, skill_id: str) -> Response:
    """Delete a skill from the user's profile."""
    profile_service.delete_skill(user_id, skill_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Project operations
# ---------------------------------------------------------------------------


@router.post(
    "/{user_id}/projects", response_model=Project, status_code=status.HTTP_201_CREATED
)
async def add_project(user_id: str, project: Project) -> Project:
    """Add a project to the user's profile."""
    return profile_service.add_project(user_id, project)


@router.put("/{user_id}/projects/{project_id}", response_model=Project)
async def update_project(user_id: str, project_id: str, project: Project) -> Project:
    """Update an existing project."""
    return profile_service.update_project(user_id, project_id, project)


@router.delete(
    "/{user_id}/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(user_id: str, project_id: str) -> Response:
    """Delete a project from the user's profile."""
    profile_service.delete_project(user_id, project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Accomplishment operations
# ---------------------------------------------------------------------------


@router.post(
    "/{user_id}/accomplishments",
    response_model=Accomplishment,
    status_code=status.HTTP_201_CREATED,
)
async def add_accomplishment(
    user_id: str, accomplishment: Accomplishment
) -> Accomplishment:
    """Add an accomplishment to the user's profile."""
    return profile_service.add_accomplishment(user_id, accomplishment)


@router.put(
    "/{user_id}/accomplishments/{accomplishment_id}", response_model=Accomplishment
)
async def update_accomplishment(
    user_id: str, accomplishment_id: str, accomplishment: Accomplishment
) -> Accomplishment:
    """Update an existing accomplishment."""
    return profile_service.update_accomplishment(
        user_id, accomplishment_id, accomplishment
    )


@router.delete(
    "/{user_id}/accomplishments/{accomplishment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_accomplishment(user_id: str, accomplishment_id: str) -> Response:
    """Delete an accomplishment from the user's profile."""
    profile_service.delete_accomplishment(user_id, accomplishment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
