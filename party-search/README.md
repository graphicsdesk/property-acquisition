The current code requires the [ACRIS Real Property Parties](https://data.cityofnewyork.us/City-Government/ACRIS-Real-Property-Parties/636b-3b5g) data. It must be manually downloaded into this directory since it's too large to commit to the repository.

In the Makefile, the KEYWORDS list dictates which keywords must show up in the names we want. The output file contains a list of party names that are likely Columbia.

Other documentation:

* `NYC_OpenData_ACRIS_Datasets.doc`: Lists and links to all ACRIS datasets. Attached to all NYC OpenData ACRIS pages.
* `ACRIS_Public_OpenData_Extract_Guide_v_1.0.doc`: ACRIS OpenData Extract Guide. Attached to all NYC OpenData ACRIS pages.