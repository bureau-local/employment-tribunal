# The Bureau's employment tribunal decisions monitor
Making sense of employment tribunal decisions

### Tasks
- [x] Write script to analyse of the decisions data (most common defendant? etc.)
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
We convert PDFs to text files with `pdf-to-txt.py`, in order to analyse their content programmatically
`json-to-csv.py` is used to convert the collected data from json to csv, so it be more easily looked at and shared with colleagues

### Data analisys
We analyse the decisions data to look at the most common defendants, the most common jurisdiction code and the number of decisions made over time. The analysis for the most common defendants includes flags for the nhs, councils, police forces and care organisations.

We perform the analysis with `analyse-decisions-data.py`.

### Preparing the care data
Unfortunately, the CQC doesn't maintain a list of providers on it's ["Using CQC data" webpage](https://www.cqc.org.uk/about-us/transparency/using-cqc-data). Instead, the data seems to be maintained by location, with all the different locations from a single providers recorded individually. To make the mather more confusing, there are also "brands" (such as Bluebird Care) which seem to work like franchises where all their locations are registered to different/single providers but under the same brand.

As such, to build our list of care organistions we will want to extract "brands" and providers which appear more than once from the data about individual locations containded in the "Care directory with filters" ODS file on the "Using CQC data" webpage linked above. The "Locations regulated by CQC" CSV download option on the same page doesn't include the "brand" information so we have to download the ODS file. To convert the data to CSV we simply import the ODS file to a googlesheet and download the tab with the data as CSV.

It's also worth noting that the CQC also has a [serching tool](https://www.cqc.org.uk/search/all) that allows to download the results as CSV, but it doesn't include brand information and the CSV download is limited to 15,000 rows which is less thamn the total number of active providers. For these reason the method described above was prefered.

We extract our list of care organisations from the CQC care directory data using `extract-care-organisations.py`.

The care directory file from the CQC is updated monthly, with the version we are working from being the one from April 2023. How often should we update the care directory list we are working with is a question we need to ask ourselves. Similarly, is it worth downloading information about inactive care organisation from years past to match against employement tribunal cases from those years?

---
### The Data
Preliminary data can be found in the following [google sheet](https://docs.google.com/spreadsheets/d/1p034Bk3G2NwtwgOKXaYXHqdx00CcbIYoMyd1q6BdHxw/edit#gid=0)

---

### Other thoughts/possible improvements
- [x] Create the pdf/txt folders if they're missing before adding files in them
- [x] Ability to run the json to csv conversion for either decisions or document
- [ ] It would be neat to check if a pdf is a scanned image or containes searchable text we can extract ([see this](https://stackoverflow.com/questions/55704218/how-to-check-if-pdf-is-scanned-image-or-contains-text))
- [x] Re-write `decisions-data.json` rather than create a 2nd file
- [ ] Do we really need the temp file in `update-decisions.py`
- [ ] Add a document count columns to the decision data
- [x] Move the requests_get_with_retries() function to a utils file
- [x] Add a function to automate retries when making requests to gov.uk
- [ ] Refactor, the similar code from `get-all-decisions.py` and `update-decisions.py` in the `utils.py`
- [ ] For example here is a [decision](https://www.gov.uk/employment-tribunal-decisions/ms-a-n-harris-v-adecco-uk-ltd-and-amazon-uk-services-ltd-4100059-slash-2021), that we collected data for and which was later updated to include the judgment with resasons as part of the reports. The Decision date was also changed from what we had on record... was it???
- [ ] Could an id ever change? We probably want to test that by checking for duplicated urls in `decisions-data.json`
- [x] In the defendant analysis, add flags for defendant type (i.e. council, nhs, police)
- [ ] It would be great to add additional sector flags (i.e. for care, gig economy...)
- [ ] Find a way to localise the decisions? Maybe from "heard at" tribunal info in the pdfs
- [x] Remove town, church and school councils from local authority flag (also British council)
- [ ] Search for Visa in the text files
- [ ] Should we be matching with lowercase as well
- [x] Extract list of care organisations from the CQC care directory
- [x] Refactor the defendant analysis in a seperate file from the jurisdiction and over time analysis
- [x] Add a "Care organisation" flag to the defendant analysis
- [ ] Add CQC rating
- [x] Refactor the local authority flag to also match on "london borough" and "royal borough"
- [x] Refactor the local authority flag to avoid false positives from the word "council"
- [ ] Would I be better with a list of local authorities like we do for care organisations 
- [x] "Ltd" is showing up in the defendant analysis
