library(tidyverse)

# Read JSON

library(jsonlite)
documents <- jsonlite::fromJSON("../data/acris-results.json")$documents

# Date analysis to check assumptions

documents %>%
  filter(`Doc Date` != "") %>% 
  mutate(docDate = as.Date(`Doc Date`, "%m/%d/%Y")) %>% 
  ggplot(aes(docDate)) +
  geom_histogram()

documents %>% 
  mutate(hasCRFN = CRFN != "") %>% 
  mutate(year = lubridate::year(as.Date(`Doc Date`, "%m/%d/%Y"))) %>% 
  ggplot(aes(year)) +
  geom_bar() +
  facet_wrap(~ hasCRFN)

# What are the document types?

documents %>% 
  count(DocumentType) %>% arrange(-n) %>% View()
