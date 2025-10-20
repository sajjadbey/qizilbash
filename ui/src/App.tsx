import { useState, useEffect } from 'react';
import './App.css';

type Word = {
  id: number;
  word: string;
  english_translation: string;
  persian_translation: string;
  meaning_english: string;
  meaning_azerbaijani: string;
  word_type: string;
};

const API_BASE = 'http://127.0.0.1:8000/api';

export default function App() {
  const [activeTab, setActiveTab] = useState<'dictionary' | 'transliterator'>('dictionary');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Word[]>([]);
  const [loading, setLoading] = useState(false);

  // Live search
  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    const timer = setTimeout(() => {
      setLoading(true);
      fetch(`${API_BASE}/search/?text=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
          setResults(data);
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

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
          {activeTab === 'dictionary' && (
            <DictionaryTab query={query} setQuery={setQuery} results={results} loading={loading} />
          )}
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

const DictionaryTab = ({ query, setQuery, results, loading }: { 
  query: string; 
  setQuery: (q: string) => void; 
  results: Word[]; 
  loading: boolean; 
}) => (
  <div className="dictionary">
    <input
      type="text"
      value={query}
      onChange={e => setQuery(e.target.value)}
      placeholder="Search words (e.g. səlâm)…"
      className="search-input"
      autoFocus
    />

    {loading && query && <div className="status">Searching…</div>}
    {!loading && results.length === 0 && query && (
      <div className="status empty">No results for "{query}"</div>
    )}

    {results.length > 0 && (
      <div className="results">
        {results.map(word => (
          <div key={word.id} className="word-item">
            <div className="word-header">
              <h3 className="word">{word.word}</h3>
              <span className="type">{word.word_type}</span>
            </div>
            {word.meaning_azerbaijani && (
              <p className="meaning">{word.meaning_azerbaijani}</p>
            )}
            {(word.english_translation || word.persian_translation) && (
              <div className="translations">
                {word.english_translation && (
                  <div><span className="label en">EN:</span> {word.english_translation}</div>
                )}
                {word.persian_translation && (
                  <div><span className="label fa">FA:</span> {word.persian_translation}</div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    )}
  </div>
);

const TransliteratorTab = () => (
  <div className="transliterator">
    <h3>Transliterator</h3>
    <p>Convert between Latin, Cyrillic, and Arabic scripts for Azerbaijani.</p>
    <div className="placeholder">Coming soon…</div>
  </div>
);