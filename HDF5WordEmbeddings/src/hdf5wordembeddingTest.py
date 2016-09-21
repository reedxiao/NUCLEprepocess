'''
Created on 20/09/2016

@author: kiarie Ndegwa

Test script for hdf5 word embedding

'''
import hdf5wordembedding
foldername = "../../NUCLEPreprocess/NUCLE2013"

hdf5 = hdf5wordembedding.hdf5wordembedding(src=foldername+"/nucle2013.src.dict",
                                           targ= foldername+"/nucle2013.targ.dict",
                                           word_embeddings="../../../glove.6B/glove.6B.100d.txt",
                                           filename = "nucle2013.hdf5", 
                                           foldername= "../../../wordEmbedding",
                                           embed_dim = 100)
                
#Generate test benchmark
hdf5.GenExp("../../../glove.6B/glove.6B.50d.txt", "nucle2013")
#Read in .dict files

#Generate hdf5 files #fingers crossed
hdf5.savehdf5("nucle2013", "src", 100)

#Test hdf5 file generated
hdf5.readhdf5("nucle2013_enc_")