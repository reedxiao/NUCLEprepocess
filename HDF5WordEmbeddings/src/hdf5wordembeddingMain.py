'''
Created on 20/09/2016

@author: Kiarie Ndegwa

Test script for hdf5 word embedding
'''

import hdf5wordembedding
foldername = "../../NUCLEPreprocess/NUCLE2014_colloc"
name = "nucle2014_colloc"
dim = 50
embeddingFile = "glove.6B."+str(dim)+"d.txt"
embeddingFolder = "glove.6B"
hdf5 = hdf5wordembedding.hdf5wordembedding(src=foldername+"/"+name+".src.dict",
                                           targ= foldername+"/"+name+".targ.dict",
                                           word_embeddings="../../../"+embeddingFile,
                                           filename = name+".hdf5", 
                                           foldername= "../../../wordEmbedding",
                                           embed_dim = dim)
                
#Generate encoding
hdf5.GenExp("../../../"+embeddingFolder+"/"+embeddingFile, name+"_"+str(dim)+"d")

#Generate hdf5 files #fingers crossed
hdf5.savehdf5(name+"_"+str(dim)+"d", "tar")
hdf5.savehdf5(name+"_"+str(dim)+"d", "src")
#Test hdf5 file generated
hdf5.readhdf5(name+"_"+str(dim)+"d_dec_")
hdf5.readhdf5(name+"_"+str(dim)+"d_enc_")

print "--------------------------------------"
print "hdf5 encoding generated!"
print "--------------------------------------"