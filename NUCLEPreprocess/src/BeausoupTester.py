'''
@author: Kiarie Ndegwa
        Sept 18th 2016

Run this file to generate data sets that can be used by a seq2seq network

Change the foldername and filename of .sgml file to extract sentences in the required format
'''
import BSoupExtract
foldername = "NUCLE2014_colloc"
fileName = "nucle3.2.sgml"
errorTag = "Wci"
#fileName = "official-2014.1.sgml"

print "Generating train and validation data sets"
NUCLE = BSoupExtract.BSoupExtract(fileName, foldername, errorTag)
#Generate and Save evaluation functions
print "Saving data sets to .txt files"
NUCLE.LengthCheckedEval()

