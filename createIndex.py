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
from progressbar.ProgressBar import ProgressBar
import json

porter=PorterStemmer()

class CreateIndex():

    def __init__(self):

        # the inverted index
        self.index=defaultdict(list)            
        # self.titleIndex={}
        # term frequencies of terms in documents
        self.tf=defaultdict(list)  
        # document frequencies of terms in the corpus 
        self.df=defaultdict(int)
        # number of documents              
        self.numDocuments=0  


    def getStopwords(self):
        '''get stopwords from the stopwords file'''
        f=open(self.stopwordsFile, 'r')
        stopwords=[line.rstrip() for line in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()


    def getTerms(self, line):
        '''given a stream of text, get the terms from the text'''
        line=line.lower()
        # put spaces instead of non-alphanumeric characters
        line=re.sub(r'[^a-z0-9 ]',' ',line)         
        line=line.split()
        # eliminate the stopwords
        line=[x for x in line if x not in self.sw]  
        line=[ porter.stem(word, 0, len(word)-1) for word in line]
        return line


    def saveIndex(self):
        '''write the index to the file'''

        self.num_documents=int(self.num_documents)
        f1=open(self.indexFile, 'w')
        f2=open(self.indexScore, 'w')
        print(self.num_documents, file=f2)
        for term in self.index.keys():
            postinglist=[]
            for p in self.index[term]:
                doc_name=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(doc_name) ,','.join(map(str,positions))]))
            json.dump(''.join((term,'|',';'.join(postinglist))), f1, indent=4)
            print('', file=f1)

            tfData=','.join(map(str,self.tf[term]))
            idfData='{:.4f}'.format(self.num_documents/self.df[term])
            json.dump('|'.join((term, tfData, idfData)), f2, indent=4)
            print('', file=f2)
            
        f1.close()
        f2.close()


        ## this one is more readable
        # self.num_documents=float(self.num_documents)
        # f1=open(self.indexFile, 'w')
        # f2=open(self.indexScore, 'w')
        # for term in self.index.keys():
        #     postinglist=[]
        #     for p in self.index[term]:
        #         doc_name=p[0]
        #         positions=p[1]
        #         postinglist.append({str(doc_name): positions})
        #     a = {term: postinglist}
        #     json.dump(a, f1, indent=4)
        #     print('', file=f1)

        #     tfData=','.join(map(str,self.tf[term]))
        #     idfData='{:.4f}'.format(self.num_documents/self.df[term])
        #     json.dump('|'.join((term, tfData, idfData)), f2, indent=4)
        #     print('', file=f2)
            
        # f1.close()
        # f2.close()
        

    def getParams(self):
        '''get the parameters stopwords file, collection file, and the output index file'''
        param=sys.argv
        self.stopwordsFile=param[1]
        self.corpus=param[2]
        self.indexFile=param[3]
        self.indexScore=param[4]


    def test_Params(self):
        '''for testing purpose'''
        self.stopwordsFile='./stopwords/english_stopwords.txt'
        self.corpus='./data/pos/'
        self.indexFile='./index_db.json'
        self.indexScore='./index_score_db.json'


    def createIndex(self):
        '''main of the program, creates the index'''
        # self.getParams()
        self.test_Params()
        # self.corpusFile=open(self.corpus,'r')
        self.getStopwords()

        documents=[]
        for file in [doc for doc in os.listdir(self.corpus) if doc.endswith(".txt")]:
            documents.append(file)

        self.num_documents=len(documents)
        print('number of documents -', self.num_documents)
        progress = ProgressBar(self.num_documents, fmt=ProgressBar.FULL)


        for doc_name in documents:
            file_t=open(self.corpus+doc_name,'r')
            progress.current += 1

            text=file_t.read()
            terms=self.getTerms(text)

            termdictPage={}
            for position, term in enumerate(terms):
                try:
                    termdictPage[term][1].append(position)
                except:
                    termdictPage[term]=[doc_name, [position]]

            norm=0
            for term, posting in termdictPage.items():
                norm+=len(posting[1])**2
            norm=math.sqrt(norm)

            for term, posting in termdictPage.items():
                self.tf[term].append('{:.4f}'.format(len(posting[1])/norm))
                self.df[term]+=1

            for termPage, postingPage in termdictPage.items():
                self.index[termPage].append(postingPage)

            # bar progress
            progress()

        # save the index to JSON file
        self.saveIndex()



if __name__=="__main__":
    c=CreateIndex()
    t = time()
    c.createIndex()
    t = time()-t

    print('\n', "Created Index in =", t,'seconds','\n')
    # c.saveIndex()
    print('how index looks like for term 'alek' ')
    print(c.index['alek'])
    

