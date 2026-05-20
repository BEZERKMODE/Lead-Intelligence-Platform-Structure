def calculate_intent(signals: dict) -> int:
    """
    Calculates enterprise buyer intent based on extracted buying signals.
    """
    score = 0
    
    if signals.get("hiring"):
        score += 25
    if signals.get("funding"):
        score += 30
    if signals.get("tech_change"):
        score += 20
    if signals.get("linkedin_activity"):
        score += 15
    if signals.get("website_growth"):
        score += 10
        
    return min(score, 100)

def detect_buying_signals(text: str) -> list:
    """
    Detects key enterprise buying signals from raw text.
    """
    BUYING_SIGNALS = [
        "hiring sales team",
        "raised funding",
        "expanding operations",
        "new product launch",
        "migrating infrastructure",
    ]
    
    found = []
    for signal in BUYING_SIGNALS:
        if signal.lower() in text.lower():
            found.append(signal)
    return found
