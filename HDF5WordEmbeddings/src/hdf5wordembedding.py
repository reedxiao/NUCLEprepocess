'''
Created on 20/09/2016

@author: kiarie Ndegwa
'''
import h5py
import numpy as np
import re
import os
import string

class hdf5wordembedding(object):
    '''This reads in word embeddings corresponding src and target .dict files
        
        src = the location of the src. dict file
        targ = the location of the targ.dict file
        word_embedding = the location of the word embeddings
        
        #Location of saved
        filename = name of hdf5 file to be saved 
        foldername = name of folder where hdf5 file is to be saved
        
    '''
    
    def __init__(self, src, targ, word_embeddings, filename, foldername):
        self.src = src
        self.targ = targ
        self.embed = word_embeddings
        self.filename = filename
        self.foldername = foldername
    
    def readInDict(self):
        src = []
        targ = []
        
        with open(self.src) as fileobject:
            for line in fileobject:
                src.append(line)
        
        with open(self.targ) as fileobject:
            for line in fileobject:
                targ.append(line)
        return src, targ
    
    def genWordText(self, src_targ):
        #Generates new text file that can be converted to hdf5 format
           
        #This finds the equivalent word embeddings within the .txt file
        if src_targ == "src":
            print "src file selected"
            dictWord, _ = self.readInDict()
        elif src_targ == "tar":
            print "tar file selected"
            _, dictWord = self.readInDict()
        #Convert dict word to searchable dictionary
        
        #search through source and find equivalent text
        indexedEmbeddings = []
        path = os.path.join(self.foldername, "testEmbedding.txt")
      
        with open(path) as we:
            for twordVec in we:
               
                wordVec = twordVec.split()[0]
                wordEmbed = twordVec.split()[1:]
                
                specChar = {"<blank>", "<unk>", "<s>", "</s>"}
                for aWord in dictWord:
                    
                    word = aWord.split()[0] 
                    #print"------------------------"
                    #print "what the fuck is going on here"
                    #print wordVec
                    #print word
                    #print "---------------------- "
                    #Get rid of special characters and replace with blank embeddings
                    #print "Searching for word in dict :"+word
                    if word in specChar:
                        specChar.remove(word)
                        print "found special character"
                        indexedEmbeddings.append(word)
                        
                    elif word == wordVec:
                        print "************embedding added************"
                        indexedEmbeddings.append(wordEmbed)
                        
        print "fucking hell"
        print len(indexedEmbeddings)
        '''with open(path, 'w') as f:
            print "writing file to test embeddings"
            for e in out:
                f.write(e)
            print "Finished writing embeddings to test file"'''
            
    def GenExp(self, embed_src):
        #This generates an experimental .txt limit word2vec data set
        #Write the file to .txt file
        count = 0
        out = [] 
        
        foldername = self.foldername
        if not os.path.exists(foldername):
            os.makedirs(foldername)
            
        path = os.path.join(foldername, "testEmbedding.txt")
    
        with open(embed_src) as FileObject:           
            for line in FileObject:
                if count <=1000:
                    Sline = line.split()
                    word = Sline[0]
                    WEmbedding = Sline[1:]
                    
                    if word == "'":
                        print "found this piece of shit"
                        print WEmbedding
                    
                    out.append(line)
                    count+=1
        print count
        with open(path, 'w') as f:
            print "writing file to test embeddings"
            for e in out:
                f.write(e)
            print "Finished writing embeddings to test file"
            
            
if __name__ == '__main__':
    pass