import type { Profile, Job, Skill, Project, Accomplishment, ChatMessage, ChatResponse, ApiError } from '../types';

const BASE_URL = '/api';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${url}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });

  if (!response.ok) {
    const errorBody: ApiError = await response.json();
    throw new Error(errorBody.error.message);
  }

  return response.json();
}

// Profile
export async function getProfile(userId: string): Promise<Profile> {
  return request<Profile>(`/profile/${userId}`);
}

export async function updateProfile(userId: string, profile: Profile): Promise<Profile> {
  return request<Profile>(`/profile/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(profile),
  });
}

// Jobs
export async function addJob(userId: string, job: Omit<Job, 'id'>): Promise<Job> {
  return request<Job>(`/profile/${userId}/jobs`, {
    method: 'POST',
    body: JSON.stringify(job),
  });
}

export async function updateJob(userId: string, jobId: string, job: Partial<Job>): Promise<Job> {
  return request<Job>(`/profile/${userId}/jobs/${jobId}`, {
    method: 'PUT',
    body: JSON.stringify(job),
  });
}

export async function deleteJob(userId: string, jobId: string): Promise<void> {
  await request(`/profile/${userId}/jobs/${jobId}`, { method: 'DELETE' });
}

// Skills
export async function addSkill(userId: string, skill: Omit<Skill, 'id'>): Promise<Skill> {
  return request<Skill>(`/profile/${userId}/skills`, {
    method: 'POST',
    body: JSON.stringify(skill),
  });
}

export async function updateSkill(userId: string, skillId: string, skill: Partial<Skill>): Promise<Skill> {
  return request<Skill>(`/profile/${userId}/skills/${skillId}`, {
    method: 'PUT',
    body: JSON.stringify(skill),
  });
}

export async function deleteSkill(userId: string, skillId: string): Promise<void> {
  await request(`/profile/${userId}/skills/${skillId}`, { method: 'DELETE' });
}

// Projects
export async function addProject(userId: string, project: Omit<Project, 'id'>): Promise<Project> {
  return request<Project>(`/profile/${userId}/projects`, {
    method: 'POST',
    body: JSON.stringify(project),
  });
}

export async function updateProject(userId: string, projectId: string, project: Partial<Project>): Promise<Project> {
  return request<Project>(`/profile/${userId}/projects/${projectId}`, {
    method: 'PUT',
    body: JSON.stringify(project),
  });
}

export async function deleteProject(userId: string, projectId: string): Promise<void> {
  await request(`/profile/${userId}/projects/${projectId}`, { method: 'DELETE' });
}

// Accomplishments
export async function addAccomplishment(userId: string, accomplishment: Omit<Accomplishment, 'id'>): Promise<Accomplishment> {
  return request<Accomplishment>(`/profile/${userId}/accomplishments`, {
    method: 'POST',
    body: JSON.stringify(accomplishment),
  });
}

export async function updateAccomplishment(userId: string, accomplishmentId: string, accomplishment: Partial<Accomplishment>): Promise<Accomplishment> {
  return request<Accomplishment>(`/profile/${userId}/accomplishments/${accomplishmentId}`, {
    method: 'PUT',
    body: JSON.stringify(accomplishment),
  });
}

export async function deleteAccomplishment(userId: string, accomplishmentId: string): Promise<void> {
  await request(`/profile/${userId}/accomplishments/${accomplishmentId}`, { method: 'DELETE' });
}

// Chat
export async function sendChatMessage(userId: string, messages: ChatMessage[]): Promise<ChatResponse> {
  return request<ChatResponse>('/chat', {
    method: 'POST',
    body: JSON.stringify({ userId, messages }),
  });
}
