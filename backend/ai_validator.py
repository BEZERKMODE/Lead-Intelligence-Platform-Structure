import logging

logger = logging.getLogger(__name__)

def validate_ai_response(response: str) -> bool:
    """
    Enterprise LLM Validation Layer.
    Detects and rejects hallucinations or generic fallback responses.
    """
    forbidden_terms = [
        "unknown",
        "maybe",
        "guess",
        "i'm sorry, but",
        "i don't have enough context",
        "as an ai language model"
    ]
    
    response_lower = response.lower()
    
    for word in forbidden_terms:
        if word in response_lower:
            logger.warning(f"AI Validator rejected response due to hallucination indicator: '{word}'")
            return False
            
    return True
