#Installation
If you run indexer,
On console,

pip install beautifulsoup4
pip install lxml

#How to use
Everything is already indexed, so run search.py to test search engine.

If you will test these from scratch, then see below.

search, indexer, and idfIndexer are seperated programs.
dev folder path is hardcoded, so open indexer and recode root path in main function.
a.zip file contains empty txt files to work with indexer and idfIndexer.
Place and update them in tfIndex and idfIndex folders under words.
Run indexer, idfIndexer, and search in order.

#indexer
This program extracts texts from html files, tokenizes unique words, and indexes words into a-z files with a term frequency(tf).

#idfIndexer
This program calculates an inverse document frequency(idf) and indexes into a-z files.

#search
This program is a search engine which allows users to search words and returns top 5 relevalnt urls.