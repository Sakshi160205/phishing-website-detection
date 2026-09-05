"""
Utility functions for phishing URL detection
Contains feature extraction, URL validation, and analysis functions
"""

import re
import difflib
from urllib.parse import urlparse


def extract_features(url):
    """
    Extract 16 features from a URL for phishing detection
    
    Features:
    1. URL length
    2. IP address detection
    3. Number of hyphens
    4. @ symbol count
    5. Number of dots
    6. HTTPS protocol
    7. Number of slashes
    8. Suspicious keywords
    9. Repeated letters in domain
    10. Repeated symbols/special characters (KEY INDICATOR)
    11. Number replacement
    12. Fake brand similarity
    13. Domain length
    14. Total digit count
    15. URL entropy
    16. Number of underscores
    
    Returns:
        list: 16-feature vector for ML model
    """
    url = str(url).lower().strip()
    
    # Add scheme for parsing
    if not url.startswith(("http://", "https://", "ftp://")):
        url = "https://" + url
    
    try:
        parsed = urlparse(url)
    except ValueError:
        cleaned = url.replace("[", "").replace("]", "")
        parsed = urlparse(cleaned)

    domain = parsed.netloc.replace("www.", "")
    if not domain:
        domain = parsed.path.split("/")[0].split("?")[0].split("#")[0]

    features = []
    
    # 1. URL length (phishing URLs tend to be longer)
    features.append(len(url))
    
    # 2. IP address detection (1 if URL contains IP, 0 otherwise)
    features.append(1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0)
    
    # 3. Number of hyphens in domain (phishing often uses hyphens)
    features.append(url.count("-"))
    
    # 4. @ symbol count (suspicious in legitimate URLs)
    features.append(url.count("@"))
    
    # 5. Number of dots (excessive dots indicate phishing)
    features.append(url.count("."))
    
    # 6. HTTPS protocol (1 if https, 0 otherwise)
    features.append(1 if "https" in url else 0)
    
    # 7. Number of slashes
    features.append(url.count("/"))
    
    # 8. Suspicious keywords detection
    suspicious_keywords = [
        "login", "verify", "verification", "secure", "account", 
        "update", "confirm", "password", "bank", "payment", 
        "urgent", "reset", "click", "action", "activity",
        "confirm identity", "unusual activity", "re-enter"
    ]
    features.append(1 if any(k in url for k in suspicious_keywords) else 0)
    
    # 9. Repeated letters in domain (e.g., "gooogle")
    features.append(1 if re.search(r"(.)\1{2,}", domain) else 0)
    
    # 10. REPEATED SYMBOLS/SPECIAL CHARACTERS (e.g., "--", "@@", "__", "..")
    repeated_special_chars = re.findall(r"([-_@.]){2,}", url)
    features.append(1 if repeated_special_chars else 0)
    
    # 11. Number replacement (number look-alike substitution, e.g., "g00gle")
    features.append(1 if re.search(r"[a-z]\d+[a-z]", domain) else 0)
    
    # 12. Fake brand similarity (brand impersonation)
    brands = [
        "google", "youtube", "facebook", "paypal", "amazon", 
        "instagram", "microsoft", "apple", "twitter", "linkedin",
        "ebay", "netflix", "dropbox", "whatsapp"
    ]

    host = parsed.netloc.replace("www.", "").split(":")[0].lower()
    host_parts = host.split('.')
    base_name = host_parts[-2] if len(host_parts) >= 2 else host
    fake_brand = 0
    for b in brands:
        similarity = difflib.SequenceMatcher(None, base_name, b).ratio()
        if similarity >= 0.65 and base_name != b:
            fake_brand = 1
            break
    features.append(fake_brand)
    
    # 13. Domain length (short domains are more suspicious)
    features.append(len(domain))
    
    # 14. Total digit count
    features.append(sum(c.isdigit() for c in url))
    
    # 15. URL entropy (randomness/unusual characters)
    unique_chars = len(set(url))
    entropy = unique_chars / len(url) if len(url) > 0 else 0
    features.append(entropy)
    
    # 16. Number of underscores (legitimate sites rarely use underscores)
    features.append(url.count("_"))
    
    return features
    features.append(url.count("_"))
    
    return features


def analyze_url(url):
    """
    Perform detailed analysis on a URL to identify phishing indicators
    
    Returns:
        dict: Analysis results with detailed findings
    """
    url = str(url).lower().strip()
    
    if not url.startswith(("http://", "https://", "ftp://")):
        url = "https://" + url
    
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    
    analysis = {
        "url": url,
        "domain": domain,
        "indicators": {},
        "risk_score": 0
    }
    
    # Check for IP address
    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        analysis["indicators"]["ip_address"] = True
        analysis["risk_score"] += 25
    
    # Check for repeated symbols
    if re.findall(r"([-_@.]){2,}", url):
        analysis["indicators"]["repeated_symbols"] = True
        analysis["risk_score"] += 20
    
    # Check for repeated letters
    if re.search(r"(.)\1{2,}", domain):
        analysis["indicators"]["repeated_letters"] = True
        analysis["risk_score"] += 15
    
    # Check for number replacement
    if re.search(r"[a-z]\d+[a-z]", domain):
        analysis["indicators"]["number_replacement"] = True
        analysis["risk_score"] += 20
    
    # Check for suspicious keywords
    suspicious_keywords = [
        "login", "verify", "verification", "secure", "account", 
        "update", "confirm", "password", "bank", "payment", 
        "urgent", "reset", "click"
    ]
    if any(k in url for k in suspicious_keywords):
        analysis["indicators"]["suspicious_keywords"] = True
        analysis["risk_score"] += 15
    
    # Check for HTTPS
    if "https" not in url:
        analysis["indicators"]["no_https"] = True
        analysis["risk_score"] += 10
    
    # Check for brand impersonation
    brands = [
        "google", "youtube", "facebook", "paypal", "amazon", 
        "instagram", "microsoft", "apple", "twitter", "linkedin",
        "ebay", "netflix"
    ]
    
    for brand in brands:
        similarity = difflib.SequenceMatcher(None, domain, brand).ratio()
        if 0.65 <= similarity <= 0.99 and domain != brand:
            analysis["indicators"]["brand_impersonation"] = brand
            analysis["risk_score"] += 25
            break
    
    # Check for excessive special characters
    special_char_count = sum(1 for c in url if c in "-_@#$%^&*")
    if special_char_count > 5:
        analysis["indicators"]["excessive_special_chars"] = special_char_count
        analysis["risk_score"] += 10
    
    # Normalize risk score to 0-100
    analysis["risk_score"] = min(100, analysis["risk_score"])
    
    return analysis


def validate_url(url):
    """
    Validate URL format and structure
    
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not url or len(url.strip()) == 0:
        return False, "URL cannot be empty"
    
    if len(url) > 2000:
        return False, "URL is too long (max 2000 characters)"
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://', 'ftp://')):
        url = 'https://' + url
    
    try:
        result = urlparse(url)
        is_valid = all([result.scheme, result.netloc])
        return is_valid, "Valid URL" if is_valid else "Invalid URL format"
    except Exception as e:
        return False, f"Invalid URL format: {str(e)}"


def get_repeated_characters(url):
    """
    Extract and analyze repeated characters in URL
    
    Returns:
        dict: Information about repeated characters found
    """
    url_lower = url.lower()
    repeated_info = {
        "found": False,
        "patterns": [],
        "total_count": 0
    }
    
    # Find all repeated character patterns
    for match in re.finditer(r"(.)\1{2,}", url_lower):
        char = match.group(1)
        count = len(match.group(0))
        repeated_info["patterns"].append({
            "character": char,
            "count": count,
            "position": match.start()
        })
        repeated_info["total_count"] += count
    
    # Find all repeated symbols
    for match in re.finditer(r"([-_@.]){2,}", url_lower):
        symbols = match.group(0)
        repeated_info["patterns"].append({
            "symbols": symbols,
            "count": len(symbols),
            "position": match.start()
        })
        repeated_info["total_count"] += len(symbols)
    
    if repeated_info["patterns"]:
        repeated_info["found"] = True
    
    return repeated_info
