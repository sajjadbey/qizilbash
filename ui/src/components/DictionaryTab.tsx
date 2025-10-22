import { useState, useEffect } from 'react';

type Word = {
  id: number;
  word: string;
  english_translation: string;
  persian_translation: string;
  meaning_english: string;
  meaning_azerbaijani: string;
  word_type: string;
};

const API_BASE = '/api';

export default function DictionaryTab() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Word[]>([]);
  const [loading, setLoading] = useState(false);

  // Live search with debounce
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
}