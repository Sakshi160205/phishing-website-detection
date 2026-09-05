import pandas as pd
import numpy as np
import pickle
import os

from phishing_utils import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score


# ==============================
# LOAD DATASET
# ==============================

# Find the dataset path
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, "archive (3) (2)", "phishing_site_urls.csv")

# Try alternative paths
if not os.path.exists(dataset_path):
    dataset_path = os.path.join(current_dir, "archive", "phishing_site_urls.csv")

if not os.path.exists(dataset_path):
    # Look for any csv file in current directory
    for file in os.listdir(current_dir):
        if file.endswith(".csv"):
            dataset_path = os.path.join(current_dir, file)
            break

print(f"Loading dataset from: {dataset_path}")

if not os.path.exists(dataset_path):
    print(f"ERROR: Dataset not found at {dataset_path}")
    print("Please ensure phishing_site_urls.csv exists in the project directory")
    exit(1)

df = pd.read_csv(dataset_path)

print("\nDataset Info:")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print("\nFirst few rows:")
print(df.head())
print(f"\nLabel distribution:\n{df['Label'].value_counts()}")

# Convert labels to numeric format
print("\nConverting labels to numeric format...")
print(f"Original labels: {df['Label'].unique()}")

df["Label"] = df["Label"].str.lower().str.strip()

# Create mapping dictionary
label_mapping = {
    "legitimate": 0,
    "phishing": 1,
    "good": 0,
    "bad": 1,
    "0":0,
    "1":1
}

# Map labels and ensure numeric values
df["Label"] = df["Label"].map(label_mapping)
print(f"After mapping: {df['Label'].unique()}")

# Drop any rows with NaN values (unmapped labels)
print(f"Before dropna - Shape: {df.shape}")
df = df.dropna()
print(f"After dropna - Shape: {df.shape}")

# Convert to int
df["Label"] = df["Label"].astype(int)
print(df[df["Label"] == 0].head(20))
print(df[df["Label"] == 1].head(20))

print(f"Label dtype: {df['Label'].dtype}")
print(f"Label distribution after conversion:\n{df['Label'].value_counts()}")
print(f"Label unique values: {df['Label'].unique()}")

# Use the entire dataset
print(f"Training on {len(df)} URLs")

# Extract features from all URLs
print("\nTraining on 549346 URLs")

print("Processing started...")   

print("\nExtracting features from URLs...")
X = []

urls = df["URL"].values

for i, url in enumerate(urls):
    X.append(extract_features(url))
    
    if i % 50000 == 0:
        print(f"Processed {i} / {len(urls)} URLs")

X = np.array(X)
y = np.array(df["Label"].values, dtype=int)
print(f"y dtype before split: {y.dtype}")
print(f"y unique values: {np.unique(y)}")
print(f"Features extracted: {len(X)} URLs")





# ==============================
# SPLIT DATASET
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
# Ensure labels are int type
y_train = np.array(y_train, dtype=int)
y_test = np.array(y_test, dtype=int)

print(f"\nTrain set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")
print(f"y_train dtype: {y_train.dtype}, unique: {np.unique(y_train)}")
print(f"y_test dtype: {y_test.dtype}, unique: {np.unique(y_test)}")

# ==============================
# RANDOM FOREST CLASSIFIER
# ==============================

print("\n" + "="*50)
print("Training Random Forest Classifier...")
print("="*50)

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=25,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

# Predictions and evaluation
rf_pred = rf.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)
rf_precision = precision_score(y_test, rf_pred, average='binary', zero_division=0)
rf_recall = recall_score(y_test, rf_pred, average='binary', zero_division=0)
rf_f1 = f1_score(y_test, rf_pred, average='binary', zero_division=0)

print(f"\nRandom Forest Accuracy: {rf_accuracy * 100:.2f}%")
print(f"Precision: {rf_precision:.2f}")
print(f"Recall: {rf_recall:.2f}")
print(f"F1-Score: {rf_f1:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, rf_pred))

# Save Random Forest model
model_path = os.path.join(current_dir, "model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(rf, f)
print(f"\nRandom Forest model saved to: {model_path}")

# ==============================
# SVM CLASSIFIER
# ==============================

print("\n" + "="*50)
print("Training SVM Classifier...")
print("="*50)

svm = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(
        kernel="rbf",
        C=1.0,
        gamma="scale",
        probability=True,
        random_state=42
    ))
])

print("Training SVM on reduced dataset...")

svm_limit = 50000

X_svm = X_train[:svm_limit]
y_svm = y_train[:svm_limit]

svm.fit(X_svm, y_svm)

print("SVM training completed")

# Predictions and evaluation
# Predictions and evaluation (reduced test)

X_svm_test = X_test[:20000]
y_svm_test = y_test[:20000]

svm_pred = svm.predict(X_svm_test)

svm_accuracy = accuracy_score(y_svm_test, svm_pred)

svm_precision = precision_score(
    y_svm_test,
    svm_pred,
    average='binary',
    zero_division=0
)

svm_recall = recall_score(
    y_svm_test,
    svm_pred,
    average='binary',
    zero_division=0
)

svm_f1 = f1_score(
    y_svm_test,
    svm_pred,
    average='binary',
    zero_division=0
)

print(f"\nSVM Accuracy: {svm_accuracy * 100:.2f}%")
print(f"Precision: {svm_precision:.2f}")
print(f"Recall: {svm_recall:.2f}")
print(f"F1-Score: {svm_f1:.2f}")

print("\nClassification Report:")
print(classification_report(y_svm_test, svm_pred))

# Save SVM model
svm_path = os.path.join(current_dir, "svm_model.pkl")
with open(svm_path, "wb") as f:
    pickle.dump(svm, f)
print(f"\nSVM model saved to: {svm_path}")

# ==============================
# MODEL COMPARISON
# ==============================

print("\n" + "="*50)
print("MODEL COMPARISON")
print("="*50)
print(f"{'Metric':<15} {'Random Forest':<15} {'SVM':<15}")
print("-"*45)
print(f"{'Accuracy':<15} {rf_accuracy*100:>13.2f}% {svm_accuracy*100:>13.2f}%")
print(f"{'Precision':<15} {rf_precision:>14.2f} {svm_precision:>14.2f}")
print(f"{'Recall':<15} {rf_recall:>14.2f} {svm_recall:>14.2f}")
print(f"{'F1-Score':<15} {rf_f1:>14.2f} {svm_f1:>14.2f}")

# ==============================
# TEST FUNCTION
# ==============================

def detect_phishing(url, model=None):
    """
    Detect if a URL is phishing or legitimate
    
    Returns: "PHISHING" or "LEGITIMATE"
    """
    if model is None:
        model = rf
    
    f = extract_features(url)
    
    # Strong phishing indicators that almost always indicate phishing
    strong_indicators = [
        f[1],   # IP address
        f[9],   # Repeated symbols
        f[10],  # Number replacement
        f[11]   # Fake brand
    ]
    
    # If multiple strong indicators present, classify as phishing
    if sum(strong_indicators) >= 2:
        return "PHISHING"
    
    # Use ML model for prediction
    result = model.predict([f])[0]
    
    return "PHISHING" if result == 1 else "LEGITIMATE"

# ==============================
# TESTING WITH SAMPLE URLs
# ==============================

print("\n" + "="*50)
print("TESTING WITH SAMPLE URLs")
print("="*50)

test_urls = [
    # Legitimate URLs
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.amazon.com",
    "https://www.microsoft.com",
    "https://github.com",
    
    # Phishing URLs
    "https://www.yooouuutube.com",  # Repeated characters
    "http://paypaaal-login-verify.com",  # Repeated symbols and suspicious keywords
    "http://192.168.1.1/login",  # IP address
    "http://g00gle-security.com",  # Number replacement
    "http://micro-soft.com",  # Brand impersonation
    "http://amaz0n-account-verify.com",  # Multiple indicators
]

print(f"\n{'URL':<50} {'RF Prediction':<15} {'SVM Prediction':<15}")
print("-"*80)

for url in test_urls:
    rf_result = detect_phishing(url, rf)
    svm_result = detect_phishing(url, svm)
    print(f"{url:<50} {rf_result:<15} {svm_result:<15}")

print("\n" + "="*50)
print("Model training complete!")
print(f"Random Forest: {rf_accuracy*100:.2f}% accuracy")
print(f"SVM: {svm_accuracy*100:.2f}% accuracy")
print("="*50)

