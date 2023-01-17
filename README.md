# The Bureau's employment tribunal decisions monitor
Making sense of employment tribunal decisions

### Tasks
- [ ] Write script to analyse of the decisions data (most common defendant? etc.)
- [ ] Write script to search within the txt files
- [x] Write a script to update the decisions data with the latest decisions
- [ ] Automate the decisions data collection process
- [ ] An automation to track/get new reports when they're published (and convert them to txt)

## Methodology

### Data collection
This data was collected using the  from the [employment tribunal decisions portal](https://www.gov.uk/employment-tribunal-decisions) on gov.uk. This coverts employment tribunal dedicisions in England, Wales and Scotland.

There are two steps to the data collection process, (1) collect the decisions from the portal listed above, (2) then go through each link from the portal and collect the additional data on each decisions and download the relevant documents.

The code for the first step can be found in `get-all-decisions.py` to scrape all decisions, or with `update-decisions.py` to only get new decisions. The data collection in `update-decisions.py` automatically breaks when it reaches a page where we've already collected data for every decision id listed on the page.

The code for the second step can be found in `get-reports.py`.

### File conversions
`pdf-to-txt.py` is used to convert the collected pdfs to txts so we can analyse their content
`json-to-csv.py` is used to convert the collected data from json to csv, so it be more easily looked at and shared with colleagues


---
### The Data
Preliminary data can be found in the following [google sheet](https://docs.google.com/spreadsheets/d/1p034Bk3G2NwtwgOKXaYXHqdx00CcbIYoMyd1q6BdHxw/edit#gid=0)

---

### Other thoughts/possible improvements
- [ ] Create the pdf/txt folders if they're missing before adding files in them
- [x] Ability to run the json to csv conversion for either decisions or document
- [ ] In the pdf to txt conversion, flag pdfs that can't be converted
- [ ] Re-write `decisions-data.json` rather than create a 2nd file
- [ ] Add a doc count columns to the decision data (?)
- [ ] Verify that all wording is consistent
- [x] Move the requests_get_with_retries() function to a utils file
- [ ] Add a function to automate retries when making requests to gov.uk
- [ ] Refactor, the similar code from `get-all-decisions.py` and `update-decisions.py` in the `utils.py`
- [ ] For example here is a [decision](https://www.gov.uk/employment-tribunal-decisions/ms-a-n-harris-v-adecco-uk-ltd-and-amazon-uk-services-ltd-4100059-slash-2021), that we collected data for and which was later updated to include the judgment with resasons as part of the reports. The Decision date was also changed from what we had on record
- [ ] Could an id ever change? We probably wan to test that by checking for duplicated urls in `decisions-data.json`
