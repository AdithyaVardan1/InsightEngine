from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.analyzers.robots_analyzer import analyze_robots_txt
from app.analyzers.schema_analyzer import analyze_schema
from app.analyzers.content_analyzer import analyze_content
from app.analyzers.technical_analyzer import analyze_technical
from app.analyzers.llms_txt_analyzer import analyze_llms_txt
from datetime import datetime
import httpx

router = APIRouter()

class AnalyzeRequest(BaseModel):
    url: HttpUrl

class AnalysisResponse(BaseModel):
    url: str
    timestamp: str
    overall_score: int
    categories: dict

@router.post("/analyze")
async def analyze_url(request: AnalyzeRequest):
    """Analyze a URL for AI SEO readiness"""
    url = str(request.url)
    
    try:
        # Fetch the page HTML
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, follow_redirects=True)
            html = response.text
            base_url = str(response.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not fetch URL: {str(e)}")
    
    # Run all analyzers
    robots = await analyze_robots_txt(base_url)
    schema = analyze_schema(html)
    content = analyze_content(html)
    technical = analyze_technical(html)
    llms_txt = await analyze_llms_txt(base_url)
    
    # Calculate weighted overall score
    weights = {
        'robots': 0.25,
        'schema': 0.25,
        'content': 0.25,
        'technical': 0.15,
        'llms_txt': 0.10
    }
    
    overall_score = int(
        robots['score'] * weights['robots'] +
        schema['score'] * weights['schema'] +
        content['score'] * weights['content'] +
        technical['score'] * weights['technical'] +
        llms_txt['score'] * weights['llms_txt']
    )
    
    return {
        "url": url,
        "timestamp": datetime.utcnow().isoformat(),
        "overall_score": overall_score,
        "categories": {
            "robots": robots,
            "schema": schema,
            "content": content,
            "technical": technical,
            "llms_txt": llms_txt
        }
    }

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
