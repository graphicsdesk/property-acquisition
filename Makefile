DATA_DIR = data
PARTY_DIR = party-search

# TODO: merge with tax lot shapefile

$(DATA_DIR)/acris-results.json: $(DATA_DIR)/acris-results-html.json documents.py
	./documents.py -parse-results $< > $@

$(DATA_DIR)/acris-results-html.json: $(PARTY_DIR)/names.json
	./documents.py -scrape-acris $< > $@

KEYWORDS = TRUSTEES COLUMBIA

$(PARTY_DIR)/names.json: $(PARTY_DIR)/all_parties.txt parties.py
	./parties.py -filter-parties $< $(KEYWORDS) > $@

$(PARTY_DIR)/all_parties.txt: $(PARTY_DIR)/ACRIS_-_Real_Property_Parties.csv
	./parties.py -all-parties $< > $@

.PHONY:
folders:
	mkdir -p $(DATA_DIR)
