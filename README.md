# The OSHA Violation Standard scraper


> *tl;dr, Download the OSHA violation standards (29 CFR) code manual as CSV:* 




## Intro

tktk


## Running the scrape yourself

There's a [Makefile](Makefile) to make re-running the scrape convenient. The following task: 

```sh
$ make ALL
```

&ndash; will erase everything in [data/collected](data/collected) and [data/compiled](data/compiled) and refetch all the pages from the online OSHA manual, and then rescrape them to extract the data.

This requires **Python 3.x** and the libraries found in [requirements.txt](requirements.txt)

