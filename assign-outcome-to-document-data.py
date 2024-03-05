import json

# Dictionary to assign outcome type
outcome_types = {
	"- dimissal": "Dismissal",
	"-dismissal": "Dismissal",
	"- dismissal": "Dismissal",
	"- dismissed": "Dismissal",
	"- amended judgment": "Judgment",
	"- amended reserved judgment": "Judgment",
	"- certificate of correction and new judgment": "Judgment",
	"- corrected judgment": "Judgment",
	"- corrected remedy judgment": "Judgment",
	"- corrected reserved judgment": "Judgment",
	"- consent judgment": "Judgment",
	"- default judgement": "Judgment",
	"- final judgment": "Judgment",
	"- judgement": "Judgment",
	"- judgmemt with reasons": "Judgment",
	"-  judgment": "Judgment", 
	"- judgment": "Judgment",
	"- judgment by consent": "Judgment",
	"- judgment and reasons": "Judgment",
	"- judgment with reasons": "Judgment",
	"- jurisdiction judgment": "Judgment",
	"- liability judgment": "Judgment",
	"- reasons judgment": "Judgment",
	"-reconsideration judgment": "Judgment",
	"- reconsideration judgment": "Judgment",
	"- reconsideration judgment with reasons": "Judgment",
	"- remedy judgment": "Judgment",
	"- reserved judgment": "Judgment",
	"- reserved judgement": "Judgment",
	"- reserved unanimous judgment": "Judgment",
	"- reserved liability judgment": "Judgment",
	"- partial dismissal": "Partial dismissal",
	"- partial strike out": "Partial strike out",
	"- partial withdrawal": "Partial withdrawal",
	"- srike out": "Strike out",
	"- stike out": "Strike out",
	"- stirke out": "Strike out",
	"- strike out": "Strike out",
	"- strike-out": "Strike out",
	"- strke out": "Strike out",
	"- struck out": "Strike out",
	"- struk out with reasons": "Strike out",
	"- full withdrawal": "Withdrawal",
	"-withdrawal": "Withdrawal",
	"- withdrawal": "Withdrawal",
	"2007 withdrawal": "Withdrawal",
	"2008 strike out": "Strike out",
	"2008 withdrawal": "Withdrawal",
	"2013 withdrawal": "Withdrawal",
	"2016 withdrawal": "Withdrawal",
	"2017 dismissal": "Dismissal",
	"2017 judgment": "Judgment",
	"2017 strike out": "Strike out",
	"2017 withdrawal": "Withdrawal",
	"2018 dismissal": "Dismissal",
	"others withdrawal": "Withdrawal"
}

# Get a case outcome based on the document name
# @params doc_name: string
def get_outcome_type_from_name(doc_name):
	for phrase in outcome_types:
		if phrase in doc_name:
			return outcome_types[phrase]
	# If no match is found assign a blank to the outcome
	return ""

# Open the documents data
with open("data-out/documents-data.json") as infile:
	documents_data = json.load(infile)

# Count for the number of doc we can't assign an outcome type for
unlabeled_count = 0
# Get an outcome type for each do if possible
for doc_id in documents_data:
	doc = documents_data[doc_id]
	# Skip if an outcome as already been assigned
	if "Outcome" in doc and doc["Outcome"] != "":
		continue
	doc_name = doc["Document name"].lower()
	outcome = get_outcome_type_from_name(doc_name)
	# If we didn't find an outcome type print the doc name to audit
	if outcome == "":
		print(doc_name)
		unlabeled_count += 1
	doc["Outcome"] = outcome

# Check how many doc we couldn't get an outcome type for
print("[*] Couldn't get an outcome type for {} documents".format(unlabeled_count))
# Write the updated documents data
print("[*] Writing the output data")
with open("data-out/documents-data.json", "w") as outfile:
	json.dump(documents_data, outfile)

print("[*] Task completed!")
