'''
@author: Kiarie Ndegwa
        Sept 18th 2016

Run this file to generate data sets that can be used by a seq2seq network

Change the foldername and filename of .sgml file to extract sentences in the required format
'''
import BSoupExtract
import subprocess
from subprocess import call
import os
#NUCLE2014 Data set in .sgml format
fileName = "nucle3.2.sgml"
#---------------------------------------------------------------#
#---------------------------------------------------------------#
#Generate training, eval and test data sets, for collocation based error detection
foldername1 = "NUCLE2014_colloc"
saveName1 = "nucle2014_colloc"
errorTag1 = "Wci"
print "Generating train and validation data sets"
NUCLE2014_colloc = BSoupExtract.BSoupExtract(fileName, foldername1, errorTag1)
#Generate and Save evaluation functions
print "Saving data sets to .txt files"
NUCLE2014_colloc.LengthCheckedEval()
#---------------------------------------------------------------#
#---------------------------------------------------------------#
#Generate training, eval and test data for G.E.C. based error detection
foldername2 = "NUCLE2014"
saveName2 = "nucle2014"
errorTag2 = None

#Generate 
print "Generating train and validation data sets"
NUCLE2014 = BSoupExtract.BSoupExtract(fileName, foldername2, errorTag2)
#Generate and Save evaluation functions
print "Saving data sets to .txt files"
NUCLE2014.LengthCheckedEval()
#---------------------------------------------------------------#
#---------------------------------------------------------------#
#Generate .dict files from data so that data can be consumed by network
print "Generating .dict files"
#Override chmode u+x 
os.chmod('.././nucle2014_colloc_dict_script.sh', 0o755)
os.chmod(".././nucle2014_dict_script.sh", 0o755)
#Run bash script against preprocess.py
rc = call(".././nucle2014_colloc_dict_script.sh", shell=True)
rc = call(".././nucle2014_dict_script.sh", shell=True)

print "Training, eval and test sets all generated and good to go! :)"