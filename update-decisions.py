import json
import time

from bs4 import BeautifulSoup

from utils import requests_get_with_retries

# Variables to build the employement tribunal decisions url
base_url = "https://www.gov.uk"
search_url = "/employment-tribunal-decisions?page={}"
page = 1
# Large inacurate page count until we get the actual page count
page_count = 1000000000000
# Variable to parse the html
pagination_class = "govuk-pagination__link-label"

# Load the decisions data we already have
with open("decisions-data.json") as infile:
    decisions_data = json.load(infile)
# Group all the deicisions ids in a set
collected_decision_ids = [dec["Decision id"] for dec in decisions_data]
# Start the update data collection process
print("[*] Starting data collection process")
while page <= page_count:
    print("[*] Collecting data for page {}".format(page))
    paginated_url = base_url + search_url.format(page)
    r = requests_get_with_retries(paginated_url)
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, "lxml")
        # If first page get page count
        if page == 1:
            label = soup.find("span", {"class": pagination_class}).text
            page_count = int(label.split(" of ")[-1])
        # Get all decisions data on the page
        decisions = soup.findAll("li", {"class": "gem-c-document-list__item"})
        # Get the decision ids of all deicisons on the page
        page_ids = [dec.find("a").text.split(": ")[-1] for dec in decisions]
        # Check if all the page ids have already been collected
        collection_check = [id in collected_decision_ids for id in page_ids]
        # Break if we've already collected data for all ids on the page
        if all(collection_check):
            break
    # Increment the page count
    page += 1
    # Sleep for 1 sec between each call to gov.uk
    time.sleep(1)
    # Break after page 3 when testing
    if page > 3:
        break
