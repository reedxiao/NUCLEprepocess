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
print len(textDict)
text.dictGen(textDict)
#print text.collapseDict(textDict)
#print text.dictGen(text.collapseDict(textDict))