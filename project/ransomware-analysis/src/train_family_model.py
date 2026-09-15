import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

df = pd.read_csv("ransomware_dataset_expanded.csv")

# Family column should exist in your 320 dataset
X = df.drop(["Sample", "Severity"], axis=1)
y = df["Sample"]

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Family Classification Results")
print("Accuracy:", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions, average="weighted", zero_division=0))
print("Recall:", recall_score(y_test, predictions, average="weighted", zero_division=0))
print("F1 Score:", f1_score(y_test, predictions, average="weighted", zero_division=0))

print("\nClassification Report:")
print(classification_report(y_test, predictions, target_names=encoder.classes_, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

joblib.dump(model, "family_model.pkl")
joblib.dump(encoder, "family_encoder.pkl")

print("\nModel saved as family_model.pkl")
print("Encoder saved as family_encoder.pkl")
