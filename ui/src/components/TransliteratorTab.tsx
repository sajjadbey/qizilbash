// src/components/TransliteratorTab.tsx
import { useState, useEffect } from 'react';

export default function TransliteratorTab() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Debounced live transliteration
  useEffect(() => {
    if (!inputText.trim()) {
      setOutputText('');
      setError(null);
      return;
    }

    const timer = setTimeout(() => {
      setLoading(true);
      setError(null);

      // URL-encode the text (handles ə, ş, etc.)
      const encodedText = encodeURIComponent(inputText);
      const url = `/api/convert/?text=${encodedText}&source=latin&target=arabic`;

      fetch(url)
        .then(res => {
          if (!res.ok) throw new Error('API error');
          return res.json();
        })
        .then(data => {
          setOutputText(data.result || '');
          setLoading(false);
        })
        .catch(err => {
          console.error('Transliteration failed:', err);
          setError('Failed to transliterate. Please try again.');
          setOutputText('');
          setLoading(false);
        });
    }, 300); // 300ms debounce

    return () => clearTimeout(timer);
  }, [inputText]);

  return (
    <div className="transliterator">
      <h3 className="transliterator-title">Azerbaijani Transliterator</h3>
      <p className="transliterator-desc">
        Type in Latin Azerbaijani — see real-time conversion to Arabic script.
      </p>
      <p className="transliterator-desc">
        Under Development ! ⚠️
      </p>

      <div className="transliterator-grid">
        {/* Input */}
        <div className="transliterator-panel">
          <label htmlFor="latin-input" className="panel-label">Latin Script</label>
          <textarea
            id="latin-input"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="e.g. səlâm, şəhər, dıl..."
            className="transliterator-input"
            dir="ltr"
            lang="az"
          />
        </div>

        {/* Output */}
        <div className="transliterator-panel">
          <label htmlFor="arabic-output" className="panel-label">Arabic Script</label>
          <textarea
            id="arabic-output"
            value={outputText}
            readOnly
            placeholder={loading ? 'Converting...' : 'Result will appear here'}
            className="transliterator-output"
            dir="rtl"
            lang="az-Arab"
          />
        </div>
      </div>

      {error && <div className="transliterator-error">{error}</div>}
      
      <div className="transliterator-hint">
        Supports: <code>ə, ş, ğ, ç, ö, ü, ı</code>
      </div>
    </div>
  );
}