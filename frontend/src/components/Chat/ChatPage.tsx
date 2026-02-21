import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { sendChatMessage } from '../../services/api';
import type { ChatMessage } from '../../types';

const USER_ID = 'user-1'; // Hardcoded for Phase 1

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: input.trim()
    };

    // Add user message to conversation
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      // Send full conversation history to backend
      const response = await sendChatMessage(USER_ID, updatedMessages);

      // Add AI response to conversation
      setMessages([...updatedMessages, response.message]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get response');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto', height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <h1>Resume Generation Chat</h1>

      {messages.length === 0 && (
        <div style={{ padding: '2rem', backgroundColor: '#f5f5f5', borderRadius: '8px', marginBottom: '1rem' }}>
          <h3>Welcome to Resume Ragu!</h3>
          <p>
            Start by asking me to generate a resume based on your profile data.
            For example:
          </p>
          <ul>
            <li>"Generate a resume for me"</li>
            <li>"Create a resume highlighting my backend experience"</li>
            <li>"I need a resume for a senior software engineer role"</li>
          </ul>
          <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#666' }}>
            Make sure you've added at least one job and accomplishment in the Data Entry page first!
          </p>
        </div>
      )}

      {/* Conversation history */}
      <div style={{ flex: 1, overflowY: 'auto', marginBottom: '1rem', border: '1px solid #ddd', borderRadius: '8px', padding: '1rem' }}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              marginBottom: '1.5rem',
              padding: '1rem',
              backgroundColor: msg.role === 'user' ? '#e3f2fd' : '#f5f5f5',
              borderRadius: '8px',
              borderLeft: `4px solid ${msg.role === 'user' ? '#2196f3' : '#4caf50'}`
            }}
          >
            <div style={{ fontWeight: 'bold', marginBottom: '0.5rem', color: '#333' }}>
              {msg.role === 'user' ? 'You' : 'AI Assistant'}
            </div>
            {msg.role === 'assistant' ? (
              <div style={{
                fontSize: '0.95rem',
                lineHeight: '1.6',
              }}>
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              </div>
            ) : (
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.95rem' }}>
                {msg.content}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div style={{
            padding: '1rem',
            backgroundColor: '#f5f5f5',
            borderRadius: '8px',
            borderLeft: '4px solid #4caf50'
          }}>
            <div style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>
              AI Assistant
            </div>
            <div style={{ color: '#666' }}>
              Thinking...
            </div>
          </div>
        )}
      </div>

      {/* Error display */}
      {error && (
        <div style={{
          padding: '1rem',
          backgroundColor: '#ffebee',
          color: '#c62828',
          borderRadius: '4px',
          marginBottom: '1rem'
        }}>
          Error: {error}
        </div>
      )}

      {/* Input area */}
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message... (Shift+Enter for new line, Enter to send)"
          disabled={loading}
          rows={3}
          style={{
            flex: 1,
            padding: '0.75rem',
            borderRadius: '4px',
            border: '1px solid #ddd',
            fontSize: '1rem',
            resize: 'vertical'
          }}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: loading || !input.trim() ? '#ccc' : '#2196f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
            fontSize: '1rem',
            fontWeight: 'bold'
          }}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
