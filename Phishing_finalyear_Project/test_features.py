"""
Testing Script for Phishing Detection System
Tests feature extraction, URL validation, and phishing detection
"""

import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from phishing_utils import extract_features, analyze_url, validate_url, get_repeated_characters


def test_feature_extraction():
    """Test feature extraction"""
    print("\n" + "="*70)
    print("TEST 1: FEATURE EXTRACTION")
    print("="*70)
    
    test_urls = [
        "https://www.google.com",
        "http://g00gle-login.com",
        "http://paypaaal-verify.com",
        "http://192.168.1.1/admin",
    ]
    
    for url in test_urls:
        features = extract_features(url)
        print(f"\n📍 URL: {url}")
        print(f"   Features: {features}")
        print(f"   Length: {len(features)}")
        
        # Explain key features
        if features[1] == 1:
            print("   ⚠️  Contains IP address")
        if features[9] == 1:
            print("   ⚠️  Contains repeated symbols")
        if features[8] == 1:
            print("   ⚠️  Contains repeated letters")
        if features[10] == 1:
            print("   ⚠️  Contains number replacement")


def test_url_validation():
    """Test URL validation"""
    print("\n" + "="*70)
    print("TEST 2: URL VALIDATION")
    print("="*70)
    
    test_cases = [
        ("https://www.google.com", True),
        ("google.com", True),
        ("", False),
        ("a" * 2100, False),
        ("not-a-valid-url-!!!!", False),
    ]
    
    for url, expected in test_cases:
        is_valid, msg = validate_url(url)
        status = "✅" if is_valid == expected else "❌"
        print(f"\n{status} URL: {url[:50] if url else '(empty)'}")
        print(f"   Valid: {is_valid}, Message: {msg}")


def test_repeated_characters():
    """Test repeated character detection"""
    print("\n" + "="*70)
    print("TEST 3: REPEATED CHARACTERS & SYMBOLS DETECTION")
    print("="*70)
    
    test_urls = [
        "https://www.google.com",           # No repeats
        "http://gooogle.com",               # Repeated 'o'
        "http://paypaaal-login.com",        # Repeated 'a' and '-'
        "http://amazz0n-verify--account",   # Multiple repeats
        "http://micro@@soft.com",           # Repeated '@'
        "http://site_____.com",             # Repeated '_'
    ]
    
    for url in test_urls:
        result = get_repeated_characters(url)
        print(f"\n📍 URL: {url}")
        print(f"   Found Repeats: {result['found']}")
        if result['patterns']:
            print(f"   Patterns Found:")
            for pattern in result['patterns']:
                if 'character' in pattern:
                    print(f"      - Character '{pattern['character']}' repeated {pattern['count']} times")
                else:
                    print(f"      - Symbols '{pattern['symbols']}' repeated {pattern['count']} chars")
            print(f"   Total Repeated Characters: {result['total_count']}")


def test_url_analysis():
    """Test comprehensive URL analysis"""
    print("\n" + "="*70)
    print("TEST 4: COMPREHENSIVE URL ANALYSIS")
    print("="*70)
    
    test_urls = [
        ("https://www.amazon.com", "LEGITIMATE"),
        ("http://amaz0n-login-verify.com", "PHISHING"),
        ("http://192.168.1.1/login", "PHISHING"),
        ("https://paypal.com", "LEGITIMATE"),
        ("http://paypaaal-confirm-account.com", "PHISHING"),
        ("https://github.com", "LEGITIMATE"),
        ("http://gitt--hub.com", "PHISHING"),
    ]
    
    for url, expected_type in test_urls:
        analysis = analyze_url(url)
        print(f"\n📊 {expected_type} - {url}")
        print(f"   Domain: {analysis['domain']}")
        print(f"   Risk Score: {analysis['risk_score']}/100")
        
        if analysis['indicators']:
            print(f"   Indicators Found:")
            for indicator, value in analysis['indicators'].items():
                if value:
                    print(f"      - {indicator}: {value}")
        else:
            print(f"   ✅ No indicators found")
        
        # Predict based on risk score
        if analysis['risk_score'] > 50:
            print(f"   ⚠️  Classification: LIKELY PHISHING")
        else:
            print(f"   ✅ Classification: LIKELY LEGITIMATE")


def test_phishing_indicators():
    """Test specific phishing indicators"""
    print("\n" + "="*70)
    print("TEST 5: SPECIFIC PHISHING INDICATORS")
    print("="*70)
    
    indicators = [
        {
            "name": "IP Address in URL",
            "test_url": "http://192.168.1.1",
            "feature_index": 1
        },
        {
            "name": "Repeated Symbols",
            "test_url": "http://site--domain.com",
            "feature_index": 9
        },
        {
            "name": "Number Replacement",
            "test_url": "http://g00gle.com",
            "feature_index": 10
        },
        {
            "name": "Brand Impersonation",
            "test_url": "http://g0ogle.com",
            "feature_index": 11
        },
        {
            "name": "Suspicious Keywords",
            "test_url": "http://verify-your-account.com",
            "feature_index": 7
        },
    ]
    
    for indicator in indicators:
        features = extract_features(indicator["test_url"])
        feature_value = features[indicator["feature_index"]]
        
        print(f"\n🔍 {indicator['name']}")
        print(f"   Test URL: {indicator['test_url']}")
        print(f"   Detected: {'✅ YES' if feature_value == 1 else '❌ NO'}")
        print(f"   Feature Value: {feature_value}")


def main():
    """Run all tests"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║     Phishing Detection System - Comprehensive Test Suite        ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    try:
        test_feature_extraction()
        test_url_validation()
        test_repeated_characters()
        test_url_analysis()
        test_phishing_indicators()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
