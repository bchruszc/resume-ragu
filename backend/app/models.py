"""Pydantic models for Resume Ragu."""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Profile data models
# ---------------------------------------------------------------------------


class Contact(BaseModel):
    """User contact information."""

    model_config = ConfigDict(populate_by_name=True)

    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class User(BaseModel):
    """User profile header."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    contact: Contact
    summary: Optional[str] = None


class Job(BaseModel):
    """Employment history entry."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    company: str
    title: str
    start_date: str = Field(alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    description: Optional[str] = None
    highlights: list[str] = Field(default_factory=list)


class Skill(BaseModel):
    """Skill or technology."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    category: str
    proficiency: Optional[Literal["beginner", "intermediate", "advanced", "expert"]] = (
        None
    )
    years_of_experience: Optional[int] = Field(None, alias="yearsOfExperience")


class Project(BaseModel):
    """Project or initiative."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    description: Optional[str] = None
    job_ids: list[str] = Field(default_factory=list, alias="jobIds")
    skill_ids: list[str] = Field(default_factory=list, alias="skillIds")
    outcome: Optional[str] = None


class Accomplishment(BaseModel):
    """Accomplishment or achievement — the core resume building block."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    statement: str
    context: Optional[str] = None
    impact: Optional[str] = None
    job_ids: list[str] = Field(default_factory=list, alias="jobIds")
    project_ids: list[str] = Field(default_factory=list, alias="projectIds")
    skill_ids: list[str] = Field(default_factory=list, alias="skillIds")
    tags: list[str] = Field(default_factory=list)


class Profile(BaseModel):
    """Complete user profile."""

    model_config = ConfigDict(populate_by_name=True)

    user: User
    jobs: list[Job] = Field(default_factory=list)
    skills: list[Skill] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    accomplishments: list[Accomplishment] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Chat / AI models
# ---------------------------------------------------------------------------


class ChatMessage(BaseModel):
    """Single chat message."""

    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """Request to chat endpoint."""

    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    """Response from chat endpoint."""

    model_config = ConfigDict(populate_by_name=True)

    message: ChatMessage
    usage: Optional[dict[str, int]] = None
