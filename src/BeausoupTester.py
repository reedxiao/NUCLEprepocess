import BSoupExtract
import re

foldername = "NUCLETEST12"
fileName = "official.sgml"
test1 = BSoupExtract.BSoupExtract(fileName, foldername).extractParagraph('20')
test11 = BSoupExtract.BSoupExtract(fileName, foldername).extractSentences()
#print test1.keys()
test2 = BSoupExtract.BSoupExtract(fileName, foldername).extractMistakesAndCorrection('26')
#print test2.keys()

#print test2.keys()

test3 = BSoupExtract.BSoupExtract(fileName, foldername).genCorrections('20', 'Wci')

test4a, test4b = BSoupExtract.BSoupExtract(fileName, foldername).preSave()

test5 = BSoupExtract.BSoupExtract(fileName, foldername).savetoFile(sent=test4a, newFilename="OrigText.txt", sorting=test4b.keys())
test6 = BSoupExtract.BSoupExtract(fileName, foldername).savetoFile(sent=test4b, newFilename="TargetText.txt", sorting=test4b.keys())
#TO do:
#Extract and save to file somehow'''