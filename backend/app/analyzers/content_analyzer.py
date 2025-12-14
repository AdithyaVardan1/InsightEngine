"""
Content Analyzer - Check content structure for AI extractability
"""
import re
from typing import Dict, List, Any
from bs4 import BeautifulSoup


def analyze_content(html: str) -> Dict[str, Any]:
    """Analyze HTML content structure for AI readability"""
    issues = []
    recommendations = []
    
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Check for H1
    h1_tags = soup.find_all("h1")
    has_h1 = len(h1_tags) >= 1
    
    if not has_h1:
        issues.append("No H1 heading found")
        recommendations.append("Add a clear H1 heading that describes the page content")
    elif len(h1_tags) > 1:
        issues.append(f"Multiple H1 tags found ({len(h1_tags)}) - should have only one")
        recommendations.append("Use only one H1 per page for clarity")
    else:
        issues.append("✓ Single H1 heading present")
    
    # Analyze heading structure
    headings = []
    for i in range(1, 7):
        for h in soup.find_all(f"h{i}"):
            text = h.get_text(strip=True)[:100]
            headings.append({"level": i, "text": text})
    
    if len(headings) < 3:
        issues.append("Limited heading structure")
        recommendations.append("Use more headings (H2, H3) to organize content hierarchically")
    else:
        issues.append(f"✓ Good heading structure ({len(headings)} headings)")
    
    # Check for FAQ sections
    text_lower = html.lower()
    has_faq = any(indicator in text_lower for indicator in [
        "faq", "frequently asked", "questions", 
        '<div class="faq', '<section class="faq',
        "accordion", "qa-section"
    ])
    
    if has_faq:
        issues.append("✓ FAQ/Q&A section detected")
    else:
        recommendations.append("Consider adding an FAQ section - very valuable for AI answers")
    
    # Check for answer-first content (first paragraph should be substantial)
    paragraphs = soup.find_all("p")
    first_substantial_p = None
    for p in paragraphs[:5]:
        text = p.get_text(strip=True)
        if len(text) > 50:
            first_substantial_p = text
            break
    
    has_answer_first = first_substantial_p and len(first_substantial_p) > 100
    if has_answer_first:
        issues.append("✓ Answer-first content pattern detected")
    else:
        recommendations.append("Start with a clear, direct answer in the first paragraph")
    
    # Word count
    text = soup.get_text(separator=" ", strip=True)
    word_count = len(text.split())
    
    if word_count < 300:
        issues.append(f"Low word count ({word_count} words)")
        recommendations.append("Add more comprehensive content (aim for 500+ words)")
    elif word_count < 500:
        issues.append(f"Moderate word count ({word_count} words)")
    else:
        issues.append(f"✓ Good content depth ({word_count} words)")
    
    # Calculate score
    score = 40  # Base score
    
    if has_h1 and len(h1_tags) == 1:
        score += 15
    if len(headings) >= 3:
        score += 15
    if has_faq:
        score += 20
    if has_answer_first:
        score += 10
    if word_count >= 500:
        score += 15
    elif word_count >= 300:
        score += 5
    
    score = min(100, max(0, score))
    
    return {
        "has_h1": has_h1,
        "heading_count": len(headings),
        "has_faq_section": has_faq,
        "has_answer_first": has_answer_first,
        "word_count": word_count,
        "score": score,
        "issues": issues,
        "recommendations": recommendations
    }
