'''
Created on 20/09/2016

@author: kiarie Ndegwa

Test script for hdf5 word embedding

'''
import hdf5wordembedding
foldername = "../../NUCLEPreprocess/NUCLE2013"

hdf5 = hdf5wordembedding.hdf5wordembedding(src=foldername+"/src.dict",
                                           targ= foldername+"/tar.dict",
                                           word_embeddings="wordEmbedding/testEmbedding.txt",
                                           filename = "test.hdf5", 
                                           foldername= "../wordEmbedding")
#Generate test benchmark
hdf5.GenExp("../../../glove.6B/glove.6B.50d.txt")

#Read in .dict files
#hdf5.genWordText("src")