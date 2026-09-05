# SYSTEM ARCHITECTURE & FLOW DIAGRAM

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   PHISHING DETECTION SYSTEM                 │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────┐
    │         User Interface (Web/API)                     │
    │  • Web: http://127.0.0.1:8000/detector/             │
    │  • API: POST /detector/api/predict                  │
    └─────────────────────┬──────────────────────────────┘
                          │
    ┌─────────────────────▼──────────────────────────────┐
    │      Django Request Handler (views.py)             │
    │  • Receives URL                                    │
    │  • Validates input                                │
    │  • Routes to detection engine                     │
    └─────────────────────┬──────────────────────────────┘
                          │
    ┌─────────────────────▼──────────────────────────────┐
    │    Feature Extraction (phishing_utils.py)          │
    │                                                    │
    │  Input: URL (string)                              │
    │  ├─ Parse URL structure                           │
    │  ├─ Extract 16 features:                          │
    │  │  ├─ Basic: length, HTTPS, dots, hyphens       │
    │  │  ├─ Security: IP address, @ symbol            │
    │  │  ├─ Content: keywords, brand similarity       │
    │  │  ├─ Anomaly: repeated chars, number replace   │
    │  │  └─ Statistical: entropy, digit count         │
    │  └─ Output: [16 numeric features]                │
    └─────────────────────┬──────────────────────────────┘
                          │
    ┌─────────────────────▼──────────────────────────────┐
    │   ML Model Prediction (Random Forest / SVM)        │
    │                                                    │
    │  Input: 16-feature vector                        │
    │  ├─ Load pre-trained model (model.pkl or svm...) │
    │  ├─ Run prediction                               │
    │  ├─ Get probability scores                       │
    │  └─ Output: [0/1, confidence %]                  │
    │            [Phishing/Legitimate, 0-100%]        │
    └─────────────────────┬──────────────────────────────┘
                          │
    ┌─────────────────────▼──────────────────────────────┐
    │    Result Formatting & History                     │
    │  • Classification: Phishing / Legitimate           │
    │  • Confidence: 95.5%                              │
    │  • Save to history (500 max)                      │
    │  • Return to user                                 │
    └─────────────────────┬──────────────────────────────┘
                          │
    ┌─────────────────────▼──────────────────────────────┐
    │    User Response (JSON/HTML)                       │
    │  {                                                 │
    │    "result": "Phishing",                           │
    │    "confidence": 95.5,                            │
    │    "url": "http://g00gle-login.com",             │
    │    "indicators": ["number_replacement", ...]      │
    │  }                                                 │
    └─────────────────────────────────────────────────────┘
```

---

## 📊 Feature Extraction Flow

```
URL Input: "http://g00gle-login-verify.com"
    │
    ├─► [1] URL Length = 34 characters
    │
    ├─► [2] IP Address = 0 (not IP)
    │
    ├─► [3] Hyphens = 2 (g00gle-login-verify)
    │
    ├─► [4] @ Symbols = 0 (no @ signs)
    │
    ├─► [5] Dots = 2 (two dots before .com)
    │
    ├─► [6] HTTPS = 0 (uses http://)
    │
    ├─► [7] Slashes = 2 (http://)
    │
    ├─► [8] Suspicious Keywords = 1 ✅ (contains "login", "verify")
    │
    ├─► [9] Repeated Letters = 0 (no repeated chars in domain)
    │
    ├─► [10] Repeated Symbols = 1 ✅ (has multiple hyphens)
    │
    ├─► [11] Number Replacement = 1 ✅ (contains "00" in "g00gle")
    │
    ├─► [12] Brand Impersonation = 1 ✅ (g00gle ≈ google, 0.75 similarity)
    │
    ├─► [13] Domain Length = 21 characters
    │
    ├─► [14] Digit Count = 2 (two zeros in "00")
    │
    ├─► [15] URL Entropy = 0.52 (character randomness)
    │
    └─► [16] Underscores = 0 (no underscores)

FEATURE VECTOR: [34, 0, 2, 0, 2, 0, 2, 1, 0, 1, 1, 1, 21, 2, 0.52, 0]
                                    ↓
                        ML Model Prediction
                                    ↓
                    Result: PHISHING (95% confidence)
```

---

## 🔴 Phishing Detection Pipeline

```
┌─ STRONG INDICATORS ─────────────────────────────┐
│  (HIGH CONFIDENCE - 2+ = PHISHING)             │
│                                                 │
│  ✅ IP Address in URL                          │
│     └─ Example: http://192.168.1.1/login       │
│                                                 │
│  ✅ Repeated Symbols (---, ___, @@)            │
│     └─ Example: site--domain.com               │
│                                                 │
│  ✅ Repeated Letters (3+)                      │
│     └─ Example: gooogle.com                    │
│                                                 │
│  ✅ Number Replacement                         │
│     └─ Example: g00gle.com                     │
│                                                 │
│  ✅ Fake Brand (0.65+ similarity)             │
│     └─ Example: goo9le.com                     │
└─────────────────────────────────────────────────┘
                    │
                    ├─ 2+ Indicators Found?
                    │  YES → PHISHING ✅
                    │  NO  → Continue to ML Model
                    │
    ┌───────────────▼──────────────────────┐
    │  ML Model Analysis (Feature Vector) │
    │  • Random Forest (95%+ accuracy)    │
    │  • SVM (92%+ accuracy)              │
    │  └─ Decision: Phishing or Legit    │
    └───────────────┬──────────────────────┘
                    │
        ┌───────────▼───────────┐
        │                       │
        ▼                       ▼
    PHISHING              LEGITIMATE
    ⚠️ WARN USER         ✅ SAFE
```

---

## 🎯 Example: Real Phishing URL

```
Input: "http://amaz0n-verify-account.com"

Detection Process:
├─ Validate URL ✅
│
├─ Extract Features
│  ├─ URL Length: 35 ✅
│  ├─ IP Address: 0 ✅
│  ├─ Hyphens: 2 ✅ (multiple)
│  ├─ @ Symbols: 0 ✅
│  ├─ Dots: 1 ✅
│  ├─ HTTPS: 0 ⚠️ (no encryption)
│  ├─ Slashes: 2 ✅
│  ├─ Suspicious Keywords: 1 ⚠️ (has "verify")
│  ├─ Repeated Letters: 0 ✅
│  ├─ Repeated Symbols: 1 ⚠️ (multiple hyphens)
│  ├─ Number Replacement: 1 ⚠️ (has "0" in amazon)
│  ├─ Brand Impersonation: 1 ⚠️ (amaz0n ≈ amazon)
│  ├─ Domain Length: 18 ✅
│  ├─ Digit Count: 1 ✅
│  ├─ Entropy: 0.51 ✅
│  └─ Underscores: 0 ✅
│
├─ Strong Indicator Count: 2+
│  ├─ Repeated Symbols: YES ⚠️
│  ├─ Number Replacement: YES ⚠️
│  └─ Decision: PHISHING (Immediate) ✅
│
├─ ML Model Prediction (if needed)
│  └─ Random Forest: PHISHING (94.2% confidence)
│
└─ RESULT: ⚠️ PHISHING DETECTED!
   Confidence: 94%+
   Indicators: number_replacement, repeated_symbols, brand_impersonation
```

---

## 🟢 Example: Legitimate URL

```
Input: "https://www.google.com"

Detection Process:
├─ Validate URL ✅
│
├─ Extract Features
│  ├─ URL Length: 21 ✅
│  ├─ IP Address: 0 ✅
│  ├─ Hyphens: 0 ✅
│  ├─ @ Symbols: 0 ✅
│  ├─ Dots: 1 ✅
│  ├─ HTTPS: 1 ✅ (encrypted)
│  ├─ Slashes: 2 ✅
│  ├─ Suspicious Keywords: 0 ✅
│  ├─ Repeated Letters: 0 ✅
│  ├─ Repeated Symbols: 0 ✅
│  ├─ Number Replacement: 0 ✅
│  ├─ Brand Impersonation: 0 ✅ (exact match to google)
│  ├─ Domain Length: 10 ✅
│  ├─ Digit Count: 0 ✅
│  ├─ Entropy: 0.48 ✅
│  └─ Underscores: 0 ✅
│
├─ Strong Indicator Count: 0
│  └─ Decision: Proceed to ML Model
│
├─ ML Model Prediction
│  └─ Random Forest: LEGITIMATE (97.8% confidence)
│
└─ RESULT: ✅ LEGITIMATE SITE
   Confidence: 97.8%
   Indicators: None detected
```

---

## 🚀 Training Pipeline

```
    ┌─────────────────────────────────┐
    │  phishing_site_urls.csv         │
    │  (URLs + Labels)                │
    │  ~10,000 URLs                   │
    └────────────┬──────────────────────┘
                 │
    ┌────────────▼──────────────────────┐
    │  Feature Extraction               │
    │  (16 features per URL)            │
    │  ~10,000 samples × 16 features   │
    └────────────┬──────────────────────┘
                 │
    ┌────────────▼──────────────────────┐
    │  Train/Test Split (80/20)         │
    │  Train: 8,000 URLs               │
    │  Test:  2,000 URLs               │
    └────────────┬──────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
    ┌──────────┐     ┌──────────┐
    │ Random   │     │  SVM     │
    │ Forest   │     │ Classifier│
    │ (300 est)│     │ (RBF)    │
    └────┬─────┘     └────┬─────┘
         │                 │
    ┌────▼─────────────────▼───┐
    │  Evaluate Performance     │
    │  • Accuracy              │
    │  • Precision             │
    │  • Recall                │
    │  • F1-Score              │
    └────┬─────────────────────┘
         │
    ┌────▼────────────────────┐
    │  Save Models             │
    │  • model.pkl (RF)       │
    │  • svm_model.pkl (SVM)  │
    └─────────────────────────┘
```

---

## 📊 Decision Tree

```
                    URL Input
                        │
                        ▼
                  [Validate URL]
                        │
            ┌───────────┴───────────┐
            │                       │
        Valid                   Invalid
            │                       │
            ▼                       ▼
    [Extract 16       Return Error
     Features]           Message
            │
            ▼
    [Check Strong Indicators]
            │
    ┌───────┼────────┐
    │       │        │
    ▼       ▼        ▼
  IP?    Repeat?  Brand?
  etc.    etc.     etc.
    │       │        │
    └───────┼────────┘
            │
            ▼
    [Count Indicators]
            │
        ┌───┴───┐
        │       │
       2+      0-1
        │       │
        ▼       ▼
    PHISHING  [ML Model]
              │
        ┌─────┴─────┐
        │           │
        ▼           ▼
    PHISHING   LEGITIMATE
```

---

## 🔄 API Flow

```
POST /detector/api/predict
{
  "url": "http://example.com",
  "model": "random_forest"
}
        │
        ▼
    [Parse JSON]
        │
        ▼
    [Validate URL]
        │
    ┌───┴───────┐
    │           │
Valid       Invalid
    │           │
    ▼           ▼
Extract     Return 400
Features    Error
    │
    ▼
[Load Model]
    │
    ▼
[Predict]
    │
    ▼
[Normalize Confidence]
    │
    ▼
[Save to History]
    │
    ▼
Return JSON Response
{
  "success": true,
  "result": "Phishing",
  "confidence": 94.5,
  "url": "http://example.com",
  "model": "random_forest",
  "status_code": 200
}
```

---

## 📈 Performance Metrics

```
Model Performance Over Time

Accuracy
│ 100%│
│ 95% ├─────[Random Forest]─────
│ 90% ├──[SVM]──
│ 85% │
└─────┴──────────────────────────

Precision vs Recall
│ 100%│
│ 95% ├─ [RF] ·● (high precision)
│ 90% ├─ [SVM] ○
│ 85% │
└─────┴──────────────────────────

F1-Score Comparison
│ 1.0 │
│0.95 │  ●─ Random Forest
│0.90 │  ○─ SVM
│0.85 │
└─────┴──────────────────────────
```

---

## 🎯 Summary

```
┌────────────────────────────────────────┐
│    Phishing Detection System Flow       │
├────────────────────────────────────────┤
│                                        │
│  Input: URL                            │
│    ↓                                  │
│  Validate                              │
│    ↓                                  │
│  Extract 16 Features                  │
│    ↓                                  │
│  Check Strong Indicators              │
│    ├─ YES → PHISHING ✅               │
│    └─ NO  → Continue                  │
│    ↓                                  │
│  ML Model Prediction                   │
│    ├─ Random Forest                   │
│    └─ SVM                             │
│    ↓                                  │
│  Output: Classification + Confidence   │
│    ├─ PHISHING (94%)                 │
│    └─ LEGITIMATE (97%)               │
│                                        │
└────────────────────────────────────────┘
```

---

**This architecture ensures fast, accurate phishing detection with multiple verification layers!**
