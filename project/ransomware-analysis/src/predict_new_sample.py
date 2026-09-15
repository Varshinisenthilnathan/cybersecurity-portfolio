import pandas as pd
import joblib

model = joblib.load("severity_model.pkl")
encoder = joblib.load("severity_encoder.pkl")

# Example unseen sample features
# Change these values using a new sample's extracted Sysmon counts
new_sample = pd.DataFrame([{
    "ProcessCreate": 30,
    "ProcessTerminate": 8,
    "FileCreate": 40,
    "RegistryCreateDelete": 2,
    "RegistryValueSet": 5,
    "DNSQuery": 3
}])

prediction = model.predict(new_sample)
severity = encoder.inverse_transform(prediction)[0]

probabilities = model.predict_proba(new_sample)[0]
confidence = max(probabilities) * 100

print("Predicted Severity:", severity)
print("Confidence:", round(confidence, 2), "%")
