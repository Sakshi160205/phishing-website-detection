# QUICK START GUIDE

## ⚡ Fast Setup (5 minutes)

### Windows
```bash
# 1. Open Terminal in project folder

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train models (2-5 minutes)
python train_model.py

# 5. Run server
python manage.py runserver

# 6. Open browser: http://127.0.0.1:8000
```

### Mac/Linux
```bash
# 1. Open Terminal in project folder

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train models (2-5 minutes)
python3 train_model.py

# 5. Run server
python3 manage.py runserver

# 6. Open browser: http://127.0.0.1:8000
```

## 🎯 Test the Application

### Web Interface
1. Go to http://127.0.0.1:8000/detector/
2. Enter test URLs:
   - ✅ Legitimate: `https://www.google.com`
   - ⚠️ Phishing: `http://g00gle-login-verify.com`
   - ⚠️ Phishing: `http://paypaaal-confirm.com`

### API Testing
```bash
# Using curl
curl -X POST http://127.0.0.1:8000/detector/api/predict \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://www.amazon.com\", \"model\": \"random_forest\"}"

# Using Python
import requests
response = requests.post(
    'http://127.0.0.1:8000/detector/api/predict',
    json={'url': 'https://example.com', 'model': 'random_forest'}
)
print(response.json())
```

## 🔑 Key Features

### Phishing Detection Indicators
✅ Detects **repeated symbols** (---, ___, @@)
✅ Detects **repeated characters** (gooogle, amazzon)
✅ Detects **brand impersonation** (goo9le, faceb00k)
✅ Detects **IP addresses** in URL
✅ Detects **suspicious keywords** (login, verify, confirm)
✅ Detects **number replacement** (g00gle, amaz0n)

### ML Models
- 🟢 **Random Forest**: 95%+ Accuracy
- 🟠 **SVM**: 92%+ Accuracy

## 📊 Analytics Dashboard
Visit: http://127.0.0.1:8000/detector/analytics/

- Phishing vs Legitimate count
- Detection accuracy
- Performance metrics
- Confusion matrix
- Detection trends

## 🐛 Troubleshooting

### "No ML models loaded"
```bash
# Solution: Train models
python train_model.py
```

### "Dataset not found"
```bash
# Make sure this file exists:
# archive (3) (2)/phishing_site_urls.csv
```

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### Models not working after update
```bash
# Delete old models and retrain
del model.pkl svm_model.pkl
python train_model.py
```

## 📁 Project Structure
```
├── train_model.py          ← Run to train models
├── manage.py              ← Django command
├── requirements.txt       ← Python packages
├── phishing_utils.py      ← Helper functions
├── README.md              ← Full documentation
├── QUICKSTART.md          ← This file
│
├── detector/
│   ├── views.py          ← Main prediction logic
│   ├── urls.py
│   └── models.py
│
├── templates/
│   ├── detector.html     ← Main interface
│   └── analytics.html    ← Dashboard
│
└── archive (3) (2)/
    └── phishing_site_urls.csv  ← Training data
```

## ⚙️ Configuration

### Change Detection Model
In `detector/views.py`, change the model:
```python
selected_model_name = "svm"  # Use SVM instead of Random Forest
```

### Adjust Phishing Sensitivity
In `phishing_utils.py`, modify suspicious keywords:
```python
suspicious_keywords = [
    "login", "verify",  # Add more keywords here
    "yourword"
]
```

## 📈 Performance

- **Detection Speed**: ~100-150ms per URL
- **Model Accuracy**: 95%+
- **False Positive Rate**: < 5%
- **Max URLs in History**: 500 (auto-clears oldest)

## 🚀 Production Deployment

### Before deploying to production:
1. Change DEBUG = False in settings.py
2. Update ALLOWED_HOSTS with your domain
3. Use PostgreSQL instead of SQLite
4. Set up HTTPS/SSL
5. Use environment variables for SECRET_KEY
6. Run: `python manage.py collectstatic --noinput`

### Run with Gunicorn:
```bash
pip install gunicorn
gunicorn phishing_project.wsgi:application --bind 0.0.0.0:8000
```

## 📧 Contact & Support

For issues or improvements, check:
- README.md for detailed documentation
- Code comments for implementation details
- Train model output for accuracy metrics

---

**Happy Phishing Hunting!** 🎣🔒
