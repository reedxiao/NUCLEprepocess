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
        print "Size of dictionary loaded"
        print len(dictWord)
        
        indexedEmbeddings = []
        path = os.path.join(self.foldername, name+".txt")
        
        print ">>>Generating word embeddings"
        
        #load word embeddings and add them to dictionary for faster search
        word_Vecs = open(path).readlines()
        print "loaded word embeddings"
        print len(word_Vecs)
        
        word_vec_dict = {}
        for word in word_Vecs:
            w = word.split()[0]
            v = word.split()[1:]
            word_vec_dict[w.lower()] = v
        print "Generated embedding dictionary"
        
        #Consider making this parallel
        for aWord in dictWord:
            word = aWord.split()[0]  
            if word.lower() in word_vec_dict:
              floatVec = [float(i) for i in word_vec_dict[word.lower()]]
              indexedEmbeddings.append(floatVec)    
              #print "******Normal embedding generated!******"
              
        print "Generating unk tokens"
        ndata = np.array(indexedEmbeddings)
        
        #Generate unkown word token
        unk = np.mean(ndata, axis=0)
        
        #Add all special tokens to embedding 2d array
        template = np.array(np.zeros(self.embed_dim)).astype(float)
        #blank char       
        blank = np.array(deepcopy(template))
        #<s>
        s = np.array(deepcopy(template))
        s[2] = float(1)
        #</s>
        s_ = np.array(deepcopy(template))
        s_[3] = float(1)
                
        finalEmbed = np.vstack((blank, unk, s, s_, ndata))
        #get average for unk token
        print ">>>>>>>>>>>>>Final length of Indexed embeddings generated"         
        print "Embeddings without special tokens"
        print len(indexedEmbeddings)
        print "Embeddings with correct tokens added"
        print len(finalEmbed)
        return  finalEmbed
            
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
            
    def savehdf5(self, hdf5Name, src_targ):
        '''Takes in list of embeddings and writes them to hdf5 file
        hdf5Name ==> Name of file to be written
        src_targ ==> word enc or dec
        '''
  
        wordEmbed =self.genWordText(src_targ, hdf5Name)
        
        print "Embedding loaded.. with size is:"
        print len(wordEmbed)
        
        name = ""
        print "Generating embedding names"
        if src_targ == "src":
            name = hdf5Name+"_"+"enc_"
        else:
            name =hdf5Name+"_"+"dec_"
      
        print "Generating hdf5 file"
        hf = h5py.File(self.foldername+"/"+name+'_data.hdf5', 'w') 
        
        #Write numpy array to hdf5 file
        print "Adding numpy array to hdf5 file"
        dset = hf.create_dataset('word_vecs', data=wordEmbed)
        print "Hdf5 file created!"
    
    def readhdf5(self, name):
        #Test generated hdf5 file
        filename = self.foldername+"/"+name+'_data.hdf5'
        
        with h5py.File(filename,'r') as hf:
            print('List of arrays in this file: \n', hf.keys())
            data = hf.get('word_vecs')
            np_data = np.array(data)
            print('Shape of the array dataset_1: \n', np_data.shape)
            print np_data[1]
        
if __name__ == '__main__':
    pass