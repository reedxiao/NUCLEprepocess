'''
@Author: Kiarie Ndegwa

Date 24th Sept 2016

This is the main pre-training script that generates all the datasets necessary
to the project scope

'''

import BrownPrep 
import subprocess
from subprocess import call
import os

#Download course trained Brown corpus
filename = "../../../brown_notags"
#Save file in standard format for pre-process.py dict fnc
filename2 = "../../PretrainCorpus/brown_full_text.txt"
brown = BrownPrep.BrownCleanUp(filename, filename2)
brown.extractText()

#Generated dict files for preprocess.py python
#---------------------------------------------------------------#
#---------------------------------------------------------------#
#Generate .dict files from data so that data can be consumed by network
print "Generating .dict files"
#Override chmode u+x 
os.chmod('../pretrain_script.sh', 0o755)
#Run bash script against preprocess.py
rc = call("../pretrain_script.sh", shell=True)

print "----------------------------------------------------------"
print "Training and eval pre-training data generated! :)"
print "----------------------------------------------------------"