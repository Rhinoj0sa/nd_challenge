import React, { useState } from "react";
import "./App.css"; // <-- Import the CSS file

function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);
    setFilename(selected ? selected.name : "");
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    const url = "http://localhost:8000/extract_entities/";

    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ error: "Upload failed" });
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <h2>Extract Entities from Document</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        {filename && (
          <div className="selected-file">
            Selected file: <b>{filename}</b>
          </div>
        )}
        <button type="submit" disabled={!file || loading}>
          {loading ? "Uploading..." : "Extract"}
        </button>
      </form>
      {result && (
        <div className="result-container">
          <h3>Result:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;