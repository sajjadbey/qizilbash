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
    <div className="w-full">
      {/* Search Input */}
      <input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search words (e.g. səlâm)…"
        className="
          w-full px-4 py-3 text-lg rounded-xl 
          bg-[#0c2238]/60 border border-[#2b465e] 
          text-white placeholder-blue-300
          focus:outline-none focus:ring-2 focus:ring-yellow-400
          transition
        "
        autoFocus
      />

      {/* Status Messages */}
      {loading && query && (
        <div className="text-center text-blue-300 mt-4 italic">
          Searching…
        </div>
      )}

      {!loading && results.length === 0 && query && (
        <div className="text-center text-red-400 mt-4 italic">
          No results for "{query}"
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div
          className="
            mt-5 max-h-[600px] overflow-y-auto space-y-4 pr-2
            scrollbar-thin scrollbar-thumb-yellow-500 
            scrollbar-track-blue-900/40
          "
        >
          {results.map(word => (
            <div
              key={word.id}
              className="
                bg-[#0b1c30]/70 p-5 rounded-xl border-l-4 border-yellow-400 
                shadow-lg hover:bg-[#0f2a46]/70 transition
              "
            >
              {/* Header */}
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-2xl font-bold text-yellow-400">
                  {word.word}
                </h3>
                <span
                  className="
                    px-3 py-1 rounded-full text-sm 
                    bg-red-900/40 text-yellow-300 capitalize
                  "
                >
                  {word.word_type}
                </span>
              </div>

              {/* Meaning */}
              {word.meaning_azerbaijani && (
                <p className="text-gray-200 leading-relaxed mb-3">
                  {word.meaning_azerbaijani}
                </p>
              )}

              {/* Translations */}
              {(word.english_translation || word.persian_translation) && (
                <div className="space-y-1 text-base">
                  {word.english_translation && (
                    <div className="text-white/90">
                      <span className="font-semibold text-blue-300 mr-2">
                        EN:
                      </span>
                      {word.english_translation}
                    </div>
                  )}
                  {word.persian_translation && (
                    <div className="text-white/90">
                      <span className="font-semibold text-yellow-300 mr-2">
                        FA:
                      </span>
                      {word.persian_translation}
                    </div>
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
