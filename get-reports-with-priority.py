import csv
import json
import os
import time

from bs4 import BeautifulSoup

from utils import requests_get_with_retries

# Create a pdf folder if there isn't one
if not os.path.isdir("pdf"):
    os.makedirs("pdf")

# Get list of prioritised ids
with open("data-in/all-skilled-home-care-sponsors.csv") as infile:
	reader = csv.DictReader(infile)
	priority_ids = [row["Employement Tribunal decisions ids"] for row in reader]
    # Remove blank values
	priority_ids = [val for val in priority_ids if val != ""]
	priority_ids = [case_id for val in priority_ids for case_id in val.split(" / ")]

# Open the decisions data
with open("data-out/decisions-data.json") as infile:
	decisions_data = json.load(infile)
# Decisions count
decisions_total = len(decisions_data)

# Load any existing documents data or start with blank list
if "documents-data.json" in os.listdir("data-out"):
	with open("data-out/documents-data.json") as infile:
		all_documents = json.load(infile)
else:
	all_documents = dict()

# Loop through decisions, collecting the relevant data and docs for each
print("[*] Collecting data and docs on {} decisions".format(decisions_total))
for i, decision in enumerate(decisions_data):
	decision_id = decision["Decision id"]
	# Skip if the id is not in the priority list
	if decision_id not in priority_ids:
		continue
	decision_url = decision["Link"]
	r = requests_get_with_retries(decision_url)
	if r.status_code == 200:
		html = r.text
		soup = BeautifulSoup(html, "lxml")
		# Grab the data that wasn't available on the search results page
		# Published date
		published_date = soup.find("dt", string="Published")
		published_date = published_date.find_next_sibling().text
		# Country
		country = soup.find("dt", string="Country: ")
		country = country.find_next_sibling().text
		# Juridiction code
		juridiction_code = soup.find("dt", string="Jurisdiction code: ")
		juridiction_code = juridiction_code.find_next_sibling().text.strip()
		# Add the new data to the decision dict
		decision["Published date"] = published_date
		decision["Country"] = country
		decision["Jurisdiction code"] = juridiction_code
		# Look for documents
		documents = soup.select("span[class=attachment-inline]")
		for doc in documents:
			doc_name = doc.text
			doc_type = doc_name.split("-")[-1].strip()
			doc_link = doc.find("a")["href"]
			filetype = doc_link.split(".")[-1]	
			# Get the first doc id
			doc_id_one = doc["id"]
			# Get the second doc id
			doc_id_two = doc_link.split("/")[4]
			# Structuring the document data in a dict
			document_data = {
				"Document id (1)": doc_id_one,
				"Document id (2)": doc_id_two,
				"Document name": doc_name,
				"Link": doc_link,
				"filetype": filetype,
				"Decision page": decision_url,
				"Decision id": decision_id
			}
			all_documents[doc_id_one] = document_data
			
			# Download the doc
			outfile_name = doc_link.split("/")[-1]
			doc_content = requests_get_with_retries(doc_link).content
			with open("pdf/" + outfile_name, "wb") as outfile:
				outfile.write(doc_content)
	
	# Print a process update in the terminal
	if (i+1) % 20 == 0:
		update_msg = "[*] Collected documents for {}/{} decisions"
		print(update_msg.format(i+1, decisions_total)) 
	# Sleep for a second between each call
	time.sleep(1)
	# Test with only the first twenty decisions
	# if i > 99:
		# break

# Write the full decision data, first to a temp file
print("[*] Writing the full decisions data")
with open("data-out/decisions-data-temp.json", "w") as outfile:
   json.dump(decisions_data, outfile)
# Delete the original file and rename the temp file
os.remove("data-out/decisions-data.json")
os.rename("data-out/decisions-data-temp.json", "data-out/decisions-data.json")

# Write the document data
print("[*] Writing the documents data")
with open("data-out/documents-data.json", "w") as outfile:
   json.dump(all_documents, outfile)

print("[+] Task Completed")
