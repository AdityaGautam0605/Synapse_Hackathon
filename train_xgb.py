import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import xgboost as xgb

from app.services.feature_pipeline import build_features


# ---- LOAD DATA ----
df = pd.read_csv("multimodal_sports_injury_dataset.csv")

# ---- FEATURE ENGINEERING ----
engineered = build_features(df)

target_col = "injury_occurred"

if target_col not in engineered.columns:
    raise ValueError("Target column 'injury_occurred' not found.")

X = engineered.drop(columns=[target_col])
y = engineered[target_col]

# Convert multi-class injury to binary
y = (y > 0).astype(int)

print("Unique target values AFTER binarization:", y.unique())

print("Unique target values:", y.unique())

feature_names = list(X.columns)

feature_names = list(X.columns)

# ---- TRAIN TEST SPLIT ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---- SCALING ----
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# ---- MODEL ----
clf = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric="logloss"
)

clf.fit(X_train_s, y_train)

# ---- EVALUATION ----
y_proba = clf.predict_proba(X_test_s)[:, 1]
auc = roc_auc_score(y_test, y_proba)

print("AUC:", auc)

# ---- SAVE ARTIFACTS ----
Path("app/models").mkdir(parents=True, exist_ok=True)

joblib.dump(clf, "app/models/xgb_model.pkl")
joblib.dump(scaler, "app/models/xgb_scaler.pkl")
joblib.dump(feature_names, "app/models/xgb_features.pkl")

print("Model artifacts saved successfully.")