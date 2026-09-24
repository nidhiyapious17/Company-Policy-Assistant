import { useState } from "react";
import "./App.css";
import "./index.css";

function App() {
  const [query, setQuery] = useState("");

  async function handleClick(e) {
    try {
      console.log("Call api");
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <main className="policy-app">
      <div className="policy-grid" />
      <div className="policy-glow policy-glow-left" />
      <div className="policy-glow policy-glow-right" />

      <section className="policy-card">
        <div className="policy-header">
          <div className="policy-meta">
            <span className="policy-kicker">
              <span className="policy-status-dot" />
              Internal knowledge
            </span>
            <span className="policy-badge">Secure</span>
          </div>
          <h2 className="policy-title">Company Policy Assistant</h2>
          <p className="policy-description">
            Answers are only based on approved company policies
          </p>
        </div>

        <div className="policy-form">
          <label className="policy-label" htmlFor="policy-question">
            Your question
          </label>
          <textarea
            id="policy-question"
            className="policy-textarea"
            placeholder="Ask your question"
            onChange={(e) => setQuery(e.target.value)}
          ></textarea>

          <div className="policy-actions">
            <span className="policy-hint">Search approved guidance</span>
            <button
              className="policy-button"
              onClick={handleClick}
              disabled={!query.trim()}
            >
              Send
              <span aria-hidden="true" className="text-lg leading-none">
                -&gt;
              </span>
            </button>
          </div>
        </div>
      </section>
    </main>
  );
}

export default App;
