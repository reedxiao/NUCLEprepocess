'''
Created on 23/08/2016

@author: kiarie
'''
import nucleDict
fileName = "official.sgml"
text = nucleDict.nucleDict(fileName)

#text.savetoFile(text.generateCorEssays(), "targetOrIG.txt")
#text.savetoFile(text.dictGen(text.generateOrig()), "orig.dict")

#text.generateOrig().keys()
textDict = (text.collapseDict(text.generateOrig()))
print textDict
test = text.generateCorEssays()
print test
#print len(textDict)
#text.dictGen(textDict)
#text.evalGen("origTxt.txt", "src")
#print text.collapseDict(textDict)
#print text.dictGen(text.collapseDict(textDict))