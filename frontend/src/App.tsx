import { useState } from 'react';
import './App.css';
import DataEntryPage from './components/DataEntry/DataEntryPage';
import ChatPage from './components/Chat/ChatPage';

type Page = 'data-entry' | 'chat';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('data-entry');

  return (
    <div>
      {/* Simple tab navigation */}
      <nav style={{
        backgroundColor: '#2c3e50',
        padding: '1rem',
        display: 'flex',
        gap: '1rem'
      }}>
        <button
          onClick={() => setCurrentPage('data-entry')}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: currentPage === 'data-entry' ? '#3498db' : '#34495e',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '1rem',
            fontWeight: currentPage === 'data-entry' ? 'bold' : 'normal'
          }}
        >
          Data Entry
        </button>
        <button
          onClick={() => setCurrentPage('chat')}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: currentPage === 'chat' ? '#3498db' : '#34495e',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '1rem',
            fontWeight: currentPage === 'chat' ? 'bold' : 'normal'
          }}
        >
          Resume Chat
        </button>
      </nav>

      {/* Page content */}
      {currentPage === 'data-entry' ? <DataEntryPage /> : <ChatPage />}
    </div>
  );
}

export default App;
