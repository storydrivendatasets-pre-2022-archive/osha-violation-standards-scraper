# The OSHA Violation Standard scraper (NOT DONE 2020-08-17)


> *tl;dr, Download the OSHA violation standards (29 CFR) code manual as CSV:* 



# TODOS

In [scripts/collect_pages](scripts/collect_pages), write `collect_number_parts()`




## Intro

tktk


## Running the scrape yourself

There's a [Makefile](Makefile) to make re-running the scrape convenient. The following task: 

```sh
$ make ALL
```

&ndash; will erase everything in [data/collected](data/collected) and [data/compiled](data/compiled) and refetch all the pages from the online OSHA manual, and then rescrape them to extract the data.

This requires **Python 3.x** and the libraries found in [requirements.txt](requirements.txt)

