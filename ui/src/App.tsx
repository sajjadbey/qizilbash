// src/App.tsx
import { useState } from 'react';
import './App.css';
import { tabs } from './tabs';

export default function App() {
  const [activeTabId, setActiveTabId] = useState<string>(tabs[0].id);

  const activeTab = tabs.find(tab => tab.id === activeTabId) || tabs[0];

  return (
    <div className="layout">
      {/* Header */}
      <header className="header">
        <h1>Qizilbash.ir</h1>
        <p>Azerbaijani Language Tools</p>
      </header>

      {/* Main Content (Centered Card) */}
      <main className="card">
        {/* Dynamic Tabs */}
        <div className="tabs">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab ${activeTabId === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTabId(tab.id)}
            >
              {tab.label}
            </button>
          ))}
          {/* Optional: animated indicator (see CSS below) */}
        </div>

        {/* Dynamic Tab Content */}
        <div className="tab-content">
          <activeTab.component />
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>© {new Date().getFullYear()} Qizilbash.ir — Preserving Azerbaijani Heritage</p>
      </footer>
    </div>
  );
}