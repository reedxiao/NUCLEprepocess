import BSoupExtract
foldername = "NUCLE2013"
fileName = "official.sgml"
#fileName = "official-2014.1.sgml"
#Instatiate object
NUCLE = BSoupExtract.BSoupExtract(fileName, foldername)
#Generate corrected sentences and save to tuple
UncorrectedTest, CorrectedText =NUCLE.preSave()
#Save original and corrected files to .txt file
NUCLE.savetoFile(par=UncorrectedTest, newFilename="OrigText.txt", sorting=UncorrectedTest.keys())
NUCLE.savetoFile(par=CorrectedText, newFilename="TargetText.txt", sorting=UncorrectedTest.keys())
#Collapse dictionaries:
cOrig = NUCLE.collapseDict(UncorrectedTest) 
cTarg = NUCLE.collapseDict(CorrectedText)
#Generate dictionary tokens for word embeddings
Dorig =  NUCLE.dictGen(cOrig) 
DTarg = NUCLE.dictGen(cTarg)
#Save dictionaries to text files
NUCLE.savetoFile(Dorig, "src.dict", None, False)
NUCLE.savetoFile(DTarg, "tar.dict", None, False)
#Save evaluation data sets
#NUCLE.evalGen("../"+foldername+"/"+"OrigText.txt", "src")
#NUCLE.evalGen("../"+foldername+"/"+"TargetText.txt", "tar")

#Save evaiauation functions
NUCLE.LengthCheckedEval()
