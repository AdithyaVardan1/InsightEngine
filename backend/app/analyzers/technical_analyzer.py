"""
Technical SEO Analyzer - Check meta tags and technical elements
"""
import re
from typing import Dict, Any
from bs4 import BeautifulSoup


def analyze_technical(html: str) -> Dict[str, Any]:
    """Analyze technical SEO elements"""
    issues = []
    recommendations = []
    
    soup = BeautifulSoup(html, "html.parser")
    
    # Check meta title
    title_tag = soup.find("title")
    has_title = title_tag is not None and len(title_tag.get_text(strip=True)) > 0
    
    if has_title:
        title_text = title_tag.get_text(strip=True)
        if len(title_text) < 30:
            issues.append(f"Title tag is short ({len(title_text)} chars)")
            recommendations.append("Expand title to 50-60 characters for better visibility")
        elif len(title_text) > 60:
            issues.append(f"Title tag may be truncated ({len(title_text)} chars)")
        else:
            issues.append("✓ Good title length")
    else:
        issues.append("Missing title tag")
        recommendations.append("Add a descriptive title tag")
    
    # Check meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    has_description = meta_desc is not None and meta_desc.get("content")
    
    if has_description:
        desc_len = len(meta_desc["content"])
        if desc_len < 120:
            issues.append(f"Meta description is short ({desc_len} chars)")
            recommendations.append("Expand meta description to 150-160 characters")
        elif desc_len > 160:
            issues.append(f"Meta description may be truncated ({desc_len} chars)")
        else:
            issues.append("✓ Good meta description length")
    else:
        issues.append("Missing meta description")
        recommendations.append("Add a compelling meta description")
    
    # Check canonical
    canonical = soup.find("link", attrs={"rel": "canonical"})
    has_canonical = canonical is not None and canonical.get("href")
    
    if has_canonical:
        issues.append("✓ Canonical URL present")
    else:
        recommendations.append("Add a canonical URL to prevent duplicate content issues")
    
    # Check Open Graph
    og_title = soup.find("meta", attrs={"property": "og:title"})
    og_desc = soup.find("meta", attrs={"property": "og:description"})
    has_og = og_title is not None or og_desc is not None
    
    if has_og:
        issues.append("✓ Open Graph tags present")
    else:
        recommendations.append("Add Open Graph meta tags for better social sharing")
    
    # Check Twitter Card
    twitter_card = soup.find("meta", attrs={"name": "twitter:card"})
    has_twitter = twitter_card is not None
    
    if has_twitter:
        issues.append("✓ Twitter Card meta present")
    else:
        recommendations.append("Add Twitter Card meta tags")
    
    # Check if SSR (simple heuristic: meaningful content in initial HTML)
    text_content = soup.get_text(strip=True)
    is_ssr = len(text_content) > 500  # If significant text in HTML, likely SSR
    
    if is_ssr:
        issues.append("✓ Content appears server-rendered (good for AI crawlers)")
    else:
        issues.append("Page may be client-rendered (limited text in initial HTML)")
        recommendations.append("Consider server-side rendering for better AI accessibility")
    
    # Calculate score
    score = 30  # Base
    
    if has_title:
        score += 15
    if has_description:
        score += 15
    if has_canonical:
        score += 10
    if has_og:
        score += 10
    if has_twitter:
        score += 5
    if is_ssr:
        score += 15
    
    score = min(100, max(0, score))
    
    return {
        "has_meta_title": has_title,
        "has_meta_description": has_description,
        "has_canonical": has_canonical,
        "has_open_graph": has_og,
        "has_twitter_card": has_twitter,
        "is_ssr": is_ssr,
        "score": score,
        "issues": issues,
        "recommendations": recommendations
    }
