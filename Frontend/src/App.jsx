import { useState } from 'react';
import './App.css';

function App() {
  const [review, setReview] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!review.trim()) return;

    setIsLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const API_BASE_URL = import.meta.env.VITE_API_URL;
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ review }),
      });

      if (!response.ok) {
        throw new Error(`Server returned status: ${response.status}`);
      }

      const data = await response.json();
      setPrediction(data.result);
    } catch (err) {
      console.error('API Error:', err);
      setError(err.message || 'Something went wrong. Make sure backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const getPredictionClass = (pred) => {
    if (!pred) return '';
    return `badge-${pred.toLowerCase()}`;
  };

  return (
    <div className="container">
      <header className="header">
        <h1 id="app-title">DriveInsight</h1>
        <p className="subtitle">AI-Powered Vehicle Review Sentiment Analysis</p>
      </header>

      <main className="main-content">
        <div className="card">
          <h2>Predict Review Sentiment</h2>
          <p className="card-description">
            Type or paste a vehicle review below. Our backend will trigger a Python script that analyzes the text and classifies it as Positive or Negative.
          </p>

          <form onSubmit={handleSubmit} className="prediction-form">
            <div className="form-group">
              <label htmlFor="review-input" className="form-label">
                Vehicle Review
              </label>
              <textarea
                id="review-input"
                name="review"
                value={review}
                onChange={(e) => setReview(e.target.value)}
                placeholder="E.g., I love my new SUV! The ride is extremely smooth, fuel efficiency is outstanding, and the cabin is quiet and spacious..."
                rows="6"
                disabled={isLoading}
                required
              />
            </div>

            <button
              id="submit-btn"
              type="submit"
              className={`submit-btn ${isLoading ? 'btn-loading' : ''}`}
              disabled={isLoading || !review.trim()}
            >
              {isLoading ? (
                <>
                  <span className="spinner"></span>
                  Processing with AI...
                </>
              ) : (
                'Analyze Sentiment'
              )}
            </button>
          </form>

          {/* Results section */}
          {(prediction || isLoading || error) && (
            <div className="results-container">
              {isLoading && (
                <div className="loading-state">
                  <div className="pulse-loader"></div>
                  <p>Spawning Python backend models...</p>
                </div>
              )}

              {error && (
                <div className="error-state" id="error-message">
                  <div className="error-icon">⚠️</div>
                  <div className="error-text">
                    <strong>Error:</strong> {error}
                  </div>
                </div>
              )}

              {prediction && (
                <div className="success-state" id="prediction-result">
                  <span className="result-label">Result:</span>
                  <div className={`result-badge ${getPredictionClass(prediction)}`}>
                    {prediction}
                  </div>
                  <p className="result-message">
                    {prediction === 'Positive' && '🎉 This review highlights positive aspects of the vehicle.'}
                    {prediction === 'Negative' && '⚠️ This review expresses issues or negative experiences.'}
                    {prediction === 'Neutral' && '⚖️ This review is balanced or lacks strong sentiment terms.'}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        <p>
          Created by Sasanka Madhumal
        </p>
      </footer>
    </div>
  );
}

export default App;
