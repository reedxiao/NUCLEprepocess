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
           
        #This finds the equivalent word embeddings within the wordvec .txt file
        if src_targ == "src":
            print "src file selected"
            dictWord, _ = self.readInDict()
        elif src_targ == "tar":
            print "tar file selected"
            _, dictWord = self.readInDict()
        
        indexedEmbeddings = []
        path = os.path.join(self.foldername, "testEmbedding.txt")
             
        specChar = {"<blank>", "<unk>", "<s>", "</s>"}
        for aWord in dictWord:
            word = aWord.split()[0]
            
            with open(path) as we:
                for twordVec in we:
                    wordVec = twordVec.split()[0]
                    wordEmbed = twordVec.split()[1:]

                    if word in specChar:
                      specChar.remove(word)
                      indexedEmbeddings.append(word)
                    elif word.lower() == wordVec.lower():
                      indexedEmbeddings.append(wordEmbed)
                      
        return indexedEmbeddings
            
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
                    
                    if word == "technology":
                        print "found this piece of shit"
                        print WEmbedding
                    
                    out.append(line)
                    count+=1
        with open(path, 'w') as f:
            print "writing file to test embeddings"
            for e in out:
                f.write(e)
            print "Finished writing embeddings to test file"
            
    def savehdf5(self, hdf5Name, src_targ, embedLength):
        '''Takes in list of embeddings and writes them to hdf5 file
        hdf5Name ==> Name of file to be written
        src_targ ==> word enc or dec
        '''
        #Load list of found vectors
        wordEmbed = self.genWordText(src_targ)
        print "Embedding loaded"
        print type(wordEmbed)
        
        name = ""
        #wordEmbed = np.random.rand(100, 100)
        print "Generating names"
        if src_targ == "src":
            name = hdf5Name+"_"+"enc_"
        else:
            name =hdf5Name+"_"+"dec_"
        print "Generating hdf5 files"
        
        hf = h5py.File('../../'+name+'data.hdf5', 'w') 
        
        #Add python array into numpy array of arrays
        ndata = np.array([np.array(xi) for xi in wordEmbed if type(xi)=="list"])
        #Write numpy array to hdf5 file
        dset = hf.create_dataset('word_vecs', data=ndata)
    
    def readHdf(self):
        pass
        
if __name__ == '__main__':
    pass