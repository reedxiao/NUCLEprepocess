import BSoupExtract
import re

fileName = "official.sgml"
test1 = BSoupExtract.BSoupExtract(fileName).extractParagraph('42')
test11 = BSoupExtract.BSoupExtract(fileName).extractSentences()
print test1.keys()
test2 = BSoupExtract.BSoupExtract(fileName).extractMistakesAndCorrection('26')
print test2.keys()

print test1.keys()
#print test2.keys()

test3 = BSoupExtract.BSoupExtract(fileName).genCorrections('26', 'Wci')
print test3.keys()

test4a, test4b = BSoupExtract.BSoupExtract(fileName).preSave()
print test4a.keys()
#TO do:
#Extract and save to file somehow'''