Looking at Columbia's acquisitions in NYC's property records.

## Reproduction

Run `make`. The Makefile goes through several steps:

Columbia goes by many different official names. To find these names, `parties.py` uses the ACRIS Real Properties Parties export on NYC OpenData. Any names containing both 'TRUSTEES' and 'COLUMBIA' are used as search keywords on ACRIS.

`documents.py` scrapes the search results from ACRIS. It extracts all the search results into one JSON file of documents.

`spatial-join.py` spatial joins each deed to a lot (~50s). (It uses the [NYC Digital Tax Map](https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page) ([docs](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/master/Metadata/Metadata_DigitalTaxMap.md)) lot polygons.) It writes another shapefile with just those lot-deed shaperecords. The output shapefile is small enough to transform with `mapshaper -points` if centroids are desired.

## Data notes

City Register File Numbers (CRFNs) are only available for documents recorded or filed [since January 2, 2003](https://acris.nyoss.com/AcrisHelp/docsearch/default.htm#!Documents/searchbydocumentidci.htm). The Document ID is a unique ACRIS identifier [for all records](https://acris.nyoss.com/AcrisHelp/docsearch/default.htm#!Documents/detailview.htm).
