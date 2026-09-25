import { useState } from "react";
import "./App.css";
import "./index.css";

const API_URL = "http://localhost:8000";

function App() {
  const [query, setQuery] = useState("");
  const [file, setFile] = useState(null);

  async function handleClick() {
    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();

      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  async function handleUploadClick() {
    try {
      if (!file) return;

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/api/upload_docs`, {
        method: "POST",
        body: formData,
      });

      if (response) {
        console.log(response);
      }
    } catch (error) {
      console.log(error);
    }
  }

  function handleFileChange(e) {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) return;

    setFile(selectedFile);
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
          <label className="upload-label" htmlFor="policy-documents">
            Upload documents
          </label>
          <input
            id="policy-documents"
            className="upload-input"
            type="file"
            onChange={handleFileChange}
          />
          <button
            className="upload-button"
            type="button"
            onClick={handleUploadClick}
            disabled={!file}
          >
            Upload
          </button>
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
