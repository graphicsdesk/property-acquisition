Looking at Columbia's acquisitions in NYC's property records.

## Data

Run `make`. The Makefile goes through several steps:

It first scrapes search results from ACRIS. The current search critera:
```
Name:   THE TRUSTEES OF COLUMBIA UNIVERSITY
Date:   01/01/1966-09/02/2020
Party Type:  All Parties
Borough/County:  All Boroughs/Counties
Document Class:  All Document Classes
```

Next, it extracts the search results into a JSON file.

It then merges the JSON with a shapefile of blocks and lots (either [this](https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page) or [this](https://data.cityofnewyork.us/Housing-Development/Department-of-Finance-Digital-Tax-Map/smk3-tmxj)).

