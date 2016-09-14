import BSoupExtract
import re

fileName = "official.sgml"
test1 = BSoupExtract.BSoupExtract(fileName).extractParagraph('41')
test2 = BSoupExtract.BSoupExtract(fileName).extractMistakesAndCorrection('41')

#print test1
#print test2.keys()

test3 = BSoupExtract.BSoupExtract(fileName).genCorrections('41', 'Wci')
print test3.keys()