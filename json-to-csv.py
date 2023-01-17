import json
import csv

convert_decisions_data = True
convert_documents_data = False

# CONVERT THE DECISIONS DATA JSON TO CSV
if convert_decisions_data == True:
    # Open the decisions data json
    with open("decisions-data.json") as infile:
        decisions_data = json.load(infile)
    # Write the decisions data to a csv
    outhead = [key for key in decisions_data[0]]
    with open("decisions-data.csv", "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=outhead)
        writer.writeheader()
        writer.writerows(decisions_data)

# CONVERT THE DOCUMENTS DATA JSON TO CSV
if convert_documents_data == True:
    # Open the documents data json
    with open("documents-data.json") as infile:
        documents_data = json.load(infile)
    # Write the documents data to a csv
    outhead = [key for key in documents_data[0]]
    with open("documents-data.csv", "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=outhead)
        writer.writeheader()
        writer.writerows(documents_data)
