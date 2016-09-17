'''
Created on 23/08/2016
finished 4/09/2016

@author: kiarie ndegwa:

Main script, this takes in .sgml files from conll2013 and conll2014 and prepares
them for training a recursive neural network
'''
#import BSoupExtract
import nucleDict
import CorpusTest
from nltk.tokenize import sent_tokenize

fileName = "official.sgml"
folderName = "NUCLE2018"
#text = nucleDict.nucleDict(fileName)
#test = BSoupExtract.BSoupExtract(fileName).extract('41', "MISTAKE")

#print test
#print text.Opt1collocationError()
#testa = CorpusTest.CorpusTest("../NUCLE2013/targetOrig.txt", "../NUCLE2013/sourceOrig.txt")
#testa.testCorpus()

#Imports .sgml NUCLE2013, and NUCLE2014 and cleans it up. This is working do not change
#fileName = "official.sgml"
text = nucleDict.nucleDict(fileName, folderName)


#Generate parallel original corpus

#Trololololol
'''text.savetoFile(text.generateCorEssays()[0], "targetOrig.txt", True)
text.savetoFile(text.generateCorEssays()[1], "sourceOrig.txt", True)
print "ok===================="

ai = [sent_tokenize(j) for j in ([i for i in text.generateCorEssays()[0]])]
len_ai = [item for sublist in ai for item in sublist]
print len(len_ai)

ab = [sent_tokenize(j) for j in ([i for i in text.generateCorEssays()[1]])]
len_ai = [item for sublist in ab for item in sublist]
print len(len_ai)'''
##print "ok=======================orig"
#print len(sent_tokenize([i for i in text.generateCorEssays()[1]]))
#text.savetoFile(text.collapseDict(text.generateOrig()), "sourceOrig.txt", True)
#Generate dictionaries
text.savetoFile(text.dictGen(text.collapseDict(text.generateOrig())), "sourceOrig.dict", False)

text.savetoFile(text.dictGen(text.generateCorEssays()[0]), "targetOrig.dict", False)

#Generate training, testing and eval test sets
#for original text
text.evalGen("sourceOrig.txt", "src")
#for target text
text.evalGen("targetOrig.txt", "targ")