##A Simple Text File Retrieval System

Documents and query are represented as vectors. The retrieved Text Documents are ranked based on Cosine similarity of document and query vector, which are represented an array of TF-Idf score of the terms.


First run the create index program:

        python createIndex.py

Then run the query index program:

        python queryDoc.py pq 
        
To run the query file, specify the the type of query 
pq - phrase query
ftq - free text query

english_stopwords.txt is the stopwords file
Index_db.json - the inverted index of the corpus, stores the term and corresponding posting list
index_score_db.json - is the tf-idf database for each word

seek

Display internet search results without ever leaving your terminal. Oh, and it can speed read the results as well. Basically, it's command line nirvana.

Seek is a sister to howdoi and Glance.

Installation

pip install seek
Examples

$ seek a nice up of tea orwell 

If you look up 'tea' in the first cookery book that comes to hand you will probably find that it is unmentioned; or at most you will find a few lines of sketchy instructions which give no ruling on several of the most important points. [etc.]
A Nice Cup of Tea
http://www.booksatoz.com/witsend/tea/orwell.htm

$ seek a nice cup of tea orwell --glance
A Nice Cup of Tea
http://www.booksatoz.com/witsend/tea/orwell.htm
stimulation      <--- (This is animated)
Features:

Glance mode! Powered by pyglance.
Diffbot article extraction
Searches DuckDuckGo, Google coming soon (maybe).
BSD 3-clause, 2014-2015.





![Index Creation](/demo_images/index.JPG)

![Index Read and Query](/demo_images/query.JPG)