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

foldername = "NUCLE2014"
fileName = "nucle3.2.sgml"
saveName = "nucle2014_colloc"
errorTag = "Wci"
#fileName = "official-2014.1.sgml"

print "Generating train and validation data sets"
NUCLE = BSoupExtract.BSoupExtract(fileName, foldername, errorTag)
#Generate and Save evaluation functions
print "Saving data sets to .txt files"
NUCLE.LengthCheckedEval()

#Generate .dict files from data
print "Generating .dict files"
os.chmod('.././nucle2014_colloc_dict_script.sh', 0o755)
os.chmod(".././nucle2014_dict_script.sh", 0o755)

rc = call(".././nucle2014_colloc_dict_script.sh", shell=True)
rc = call(".././nucle2014_dict_script.sh", shell=True)