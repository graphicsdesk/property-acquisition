# Set number of parallel jobs to number of available processors
NPROCS = $(shell sysctl hw.ncpu | grep -o '[0-9]\+')
MAKEFLAGS += -j$(NPROCS)

DATA_DIR = data
HTML_DIR = $(DATA_DIR)/html
PARTY_DIR = party-search
SHP_DIR = shapefiles
OUTPUT_DIR = ../policing-history/data

DTM_PATH = $(SHP_DIR)/Digital_Tax_Map_20200828/DTM_Tax_Lot_Polygon.shp


##############
# WEB EXPORT #
##############

$(OUTPUT_DIR)/acquisitions.json: $(SHP_DIR)/acquisitions.shp
	mapshaper $< \
	-proj wgs84 \
	-filter "party_type == '2'" \
	-each "doc_date = doc_date.includes('1899') ? null : doc_date" \
	-each "record_date = record_date.includes('1899') ? null : record_date" \
	-each "lazy_date = doc_date || record_date" \
	-each "year = +lazy_date.substring(0, 4)" \
	-filter 'doc_type !== "MORTGAGE"' \
	-o format=topojson $@

all: $(OUTPUT_DIR)/acquisitions.json $(OUTPUT_DIR)/acquisitions.geojson

$(OUTPUT_DIR)/acquisitions.geojson: $(SHP_DIR)/acquisitions.shp
	mapshaper $< \
	-proj wgs84 \
	-each "doc_date = doc_date.includes('1899') ? null : doc_date" \
	-each "record_date = record_date.includes('1899') ? null : record_date" \
	-each "lazy_date = doc_date || record_date" \
	-filter 'doc_type !== "MORTGAGE"' \
	-o $@


###################
# SPATIAL JOINING #
###################

$(SHP_DIR)/acquisitions.shp: $(DATA_DIR)/acris-results.json $(DATA_DIR)/document_parties.json $(DTM_PATH)
	./spatial-join.py $< $(word 2,$^) $(word 3,$^) $@
	cp $(basename $(word 3,$^)).prj $(basename $@).prj


######################
# DOCUMENT SEARCHING #
######################

$(DATA_DIR)/document_parties.json: $(DATA_DIR)/acris-results.json
	./documents.py -get-parties $< > $@

$(DATA_DIR)/acris-results.json: $(DATA_DIR)/acris-results-html.json
	./documents.py -parse-results $< > $@

$(DATA_DIR)/acris-results-html.json: $(PARTY_DIR)/names.json
	./documents.py -scrape-acris $< > $@


###################
# PARTY SEARCHING #
###################

$(PARTY_DIR)/names.json: $(PARTY_DIR)/all_parties.txt
	./parties.py -filter-parties $< > $@

$(PARTY_DIR)/all_parties.txt: $(PARTY_DIR)/ACRIS_-_Real_Property_Parties.csv
	./parties.py -all-parties $< > $@
