// src/App.tsx
import { useState } from 'react';
import { tabs } from './tabs';

export default function App() {
  const [activeTabId, setActiveTabId] = useState<string>(tabs[0].id);

  const activeTab = tabs.find(tab => tab.id === activeTabId) || tabs[0];

  return (
    <div className="min-h-screen w-full flex flex-col items-center px-4 py-10 bg-[#071421] text-white">

      {/* Header */}
      <header className="text-center mb-10 max-w-xl">
        <h1 
          className="
            text-4xl md:text-5xl font-extrabold 
            bg-gradient-to-r from-yellow-400 to-cyan-400 
            text-transparent bg-clip-text
          "
        >
          Qizilbash.ir
        </h1>
        <p className="text-blue-300 mt-3 text-lg">Azerbaijani Language Tools</p>
      </header>

      {/* Main Card */}
      <main
        className="
          w-full max-w-3xl 
          bg-[#0b1c30]/70 backdrop-blur 
          rounded-2xl shadow-2xl 
          border border-white/10 
          flex flex-col overflow-hidden
        ">
        <div className="flex w-full border-b border-white/10">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTabId(tab.id)}
              className={`
                flex-1 px-4 py-4 text-center font-medium 
                transition relative whitespace-nowrap
                ${activeTabId === tab.id
                  ? "text-yellow-300"
                  : "text-blue-300 hover:text-yellow-300"}
              `}
            >
              {tab.label}

              {/* Underline */}
              <span
                className={`
                  absolute left-1/2 -bottom-1 h-[3px] w-0 
                  bg-yellow-300 rounded-full transition-all 
                  ${activeTabId === tab.id ? "w-2/3 -translate-x-1/2" : ""}
                `}
              ></span>
            </button>
          ))}
      </div>

        {/* Tab Content */}
        <div className="p-6 md:p-8">
          <activeTab.component />
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-10 text-blue-300 text-sm text-center">
        © {new Date().getFullYear()} Qizilbash.ir — Preserving Azerbaijani Heritage
      </footer>
    </div>
  );
}
