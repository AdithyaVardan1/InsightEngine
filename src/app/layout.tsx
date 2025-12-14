import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "InsightEngine - AI SEO Analyzer | Optimize for AI Search",
  description: "Analyze your website's AI SEO readiness. Get actionable recommendations to optimize for ChatGPT, Perplexity, Google AI Overviews, and more AI-powered search engines.",
  keywords: ["AI SEO", "GEO", "Generative Engine Optimization", "ChatGPT SEO", "Perplexity SEO", "LLM optimization"],
  openGraph: {
    title: "InsightEngine - AI SEO Analyzer",
    description: "Is your website ready for AI-powered search? Find out now.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="bg-pattern">
          <div className="bg-grid" />
        </div>
        {children}
      </body>
    </html>
  );
}
