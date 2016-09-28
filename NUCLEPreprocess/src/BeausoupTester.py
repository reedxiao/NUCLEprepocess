'''
@author: Kiarie Ndegwa
        Sept 18th 2016

Run this file to generate data sets that can be used by a seq2seq network

Change the foldername and filename of .sgml file to extract sentences in the required format
'''
import BSoupExtract
foldername = "NUCLE2014"
fileName = "nucle3.2.sgml"
#fileName = "official-2014.1.sgml"
#Instatiate object

print "Generating train and validation data sets"
NUCLE = BSoupExtract.BSoupExtract(fileName, foldername)
#Generate and Save evaluation functions
NUCLE.LengthCheckedEval()

