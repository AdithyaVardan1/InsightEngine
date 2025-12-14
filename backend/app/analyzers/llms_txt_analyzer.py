"""
llms.txt Analyzer - Check for the emerging LLM instruction file
"""
import httpx
from typing import Dict, Any


async def analyze_llms_txt(base_url: str) -> Dict[str, Any]:
    """Analyze llms.txt file presence and content"""
    issues = []
    recommendations = []
    
    try:
        llms_url = f"{base_url.rstrip('/')}/llms.txt"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(llms_url)
            
            if response.status_code == 404:
                return {
                    "found": False,
                    "content": None,
                    "score": 40,
                    "issues": ["No llms.txt file found"],
                    "recommendations": [
                        "Consider adding an llms.txt file to guide AI assistants",
                        "llms.txt is an emerging standard for AI crawler instructions",
                        "Include: site purpose, key content areas, preferred citation format"
                    ]
                }
            
            if response.status_code == 200:
                content = response.text
                
                # Basic analysis of llms.txt content
                score = 80
                issues.append("✓ llms.txt file found!")
                
                # Check content quality
                if len(content) < 50:
                    score -= 20
                    issues.append("llms.txt content is minimal")
                    recommendations.append("Expand llms.txt with more details about your site")
                elif len(content) > 200:
                    score += 10
                    issues.append("✓ llms.txt has substantial content")
                
                # Check for key sections (heuristic)
                content_lower = content.lower()
                if any(kw in content_lower for kw in ["purpose", "about", "description"]):
                    score += 5
                    issues.append("✓ Includes site description")
                
                if any(kw in content_lower for kw in ["contact", "author", "source"]):
                    score += 5
                    issues.append("✓ Includes attribution info")
                
                score = min(100, max(0, score))
                
                return {
                    "found": True,
                    "content": content[:1000],
                    "score": score,
                    "issues": issues,
                    "recommendations": recommendations
                }
            
            # Other status codes
            return {
                "found": False,
                "content": None,
                "score": 40,
                "issues": [f"llms.txt returned status {response.status_code}"],
                "recommendations": ["Ensure llms.txt is publicly accessible"]
            }
            
    except Exception as e:
        return {
            "found": False,
            "content": None,
            "score": 40,
            "issues": [f"Could not check llms.txt: {str(e)}"],
            "recommendations": ["Consider adding an llms.txt file"]
        }
