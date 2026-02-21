export interface Contact {
  email: string;
  phone?: string;
  location?: string;
  linkedin?: string;
  github?: string;
}

export interface User {
  id: string;
  name: string;
  contact: Contact;
  summary?: string;
}

export interface Job {
  id: string;
  company: string;
  title: string;
  startDate: string;
  endDate?: string;
  description?: string;
  highlights?: string[];
}

export interface Skill {
  id: string;
  name: string;
  category: string;
  proficiency?: string;
  yearsOfExperience?: number;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  jobIds?: string[];
  skillIds?: string[];
  outcome?: string;
}

export interface Accomplishment {
  id: string;
  statement: string;
  context?: string;
  impact?: string;
  jobIds?: string[];
  projectIds?: string[];
  skillIds?: string[];
  tags?: string[];
}

export interface Profile {
  user: User;
  jobs: Job[];
  skills: Skill[];
  projects: Project[];
  accomplishments: Accomplishment[];
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  userId: string;
  messages: ChatMessage[];
}

export interface ChatResponse {
  message: ChatMessage;
  usage?: {
    inputTokens: number;
    outputTokens: number;
  };
}

export interface ApiError {
  error: {
    code: string;
    message: string;
  };
}
