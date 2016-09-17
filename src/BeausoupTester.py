import BSoupExtract
foldername = "NUCLE13"
fileName = "official.sgml"
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
NUCLE.savetoFile(Dorig, "src.dict", None)
NUCLE.savetoFile(DTarg, "tar.dict", None)
#Save evaluation data sets
NUCLE.evalGen("OrigText.txt", "src")
NUCLE.evalGen("TargetText.txt", "tar")
