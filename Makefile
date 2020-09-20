DATA_DIR = data
PARTY_DIR = party-search
SHP_DIR = shapefiles

DTM_PATH = $(SHP_DIR)/Digital_Tax_Map_20200828/DTM_Tax_Lot_Polygon.shp

acquisition-centroids.csv: $(SHP_DIR)/acquisitions.shp
	mapshaper $< \
	-points \
	-proj wgs84 \
	-each 'longitude = this.x, latitude = this.y' \
	-o format=csv $@

$(SHP_DIR)/acquisitions.shp: $(DATA_DIR)/acris-results.json $(DATA_DIR)/document_parties.json $(DTM_PATH) spatial-join.py
	./spatial-join.py $< $(word 2,$^) $(word 3,$^) $@
	cp $(basename $(word 3,$^)).prj $(basename $@).prj

$(DATA_DIR)/document_parties.json: $(DATA_DIR)/acris-results.json documents.py
	./documents.py -get-parties $< > $@

$(DATA_DIR)/acris-results.json: $(DATA_DIR)/acris-results-html.json
	./documents.py -parse-results $< > $@

$(DATA_DIR)/acris-results-html.json: $(PARTY_DIR)/names.json
	./documents.py -scrape-acris $< > $@

KEYWORDS = TRUSTEES COLUMBIA

$(PARTY_DIR)/names.json: $(PARTY_DIR)/all_parties.txt parties.py
	./parties.py -filter-parties $< $(KEYWORDS) > $@

$(PARTY_DIR)/all_parties.txt: $(PARTY_DIR)/ACRIS_-_Real_Property_Parties.csv
	./parties.py -all-parties $< > $@
