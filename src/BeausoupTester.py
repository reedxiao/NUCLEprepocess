import BSoupExtract
import re

fileName = "official.sgml"
test1 = BSoupExtract.BSoupExtract(fileName).extractParagraph('20')
test11 = BSoupExtract.BSoupExtract(fileName).extractSentences()
#print test1.keys()
test2 = BSoupExtract.BSoupExtract(fileName).extractMistakesAndCorrection('26')
#print test2.keys()

#print test2.keys()

test3 = BSoupExtract.BSoupExtract(fileName).genCorrections('20', 'Wci')

test4a, test4b = BSoupExtract.BSoupExtract(fileName).preSave()
print test4a[('10', '0')]
print test4b[('10', '0')]
#TO do:
#Extract and save to file somehow'''