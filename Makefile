DATA_DIR = data

$(DATA_DIR)/acris-results.html:
	./main.py -scrape-acris > $@

.PHONY:
folders:
	mkdir -p $(DATA_DIR)
