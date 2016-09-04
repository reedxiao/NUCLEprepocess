'''
Created on 23/08/2016
finished 4/08/2016

@author: kiarie ndegwa
'''

import nucleDict
from docutils.parsers.rst.directives import flag
fileName = "official.sgml"
text = nucleDict.nucleDict(fileName)

#Generate parallel original corpus
text.savetoFile(text.generateCorEssays(), "targetOrig.txt", True)
text.savetoFile(text.generateOrig(), "sourceOrig.txt", True)
#Generate dictionaries
text.savetoFile(text.dictGen(text.generateOrig()), "sourceOrig.dict", False)
text.savetoFile(text.dictGen(text.generateCorEssays()), "targetOrig.dict", False)

#Generate training, testing and eval test sets
#for original text
text.evalGen("sourceOrig.txt", "src")
#for target text
text.evalGen("targetOrig.txt", "targ")
