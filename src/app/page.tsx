'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setIsLoading(true);

    // Navigate to results page with URL as query param
    const encodedUrl = encodeURIComponent(url.trim());
    router.push(`/analyze?url=${encodedUrl}`);
  };

  return (
    <div className="container">
      {/* Navigation */}
      <nav className="nav">
        <div className="logo">
          <div className="logo-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
          </div>
          InsightEngine
        </div>
        <ul className="nav-links">
          <li><a href="#features">Features</a></li>
          <li><a href="#how-it-works">How it Works</a></li>
          <li><a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a></li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="badge">
          <span className="badge-dot"></span>
          AI-Powered SEO Analysis
        </div>

        <h1>
          Is Your Website Ready for{' '}
          <span className="gradient-text">AI Search?</span>
        </h1>

        <p className="hero-desc">
          Analyze how well your website is optimized for ChatGPT, Perplexity, Google AI Overviews,
          and other AI-powered search engines. Get actionable recommendations powered by AI.
        </p>

        <form className="url-form" onSubmit={handleSubmit}>
          <input
            type="url"
            className="url-input"
            placeholder="Enter your website URL (e.g., https://example.com)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
          />
          <button
            type="submit"
            className="analyze-btn"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              'Analyze Now'
            )}
          </button>
        </form>
      </section>

      {/* Features Section */}
      <section className="features" id="features">
        <h2 className="features-title">What We Analyze</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI Crawler Access</h3>
            <p>Check if your robots.txt allows GPTBot, ClaudeBot, PerplexityBot, and other AI crawlers to access your content.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Structured Data</h3>
            <p>Validate your JSON-LD schema markup to ensure AI systems can accurately extract and understand your content.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📝</div>
            <h3>Content Structure</h3>
            <p>Analyze your heading hierarchy, FAQ sections, and answer-first content patterns for LLM extractability.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Technical SEO</h3>
            <p>Evaluate meta tags, semantic HTML, and page accessibility for optimal AI crawling and indexing.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📄</div>
            <h3>llms.txt Detection</h3>
            <p>Check for the emerging llms.txt standard - the robots.txt equivalent for AI assistants.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">✨</div>
            <h3>AI Recommendations</h3>
            <p>Get personalized, AI-generated suggestions to improve your content&apos;s visibility in AI search results.</p>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="stats">
        <div className="stat">
          <div className="stat-value">5</div>
          <div className="stat-label">Analysis Categories</div>
        </div>
        <div className="stat">
          <div className="stat-value">6+</div>
          <div className="stat-label">AI Crawlers Checked</div>
        </div>
        <div className="stat">
          <div className="stat-value">∞</div>
          <div className="stat-label">Free Analyses</div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <p>Built with ❤️ for the AI-first web • InsightEngine © 2024</p>
      </footer>
    </div>
  );
}
