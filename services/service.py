def calculate_risk_level(level):
    if 0 <= level <= 9:
        return "LOW"
    
    if 10 <= level <= 17:
        return "MEDIUM"
    
    if 18 <= level <= 24:
        return "HIGH"
    
    if level >= 25:
        return "CRITICAL"