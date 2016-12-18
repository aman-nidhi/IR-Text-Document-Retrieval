'''
	Cantact:    aman.sharefiles@gmail.com
	Date:       2016
'''

#!/usr/bin/env python

import sys
import re
from time import time
from stemmer.PorterStemmer import PorterStemmer
from collections import defaultdict
import gc
import os
import math
import json
from functools import reduce
import copy



porter=PorterStemmer()

class QueryIndex:

    def __init__(self):
        self.index={}
        #term frequencies
        self.tf={} 
        #inverse document frequencies     
        self.idf={}    

    # sort the list with decreasing order of length( number of documents per terms)
    # and take the intersection of the set 
    # this method is better complexity wise
    def intersectLists(self,lists):
        if len(lists)==0:
            return []
        # start intersecting from the smaller list
        lists.sort(key=len)
        return list(reduce(lambda x,y: set(x)&set(y),lists))
        
    
    def getStopwords(self):
        f=open(self.stopwordsFile, 'r')
        stopwords=[line.rstrip() for line in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()
        

    def getTerms(self, line):
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ' ,line) #put spaces instead of non-alphanumeric characters
        line=line.split()
        line=[x for x in line if x not in self.sw]
        line=[ porter.stem(word, 0, len(word)-1) for word in line]
        return line
        
    
    def getPostings(self, terms):
        # all terms in the list are guaranteed to be in the index
        return [ self.index[term] for term in terms ]
    
    
    def getDocsFromPostings(self, postings):
        # no empty list in postings
        return [ [x[0] for x in p] for p in postings ]


    def readIndex(self):
        # read main index
        f1=open(self.indexFile, 'r');
        f2=open(self.indexScore, 'r')
        # first read the number of documents
        self.numDocuments=int(f2.readline().strip())

        for line in f1:
            score = f2.readline()[1:-2]
            line = line.strip()[1:-1]
            # posting  = cv228_5806.txt:231;cv068_13400.txt:404;cv087_1989.txt:371"
            term, postings = line.split('|')
            _term, tf, idf = score.split('|')

            # postings=['docId1:pos1,pos2','docID2:pos1,pos2']
            postings=postings.split(';')  
            # postings=[['docId1', 'pos1,pos2'], ['docID2', 'pos1,pos2']]      
            postings=[x.split(':') for x in postings] 
            postings=[ [x[0], list(map(int, x[1].split(',')))] for x in postings ]             #final postings list  
            self.index[term]=postings

            # read term frequencies
            tf=tf.split(',')
            self.tf[term]=list(map(float, tf))
            # read inverse document frequency
            self.idf[term]=float(idf.strip()[:-1])

        f1.close()
        f2.close()
        print("read index complete\n")

        
     
    def dotProduct(self, vec1, vec2):
        if len(vec1)!=len(vec2):
            return 0
        return sum([ x*y for x,y in zip(vec1,vec2) ])
            
        
    def rankDocuments(self, terms, docs):
        # term at a time evaluation
        docVectors=defaultdict(lambda: [0]*len(terms))
        queryVector=[0]*len(terms)
        for termIndex, term in enumerate(terms):
            if term not in self.index:
                continue
            
            queryVector[termIndex]=self.idf[term]
            
            for docIndex, (doc, postings) in enumerate(self.index[term]):
                if doc in docs:
                    docVectors[doc][termIndex]=self.tf[term][docIndex]
                    
        # calculate the score of each doc
        docScores=[ [self.dotProduct(curDocVec, queryVector), doc] for doc, curDocVec in docVectors.items() ]
        docScores.sort(reverse=True)
        resultDocs=[x[1] for x in docScores][:10]
        # print document titles instead if document id's
        # resultDocs=[ self.titleIndex[x] for x in resultDocs ]
        print('\n'.join(resultDocs), '\n')
          

    def ftq(self,q):
        """Free Text Query"""
        q=self.getTerms(q)
        if len(q)==0:
            print('')
            return
        
        li=set()
        # li will store the list of documents that contains all the terms
        for term in q:
            try:
                postings=self.index[term]
                docs=[x[0] for x in postings]
                # li is taking the intersection of the documents that contains all the term
                li=li|set(docs)
            except:
                #term not in index
                pass
        
        li=list(li)
        self.rankDocuments(q, li)


    def pq(self,q):
        '''Phrase Query'''
        originalQuery=q
        q=self.getTerms(q)
        if len(q)==0:
            print ('')
            return

        phraseDocs=self.pqDocs(q)
        self.rankDocuments(q, phraseDocs)
        
        
    def pqDocs(self, q):
        """ here q is not the query, it is the list of terms """
        phraseDocs=[]
        length=len(q)
        # first find matching docs
        for term in q:
            if term not in self.index:
                # if a term doesn't appear in the index
                # there can't be any document maching it
                return []


        # posting of all terms in the query
        postings=self.getPostings(q)
        # returns list of documents in which that term occour, same for all terms 
        # like a list of list
        docs=self.getDocsFromPostings(postings)
        # returns only those documents that contains all the terms
        docs=self.intersectLists(docs)
        # check whether the term ordering in the docs is like in the phrase query
        for i in range(len(postings)):
            postings[i]=[x for x in postings[i] if x[0] in docs]
        
        
        # subtract i from the ith terms location in the docs
        # this is important since we are going to modify the postings list
        postings=copy.deepcopy(postings)    
        
        for i in range(len(postings)):
            for j in range(len(postings[i])):
                postings[i][j][1]=[x-i for x in postings[i][j][1]]
        
        # intersect the locations
        result=[]
        for i in range(len(postings[0])):
            li=self.intersectLists( [x[i][1] for x in postings] )
            if li==[]:
                continue
            else:
                result.append(postings[0][i][0])    
                #append the docid to the result
        
        return result

        
    def getParams(self):
        param=sys.argv
        self.stopwordsFile=param[1]
        self.indexFile=param[2]
        self.indexScore=param[3]

    def test_Params(self):
        '''for testing purpose'''
        self.stopwordsFile='./stopwords/english_stopwords.txt'
        self.indexFile='./index_db.json'
        self.indexScore='./index_score_db.json'

    def queryIndex(self):
        # self.getParams()
        self.test_Params()
        self.readIndex()  
        self.getStopwords() 
        par=sys.argv
        qt = par[1]

        while True:
        #     user query
            q = sys.stdin.readline()

            if qt=='':
                print('type some query: Error!')
                # break
            if qt=='ftq'
                self.ftq(q)
            if qt=='pq':
                self.pq(q)

        print("program end")
        
        
if __name__=='__main__':
    q=QueryIndex()

    q.queryIndex()
    print(q.index['alek'])




    
