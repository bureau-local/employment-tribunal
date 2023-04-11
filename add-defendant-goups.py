import json

# Open the data about defendant groups
with open("data-out/defendant-data.json") as infile:
    groups_data = json.load(infile)

# Open the decisions data
with open("data-out/decisions-data.json") as infile:
    decisions_data = json.load(infile)

# The key group contained in the defendant groups data
# Which we want to add to the decisions data
key_groups = ["Local authority", "NHS", "Police", "Care organisation"]

# Loop through decisions
for i, decision in enumerate(decisions_data):
    listed_defendants = decision["Defendant"].split(" / ")

    # Add flags for each key group to the decisions data
    for group in key_groups:
        group_flags = [groups_data[defendant][group] for defendant in listed_defendants]
        if any(group_flags):
            decision[group] = True
        else:
            decision[group] = False
    
    # Conditional break used when testing
    # if i > 99:
        # break

# Write the data to the output file
with open("data-out/decisions-data.json", "w") as outfile:
    json.dump(decisions_data, outfile)
