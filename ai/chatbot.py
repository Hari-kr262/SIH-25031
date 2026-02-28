"""
AI-powered civic assistant using OpenAI API.
Falls back to rule-based responses when API is unavailable.
"""

from typing import Optional
from config.settings import settings


SYSTEM_PROMPT = """You are CivicBot, an AI assistant for CivicResolve - a civic issue 
reporting platform for Jharkhand, India. Help citizens:
1. Report civic issues (potholes, garbage, water leaks, streetlights, etc.)
2. Track their issue status
3. Understand the points and badge system
4. Navigate the platform
Be helpful, concise, and friendly. Respond in the user's preferred language if possible."""


def get_chatbot_response(message: str, user=None) -> str:
    """
    Get AI response using OpenAI API.
    Falls back to rule-based if API key is not configured.
    """
    if not settings.OPENAI_API_KEY:
        return _rule_based_response(message)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if user:
            messages.append({
                "role": "system",
                "content": f"User: {user.full_name}, Role: {user.role.value}, Points: {user.points}"
            })
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Chatbot] OpenAI API error: {e}")
        return _rule_based_response(message)


def _rule_based_response(message: str) -> str:
    """Keyword-based fallback response."""
    msg = message.lower()
    if any(w in msg for w in ["report", "pothole", "garbage", "light", "water"]):
        return ("To report an issue: 1) Tap 'Report Issue', 2) Select category, "
                "3) Add description & photo, 4) Submit. I'll route it to the right department!")
    if "status" in msg or "track" in msg:
        return "Check 'My Issues' to see your reports. You'll get notifications on every update."
    if "badge" in msg or "point" in msg:
        return ("Earn points: Report=10pts, Upvote=2pts, Verify fix=5pts. "
                "Badges: First Report 🎯, Active Reporter 📣, Community Hero 🦸 and more!")
    return ("Hi! I'm CivicBot. I can help you report civic issues, track reports, "
            "or explain how the platform works. What do you need?")
