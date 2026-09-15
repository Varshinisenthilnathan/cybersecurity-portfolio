import streamlit as st
import pandas as pd
import re
import joblib

df = pd.read_csv("ransomware_dataset_expanded.csv")

# The six behavioural feature columns used everywhere in this project
# (same order as in train_model.py, train_family_model.py, predict_sample.py)
FEATURE_COLS = [
    "ProcessCreate", "ProcessTerminate", "FileCreate",
    "RegistryCreateDelete", "RegistryValueSet", "DNSQuery",
]
def calculate_severity_score(row):
    return (
        row["ProcessCreate"] * 1 +
        row["ProcessTerminate"] * 1 +
        row["FileCreate"] * 3 +
        row["RegistryCreateDelete"] * 2 +
        row["RegistryValueSet"] * 2 +
        row["DNSQuery"] * 1
    )

def explain_severity_range(score):
    if score <= 40:
        return "Low", "0–40"
    elif score <= 108:
        return "Medium", "41–108"
    else:
        return "Critical", "109+"

st.title("Ransomware Behaviour Analysis Dashboard")

# ------------------------------------------------------------------
# 1. Dataset Summary
# ------------------------------------------------------------------
st.header("1. Dataset Summary")
st.caption("An overview of every ransomware sample used to train the models.")

st.metric("Samples Analysed", len(df))

with st.expander("View raw dataset"):
    st.dataframe(df)

# Replaces the old confusing "all 320 samples x all features" chart.
# NOTE: if your CSV's family column is named something other than
# "Family", change the line below to match.
if "Family" in df.columns:
    st.write("Samples per ransomware family:")
    st.bar_chart(df["Family"].value_counts())
else:
    st.write("Average behavioural activity across all samples:")
    st.bar_chart(df[FEATURE_COLS].mean())


# ------------------------------------------------------------------
# 2. Browse a Specific Sample
# ------------------------------------------------------------------
st.header("2. Browse a Specific Sample")
st.caption("Look up the recorded behaviour and severity for any sample already in the dataset.")

sample = st.selectbox("Select ransomware sample", df["Sample"])
selected = df[df["Sample"] == sample].iloc[0]

st.write("Behaviour counts for this sample:")
st.bar_chart(selected[FEATURE_COLS])

# Renamed from "Predicted Severity" -- this is the sample's actual
# recorded label from the dataset, not a live model prediction.
#st.metric("Recorded Severity", selected["Severity"])

recorded = selected["Severity"]

if recorded == "Low":
    recorded_text = "Low (score: 0–40)"
elif recorded == "Medium":
    recorded_text = "Medium (score: 41–108)"
else:
    recorded_text = "Critical (score: 109+)"

st.metric("Recorded Severity", recorded_text)

with st.expander("View full row"):
    st.write(selected)

# -----------------------------------------------------------------
# 3. Feature Importance Analysis
# ------------------------------------------------------------------
st.header("3. Feature Importance Analysis")
st.caption("Which behaviours the trained model actually relied on most, taken directly from the model itself.")

severity_model_for_fi = joblib.load("severity_model.pkl")

importance_df = pd.DataFrame({
    "Feature": FEATURE_COLS,
    "Importance": severity_model_for_fi.feature_importances_,
}).sort_values("Importance", ascending=False)

st.bar_chart(importance_df.set_index("Feature"))

# ------------------------------------------------------------------
# 4. Predict From a New Sysmon Log
# ------------------------------------------------------------------
st.header("4. Predict Severity and Family From a New Sysmon Log")
st.caption("Upload a Sysmon log from a newly executed sample to get a severity and family prediction.")

uploaded_file = st.file_uploader("Upload Sysmon log file", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8", errors="ignore")

    event_map = {
        "1": "ProcessCreate",
        "5": "ProcessTerminate",
        "11": "FileCreate",
        "12": "RegistryCreateDelete",
        "13": "RegistryValueSet",
        "22": "DNSQuery",
    }
    counts = {feature: 0 for feature in event_map.values()}

    events = re.findall(r"Event ID:\s*(\d+)", content)
    for event_id in events:
        if event_id in event_map:
            counts[event_map[event_id]] += 1

    features = pd.DataFrame([counts])

    st.write("Extracted behaviour features for this sample:")
    st.dataframe(features)

    severity_model = joblib.load("severity_model.pkl")
    severity_encoder = joblib.load("severity_encoder.pkl")
    family_model = joblib.load("family_model.pkl")
    family_encoder = joblib.load("family_encoder.pkl")

    severity_pred = severity_model.predict(features)
    family_pred = family_model.predict(features)

    severity = severity_encoder.inverse_transform(severity_pred)[0]
    family = family_encoder.inverse_transform(family_pred)[0]

    st.success(f"Predicted Family: {family}")
    
    if severity == "Low":
        severity_text = "Low (score: 0–40)"
    elif severity == "Medium":
        severity_text = "Medium (score: 41–108)"
    else:
        severity_text = "Critical (score: 109+)"

    st.warning(f"Predicted Severity: {severity_text}")
