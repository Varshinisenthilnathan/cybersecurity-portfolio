import os
import re
import csv

dataset_folder = "."
output_csv = "ransomware_dataset.csv"

event_ids = ["1", "5", "11", "12", "13", "22"]

rows = []

for file in os.listdir(dataset_folder):
    if file.endswith("_log.txt"):

        counts = {eid: 0 for eid in event_ids}

        with open(file, "r", errors="ignore") as f:
            content = f.read()

        matches = re.findall(r"Event ID:\s*(\d+)", content)

        for m in matches:
            if m in counts:
                counts[m] += 1

        rows.append([
            file.replace("_log.txt", ""),
            counts["1"],
            counts["5"],
            counts["11"],
            counts["12"],
            counts["13"],
            counts["22"]
        ])

with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow([
        "Sample",
        "ProcessCreate",
        "ProcessTerminate",
        "FileCreate",
        "RegistryCreateDelete",
        "RegistryValueSet",
        "DNSQuery"
    ])

    writer.writerows(rows)

print(f"Dataset saved as {output_csv}")
