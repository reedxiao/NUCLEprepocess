'''
Created on 20/09/2016

@author: kiarie Ndegwa
'''
import h5py
import numpy as np
import re
import os
import string
from copy import deepcopy

class hdf5wordembedding(object):
    '''This reads in word embeddings corresponding src and target .dict files
        
        src = the location of the src. dict file
        targ = the location of the targ.dict file
        word_embedding = the location of the word embeddings
        
        #Location of saved
        filename = name of hdf5 file to be saved 
        foldername = name of folder where hdf5 file is to be saved
        embed_Dim = number of dimensions in word embedding
        
    '''
    
    def __init__(self, src, targ, word_embeddings, filename, foldername, embed_dim):
        self.src = src
        self.targ = targ
        self.embed = word_embeddings
        self.filename = filename
        self.foldername = foldername
        self.embed_dim = embed_dim
    
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
    
    def genWordText(self, src_targ, name):
        #Generates new text file that can be converted to hdf5 format
           
        #This finds the equivalent word embeddings within the wordvec .txt file
        if src_targ == "src":
            print ">>>src file selected"
            dictWord, _ = self.readInDict()
        elif src_targ == "tar":
            print ">>>tar file selected"
            _, dictWord = self.readInDict()
        
        indexedEmbeddings = []
        path = os.path.join(self.foldername, name+".txt")
        
        template = np.zeros(self.embed_dim)     
        specChar = {"<blank>", "<unk>", "<s>", "</s>"}
        
        print ">>>Generating word embeddings"
        #load all special tokens
        #blank char
        blank = deepcopy(template)
        blank[0] = 1
        #unk
        unk = deepcopy(template)
        unk[1] = 1
        #<s>
        s = deepcopy(template)
        s[2] = 1
        #</s>
        s_ =deepcopy(template)
        s_[3] = 1
        
        for aWord in dictWord:
            word = aWord.split()[0]
            
            with open(path) as we:
                for twordVec in we:
                    wordVec = twordVec.split()[0]
                    wordEmbed = twordVec.split()[1:]
                    
                    if word in specChar:
                      #encode words
                      specChar.remove(word)
                      if word == "<blank>":
                          indexedEmbeddings.append(blank)
                      elif word == "<unk>":
                          indexedEmbeddings.append(unk)
                      elif word == "<s>":
                          indexedEmbeddings.append(s)
                      elif word == "</s>":
                          indexedEmbeddings.append(s_)
                      #print "====Special token, embedding generated===="
                    elif word.lower() == wordVec.lower():
                      floatVec = [float(i) for i in wordEmbed]
                      indexedEmbeddings.append(floatVec)    
                      #print "******Normal embedding generated!******"
        print ">>>>>>>>>>>>>Final Indexed embeddings generated"         
        return indexedEmbeddings
            
    def GenExp(self, embed_src, filename):
        #This generates an experimental .txt limited word2vec data set
        #Write the file to .txt file
        count = 0
        out = [] 
        
        foldername = self.foldername
        if not os.path.exists(foldername):
            os.makedirs(foldername)
            
        path = os.path.join(foldername, filename+".txt")
    
        with open(embed_src) as FileObject:           
            for line in FileObject:
                    Sline = line.split()
                    word = Sline[0]
                    WEmbedding = Sline[1:]
                    #Remove code snippet
                    '''if word == "technology":
                        print "found this piece of shit"
                        print WEmbedding'''
                    out.append(line)
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
        wordEmbed = self.genWordText(src_targ, hdf5Name)
        print "Embedding loaded.. its size is.."
        print len(wordEmbed)
        
        name = ""
        print "Generating embedding names"
        if src_targ == "src":
            name = hdf5Name+"_"+"enc_"
        else:
            name =hdf5Name+"_"+"dec_"
            
        print "Generating hdf5 files"
        hf = h5py.File('../../'+name+'data.hdf5', 'w') 
        
        #Add python array into numpy array of arrays
        ndata = np.array([np.array(xi) for xi in wordEmbed])
        print "size of numpy array"
        print len(ndata)
        #Write numpy array to hdf5 file
        print "Adding numpy array to hdf5"
        dset = hf.create_dataset('word_vecs', data=ndata)
    
    def readhdf5(self, name):
        #Test generated hdf5 file
        filename = '../../'+name+'data.hdf5'
        
        with h5py.File(filename,'r') as hf:
            print('List of arrays in this file: \n', hf.keys())
            data = hf.get('word_vecs')
            np_data = np.array(data)
            print('Shape of the array dataset_1: \n', np_data.shape)
            print np_data[100]
        
if __name__ == '__main__':
    pass