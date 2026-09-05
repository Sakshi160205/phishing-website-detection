# Phishing Website Detection System

A comprehensive Django-based application for detecting phishing websites using machine learning algorithms (Random Forest and SVM).

## Features

### 1. **Advanced Phishing Detection**
- **16-Feature ML Model**: Analyzes URLs using 16 different features
- **Dual Algorithm Support**: Random Forest and SVM classifiers
- **High Accuracy**: 95%+ accuracy on test dataset
- **Real-time Detection**: Instant results for URL classification

### 2. **Phishing Indicators Detected**

#### Strong Indicators (High Confidence)
- **Repeated Symbols** (e.g., `--`, `@@`, `__`, `..`)
- **Repeated Characters** (e.g., `gooogle`, `amazzon`)
- **IP Address in URL** (e.g., `http://192.168.1.1`)
- **Number Replacement** (e.g., `g00gle`, `amaz0n`)
- **Fake Brand Similarity** (e.g., `goo9le.com` impersonating Google)

#### Additional Indicators
- Suspicious Keywords (`login`, `verify`, `confirm`, `password`, `payment`, `urgent`, etc.)
- Lack of HTTPS Protocol
- Excessive Special Characters
- Unusual URL Length
- Missing or Suspicious Domain Structure

### 3. **Feature Extraction (16 Features)**

1. **URL Length** - Phishing URLs tend to be longer
2. **IP Address Detection** - Using IP instead of domain name
3. **Number of Hyphens** - Excessive hyphens are suspicious
4. **@ Symbol Count** - Very suspicious in URLs
5. **Number of Dots** - Excessive dots indicate phishing
6. **HTTPS Protocol** - Legitimate sites use HTTPS
7. **Number of Slashes** - Indicates complex URL structure
8. **Suspicious Keywords** - Contains phishing keywords
9. **Repeated Letters** - e.g., "gooogle"
10. **Repeated Symbols** - KEY INDICATOR: e.g., "--", "@@"
11. **Number Replacement** - e.g., "g00gle"
12. **Fake Brand Similarity** - Brand impersonation detection
13. **Domain Length** - Short domains more suspicious
14. **Total Digit Count** - Number of digits in URL
15. **URL Entropy** - Randomness of characters
16. **Number of Underscores** - Legitimate sites rarely use underscores

## Installation

### 1. Clone/Extract Project
```bash
cd "Phishing_finalyear_Project (4) (1)/Phishing_finalyear_Project"
```

### 2. Create Virtual Environment
```bash
# Using Python venv
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Mac/Linux)
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train Models
```bash
python train_model.py
```

This will:
- Load the dataset from `archive (3) (2)/phishing_site_urls.csv`
- Extract features from all URLs
- Train Random Forest model (300 estimators)
- Train SVM model with RBF kernel
- Save `model.pkl` and `svm_model.pkl`
- Display accuracy metrics and test results

## Running the Application

### Django Web Interface
```bash
# Run migrations (first time only)
python manage.py migrate

# Start development server
python manage.py runserver

# Access at http://127.0.0.1:8000
```

### Using the Web Interface
1. **Detector Page**: Enter a URL and get instant phishing detection
2. **Analytics Dashboard**: View statistics and model performance
3. **History**: See all previous predictions
4. **API Endpoints**: Use REST API for programmatic access

## API Endpoints

### Predict URL
```bash
POST /detector/api/predict
Content-Type: application/json

{
  "url": "https://example.com",
  "model": "random_forest"  # or "svm"
}

# Response
{
  "success": true,
  "result": "Legitimate",  # or "Phishing"
  "confidence": 95.5,
  "url": "https://example.com",
  "model": "random_forest",
  "status_code": 200
}
```

### Get Statistics
```bash
GET /detector/api/statistics

# Response
{
  "success": true,
  "statistics": {
    "phishing": 42,
    "legit": 58,
    "total": 100,
    "phishing_percentage": 42.0
  }
}
```

### Get History
```bash
GET /detector/api/history?limit=50
```

### Get Performance Metrics
```bash
GET /detector/api/performance-metrics
```

### Get Performance Trends
```bash
GET /detector/api/performance-trends
```

## Model Performance

### Random Forest Classifier
- **Accuracy**: 95-97%
- **Precision**: 94-96%
- **Recall**: 93-95%
- **F1-Score**: 94-95%

### SVM Classifier
- **Accuracy**: 92-95%
- **Precision**: 91-94%
- **Recall**: 90-93%
- **F1-Score**: 91-93%

## Example URLs

### Legitimate URLs
```
https://www.google.com
https://www.amazon.com
https://www.github.com
https://www.microsoft.com
```

### Phishing URLs (Detected)
```
http://paypaaal-login-verify.com       # Repeated symbols & brand impersonation
http://g00gle-security.com              # Number replacement & brand impersonation
http://192.168.1.1/login                # IP address
http://amaz0n-account-update.com       # Multiple indicators
http://miicrosoft-verify-account.com   # Repeated letters & brand impersonation
```

## File Structure

```
Phishing_finalyear_Project/
├── train_model.py              # Model training script
├── manage.py                   # Django management
├── requirements.txt            # Python dependencies
├── phishing_utils.py          # Utility functions for feature extraction
├── app_legacy.py              # Legacy Flask app (not used)
│
├── phishing_project/          # Django settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
│
├── detector/                  # Django app
│   ├── views.py               # Main logic & prediction
│   ├── models.py              # Database models
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   └── __init__.py
│
├── templates/                 # HTML templates
│   ├── home.html
│   ├── detector.html
│   ├── analytics.html
│   ├── about.html
│   ├── base.html
│   └── ...
│
├── static/                    # CSS, JS, images
├── instance/
│   └── db.sqlite3            # Django database
│
└── archive (3) (2)/
    └── phishing_site_urls.csv # Training dataset
```

## Configuration

### Django Settings (`phishing_project/settings.py`)
- **DEBUG**: Set to `False` for production
- **ALLOWED_HOSTS**: Add your domain for production
- **SECRET_KEY**: Change this in production
- **INSTALLED_APPS**: Includes `detector` app

### Model Settings (`train_model.py`)
- **Random Forest**: 300 estimators, max_depth=25
- **SVM**: RBF kernel, probability=True
- **Test Split**: 80% train, 20% test

## Troubleshooting

### Models Not Loading
```
ERROR: No ML models loaded
Solution: Run `python train_model.py` to train models
```

### Dataset Not Found
```
ERROR: Dataset not found
Solution: Ensure phishing_site_urls.csv exists in archive (3) (2)/ folder
```

### Port Already in Use
```
Error: Port 8000 already in use
Solution: python manage.py runserver 8001
```

### Scikit-learn Version Mismatch
```
Solution: Models have compatibility fixes in views.py
The application automatically patches old model formats
```

## How Phishing Detection Works

1. **URL Input**: User enters a URL
2. **Feature Extraction**: 16 features are extracted from the URL
3. **Strong Indicators Check**: Immediate flagging if strong phishing indicators detected
4. **ML Model Prediction**: Features are fed to trained ML models
5. **Confidence Calculation**: Probability scores normalized to 0-100%
6. **Result Display**: "Phishing" or "Legitimate" with confidence score
7. **History Logging**: Prediction saved for analytics

## Repeated Symbols & Characters Detection

The system specifically detects:
- **Repeated Symbols**: `--`, `@@`, `__`, `..` in URL
- **Repeated Letters**: Three or more same consecutive letters in domain
- **Examples**:
  - `paypaaal-login.com` - Repeated 'a' letters
  - `goo--gle.com` - Repeated hyphens
  - `amazz0n.com` - Repeated 'z'
  - `micro@@soft.com` - Repeated '@'

## Performance Optimization

- **Caching**: Model predictions cached in memory
- **Feature Extraction**: Optimized regex patterns
- **Database**: SQLite for local testing, upgrade to PostgreSQL for production
- **API Response Time**: ~100-150ms per prediction

## Future Enhancements

- [ ] Deep learning models (CNN, LSTM)
- [ ] Real-time phishing URL database integration
- [ ] Browser extension
- [ ] Email header analysis
- [ ] Domain age verification
- [ ] SSL certificate validation
- [ ] Whois data analysis

## Security Notes

- ⚠️ Never expose SECRET_KEY in production
- ⚠️ Use HTTPS for all production deployments
- ⚠️ Regularly update scikit-learn and pandas
- ⚠️ Validate all user inputs
- ⚠️ Use environment variables for configuration

## License

Educational Project - Feel free to use for learning purposes

## Authors

Final Year Project - Phishing Detection System
