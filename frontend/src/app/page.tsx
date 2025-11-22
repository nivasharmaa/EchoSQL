"use client";

import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000/api";

type RunSQLResponse = {
  columns: string[];
  rows: unknown[][];
};

export default function HomePage() {
  const [question, setQuestion] = useState("");
  const [generatedSQL, setGeneratedSQL] = useState("");
  const [result, setResult] = useState<RunSQLResponse | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerateSQL() {
    if (!question.trim()) return;
    setIsGenerating(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(`${API_BASE}/sql/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        const body = await res.text();
        throw new Error(`Generate failed: ${res.status} ${body}`);
      }

      const data = await res.json();
      setGeneratedSQL(data.sql || "");
    } catch (e: unknown) {
      if (e instanceof Error) {
        setError(e.message);
      }else{
        setError("Something went wrong");
      }
    } finally {
      setIsGenerating(false);
    }
  }

  async function handleRunSQL() {
    if (!generatedSQL.trim()) return;
    setIsRunning(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE}/run-sql`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sql: generatedSQL }),
      });

      if (!res.ok) {
        const body = await res.text();
        throw new Error(`Run failed: ${res.status} ${body}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (e: unknown) {
      if (e instanceof Error) {
        setError(e.message);
      }else{
        setError("Something went wrong");
      }
    } finally {
      setIsRunning(false);
    }
  }

  const buttonBase =
    "rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed";

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex max-w-5xl flex-col gap-6 px-4 py-8">
        <header>
          <h1 className="text-2xl font-semibold">EchoSQL</h1>
          <p className="mt-1 text-sm text-slate-400">
            Ask a question in natural language, generate SQL, and run it against the demo database.
          </p>
        </header>

        {/* Error banner */}
        {error && (
          <div className="rounded-md border border-red-500 bg-red-950/40 px-3 py-2 text-sm text-red-200">
            {error}
          </div>
        )}

        {/* Question + Generate */}
        <section className="grid gap-4 md:grid-cols-[2fr,auto] md:items-end">
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium text-slate-200">
              Ask a question about the database
            </label>
            <textarea
              className="min-h-[80px] rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 outline-none focus:border-blue-500"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder='e.g. "List all customers who have placed more than 3 orders."'
            />
          </div>
          <button
            className={buttonBase}
            onClick={handleGenerateSQL}
            disabled={isGenerating || !question.trim()}
          >
            {isGenerating ? "Generating…" : "Generate SQL"}
          </button>
        </section>

        {/* Generated SQL + Run */}
        <section className="grid gap-4 md:grid-cols-[2fr,auto] md:items-end">
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium text-slate-200">Generated SQL</label>
            <textarea
              className="min-h-[120px] rounded-md border border-slate-700 bg-slate-900 px-3 py-2 font-mono text-sm text-slate-100 outline-none focus:border-blue-500"
              value={generatedSQL}
              onChange={(e) => setGeneratedSQL(e.target.value)}
              placeholder="Generated SQL will appear here..."
            />
          </div>
          <button
            className={buttonBase}
            onClick={handleRunSQL}
            disabled={isRunning || !generatedSQL.trim()}
          >
            {isRunning ? "Running…" : "Run SQL"}
          </button>
        </section>

        {/* Results */}
        <section className="flex flex-col gap-2">
          <h2 className="text-sm font-medium text-slate-200">Query Results</h2>
          {!result && <p className="text-sm text-slate-500">No results yet.</p>}

          {result && result.columns.length === 0 && (
            <p className="text-sm text-slate-400">Query returned no rows.</p>
          )}

          {result && result.columns.length > 0 && (
            <div className="overflow-auto rounded-md border border-slate-800 bg-slate-900">
              <table className="min-w-full text-left text-sm">
                <thead className="bg-slate-800/60">
                  <tr>
                    {result.columns.map((col) => (
                      <th key={col} className="px-3 py-2 font-semibold text-slate-100">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.rows.map((row, idx) => (
                    <tr key={idx} className={idx % 2 === 0 ? "bg-slate-900" : "bg-slate-900/60"}>
                      {row.map((cell, i) => (
                        <td key={i} className="px-3 py-2 text-slate-200">
                          {String(cell)}
                        </td>
                      ))}
                  </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
