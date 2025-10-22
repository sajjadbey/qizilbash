// src/App.tsx
import { useState } from 'react';
import './App.css';
import DictionaryTab from './components/DictionaryTab';
import TransliteratorTab from './components/TransliteratorTab';

export default function App() {
  const [activeTab, setActiveTab] = useState<'dictionary' | 'transliterator'>('dictionary');

  return (
    <div className="layout">
      {/* Header */}
      <header className="header">
        <h1>Qizilbash.ir</h1>
        <p>Azerbaijani Language Tools</p>
      </header>

      {/* Main Content (Centered Card) */}
      <main className="card">
        {/* Tabs */}
        <div className="tabs">
          <button
            className={activeTab === 'dictionary' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('dictionary')}
          >
            Dictionary
          </button>
          <button
            className={activeTab === 'transliterator' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('transliterator')}
          >
            Transliterator
          </button>
          <div className="tab-indicator"></div>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'dictionary' && <DictionaryTab />}
          {activeTab === 'transliterator' && <TransliteratorTab />}
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>© {new Date().getFullYear()} Qizilbash.ir — Preserving Azerbaijani Heritage</p>
      </footer>
    </div>
  );
}