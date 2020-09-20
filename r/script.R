library(tidyverse)

# Read JSON

library(jsonlite)
documents <- jsonlite::fromJSON("../data/acris-results.json")

# Date analysis to check assumptions

documents %>%
  filter(`Doc Date` != "") %>% 
  filter(DocumentType %in% c('DEED', 'MORTGAGE', 'DEED, OTHER')) %>% 
  mutate(docDate = as.Date(`Doc Date`, "%m/%d/%Y")) %>% 
  ggplot(aes(docDate)) +
  geom_histogram() +
  facet_grid(`Party Type/Other` ~ DocumentType)

documents %>% 
  mutate(hasCRFN = CRFN != "") %>% 
  mutate(year = lubridate::year(as.Date(`Doc Date`, "%m/%d/%Y"))) %>% 
  ggplot(aes(year)) +
  geom_bar() +
  facet_wrap(~ hasCRFN)

# What are the document types?

documents %>% 
  count(DocumentType, `Party Type/Other`) %>% arrange(-n) %>% View()
