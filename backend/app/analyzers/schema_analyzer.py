"""
Schema Analyzer - Check JSON-LD structured data
"""
import re
import json
from typing import Dict, List, Any

# Valuable schema types for AI
VALUABLE_SCHEMAS = [
    "Article", "NewsArticle", "BlogPosting",
    "FAQPage", "HowTo", "QAPage",
    "Product", "Review", "Organization",
    "Person", "WebPage", "WebSite",
    "BreadcrumbList", "ItemList"
]


def extract_json_ld(html: str) -> List[dict]:
    """Extract JSON-LD schemas from HTML"""
    schemas = []
    pattern = r'<script[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        try:
            content = match.strip()
            parsed = json.loads(content)
            
            if isinstance(parsed, list):
                schemas.extend(parsed)
            else:
                schemas.append(parsed)
        except json.JSONDecodeError:
            pass  # Skip invalid JSON
    
    return schemas


def analyze_schema_item(schema: dict) -> dict:
    """Analyze a single schema item"""
    schema_type = schema.get("@type", "Unknown")
    properties = [k for k in schema.keys() if not k.startswith("@")]
    
    valid = True
    
    # Check required properties based on type
    if schema_type in ["Article", "BlogPosting", "NewsArticle"]:
        if not schema.get("headline") or not schema.get("author"):
            valid = False
    
    if schema_type == "FAQPage":
        if not schema.get("mainEntity") or not isinstance(schema.get("mainEntity"), list):
            valid = False
    
    if schema_type == "Organization":
        if not schema.get("name"):
            valid = False
    
    return {"type": schema_type, "properties": properties, "valid": valid}


def analyze_schema(html: str) -> Dict[str, Any]:
    """Analyze JSON-LD structured data in HTML"""
    issues = []
    recommendations = []
    
    json_ld_schemas = extract_json_ld(html)
    
    if not json_ld_schemas:
        return {
            "found": False,
            "schemas": [],
            "score": 20,
            "issues": ["No JSON-LD structured data found on the page"],
            "recommendations": [
                "Add JSON-LD structured data to help AI understand your content",
                "Consider adding Article, FAQPage, or Organization schema",
                "Use Google's Structured Data Testing Tool to validate"
            ]
        }
    
    schemas = [analyze_schema_item(s) for s in json_ld_schemas]
    
    # Calculate score
    score = 50  # Base score for having some schema
    
    # Bonus for valuable schema types
    found_types = set(s["type"] for s in schemas)
    valuable_found = [t for t in VALUABLE_SCHEMAS if t in found_types]
    score += len(valuable_found) * 10
    
    # Check for FAQPage (very valuable for AI)
    if "FAQPage" in found_types:
        score += 15
        issues.append("✓ FAQPage schema found - excellent for AI answers!")
    else:
        recommendations.append("Consider adding FAQPage schema for Q&A content")
    
    # Check for Article schemas
    if any(t in found_types for t in ["Article", "BlogPosting", "NewsArticle"]):
        score += 10
        issues.append("✓ Article schema found - helps AI understand your content")
    
    # Check for Organization/Author (E-E-A-T)
    if "Organization" in found_types or "Person" in found_types:
        score += 10
        issues.append("✓ Organization/Person schema found - supports E-E-A-T signals")
    else:
        recommendations.append("Add Organization or Person schema for credibility")
    
    # Check for validity
    invalid_schemas = [s for s in schemas if not s["valid"]]
    if invalid_schemas:
        score -= 10
        issues.append(f"{len(invalid_schemas)} schema(s) may be missing required properties")
        recommendations.append("Review and complete required properties in your schemas")
    
    # Cap score
    score = min(100, max(0, score))
    
    return {
        "found": True,
        "schemas": schemas,
        "score": score,
        "issues": issues,
        "recommendations": recommendations
    }
