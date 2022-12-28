from bs4 import BeautifulSoup

import json
import requests
import time

# Variables to build the url
base_url = "https://www.gov.uk"
search_url = "/employment-tribunal-decisions?page="
page = 1
# Large inacurate page count until we get the actual page count
page_count = 1000000000000
# Variable to parse the html
pagination_class = "gem-c-pagination__link-label"

# A list to group all decisions data we collect
all_decisions = list()
# Start the data collection process
print("[*] Starting data collection process")
while page <= page_count:
	print(page)
	paginated_url = base_url + search_url + str(page)
	r = requests.get(paginated_url)
	time.sleep(1)
	if r.status_code == 200:
		html = r.text
		soup = BeautifulSoup(html, "lxml")
		# If first page get page count
		if page == 1:
			label = soup.find("span", {"class": pagination_class}).text
			page_count = int(label.split(" of ")[-1])
		# Get all decisions data on the page
		decisions = soup.findAll("li", {"class": "gem-c-document-list__item"})
		# Get individual decisions
		for decision in decisions:
			# Getting the individual data points
			decision_name = decision.find("a").text
			decision_id = decision_name.split(": ")[-1]
			plaintiff_and_defendant = decision_name.split(": ")[0]
			plaintiff = plaintiff_and_defendant.split(" v ")[0]
			defendant = plaintiff_and_defendant.split(" v ")[-1]
			link = base_url + decision.find("a")["href"]
			decision_date = decision.find("time")["datetime"]
			# Structuring the data in a dict
			decision_data = {
				"Decision id": decision_id,
				"Decision name": decision_name,
				"Plaintiff": plaintiff,
				"Defendant": defendant,
				"Link": link,
				"Decision date": decision_date
			}
			all_decisions.append(decision_data)
	# print a process update
	if page % 100 == 0:
		update_string = "[*] Collected decisions data from {}/{} pages"
		print(update_string.format(page, page_count))
	# increment the page count
	page += 1
	# break after first page when testing
	# if page > 1:
		# break

# Write the data to the output file:
print("[*] Writing the data to the outputfile")
with open("decisions-data.json", "w") as outfile:
   json.dump(all_decisions, outfile)

print("[*] Job completed :))")
