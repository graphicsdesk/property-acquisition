DATA_DIR = data
PARTY_DIR = party-search
SHP_DIR = shapefiles

DTM_PATH = $(SHP_DIR)/Digital_Tax_Map_20200828/DTM_Tax_Lot_Polygon.shp

# TODO: merge with tax lot shapefile.
# Look at https://github.com/GeospatialPython/pyshp#reading-shapefiles

deed-centroids.csv: $(SHP_DIR)/deeds.shp
	mapshaper $^ \
	-points \
	-proj wgs84 \
	-each 'longitude = this.x, latitude = this.y' \
	-o format=csv $@

$(SHP_DIR)/deeds.shp: $(DATA_DIR)/acris-results.json $(DTM_PATH) documents.py Makefile
	# ./spatial-join.py -spatial-join $< $(word 2,$^) $@
	cp $(basename $(word 2,$^)).prj $(basename $@).prj

$(DATA_DIR)/acris-results.json: $(DATA_DIR)/acris-results-html.json
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
