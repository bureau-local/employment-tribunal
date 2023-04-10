import csv

from utils import get_fingerprint_plus



# Open the decicions data
with open("data-out/decisions-data.csv") as infile:
    reader = csv.DictReader(infile)
    decisions_data = [row for row in reader]

# List of defendants to split from when multiple defendants are listed
with open("data-in/defendant-split.csv") as infile:
    reader = csv.DictReader(infile)
    defendant_split = {row["Defendant"] for row in reader}

# List to consolidate spelling varions of the same defendant name
with open("data-in/defendant-consolidation.csv") as infile:
    reader = csv.DictReader(infile)
    consolidate = {row["Listed name"]: row["Consolidated name"] for row in reader}

# List of care organisations
with open("data-in/care-organisations.csv") as infile:
    reader = csv.DictReader(infile)
    care_organisations = {get_fingerprint_plus(row["Organisation name"]) for row in reader}

# We will collect data on individual years since 2015
years = ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
# Dict to collect the defendant data
defendant_data = dict()

# Loop through each decision
for decision in decisions_data:
    # Assign the relevant data from the spreadsheet to vars
    decision_id = decision["Decision id"]
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
    
    # Get the year of complaint from the decision id
    year_of_complaint = decision_id.split("/")[-1][:4]
    # For now we just skip if we get an unexpected year
    if year_of_complaint not in years:
        # !!! TO BE UPDATED !!!
        pass

    # DEFENDANT ANALYSIS
    # Add defendant to the defendant data dict
    for defendant in all_defendants:
        # Consolidate the defendant names:
        if defendant in consolidate:
            defendant  = consolidate[defendant]
        # Add defendant to defendant data dict
        if defendant not in defendant_data:
            defendant_data[defendant] = dict()
            defendant_data[defendant]["Defendant"] = defendant
            for y in years:
                defendant_data[defendant][y] = 0
            defendant_data[defendant]["Total"] = 0
            
            # Check if the defendant is a local authority
            defendant_data[defendant]["Local authority"] = False
            council_flags = ("council", "london borough", "royal borough")
            # Exceptions are false positives
            exceptions = ("arts council", "british council", "church council", "midwifery council", "national council", "reporting council", "research council", "school council", "services council", "toursim council", "town council")
            # Check if any flag and not any exceptions are in the name
            flag_test = [True for flag in council_flags if flag in defendant.lower()]
            exceptions_test = [True for val in exceptions if val in defendant.lower()]
            if any(flag_test) and not any(exceptions_test): 
                defendant_data[defendant]["Local authority"] = True
            else:
                defendant_data[defendant]["Local authority"] = False
            
            # Check if the defendant belongs to one of those key groups
            key_groups = ["NHS", "Police"]
            for group in key_groups:
                if group.lower() in defendant.lower():
                    defendant_data[defendant][group] = True
                else:
                    defendant_data[defendant][group] = False
            
            # Check if the defendant is a care organisations
            if get_fingerprint_plus(defendant) in care_organisations:
                defendant_data[defendant]["Care organisation"] = True
            else:
                defendant_data[defendant]["Care organisation"] = False
        
        # Increment the totals
        if year_of_complaint in years:
            defendant_data[defendant][year_of_complaint] += 1
            defendant_data[defendant]["Total"] += 1

# Remove the key in the defendant dict and write the output data
defendant_data = [val for key, val in defendant_data.items()]
outhead = ["Defendant"] + years + ["Total", "Local authority"] + key_groups + ["Care organisation"]
with open("data-out/defendant-analysis.csv", "w") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=outhead)
    writer.writeheader()
    writer.writerows(defendant_data)
