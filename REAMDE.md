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

Then, it extracts the search results into a CSV file.