import csv
import json

from utils import get_fingerprint_plus

# Open the data about defendant groups
with open("data-out/defendant-data.json") as infile:
    groups_data = json.load(infile)

# Open the list of care organisations
with open("data-in/care-organisations.csv") as infile:
    reader = csv.DictReader(infile)
    care_organisations = {get_fingerprint_plus(row["Organisation name"]) for row in reader}

# Open the decicions data
with open("data-out/decisions-data.csv") as infile:
    reader = csv.DictReader(infile)
    decisions_data = [row for row in reader]

# We will collect data on individual years since 2015
years = ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
# The key group contained in the defendant groups data
# Which we want to add to analysis
key_groups = ["Local authority", "NHS", "Police", "Care organisation"]

# Dict to collect the defendant data
defendant_data = dict()

# Loop through the decisions
for decision in decisions_data:
    # Assign the relevant data from the spreadsheet to vars
    decision_id = decision["Decision id"]
    listed_defendant = decision["Defendant"].split(" / ")
    
    # Get the year of complaint from the decision id
    year_of_complaint = decision_id.split("/")[-1][:4]
    # For now we just skip if we get an unexpected year
    if year_of_complaint not in years:
        # !!! TO BE UPDATED !!!
        pass

    # DEFENDANT ANALYSIS
    # Add defendant to the defendant data dict
    for defendant in listed_defendant:
        # Add defendant to defendant data dict
        if defendant not in defendant_data:
            defendant_data[defendant] = dict()
            defendant_data[defendant]["Defendant"] = defendant
            for y in years:
                defendant_data[defendant][y] = 0
            defendant_data[defendant]["Total"] = 0
            
            # Add the defendant key group flags
            for group in key_groups:
                defendant_data[defendant][group] = groups_data[defendant][group]
                    
        # Increment the totals
        if year_of_complaint in years:
            defendant_data[defendant][year_of_complaint] += 1
            defendant_data[defendant]["Total"] += 1

# Remove the key in the defendant dict and write the output data
defendant_data = [val for key, val in defendant_data.items()]
outhead = ["Defendant"] + years + ["Total"] + key_groups
with open("data-out/defendant-analysis.csv", "w") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=outhead)
    writer.writeheader()
    writer.writerows(defendant_data)
