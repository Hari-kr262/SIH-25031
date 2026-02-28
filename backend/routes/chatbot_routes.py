"""Chatbot routes — AI-powered civic assistant."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.models.user import User
from backend.middleware.auth_middleware import get_optional_user
from backend.utils.response_utils import success_response

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


class ChatMessage(BaseModel):
    message: str
    context: str = "general"


@router.post("/chat", response_model=dict)
def chat(
    data: ChatMessage,
    current_user: User = Depends(get_optional_user),
):
    """
    AI-powered civic assistant.
    Uses OpenAI API if configured, otherwise returns a rule-based response.
    """
    try:
        from ai.chatbot import get_chatbot_response
        response = get_chatbot_response(data.message, user=current_user)
        return success_response({"reply": response})
    except ImportError:
        pass

    # Rule-based fallback
    msg = data.message.lower()
    reply = _rule_based_response(msg)
    return success_response({"reply": reply})


def _rule_based_response(msg: str) -> str:
    """Simple rule-based chatbot for common civic queries."""
    if "report" in msg or "pothole" in msg or "issue" in msg:
        return ("To report a civic issue, go to the 'Report Issue' section, "
                "describe the problem, add a photo, and submit. "
                "Your report will be automatically routed to the correct department.")
    if "status" in msg or "track" in msg:
        return ("You can track your issue status under 'My Issues'. "
                "You'll also receive notifications when the status changes.")
    if "vote" in msg or "upvote" in msg:
        return ("You can upvote issues to increase their priority. "
                "More upvotes = faster government response!")
    if "badge" in msg or "points" in msg or "level" in msg:
        return ("Earn points by reporting issues (+10), verifying fixes (+5), "
                "and more. Collect badges and climb the leaderboard!")
    if "contact" in msg or "help" in msg:
        return "For urgent civic issues, please also contact your local ward office directly."
    return ("I'm the CivicResolve assistant! I can help you report civic issues, "
            "track your reports, understand the points system, or answer general questions "
            "about the platform. What would you like to know?")
