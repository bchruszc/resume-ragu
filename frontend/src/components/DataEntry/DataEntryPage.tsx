import { useState, useEffect } from 'react';
import JobForm from './JobForm';
import AccomplishmentForm from './AccomplishmentForm';
import { getProfile } from '../../services/api';
import type { Profile, Job, Accomplishment } from '../../types';

const USER_ID = 'user-1'; // Hardcoded for Phase 1

export default function DataEntryPage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await getProfile(USER_ID);
      setProfile(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfile();
  }, []);

  const handleJobAdded = (job: Job) => {
    if (profile) {
      setProfile({ ...profile, jobs: [...profile.jobs, job] });
    }
  };

  const handleAccomplishmentAdded = (accomplishment: Accomplishment) => {
    if (profile) {
      setProfile({
        ...profile,
        accomplishments: [...profile.accomplishments, accomplishment]
      });
    }
  };

  if (loading) {
    return <div>Loading profile...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Error: {error}</div>;
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Resume Data Entry</h1>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        <div>
          <JobForm userId={USER_ID} onSuccess={handleJobAdded} />
          <AccomplishmentForm userId={USER_ID} onSuccess={handleAccomplishmentAdded} />
        </div>

        <div>
          <h2>Current Profile Data</h2>

          <h3>Jobs ({profile?.jobs.length || 0})</h3>
          {profile?.jobs.length === 0 ? (
            <p style={{ color: '#666' }}>No jobs added yet</p>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {profile?.jobs.map((job) => (
                <li key={job.id} style={{
                  marginBottom: '1rem',
                  padding: '1rem',
                  border: '1px solid #ddd',
                  borderRadius: '4px'
                }}>
                  <strong>{job.title}</strong> at {job.company}
                  <br />
                  <small style={{ color: '#666' }}>
                    {job.startDate} - {job.endDate || 'Present'}
                  </small>
                  {job.description && (
                    <p style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>
                      {job.description}
                    </p>
                  )}
                </li>
              ))}
            </ul>
          )}

          <h3>Accomplishments ({profile?.accomplishments.length || 0})</h3>
          {profile?.accomplishments.length === 0 ? (
            <p style={{ color: '#666' }}>No accomplishments added yet</p>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {profile?.accomplishments.map((acc) => (
                <li key={acc.id} style={{
                  marginBottom: '1rem',
                  padding: '1rem',
                  border: '1px solid #ddd',
                  borderRadius: '4px'
                }}>
                  <strong>{acc.statement}</strong>
                  {acc.context && (
                    <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#666' }}>
                      Context: {acc.context}
                    </p>
                  )}
                  {acc.impact && (
                    <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#666' }}>
                      Impact: {acc.impact}
                    </p>
                  )}
                  {acc.tags && acc.tags.length > 0 && (
                    <div style={{ marginTop: '0.5rem' }}>
                      {acc.tags.map((tag, idx) => (
                        <span
                          key={idx}
                          style={{
                            display: 'inline-block',
                            padding: '0.25rem 0.5rem',
                            marginRight: '0.5rem',
                            backgroundColor: '#e0e0e0',
                            borderRadius: '3px',
                            fontSize: '0.8rem'
                          }}
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
