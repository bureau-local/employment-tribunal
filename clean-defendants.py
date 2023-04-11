import csv
import json

# Set a test varible to write to a different file and break early
test = False
if test == True:
    decisions_data_file = "data-out/decisions-data-test.json"
else:
    decisions_data_file = "data-out/decisions-data.json"

# List of defendants to split from when multiple defendants are listed
with open("data-in/defendant-split.csv") as infile:
    reader = csv.DictReader(infile)
    defendant_split = [row["Defendant"] for row in reader]

# List to consolidate spelling varions of the same defendant name
with open("data-in/defendant-consolidation.csv") as infile:
    reader = csv.DictReader(infile)
    consolidate = {row["Listed name"]: row["Consolidated name"] for row in reader}

# Open the decisions data
with open(decisions_data_file) as infile:
    decisions_data = json.load(infile)

for i, decision in enumerate(decisions_data):
    defendant = decision["Defendant"].strip()
    
    # Correct the defendant name if needed
    if defendant.lower().endswith(" and others"):
        defendant = defendant[:-11]
    # Split multiple defendants into a list
    all_defendants = list()
    for entity_name in defendant_split:
        if entity_name in defendant:
            defendant = defendant.replace(entity_name, "")
            if defendant.startswith(" and "):
                defendant = defendant[5:]
            elif defendant.endswith(" and "):
                defendant = defendant[:-5]
            all_defendants.append(entity_name)
    if defendant != "":
        all_defendants.append(defendant)
    
    # Consolidate and check if they belong to a key group
    for defendant in all_defendants:
        # Consolidate the name
        if defendant in consolidate:
            defendant  = consolidate[defendant]

    # Assigned the cleaned defendant names to the decisons data
    decision["Defendant"] = " / ".join(all_defendants)

    # Print a process update
    if (i + 1) % 5000 == 0:
        update_msg = "[*] Cleaned the defendant names of {}/{} decisions"
        print(update_msg.format((i + 1), len(decisions_data)))
    
    # Conditional break used when testing
    if test and (i > 99):
        break

# Write the data to the output file
with open(decisions_data_file, "w") as outfile:
    json.dump(decisions_data, outfile)
