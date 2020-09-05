DATA_DIR = data

# TODO: transform to CSV
# TODO: merge with tax lot shapefile

$(DATA_DIR)/acris-results.json: $(DATA_DIR)/acris-results.html
	./main.py -parse-results $< > $@

$(DATA_DIR)/acris-results.html:
	./main.py -scrape-acris > $@

.PHONY:
folders:
	mkdir -p $(DATA_DIR)
