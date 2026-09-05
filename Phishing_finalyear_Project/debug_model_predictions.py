import os
import warnings
import pickle
from phishing_utils import extract_features

warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

urls = [
    'https://www.google.com',
    'https://www.youtube.com',
    'https://github.com',
    'https://www.amazon.com',
    'https://www.microsoft.com',
    'http://192.168.1.1/login',
    'http://g00gle-security.com',
    'http://paypaaal-login-verify.com',
    'https://secure-paypal.com',
    'https://www.facebook.com/settings',
]

for name in ['model.pkl', 'svm_model.pkl']:
    print('===', name)
    with open(name, 'rb') as f:
        model = pickle.load(f)
    print('model type:', type(model))
    print('has predict_proba:', hasattr(model, 'predict_proba'))
    for url in urls:
        features = [extract_features(url)]
        pred = model.predict(features)[0]
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(features)[0]
            conf = max(probs) * 100
        else:
            conf = 'N/A'
        print(url, '->', pred, 'conf', conf)
    print()