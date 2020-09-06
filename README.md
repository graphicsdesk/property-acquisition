Looking at Columbia's acquisitions in NYC's property records.

## Data

Run `make`. The Makefile goes through several steps:

Columbia goes by many different official names. To find these names, `parties.py` uses the ACRIS Real Properties Parties export on NYC OpenData. Any names containing both 'TRUSTEES' and 'COLUMBIA' are used as search keywords on ACRIS.

`documents.py` scrapes the search results from ACRIS. It extracts all the search results into one JSON file of documents.

It then merges the JSON with a shapefile of blocks and lots (either [this](https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page) or [this](https://data.cityofnewyork.us/Housing-Development/Department-of-Finance-Digital-Tax-Map/smk3-tmxj)).
