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
                                           foldername= "../wordEmbedding",
                                           embed_dim = 50)
                
#Generate test benchmark
#hdf5.GenExp("../../../glove.6B/glove.6B.50d.txt")
#Read in .dict files

#Generate hdf5 files #fingers crossed
#hdf5.savehdf5("test", "src", 50)

#Test hdf5 file generated
hdf5.readhdf5("test_enc_")