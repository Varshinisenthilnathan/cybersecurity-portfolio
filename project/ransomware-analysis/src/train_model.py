import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

# Load expanded 320-sample dataset
df = pd.read_csv("ransomware_dataset_expanded.csv")

# Features and target
X = df.drop(["Sample", "Severity", "SeverityScore"], axis=1)
y = df["Severity"]

# Encode Low/Medium/Critical into numbers
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Predict test set
predictions = model.predict(X_test)

# Evaluation
acc = accuracy_score(y_test, predictions)
prec = precision_score(y_test, predictions, average="weighted", zero_division=0)
rec = recall_score(y_test, predictions, average="weighted", zero_division=0)
f1 = f1_score(y_test, predictions, average="weighted", zero_division=0)
 
print("\n===== Severity Model Performance =====")
print(f"Accuracy:  {acc*100:.2f}%")
print(f"Precision: {prec*100:.2f}%")
print(f"Recall:    {rec*100:.2f}%")
print(f"F1 Score:  {f1*100:.2f}%")
 
print("\n===== Performance by Severity Level =====")
print("Low      : SeverityScore 0–40")
print("Medium   : SeverityScore 41–108")
print("Critical : SeverityScore 109+")
print()
report = classification_report(
    y_test, predictions, target_names=encoder.classes_,
    output_dict=True, zero_division=0
)
for label in encoder.classes_:
    r = report[label]
    print(f"{label:<10} -> correctly identified {r['recall']*100:.0f}% of the time "
          f"({int(r['support'])} samples tested)")
 
print("\n===== Which Behaviours Mattered Most =====")
feature_names = {
    "ProcessCreate": "Process creation activity",
    "ProcessTerminate": "Process termination activity",
    "FileCreate": "File creation/modification activity",
    "RegistryCreateDelete": "Registry create/delete activity",
    "RegistryValueSet": "Registry value changes",
    "DNSQuery": "Network DNS queries",
}
ranked = sorted(zip(X.columns, model.feature_importances_), key=lambda x: x[1], reverse=True)
for feature, importance in ranked:
    label = feature_names.get(feature, feature)
    print(f"{label:<38} {importance*100:.1f}%")
# Save model and encoder
joblib.dump(model, "severity_model.pkl")
joblib.dump(encoder, "severity_encoder.pkl")

print("\nModel saved as severity_model.pkl")
print("Encoder saved as severity_encoder.pkl")
