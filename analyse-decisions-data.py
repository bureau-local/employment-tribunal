import csv

# Open the decicions data
with open("decisions-data.csv") as infile:
    reader = csv.DictReader(infile)
    header = reader.fieldnames
    decisions_data = [row for row in reader]

# We will collect data on individual years since 2015
years = ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
# Dict to collect the defendant data
defendant_data = dict()
# Dict to collect the jurisdiction code data
jurisdiction_code_data = dict()
# Dict to collect the volume of decisions over time data (by quarter)
over_time_data = dict()

# Loop through each decision
for decision in decisions_data:
    # Assign the relevant data from the spreadsheet to vars
    decision_id = decision["Decision id"]
    defendant = decision["Defendant"]
    jurisdiction_codes = decision["Jurisdiction code"].split(", ")
    decision_date = decision["Decision date"]
    
    # Get the year of complaint from the decision id
    year_of_complaint = decision_id.split("/")[-1][:4]
    # For now we just skip if we get an unexpected year
    if year_of_complaint not in years:
        # !!! TO BE UPDATED !!!
        pass

    # DEFENDANT ANALYSIS
    # Add defendant to the defendant data dict
    if defendant not in defendant_data:
        defendant_data[defendant] = dict()
        defendant_data[defendant]["Defendant"] = defendant
        for y in years:
            defendant_data[defendant][y] = 0
        defendant_data[defendant]["Total"] = 0
        # Check if the defendant belongs to one of those key groups
        key_groups = ["NHS", "Council", "Police"]
        for group in key_groups:
            if group.lower() in defendant.lower():
                defendant_data[defendant][group] = True
            else:
                defendant_data[defendant][group] = False
    # Increment the totals
    if year_of_complaint in years:
        defendant_data[defendant][year_of_complaint] += 1
    defendant_data[defendant]["Total"] += 1

    # JURISDICTION CODE ANALYSIS
    for code in jurisdiction_codes:
        if code not in jurisdiction_code_data:
            jurisdiction_code_data[code] = dict()
            jurisdiction_code_data[code]["Jurisdiction code"] = code
            for y in years:
                jurisdiction_code_data[code][y] = 0
            jurisdiction_code_data[code]["Total"] = 0
        # Increment the totals
        if year_of_complaint in years:
            jurisdiction_code_data[code][year_of_complaint] += 1
        jurisdiction_code_data[code]["Total"] += 1

    # OVER TIME ANALYSIS
    # Get the quarter the decision was made in
    decision_year = decision_date[:4]
    decision_month = decision_date[5:7]
    if decision_month in ("01", "02", "03"):
        decision_quarter = decision_year + "-01"
    elif decision_month in ("04", "05", "06"):
        decision_quarter = decision_year + "-02"
    elif decision_month in ("07", "08", "09"):
        decision_quarter = decision_year + "-03"
    elif decision_month in ("10", "11", "12"):
        decision_quarter = decision_year + "-04"
    
    # Add quarter to over time dict
    if decision_quarter not in over_time_data:
        over_time_data[decision_quarter] = dict()
        over_time_data[decision_quarter]["Quarter"] = decision_quarter
        for y in years:
            over_time_data[decision_quarter][y] = 0
        over_time_data[decision_quarter]["Total"] = 0
    # Increment the totals
    if year_of_complaint in years:
        over_time_data[decision_quarter][year_of_complaint] += 1
    over_time_data[decision_quarter]["Total"] += 1


# Remove the key in the defendant dict and write the output data
defendant_data = [val for key, val in defendant_data.items()]
outhead = ["Defendant"] + years + ["Total"] + key_groups
with open("defendant-analysis.csv", "w") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=outhead)
    writer.writeheader()
    writer.writerows(defendant_data)

# Remove the key in the jurisdiction code dict and write the output data
jurisdiction_code_data = [val for key, val in jurisdiction_code_data.items()]
outhead = ["Jurisdiction code"] + years + ["Total"]
with open("jurisdiction-code-analysis.csv", "w") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=outhead)
    writer.writeheader()
    writer.writerows(jurisdiction_code_data)

# Remove the keys in the over time analysis and write the output data
over_time_data = [val for key, val in over_time_data.items()]
outhead = ["Quarter"] + years + ["Total"]
with open("over-time-analysis.csv", "w") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=outhead)
    writer.writeheader()
    writer.writerows(over_time_data)
