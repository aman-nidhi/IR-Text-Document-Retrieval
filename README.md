##A Simple Text File Retrieval System

Documents and query are represented as vectors. The retrieved Text Files are ranked based on Cosine similarity of document vectors and the query vector. The vector representation of any document is an array of Tf-Idf score of the terms present in the respective document.


First run the create index program:

        python createIndex.py

Then run the query index program:

        python queryDoc.py pq 
        
To run the query file, specify the the type of query 

pq -	phrase query 								
ftq -	free text query 								

english_stopwords.txt :is the stopwords File									
Index_db.json :is the inverted index of the corpus, stores the term and corresponding posting list				      
index_score_db.json :is the tf-idf database for each word												



![Index Creation](/demo_images/index.JPG)

![Index Read and Query](/demo_images/query.JPG)