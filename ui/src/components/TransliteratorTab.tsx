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
    }, 300);

    return () => clearTimeout(timer);
  }, [inputText]);

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white dark:bg-gray-900 rounded-xl shadow-lg space-y-6">
      <div className="text-center space-y-2">
        <h3 className="text-2xl font-bold text-gray-800 dark:text-white">
          Azerbaijani Transliterator
        </h3>
        <p className="text-gray-600 dark:text-gray-300">
          Type in Latin Azerbaijani and see real-time conversion to Arabic script.
        </p>
        <p className="text-yellow-600 dark:text-yellow-400 font-medium">
          Under Development ⚠️
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Input */}
        <div className="flex flex-col">
          <label htmlFor="latin-input" className="mb-2 font-semibold text-gray-700 dark:text-gray-200">
            Latin Script
          </label>
          <textarea
            id="latin-input"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="e.g. səlâm, şəhər, dıl..."
            className="resize-none p-4 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 dark:bg-gray-800 dark:text-white transition-all min-h-[120px]"
            dir="ltr"
            lang="az"
          />
        </div>

        {/* Output */}
        <div className="flex flex-col">
          <label htmlFor="arabic-output" className="mb-2 font-semibold text-gray-700 dark:text-gray-200">
            Arabic Script
          </label>
          <textarea
            id="arabic-output"
            value={outputText}
            readOnly
            placeholder={loading ? 'Converting...' : 'Result will appear here'}
            className={`resize-none p-4 border rounded-lg shadow-sm min-h-[120px] transition-all
              ${loading ? 'bg-gray-100 dark:bg-gray-800 text-gray-400' : 'bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-white'}
              border-gray-300 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-400`}
            dir="rtl"
            lang="az-Arab"
          />
        </div>
      </div>

      {error && (
        <div className="text-red-600 dark:text-red-400 font-medium text-center">
          {error}
        </div>
      )}

      <div className="text-sm text-gray-500 dark:text-gray-400 text-center">
        Supports: <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">ə, ş, ğ, ç, ö, ü, ı</code>
      </div>
    </div>
  );
}
