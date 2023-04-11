import csv
import json

from utils import get_fingerprint_plus

# Open the list of care organisations
with open("data-in/care-organisations.csv") as infile:
    reader = csv.DictReader(infile)
    care_organisations = {get_fingerprint_plus(row["Organisation name"]) for row in reader}

# Open the decisions data
with open("data-out/decisions-data.json") as infile:
    decisions_data = json.load(infile)

# Dictionary to store defendant level data
defendant_data = dict()

# Loop through the decisions
for i, decision in enumerate(decisions_data):
    listed_defendants = decision["Defendant"].split(" / ")
    
    # Loop through the decision listed defendants
    for defendant in listed_defendants:
        # If not already in the defendant level data dict...
        if defendant not in defendant_data:
            # ...create a dict to store data about them
            defendant_data[defendant] = dict()
            # And test if they belong to some key group
            
            # Local authority check - exceptions are false positives
            council_flags = ("council", "london borough", "royal borough")
            exceptions = ("arts council", "british council", "church council", "midwifery council", "national council", "reporting council", "research council", "school council", "services council", "toursim council", "town council")
            # Check if any flag and not any exceptions are in the name
            flag_test = [True for flag in council_flags if flag in defendant.lower()]
            exceptions_test = [True for val in exceptions if val in defendant.lower()]
            if any(flag_test) and not any(exceptions_test): 
                defendant_data[defendant]["Local authority"] = True
            else:
                defendant_data[defendant]["Local authority"] = False
            
            # NHS and Police checks
            key_groups = ["NHS", "Police"]
            for group in key_groups:
                if group.lower() in defendant.lower():
                    defendant_data[defendant][group] = True
                else:
                    defendant_data[defendant][group] = False
            
            # Care organisation check
            if get_fingerprint_plus(defendant) in care_organisations:
                defendant_data[defendant]["Care organisation"] = True
            else:
                defendant_data[defendant]["Care organisation"] = False

# Write the output defendant data
with open("data-out/defendant-data.json", "w") as outfile:
    json.dump(defendant_data, outfile)

