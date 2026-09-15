import pandas as pd

df = pd.read_csv("ransomware_dataset_expanded.csv")

# Behaviour Score
df["SeverityScore"] = (
    df["ProcessCreate"] * 1 +
    df["ProcessTerminate"] * 1 +
    df["FileCreate"] * 3 +
    df["RegistryCreateDelete"] * 2 +
    df["RegistryValueSet"] * 2 +
    df["DNSQuery"] * 1
)

def assign_severity(score):
    if score <= 40:
        return "Low"
    elif score <= 108:
        return "Medium"
    else:
        return "Critical"

df["Severity"] = df["SeverityScore"].apply(assign_severity)

df.to_csv("ransomware_dataset_scored.csv", index=False)

print(df[["Sample","SeverityScore","Severity"]].head())
