'''
Created on 23/08/2016
finished 4/08/2016

@author: kiarie ndegwa
'''
import BSoupExtract
import nucleDict
fileName = "official.sgml"
text = nucleDict.nucleDict(fileName)
test = BSoupExtract.BSoupExtract(fileName).extract('41', "MISTAKE")

#print test
print text.Opt1collocationError()
#Generate parallel original corpus
#text.savetoFile(text.generateCorEssays(), "targetOrig.txt", True)
#text.savetoFile(text.collapseDict(text.generateOrig()), "sourceOrig.txt", True)
#Generate dictionaries
#text.savetoFile(text.dictGen(text.collapseDict(text.generateOrig())), "sourceOrig.dict", False)
#text.savetoFile(text.dictGen(text.generateCorEssays()), "targetOrig.dict", False)

#Generate training, testing and eval test sets
#for original text
#text.evalGen("sourceOrig.txt", "src")
#for target text
#text.evalGen("targetOrig.txt", "targ")
