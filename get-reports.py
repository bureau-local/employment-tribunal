import json
import requests
from bs4 import BeautifulSoup

# Open the decisions data
with open("decisions-data.json") as infile:
	decisions_data = json.load(infile)

for i, decision in enumerate(decisions_data):
	# Go to the decision page
	decision_url = decision["Link"]
	# print(decision_url)
	r = requests.get(decision_url)
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
			# Get the first doc id
			doc_id_one = doc["id"]
			# Get the second doc id
			doc_id_two = doc_link.split("/")[4]
			# Get the filetype
			filetype = doc_link.split(".")[-1]
			
			# Download the doc
			outfile_name = doc_link.split("/")[-1]
			outfile_path = "pdf/" + outfile_name
			doc_content = requests.get(doc_link).content
			with open(outfile_path, "wb") as outfile:
			    outfile.write(doc_content)

	# Test with only the first two cases
	# if i > 0:
		# break

# Write the data to the output file:
# print("[*] Writing the data to the outputfile")
# with open("detailed-decisions-data.json", "w") as outfile:
   # json.dump(all_decisions, outfile)