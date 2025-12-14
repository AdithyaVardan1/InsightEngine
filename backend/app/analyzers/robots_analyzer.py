"""
Robots.txt Analyzer - Check AI bot access
"""
import httpx
from typing import Dict, List, Any

# AI bots and their user agent strings
AI_BOTS = [
    {"name": "GPTBot", "user_agent": "GPTBot", "owner": "OpenAI"},
    {"name": "ChatGPT-User", "user_agent": "ChatGPT-User", "owner": "OpenAI"},
    {"name": "ClaudeBot", "user_agent": "ClaudeBot", "owner": "Anthropic"},
    {"name": "Claude-Web", "user_agent": "Claude-Web", "owner": "Anthropic"},
    {"name": "PerplexityBot", "user_agent": "PerplexityBot", "owner": "Perplexity"},
    {"name": "Google-Extended", "user_agent": "Google-Extended", "owner": "Google (Gemini)"},
    {"name": "CCBot", "user_agent": "CCBot", "owner": "Common Crawl"},
    {"name": "Bytespider", "user_agent": "Bytespider", "owner": "ByteDance"},
]


def parse_robots_txt(content: str) -> Dict[str, set]:
    """Parse robots.txt content into rules by user-agent"""
    rules = {}
    current_agent = "*"
    
    for line in content.split("\n"):
        line = line.strip().lower()
        
        if line.startswith("user-agent:"):
            current_agent = line.replace("user-agent:", "").strip()
            if current_agent not in rules:
                rules[current_agent] = set()
                
        elif line.startswith("disallow:"):
            path = line.replace("disallow:", "").strip()
            if path in ["/", "/*"]:
                rules.setdefault(current_agent, set()).add("disallow-all")
            elif path:
                rules.setdefault(current_agent, set()).add(f"disallow:{path}")
                
        elif line.startswith("allow:"):
            path = line.replace("allow:", "").strip()
            if path in ["/", "/*"]:
                rules.setdefault(current_agent, set()).add("allow-all")
    
    return rules


def is_bot_allowed(rules: Dict[str, set], user_agent: str) -> bool:
    """Check if a specific bot is allowed based on rules"""
    lower_agent = user_agent.lower()
    
    # Check specific bot rules first
    for agent, agent_rules in rules.items():
        if agent == lower_agent:
            if "disallow-all" in agent_rules and "allow-all" not in agent_rules:
                return False
            if "allow-all" in agent_rules:
                return True
    
    # Fall back to wildcard rules
    wildcard_rules = rules.get("*", set())
    if "disallow-all" in wildcard_rules and "allow-all" not in wildcard_rules:
        return False
    
    return True  # Default to allowed


async def analyze_robots_txt(base_url: str) -> Dict[str, Any]:
    """Analyze robots.txt for AI bot access"""
    issues = []
    recommendations = []
    
    try:
        robots_url = f"{base_url.rstrip('/')}/robots.txt"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(robots_url)
            
            if response.status_code == 404:
                return {
                    "found": False,
                    "content": None,
                    "ai_bots": [{"name": b["name"], "owner": b["owner"], "allowed": True} for b in AI_BOTS],
                    "score": 70,
                    "issues": ["No robots.txt file found (all bots allowed by default)"],
                    "recommendations": [
                        "Create a robots.txt file to explicitly control crawler access",
                        "Consider adding specific rules for AI bots"
                    ]
                }
            
            content = response.text
            rules = parse_robots_txt(content)
            
            # Check each AI bot
            ai_bots = []
            for bot in AI_BOTS:
                allowed = is_bot_allowed(rules, bot["user_agent"])
                ai_bots.append({
                    "name": bot["name"],
                    "owner": bot["owner"],
                    "allowed": allowed
                })
            
            # Calculate score
            allowed_count = sum(1 for b in ai_bots if b["allowed"])
            score = int((allowed_count / len(ai_bots)) * 100)
            
            # Check for issues
            blocked_bots = [b["name"] for b in ai_bots if not b["allowed"]]
            if blocked_bots:
                issues.append(f"{len(blocked_bots)} AI bot(s) blocked: {', '.join(blocked_bots)}")
                recommendations.append(f"Consider allowing {', '.join(blocked_bots)} for better AI visibility")
            
            # Check if all bots blocked via wildcard
            if "disallow-all" in rules.get("*", set()) and "allow-all" not in rules.get("*", set()):
                issues.append("Wildcard rule blocks all crawlers by default")
                recommendations.append("Add explicit Allow rules for AI bots you want to permit")
                score = min(score, 30)
            
            if allowed_count == len(ai_bots):
                issues.append("All AI bots are allowed - great for visibility!")
            
            return {
                "found": True,
                "content": content[:2000],
                "ai_bots": ai_bots,
                "score": score,
                "issues": issues,
                "recommendations": recommendations
            }
            
    except Exception as e:
        return {
            "found": False,
            "content": None,
            "ai_bots": [{"name": b["name"], "owner": b["owner"], "allowed": True} for b in AI_BOTS],
            "score": 50,
            "issues": [f"Could not fetch robots.txt: {str(e)}"],
            "recommendations": ["Ensure your robots.txt is publicly accessible"]
        }
