import { useState, type FormEvent } from 'react';
import { addJob } from '../../services/api';
import type { Job } from '../../types';

interface JobFormProps {
  userId: string;
  onSuccess: (job: Job) => void;
}

export default function JobForm({ userId, onSuccess }: JobFormProps) {
  const [company, setCompany] = useState('');
  const [title, setTitle] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const job = await addJob(userId, {
        company,
        title,
        startDate,
        endDate: endDate || undefined,
        description: description || undefined,
      });

      setSuccess(true);
      onSuccess(job);

      // Reset form
      setCompany('');
      setTitle('');
      setStartDate('');
      setEndDate('');
      setDescription('');

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add job');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
      <h3>Add Job</h3>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Company *
          <input
            type="text"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            required
            style={{ display: 'block', width: '100%', marginTop: '0.25rem' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Title *
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            style={{ display: 'block', width: '100%', marginTop: '0.25rem' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Start Date *
          <input
            type="text"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            placeholder="e.g., 2020-01 or Jan 2020"
            required
            style={{ display: 'block', width: '100%', marginTop: '0.25rem' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          End Date (leave blank if current)
          <input
            type="text"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            placeholder="e.g., 2022-06 or Jun 2022"
            style={{ display: 'block', width: '100%', marginTop: '0.25rem' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Description
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            style={{ display: 'block', width: '100%', marginTop: '0.25rem' }}
          />
        </label>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Adding...' : 'Add Job'}
      </button>

      {success && (
        <div style={{ color: 'green', marginTop: '0.5rem' }}>
          Job added successfully!
        </div>
      )}

      {error && (
        <div style={{ color: 'red', marginTop: '0.5rem' }}>
          Error: {error}
        </div>
      )}
    </form>
  );
}
