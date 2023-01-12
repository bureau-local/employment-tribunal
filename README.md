# The Bureau's employment tribunal decisions monitor
Making sense of employment tribunal decisions

### Tasks
- [ ] Write script to analyse of the decisions data (most common defendant? etc.)
- [ ] Write script to search within the txt files
- [ ] An automation that runs/updates all step of the process automatically

## Methodology

### Data collection
This data was collected using the  from the [employment tribunal decisions portal](https://www.gov.uk/employment-tribunal-decisions) on gov.uk. This coverts employment tribunal dedicisions in England, Wales and Scotland.

There are two steps to the data collection process, (1) collect the decisions from the portal listed above, (2) then go through each link from the portal and collect the additional data on each decisions and download the relevant documents.

The code for the first step can be found in `get-all-decisions.py` and the code for the second step in `get-reports.py`.

### File conversions
`pdf-to-txt.py` is used to convert the collected pdfs to txts so we can analyse their content
`json-to-csv.py` is used to convert the collected data from json to csv, so it be more easily looked at and shared with colleagues


---
### The Data
Preliminary data can be found in the following [google sheet](https://docs.google.com/spreadsheets/d/1p034Bk3G2NwtwgOKXaYXHqdx00CcbIYoMyd1q6BdHxw/edit#gid=0)

---

### Other possible improvements
- [ ] Create the pdf/txt folders if they're missing before adding files in them
- [x] Ability to run the json to csv conversion for either decisions or document
- [ ] In the pdf to txt conversion, flag pdfs that can't be converted
- [ ] Re-write decisions-data.json rather than create a 2nd file
- [ ] Add a doc count columns to the decision data (?)
- [ ] Verify that all wording is consistent
- [ ] Move the requests_get_with_retries() function to a utils file
