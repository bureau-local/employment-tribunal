from collections import Counter
import csv

# Open the CQC care directory data
with open("data-in/CQC-April-2023-Active-Locations.csv") as infile:
    reader = csv.DictReader(infile)
    header = reader.fieldnames
    cqc_locations = [row for row in reader]

# To group all care organisations
care_organisations = list()

# Get brands, slice the brand name to remove "BRAND "
brands = {(x["Brand ID"], x["Brand Name"][6:]) for x in cqc_locations if x["Brand ID"] != "-"}
# Format the brands data and add to the care organisations list
brands = [{"Organisation ID": org[0], "Organisation name": org[1]} for org in brands]
care_organisations.extend(brands)

# Get providers
providers = {(loc["Provider ID"], loc["Provider Name"]) for loc in cqc_locations}
# Get all the providers ids
providers_ids = [loc["Provider ID"] for loc in cqc_locations]
# Get a count of all provider ids
providers_ids = Counter(providers_ids)
# Keep only the providers with more than one active locations
providers = {org for org in providers if providers_ids[org[0]] > 1}
# Add to the care orgs list
providers = [{"Organisation ID": org[0], "Organisation name": org[1]} for org in providers]
care_organisations.extend(providers)

# Write the output data
with open("data-in/care-organisations.csv", "w") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=["Organisation ID", "Organisation name"])
    writer.writeheader()
    writer.writerows(care_organisations)
