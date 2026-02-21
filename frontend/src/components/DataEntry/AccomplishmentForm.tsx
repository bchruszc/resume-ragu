import { useState, type FormEvent } from 'react';
import { addAccomplishment } from '../../services/api';
import type { Accomplishment } from '../../types';

interface AccomplishmentFormProps {
  userId: string;
  onSuccess: (accomplishment: Accomplishment) => void;
}

export default function AccomplishmentForm({ userId, onSuccess }: AccomplishmentFormProps) {
  const [statement, setStatement] = useState('');
  const [context, setContext] = useState('');
  const [impact, setImpact] = useState('');
  const [tags, setTags] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const accomplishment = await addAccomplishment(userId, {
        statement,
        context: context || undefined,
        impact: impact || undefined,
        tags: tags ? tags.split(',').map(t => t.trim()).filter(Boolean) : undefined,
      });

      setSuccess(true);
      onSuccess(accomplishment);

      // Reset form
      setStatement('');
      setContext('');
      setImpact('');
      setTags('');

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add accomplishment');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
      <h3>Add Accomplishment</h3>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Statement *
          <textarea
            value={statement}
            onChange={(e) => setStatement(e.target.value)}
            placeholder="What you accomplished (e.g., Reduced API response time by 40%)"
            required
            rows={2}
            style={{ display: 'block', width: '100%', marginTop: '0.25rem' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Context
          <textarea
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="The situation or problem (optional)"
            rows={2}
            style={{ display: 'block', width: '100%', marginTop: '0.25rem' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Impact
          <textarea
            value={impact}
            onChange={(e) => setImpact(e.target.value)}
            placeholder="The result or outcome (optional)"
            rows={2}
            style={{ display: 'block', width: '100%', marginTop: '0.25rem' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Tags (comma-separated)
          <input
            type="text"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            placeholder="e.g., backend, performance, API"
            style={{ display: 'block', width: '100%', marginTop: '0.25rem' }}
          />
        </label>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Adding...' : 'Add Accomplishment'}
      </button>

      {success && (
        <div style={{ color: 'green', marginTop: '0.5rem' }}>
          Accomplishment added successfully!
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
